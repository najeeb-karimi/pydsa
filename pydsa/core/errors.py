"""Exceptions raised by the PyDSA data structures."""


class PyDSAError(Exception):
    """Base class for every error raised by a PyDSA data structure."""


class OutOfBoundsError(PyDSAError, IndexError):
    """An index, position or vertex is outside the valid range."""


class CapacityError(PyDSAError):
    """A fixed-size structure has no room left."""


class EmptyError(PyDSAError):
    """The operation needs at least one element, but the structure is empty."""


class NotFoundError(PyDSAError, LookupError):
    """A key, node or vertex doesn't exist."""


class DuplicateError(PyDSAError):
    """An item that must be unique already exists."""


class InvalidTypeError(PyDSAError, TypeError):
    """A value doesn't match the data type the structure holds."""
