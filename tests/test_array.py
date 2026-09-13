"""Static, fixed-type array."""

import pytest

from pydsa.core.array import Array
from pydsa.core.errors import InvalidTypeError, OutOfBoundsError


def test_starts_filled_with_the_default_value():
    assert Array(3, int, 0).items == [0, 0, 0]
    assert Array(2, str, "").items == ["", ""]
    # A default of the wrong type falls back to the type's own default
    assert Array(2, int, "x").items == [0, 0]


def test_insert_get_and_remove():
    array = Array(3, int, 0)
    array.insert(1, 42)
    assert array.get(1) == 42
    assert array.items == [0, 42, 0]
    array.remove(1)
    assert array.items == [0, 0, 0]


@pytest.mark.parametrize("index", [-1, 3, 10])
def test_out_of_bounds(index):
    array = Array(3, int, 0)
    with pytest.raises(OutOfBoundsError):
        array.insert(index, 1)
    with pytest.raises(OutOfBoundsError):
        array.remove(index)
    with pytest.raises(OutOfBoundsError):
        array.get(index)


def test_rejects_other_types_before_checking_the_index():
    array = Array(3, int, 0)
    with pytest.raises(InvalidTypeError):
        array.insert(99, "hello")
    assert array.items == [0, 0, 0]
