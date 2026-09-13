"""Searching algorithms that return an index into the original list, or -1 if the target isn't there."""


def linear_search(items, target):
    """Check every element in turn and return the index of the first match."""
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


def binary_search(items, target):
    """Binary Search on a sorted copy, returning the target's first index in the original list."""
    # Map each value to its first index, so duplicates report the same index as Linear Search
    first_index = {}
    for index, value in enumerate(items):
        first_index.setdefault(value, index)
    # Sort a copy so the original list keeps its order
    sorted_items = sorted(items)

    left, right = 0, len(sorted_items) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_items[mid] == target:
            # Map the match back to its index in the original list
            return first_index[sorted_items[mid]]
        elif sorted_items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
