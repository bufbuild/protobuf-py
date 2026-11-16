use pyo3::{Bound, PyResult, exceptions::PyValueError, types::PyString};

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

// Python strings have two structs, one for ASCII and one for others.
// They also always contain a trailing NUL, so the total overhead is
// the size of the header (40 or 56) + the size of the trailing NUL
// which depends on the width.
const STR_ASCII_OVERHEAD: usize = 41;
const STR_LATIN1_OVERHEAD: usize = 57;
const STR_UCS2_OVERHEAD: usize = 58;
const STR_UCS4_OVERHEAD: usize = 60;

/// The size of a str holding `chars` characters and its largest codepoint.
/// Python picks different representations based on the largest codepoint.
fn str_size_for(chars: usize, max_char: u32) -> usize {
    match max_char {
        0..0x80 => STR_ASCII_OVERHEAD + chars,
        0x80..0x100 => STR_LATIN1_OVERHEAD + chars,
        0x100..0x1_0000 => STR_UCS2_OVERHEAD + 2 * chars,
        _ => STR_UCS4_OVERHEAD + 4 * chars,
    }
}

/// The decoded size of a str.
fn str_size(utf8: &[u8]) -> usize {
    let max_byte = utf8.iter().fold(0, |max, &byte| max.max(byte));
    if max_byte < 0x80 {
        return STR_ASCII_OVERHEAD + utf8.len();
    }
    let chars = utf8.iter().filter(|&&byte| byte & 0xC0 != 0x80).count();
    match max_byte {
        // U+0080 to U+00FF
        0..=0xC3 => STR_LATIN1_OVERHEAD + chars,
        // U+0100 to U+FFFF
        0xC4..=0xEF => STR_UCS2_OVERHEAD + 2 * chars,
        _ => STR_UCS4_OVERHEAD + 4 * chars,
    }
}

/// The size of Python str.
#[cfg(not(any(Py_LIMITED_API, PyPy, GraalPy)))]
fn py_str_size(value: &Bound<'_, PyString>) -> PyResult<usize> {
    use pyo3::types::{PyStringMethods as _, string::PyStringData};

    // SAFETY - the data is only read, while the str is borrowed.
    Ok(match unsafe { value.data()? } {
        // An ASCII str has a smaller header than other single byte ones.
        PyStringData::Ucs1(data) => {
            let max_char = data.iter().fold(0, |max, &ch| max.max(ch));
            str_size_for(data.len(), max_char.into())
        }
        PyStringData::Ucs2(data) => STR_UCS2_OVERHEAD + 2 * data.len(),
        PyStringData::Ucs4(data) => STR_UCS4_OVERHEAD + 4 * data.len(),
    })
}

/// The size of Python str. The limited API cannot read how a str is stored,
/// so this finds its widest character one at a time.
#[cfg(any(Py_LIMITED_API, PyPy, GraalPy))]
fn py_str_size(value: &Bound<'_, PyString>) -> PyResult<usize> {
    use pyo3::{ffi, types::PyAnyMethods as _};

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

    /// Charges for the pre-decoded str.
    fn charge_str(&mut self, utf8: &[u8]) -> PyResult<()>;

    /// Charges for an existing Python string.
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
/// without a limit includes no accounting code.
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
