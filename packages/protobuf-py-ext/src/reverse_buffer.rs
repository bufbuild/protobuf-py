#![allow(
    clippy::cast_possible_truncation,
    reason = "truncation is expected by protobuf varint encoding"
)]

use std::mem::MaybeUninit;

use pyo3::{Bound, Python, types::PyBytes};

/// A buffer that is filled from back to front.
///
/// One-pass protobuf serialization writes each length-delimited payload before
/// its length prefix. By writing toward the front, the payload length is known
/// (from how far the cursor moved) by the time the prefix must be written, so it
/// can simply be prepended.
///
/// The backing storage is `MaybeUninit`, so the allocation is never zeroed;
/// bytes are written into it and addressed manually. Two invariants make the
/// `unsafe` here sound, and every method upholds them:
///
/// 1. `pos <= buf.len()` (the cursor never escapes the allocation).
/// 2. `[pos, buf.len())` is always initialized (and `[0, pos)` is never read).
///
/// `ensure` reestablishes `pos >= n` before a write of `n` bytes lowers `pos`,
/// so each write stays in bounds and only ever initializes fresh space.
pub(crate) struct ReverseBuffer {
    /// Backing allocation. Its length always equals its capacity (see
    /// [`alloc_uninit`]); written bytes live in `[pos, len)`, in forward order.
    buf: Vec<MaybeUninit<u8>>,
    /// Index of the first written byte. Shrinks toward zero as bytes are
    /// written. Everything in `[pos, len)` is initialized.
    pos: usize,
}

/// Minimum allocation size once a write forces one, matching upb's encoder
/// floor. Empty messages never reach `grow`, so they allocate nothing.
const MIN_CAPACITY: usize = 128;

/// Allocates `capacity` (rounded up to the allocator's choice) uninitialized
/// bytes, exposed as a full-length `Vec`.
fn alloc_uninit(capacity: usize) -> Vec<MaybeUninit<u8>> {
    let mut buf = Vec::with_capacity(capacity);
    // SAFETY: `MaybeUninit<u8>` is valid in any state, including uninitialized,
    // so growing the length to the full allocated capacity is sound. This is
    // the only `set_len` in the file.
    unsafe {
        buf.set_len(buf.capacity());
    }
    buf
}

impl ReverseBuffer {
    /// Creates an empty buffer. No allocation happens until the first write, so
    /// serializing an empty message (e.g. `google.protobuf.Empty`) is
    /// allocation-free.
    pub(crate) fn new() -> Self {
        Self {
            buf: Vec::new(),
            pos: 0,
        }
    }

    /// Number of valid bytes written so far.
    #[must_use]
    pub(crate) fn len(&self) -> usize {
        self.buf.len() - self.pos
    }

    /// Ensures `additional` bytes can be prepended without overrunning.
    #[inline]
    fn ensure(&mut self, additional: usize) {
        if self.pos < additional {
            self.grow(additional);
        }
        debug_assert!(self.pos >= additional, "ensure failed to reserve room");
    }

    /// Reallocates with the existing data anchored to the end of the new buffer.
    #[cold]
    #[inline(never)]
    fn grow(&mut self, additional: usize) {
        let data_len = self.len();
        // Round the required size up to a power of two (>= the floor).
        let new_cap = (data_len + additional)
            .max(MIN_CAPACITY)
            .next_power_of_two();
        let mut new_buf = alloc_uninit(new_cap);
        let new_pos = new_buf.len() - data_len;
        new_buf[new_pos..].copy_from_slice(&self.buf[self.pos..]);
        self.buf = new_buf;
        self.pos = new_pos;
    }

    /// Prepends a byte slice in front of the current contents.
    #[inline]
    pub(crate) fn prepend_slice(&mut self, src: &[u8]) {
        let len = src.len();
        self.ensure(len);
        self.pos -= len;
        // SAFETY: `ensure(len)` guaranteed `pos >= len` before the decrement, so
        // `[pos, pos + len)` is within the allocation and src is never a slice
        // to this buffer.
        unsafe {
            std::ptr::copy_nonoverlapping(
                src.as_ptr(),
                self.buf.as_mut_ptr().add(self.pos).cast::<u8>(),
                len,
            );
        }
    }

    /// Prepends a single byte in front of the current contents.
    #[inline]
    pub(crate) fn prepend_u8(&mut self, byte: u8) {
        self.ensure(1);
        self.pos -= 1;
        // SAFETY: `ensure(1)` guaranteed `pos >= 1` before the decrement, so
        // `pos` is a valid index; the write initializes that byte.
        unsafe {
            self.buf.get_unchecked_mut(self.pos).write(byte);
        }
    }

    /// Prepends a base-128 varint encoding of `value`.
    #[inline]
    pub(crate) fn prepend_varint(&mut self, value: u64) {
        // Fast path: single-byte varints (values < 128) are by far the most
        // common — they cover field tags for numbers 1-15 plus many small
        // lengths and integers — and lower to one byte store, skipping the
        // scratch array and the runtime-length copy of the general path.
        if value < 0x80 {
            self.prepend_u8(value as u8);
        } else {
            self.prepend_varint_multibyte(value);
        }
    }

    /// Prepends a multi-byte (>= 2 byte) varint. Kept out of line so the hot
    /// single-byte path stays small enough to inline at every call site.
    #[inline(never)]
    fn prepend_varint_multibyte(&mut self, mut value: u64) {
        // Encode forward into a scratch array (LSB group first, matching wire
        // order) then prepend it as one contiguous block.
        let mut tmp = [0u8; 10];
        let mut n = 0;
        loop {
            if value < 0x80 {
                tmp[n] = value as u8;
                n += 1;
                break;
            }
            tmp[n] = ((value & 0x7F) | 0x80) as u8;
            n += 1;
            value >>= 7;
        }
        self.prepend_slice(&tmp[..n]);
    }

    /// Consumes the buffer, copying the written bytes into a Python `bytes`.
    pub(crate) fn into_py_bytes(self, py: Python<'_>) -> Bound<'_, PyBytes> {
        // SAFETY: every byte in `[pos, len)` was initialized when it was written
        // (invariant 2), so the window is a valid initialized `&[u8]`.
        let written = unsafe { self.buf[self.pos..].assume_init_ref() };
        PyBytes::new(py, written)
    }
}
