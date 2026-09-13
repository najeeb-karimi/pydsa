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


class NegativeWeightError(PyDSAError, ValueError):
    """A graph algorithm that needs non-negative weights found a negative one."""

    def __init__(self, u, v, weight):
        super().__init__(f"The edge from {u} to {v} has the negative weight {weight}.")
        self.edge = (u, v, weight)


class CycleError(PyDSAError):
    """A graph algorithm that needs an acyclic graph found a cycle.

    order holds the vertices that could still be placed, and remaining the ones on or behind a cycle.
    """

    def __init__(self, order, remaining):
        super().__init__("The graph has a cycle.")
        self.order = order
        self.remaining = remaining
