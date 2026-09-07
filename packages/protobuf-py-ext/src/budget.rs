use pyo3::{PyResult, exceptions::PyValueError};

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
/// Header of a compact ASCII str. The UTF-8 byte length is charged on top
/// as an approximation of the payload.
pub(crate) const STR_OVERHEAD: usize = 41;
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

/// Tracks the approximate bytes of Python objects allocated while parsing a
/// message, raising an error once a configured limit is exceeded.
pub(crate) struct Budget {
    current: usize,
    max: usize,
}

impl Budget {
    pub(crate) fn new(limit: Option<usize>) -> Self {
        Self {
            current: 0,
            max: limit.unwrap_or(usize::MAX),
        }
    }

    pub(crate) fn charge(&mut self, amount: usize) -> PyResult<()> {
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
}
