use pyo3::{
    Bound, PyResult,
    exceptions::PyValueError,
    ffi,
    types::{PyAnyMethods as _, PyString},
};

// Approximate sizes of CPython heap allocations, measured with
// `sys.getsizeof` on 64-bit CPython 3.14. The budget guards against
// unbounded allocation from malicious payloads rather than providing exact
// accounting, so small inaccuracies across versions and builds are fine.

/// GC header allocated in front of every GC-tracked object.
pub(crate) const GC_HEAD_SIZE: usize = 16;
/// A float object.
pub(crate) const FLOAT_SIZE: usize = 24;
/// A 64-bit int object. Smaller ints are slightly smaller.
pub(crate) const INT_SIZE: usize = 36;
/// Header of a bytes object.
pub(crate) const BYTES_OVERHEAD: usize = 33;
/// An empty list.
pub(crate) const EMPTY_LIST_SIZE: usize = 56;
/// An empty dict.
pub(crate) const EMPTY_DICT_SIZE: usize = 64;
/// One appended list element: an 8-byte pointer slot.
pub(crate) const LIST_SLOT_SIZE: usize = 8;
/// One inserted dict entry: hash + key + value words plus growth slack.
pub(crate) const DICT_ENTRY_SIZE: usize = 40;
/// A `Oneof` wrapper object: `PyObject` header plus two object pointers.
pub(crate) const ONEOF_SIZE: usize = 32;

// A str stores every character at the width of its widest one, with a header
// (including the trailing NUL) that depends on that width.
const STR_ASCII_OVERHEAD: usize = 41;
const STR_LATIN1_OVERHEAD: usize = 57;
const STR_UCS2_OVERHEAD: usize = 58;
const STR_UCS4_OVERHEAD: usize = 60;

/// The size of a str holding `chars` characters, the widest being `max_char`.
fn str_size_for(chars: usize, max_char: u32) -> usize {
    match max_char {
        0..0x80 => STR_ASCII_OVERHEAD + chars,
        0x80..0x100 => STR_LATIN1_OVERHEAD + chars,
        0x100..0x1_0000 => STR_UCS2_OVERHEAD + 2 * chars,
        _ => STR_UCS4_OVERHEAD + 4 * chars,
    }
}

/// The size of the str that `utf8` decodes to. Does not validate the input;
/// the result is only meaningful for valid UTF-8.
fn str_size(utf8: &[u8]) -> usize {
    if utf8.is_ascii() {
        return STR_ASCII_OVERHEAD + utf8.len();
    }
    // Continuation bytes are below every lead byte of a multi-byte sequence,
    // so the largest byte is the lead byte of the widest character.
    let max_byte = utf8.iter().fold(0, |max, &byte| max.max(byte));
    let chars = utf8.iter().filter(|&&byte| byte & 0xC0 != 0x80).count();
    match max_byte {
        // U+0080 to U+00FF
        0..=0xC3 => STR_LATIN1_OVERHEAD + chars,
        // U+0100 to U+FFFF
        0xC4..=0xEF => STR_UCS2_OVERHEAD + 2 * chars,
        _ => STR_UCS4_OVERHEAD + 4 * chars,
    }
}

/// The size of an existing str, without materializing its UTF-8 form.
fn py_str_size(value: &Bound<'_, PyString>) -> PyResult<usize> {
    let len = value.len()?;
    let mut max_char = 0;
    for i in 0..len {
        // SAFETY - value is a str and i is within its length.
        let ch = unsafe { ffi::PyUnicode_ReadChar(value.as_ptr(), i.cast_signed()) };
        max_char = max_char.max(ch);
        if max_char > 0xFFFF {
            break;
        }
    }
    Ok(str_size_for(len, max_char))
}

/// Accounts for the Python objects allocated while parsing a message.
pub(crate) trait Budget {
    /// Charges `amount` bytes.
    fn charge(&mut self, amount: usize) -> PyResult<()>;

    /// Charges for the str that `utf8` decodes to.
    fn charge_str(&mut self, utf8: &[u8]) -> PyResult<()>;

    /// Charges for an existing str.
    fn charge_py_str(&mut self, value: &Bound<'_, PyString>) -> PyResult<()>;
}

/// Tracks the approximate bytes allocated, raising an error once a limit is
/// exceeded.
pub(crate) struct TrackingBudget {
    current: usize,
    max: usize,
}

impl TrackingBudget {
    pub(crate) fn new(limit: usize) -> Self {
        Self {
            current: 0,
            max: limit,
        }
    }
}

impl Budget for TrackingBudget {
    fn charge(&mut self, amount: usize) -> PyResult<()> {
        self.current = self.current.saturating_add(amount);
        if self.current > self.max {
            Err(PyValueError::new_err(format!(
                "allocation budget exceeded: needed {} bytes, limit is {}",
                self.current, self.max
            )))
        } else {
            Ok(())
        }
    }

    fn charge_str(&mut self, utf8: &[u8]) -> PyResult<()> {
        self.charge(str_size(utf8))
    }

    fn charge_py_str(&mut self, value: &Bound<'_, PyString>) -> PyResult<()> {
        self.charge(py_str_size(value)?)
    }
}

/// Does no accounting, for parsing without an allocation limit.
pub(crate) struct NoopBudget;

impl Budget for NoopBudget {
    fn charge(&mut self, _amount: usize) -> PyResult<()> {
        Ok(())
    }

    fn charge_str(&mut self, _utf8: &[u8]) -> PyResult<()> {
        Ok(())
    }

    fn charge_py_str(&mut self, _value: &Bound<'_, PyString>) -> PyResult<()> {
        Ok(())
    }
}

/// Evaluates `$body` with `$budget` bound to the budget for an optional
/// allocation limit. The body is compiled for each implementation, so parsing
/// without a limit does no accounting.
macro_rules! with_budget {
    ($limit:expr, |$budget:ident| $body:expr) => {
        match $limit {
            Some(limit) => {
                let $budget = &mut $crate::budget::TrackingBudget::new(limit);
                $body
            }
            None => {
                let $budget = &mut $crate::budget::NoopBudget;
                $body
            }
        }
    };
}
pub(crate) use with_budget;
