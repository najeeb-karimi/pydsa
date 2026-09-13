"""Searching algorithms that return an index into the original list, or -1 if the target isn't there.

Every search but linear search runs on a sorted copy, so the original list keeps its order, and reports the
target's first index in the original list. Pass a list as probes to record the positions that were checked:
indexes of the original list for linear search, and positions in the sorted copy for the others.
"""

from math import isqrt

from pydsa.core.errors import InvalidTypeError


def _record(probes, position):
    if probes is not None:
        probes.append(position)


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def accepts(search, items):
    """Return True if search can run on items; interpolation search needs numbers, since it does math on them."""
    return search is not interpolation_search or all(_is_number(item) for item in items)


def linear_search(items, target, probes=None):
    """Check every element in turn and return the index of the first match."""
    for index, value in enumerate(items):
        _record(probes, index)
        if value == target:
            return index
    return -1


def _on_sorted_copy(items, target, search, probes):
    """Run search on a sorted copy of items and map the position it finds back to the original list."""
    # Map each value to its first index, so duplicates report the same index as Linear Search
    first_index = {}
    for index, value in enumerate(items):
        first_index.setdefault(value, index)
    values = sorted(items)
    position = search(values, target, probes)
    return -1 if position == -1 else first_index[values[position]]


def binary_search(items, target, probes=None):
    """Binary Search on a sorted copy, returning the target's first index in the original list."""
    return _on_sorted_copy(items, target, _binary, probes)


def _binary(values, target, probes, left=0, right=None):
    """Halve values[left..right] until target is found; return its position or -1."""
    right = len(values) - 1 if right is None else right
    while left <= right:
        mid = (left + right) // 2
        _record(probes, mid)
        if values[mid] == target:
            return mid
        elif values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def jump_search(items, target, probes=None):
    """Jump Search on a sorted copy, returning the target's first index in the original list."""
    return _on_sorted_copy(items, target, _jump, probes)


def _jump(values, target, probes):
    """Jump ahead √n positions at a time until a block could hold target, then check that block one by one."""
    n = len(values)
    if not n:
        return -1
    step = isqrt(n)
    start, end = 0, min(step, n)
    while True:
        _record(probes, end - 1)  # The last value of the block
        if values[end - 1] >= target:
            break
        start = end
        if start >= n:
            return -1
        end = min(end + step, n)
    for position in range(start, end):
        _record(probes, position)
        if values[position] == target:
            return position
        if values[position] > target:
            return -1
    return -1


def interpolation_search(items, target, probes=None):
    """Interpolation Search on a sorted copy of numbers, returning the target's first index in the original list.

    Raises InvalidTypeError if items or target aren't all numbers.
    """
    if not accepts(interpolation_search, items) or not _is_number(target):
        raise InvalidTypeError("Interpolation search only works on numbers.")
    return _on_sorted_copy(items, target, _interpolation, probes)


def _interpolation(values, target, probes):
    """Estimate target's position from its value, like looking up a name in a phone book."""
    low, high = 0, len(values) - 1
    while low <= high and values[low] <= target <= values[high]:
        if values[low] == values[high]:
            position = low
        else:
            # How far target is between the lowest and highest value decides how far along to look
            position = low + int((target - values[low]) * (high - low) / (values[high] - values[low]))
        _record(probes, position)
        if values[position] == target:
            return position
        if values[position] < target:
            low = position + 1
        else:
            high = position - 1
    return -1


def exponential_search(items, target, probes=None):
    """Exponential Search on a sorted copy, returning the target's first index in the original list."""
    return _on_sorted_copy(items, target, _exponential, probes)


def _exponential(values, target, probes):
    """Double a bound until it passes target, then binary search between the last two bounds."""
    n = len(values)
    if not n:
        return -1
    _record(probes, 0)
    if values[0] == target:
        return 0
    bound = 1
    while bound < n:
        _record(probes, bound)
        if values[bound] == target:
            return bound
        if values[bound] > target:
            # The target can only sit after the previous bound, which was smaller, and before this one
            return _binary(values, target, probes, bound // 2 + 1, bound - 1)
        bound *= 2
    return _binary(values, target, probes, bound // 2 + 1, n - 1)
