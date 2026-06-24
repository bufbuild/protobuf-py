use std::{collections::HashSet, sync::Mutex};

use bitvec::{BitArr, array::BitArray};
use pyo3::PyResult;

// Match size of Inline enum variant by using the size of a HashSet, accounting
// for its niche by subtracting one word.
#[allow(clippy::cast_possible_truncation)]
const INLINE_BITS: u32 = ((std::mem::size_of::<HashSet<u32>>() - 8) * 8) as u32;

enum BitSetInner {
    Inline(BitArr!(for INLINE_BITS as usize)),
    Set(HashSet<u32>),
}

/// Very simple bitset for protobuf field presence checks.
///
/// There are two implementations
///
/// - Inline: tracks up to `INLINE_BITS` bits with an inline array. Used for messages requiring presence tracking with a maximum field number up to `INLINE_BITS`
/// - Set: tracks bits using a `HashSet`. Fallback, allows any combination of field numbers even if very sparse
pub(crate) struct BitSet {
    inner: Mutex<BitSetInner>,
}

impl BitSet {
    /// Returns a new `BitSet` for tracking a message with the given maximum field number.
    pub(crate) fn new(max_field_number: u32) -> Self {
        let inner = if max_field_number < INLINE_BITS {
            BitSetInner::Inline(BitArray::ZERO)
        } else {
            BitSetInner::Set(HashSet::new())
        };
        Self {
            inner: Mutex::new(inner),
        }
    }

    pub(crate) fn set(&self, field_number: u32, bit: bool) {
        let inner = &mut *self.inner.lock().unwrap();
        match inner {
            BitSetInner::Inline(bits) => {
                bits.set(field_number as usize, bit);
            }
            BitSetInner::Set(set) => {
                if bit {
                    set.insert(field_number);
                } else {
                    set.remove(&field_number);
                }
            }
        }
    }

    pub(crate) fn get(&self, field_number: u32) -> bool {
        let inner = &*self.inner.lock().unwrap();
        match inner {
            BitSetInner::Inline(bits) => bits.get(field_number as usize).is_some_and(|b| *b),
            BitSetInner::Set(set) => set.contains(&field_number),
        }
    }

    pub(crate) fn for_each(&self, f: impl Fn(usize) -> PyResult<()>) -> PyResult<()> {
        let inner = &*self.inner.lock().unwrap();
        match inner {
            BitSetInner::Inline(bits) => {
                for i in bits.iter_ones() {
                    f(i)?;
                }
            }
            BitSetInner::Set(set) => {
                for &i in set {
                    f(i as usize)?;
                }
            }
        }
        Ok(())
    }

    pub(crate) fn set_all(&self, set: &BitSet) {
        let mut inner = self.inner.lock().unwrap();
        let other_inner = set.inner.lock().unwrap();
        match (&mut *inner, &*other_inner) {
            (BitSetInner::Inline(bits), BitSetInner::Inline(other_bits)) => {
                *bits |= *other_bits;
            }
            (BitSetInner::Set(set), BitSetInner::Set(other_set)) => {
                set.extend(other_set);
            }
            _ => unreachable!("incompatible bitset types when copying. This is a bug in protobuf"),
        }
    }
}
