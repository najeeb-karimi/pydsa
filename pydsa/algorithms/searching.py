"""Searching algorithms that return an index into the original list, or -1 if the target isn't there.

Every search but linear search runs on a sorted copy, so the original list keeps its order, and reports the
target's first index in the original list. Pass a list as trace to record one TraceEvent per position that
was checked: positions in the original list for linear search, and in the sorted copy for the others. Each
event holds the list it searched, the position it checked and why the search moved on.
"""

from math import isqrt

from pydsa.algorithms.trace import record
from pydsa.core.errors import InvalidTypeError


def positions(trace):
    """Return the positions the recorded events checked, in order."""
    return [event.data["index"] for event in trace]


def _check(trace, kind, values, position, **data):
    """Record that a search looked at values[position] and what it decided."""
    record(trace, kind, list(values), {position: "checked"}, index=position, value=values[position], **data)


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def accepts(search, items):
    """Return True if search can run on items; interpolation search needs numbers, since it does math on them."""
    return search is not interpolation_search or all(_is_number(item) for item in items)


def linear_search(items, target, trace=None):
    """Check every element in turn and return the index of the first match."""
    for index, value in enumerate(items):
        if value == target:
            _check(trace, "match", items, index)
            return index
        _check(trace, "passed", items, index)
    return -1


def _on_sorted_copy(items, target, search, trace):
    """Run search on a sorted copy of items and map the position it finds back to the original list."""
    # Map each value to its first index, so duplicates report the same index as Linear Search
    first_index = {}
    for index, value in enumerate(items):
        first_index.setdefault(value, index)
    values = sorted(items)
    position = search(values, target, trace)
    return -1 if position == -1 else first_index[values[position]]


def binary_search(items, target, trace=None):
    """Binary Search on a sorted copy, returning the target's first index in the original list."""
    return _on_sorted_copy(items, target, _binary, trace)


def _binary(values, target, trace, left=0, right=None):
    """Halve values[left..right] until target is found; return its position or -1."""
    right = len(values) - 1 if right is None else right
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            _check(trace, "match", values, mid)
            return mid
        elif values[mid] < target:
            _check(trace, "too_small", values, mid, target=target)
            left = mid + 1
        else:
            _check(trace, "too_large", values, mid, target=target)
            right = mid - 1
    return -1


def jump_search(items, target, trace=None):
    """Jump Search on a sorted copy, returning the target's first index in the original list."""
    return _on_sorted_copy(items, target, _jump, trace)


def _jump(values, target, trace):
    """Jump ahead √n positions at a time until a block could hold target, then check that block one by one."""
    n = len(values)
    if not n:
        return -1
    step = isqrt(n)
    start, end = 0, min(step, n)
    while True:
        if values[end - 1] >= target:  # The last value of the block
            _check(trace, "block", values, end - 1, target=target)
            break
        _check(trace, "too_small", values, end - 1, target=target)
        start = end
        if start >= n:
            return -1
        end = min(end + step, n)
    for position in range(start, end):
        if values[position] == target:
            _check(trace, "match", values, position)
            return position
        if values[position] > target:
            _check(trace, "too_large", values, position, target=target)
            return -1
        _check(trace, "passed", values, position)
    return -1


def interpolation_search(items, target, trace=None):
    """Interpolation Search on a sorted copy of numbers, returning the target's first index in the original list.

    Raises InvalidTypeError if items or target aren't all numbers.
    """
    if not accepts(interpolation_search, items) or not _is_number(target):
        raise InvalidTypeError("Interpolation search only works on numbers.")
    return _on_sorted_copy(items, target, _interpolation, trace)


def _interpolation(values, target, trace):
    """Estimate target's position from its value, like looking up a name in a phone book."""
    low, high = 0, len(values) - 1
    while low <= high and values[low] <= target <= values[high]:
        if values[low] == values[high]:
            position = low
        else:
            # How far target is between the lowest and highest value decides how far along to look
            position = low + int((target - values[low]) * (high - low) / (values[high] - values[low]))
        if values[position] == target:
            _check(trace, "match", values, position)
            return position
        if values[position] < target:
            _check(trace, "too_small", values, position, target=target)
            low = position + 1
        else:
            _check(trace, "too_large", values, position, target=target)
            high = position - 1
    return -1


def exponential_search(items, target, trace=None):
    """Exponential Search on a sorted copy, returning the target's first index in the original list."""
    return _on_sorted_copy(items, target, _exponential, trace)


def _exponential(values, target, trace):
    """Double a bound until it passes target, then binary search between the last two bounds."""
    n = len(values)
    if not n:
        return -1
    if values[0] == target:
        _check(trace, "match", values, 0)
        return 0
    _check(trace, "passed", values, 0)
    bound = 1
    while bound < n:
        if values[bound] == target:
            _check(trace, "match", values, bound)
            return bound
        if values[bound] > target:
            # The target can only sit after the previous bound, which was smaller, and before this one
            _check(trace, "bound", values, bound, target=target)
            return _binary(values, target, trace, bound // 2 + 1, bound - 1)
        _check(trace, "too_small", values, bound, target=target)
        bound *= 2
    return _binary(values, target, trace, bound // 2 + 1, n - 1)
