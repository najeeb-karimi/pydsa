"""Static, fixed-type array."""

from pydsa.core.errors import InvalidTypeError, OutOfBoundsError


class Array:
    """Fixed-size array that only accepts elements of a single data type."""

    def __init__(self, size, data_type, default_value=None):
        """Initialize the array with a size, data type and default value."""
        self.size = size
        self.data_type = data_type
        self.default_value = default_value
        if default_value is None or isinstance(default_value, data_type):
            self.items = [default_value] * size
        else:
            self.items = [data_type()] * size

    def _check_index(self, index):
        """Raise OutOfBoundsError if index is outside the array."""
        if not 0 <= index < self.size:
            raise OutOfBoundsError(f"Array index {index} is out of bounds for size {self.size}.")

    def insert(self, index, value):
        """Store value at index, replacing the element that was there."""
        if not isinstance(value, self.data_type):
            raise InvalidTypeError(f"Array can only contain elements of type {self.data_type.__name__}.")
        self._check_index(index)
        self.items[index] = value

    def remove(self, index):
        """Remove the element at index by resetting it to the default value."""
        self._check_index(index)
        self.items[index] = self.default_value

    def get(self, index):
        """Return the element at index."""
        self._check_index(index)
        return self.items[index]
