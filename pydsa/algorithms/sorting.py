"""Sorting algorithms written as generators that sort a list in place, one step at a time.

Every generator yields a snapshot (a copy) of the list after each step, so a caller can show the
intermediate states or simply exhaust the generator. When it finishes, the list is sorted and is also
the generator's return value. order is "asc" or "desc", and an optional SortStats counts the work done.
"""

from pydsa.core.errors import InvalidTypeError

COUNTING_RANGE_LIMIT = 10_000  # Counting sort needs one counter per value between the smallest and largest


class SortStats:
    """Counts the comparisons between values and the writes of values into the list; a swap is two writes."""

    def __init__(self):
        self.comparisons = 0
        self.writes = 0


def _out_of_order(a, b, order, stats):
    """Return True if a has to come after b in the given order."""
    stats.comparisons += 1
    return a > b if order == "asc" else a < b


def _swap(items, i, j, stats):
    items[i], items[j] = items[j], items[i]
    stats.writes += 2


def accepts(algorithm, items):
    """Return True if algorithm can sort items.

    Counting sort needs ints that are less than COUNTING_RANGE_LIMIT apart, and radix sort needs ints that
    aren't negative. Every other algorithm sorts any values that can be compared with each other.
    """
    if algorithm in (counting_sort, radix_sort) and not all(type(item) is int for item in items):
        return False
    if algorithm is counting_sort and items:
        return max(items) - min(items) < COUNTING_RANGE_LIMIT
    if algorithm is radix_sort:
        return all(item >= 0 for item in items)
    return True


def bubble_sort(items, order="asc", stats=None):
    """Bubble Sort, yielding the list after every swap."""
    stats = stats or SortStats()
    n = len(items)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if _out_of_order(items[j], items[j + 1], order, stats):
                _swap(items, j, j + 1, stats)
                swapped = True
                yield list(items)
        # A pass without swaps means the list is already sorted
        if not swapped:
            break
    return items


def selection_sort(items, order="asc", stats=None):
    """Selection Sort, yielding the list after every pass."""
    stats = stats or SortStats()
    n = len(items)
    for i in range(n):
        # Find the minimum (or maximum) element in the unsorted part
        min_max_index = i
        for j in range(i + 1, n):
            if _out_of_order(items[min_max_index], items[j], order, stats):
                min_max_index = j
        # Swap it with the first unsorted element
        _swap(items, i, min_max_index, stats)
        yield list(items)
    return items


def insertion_sort(items, order="asc", stats=None):
    """Insertion Sort, yielding the list after every insertion."""
    stats = stats or SortStats()
    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        # Shift the elements of items[0..i-1] that belong after key one position ahead
        while j >= 0 and _out_of_order(items[j], key, order, stats):
            items[j + 1] = items[j]
            stats.writes += 1
            j -= 1
        items[j + 1] = key
        stats.writes += 1
        yield list(items)
    return items


def quick_sort(items, order="asc", stats=None):
    """Quick Sort, yielding the list after every partition."""
    yield from _quick_sort(items, 0, len(items) - 1, order, stats or SortStats())
    return items


def _quick_sort(items, low, high, order, stats):
    """Recursively sort items[low..high] around a pivot."""
    if low < high:
        pivot_index = yield from _partition(items, low, high, order, stats)
        yield from _quick_sort(items, low, pivot_index - 1, order, stats)
        yield from _quick_sort(items, pivot_index + 1, high, order, stats)


def _partition(items, low, high, order, stats):
    """Move the pivot (the last element) to its sorted position and return that index."""
    pivot = items[high]
    i = low - 1
    for j in range(low, high):
        if not _out_of_order(items[j], pivot, order, stats):
            i += 1
            _swap(items, i, j, stats)
    _swap(items, i + 1, high, stats)
    yield list(items)
    return i + 1


def heap_sort(items, order="asc", stats=None):
    """Heap Sort, yielding the list while building the heap and while emptying it."""
    stats = stats or SortStats()
    n = len(items)

    # Build a max heap (or min heap)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(items, n, i, order, stats)
        yield list(items)

    # Repeatedly move the root to the end and restore the heap
    for i in range(n - 1, 0, -1):
        _swap(items, 0, i, stats)
        yield list(items)

        _heapify(items, i, 0, order, stats)
        yield list(items)

    return items


def _heapify(items, n, i, order, stats):
    """Sift node i down so its subtree is a max heap (or a min heap for descending order)."""
    while True:
        # Start by treating the root as the largest (or smallest)
        largest_smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Check whether the left child should replace the root
        if left < n and _out_of_order(items[left], items[largest_smallest], order, stats):
            largest_smallest = left

        # Check whether the right child should replace the current pick
        if right < n and _out_of_order(items[right], items[largest_smallest], order, stats):
            largest_smallest = right

        # Stop once the root is in place; otherwise swap and keep sifting down from the child
        if largest_smallest == i:
            return
        _swap(items, i, largest_smallest, stats)
        i = largest_smallest


def shell_sort(items, order="asc", stats=None):
    """Shell Sort, yielding the list after every gap size."""
    stats = stats or SortStats()
    n = len(items)
    gap = n // 2

    # Start with a big gap, then reduce it
    while gap > 0:
        # Gapped insertion sort: the first gap elements are already in gapped order,
        # so keep adding one more element until the whole list is gap-sorted
        for i in range(gap, n):
            temp = items[i]
            # Shift earlier gap-sorted elements up until the correct spot for temp is found
            j = i
            while j >= gap and _out_of_order(items[j - gap], temp, order, stats):
                items[j] = items[j - gap]
                stats.writes += 1
                j -= gap

            # Put temp in its correct location
            items[j] = temp
            stats.writes += 1
        yield list(items)
        gap //= 2

    return items


def merge_sort(items, order="asc", stats=None):
    """Merge Sort, yielding the list after every merge."""
    yield from _merge_sort(items, 0, len(items), order, stats or SortStats())
    return items


def _merge_sort(items, low, high, order, stats):
    """Recursively sort items[low:high] by sorting both halves and merging them."""
    if high - low < 2:
        return
    mid = (low + high) // 2
    yield from _merge_sort(items, low, mid, order, stats)
    yield from _merge_sort(items, mid, high, order, stats)

    # Repeatedly take the front value of whichever half comes first; ties take the left one, keeping equal values in order
    merged, i, j = [], low, mid
    while i < mid and j < high:
        if _out_of_order(items[i], items[j], order, stats):
            merged.append(items[j])
            j += 1
        else:
            merged.append(items[i])
            i += 1
    merged += items[i:mid] + items[j:high]

    for offset, value in enumerate(merged):
        items[low + offset] = value
        stats.writes += 1
    yield list(items)


def counting_sort(items, order="asc", stats=None):
    """Counting Sort for ints, yielding the list after all copies of a value are written back.

    Raises InvalidTypeError right away if accepts() rejects items.
    """
    if not accepts(counting_sort, items):
        raise InvalidTypeError(f"Counting sort only sorts ints that are less than {COUNTING_RANGE_LIMIT} apart.")
    return _counting_sort(items, order, stats or SortStats())


def _counting_sort(items, order, stats):
    if items:
        # Subtracting the smallest value turns every value into a counter index, even negative values
        offset = min(items)
        counts = [0] * (max(items) - offset + 1)
        for value in items:
            counts[value - offset] += 1

        positions = range(len(counts)) if order == "asc" else range(len(counts) - 1, -1, -1)
        index = 0
        for position in positions:
            for _ in range(counts[position]):
                items[index] = position + offset
                stats.writes += 1
                index += 1
            if counts[position]:
                yield list(items)
    return items


def radix_sort(items, order="asc", stats=None):
    """Radix Sort (least significant digit first) for non-negative ints, yielding the list after every digit.

    Raises InvalidTypeError right away if accepts() rejects items.
    """
    if not accepts(radix_sort, items):
        raise InvalidTypeError("Radix sort only sorts ints that aren't negative.")
    return _radix_sort(items, order, stats or SortStats())


def _radix_sort(items, order, stats):
    place = 1
    largest = max(items, default=0)
    while largest // place > 0:
        # Deal the values into one bucket per digit, keeping their current order within each bucket
        buckets = [[] for _ in range(10)]
        for value in items:
            buckets[value // place % 10].append(value)
        if order == "desc":
            buckets.reverse()

        for index, value in enumerate(value for bucket in buckets for value in bucket):
            items[index] = value
            stats.writes += 1
        yield list(items)
        place *= 10
    return items
