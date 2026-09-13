"""Sorting algorithms written as generators that sort a list in place, one step at a time.

Every generator yields a snapshot (a copy) of the list after each step, so a caller can show the
intermediate states or simply exhaust the generator. When it finishes, the list is sorted and is also
the generator's return value. order is "asc" or "desc".
"""


def _out_of_order(a, b, order):
    """Return True if a has to come after b in the given order."""
    return a > b if order == "asc" else a < b


def bubble_sort(items, order="asc"):
    """Bubble Sort, yielding the list after every swap."""
    n = len(items)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if _out_of_order(items[j], items[j + 1], order):
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
                yield list(items)
        # A pass without swaps means the list is already sorted
        if not swapped:
            break
    return items


def selection_sort(items, order="asc"):
    """Selection Sort, yielding the list after every pass."""
    n = len(items)
    for i in range(n):
        # Find the minimum (or maximum) element in the unsorted part
        min_max_index = i
        for j in range(i + 1, n):
            if _out_of_order(items[min_max_index], items[j], order):
                min_max_index = j
        # Swap it with the first unsorted element
        items[i], items[min_max_index] = items[min_max_index], items[i]
        yield list(items)
    return items


def insertion_sort(items, order="asc"):
    """Insertion Sort, yielding the list after every insertion."""
    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        # Shift the elements of items[0..i-1] that belong after key one position ahead
        while j >= 0 and _out_of_order(items[j], key, order):
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key
        yield list(items)
    return items


def quick_sort(items, order="asc"):
    """Quick Sort, yielding the list after every partition."""
    yield from _quick_sort(items, 0, len(items) - 1, order)
    return items


def _quick_sort(items, low, high, order):
    """Recursively sort items[low..high] around a pivot."""
    if low < high:
        pivot_index = yield from _partition(items, low, high, order)
        yield from _quick_sort(items, low, pivot_index - 1, order)
        yield from _quick_sort(items, pivot_index + 1, high, order)


def _partition(items, low, high, order):
    """Move the pivot (the last element) to its sorted position and return that index."""
    pivot = items[high]
    i = low - 1
    for j in range(low, high):
        if not _out_of_order(items[j], pivot, order):
            i += 1
            items[i], items[j] = items[j], items[i]
    items[i + 1], items[high] = items[high], items[i + 1]
    yield list(items)
    return i + 1


def heap_sort(items, order="asc"):
    """Heap Sort, yielding the list while building the heap and while emptying it."""
    n = len(items)

    # Build a max heap (or min heap)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(items, n, i, order)
        yield list(items)

    # Repeatedly move the root to the end and restore the heap
    for i in range(n - 1, 0, -1):
        items[i], items[0] = items[0], items[i]
        yield list(items)

        _heapify(items, i, 0, order)
        yield list(items)

    return items


def _heapify(items, n, i, order):
    """Sift node i down so its subtree is a max heap (or a min heap for descending order)."""
    while True:
        # Start by treating the root as the largest (or smallest)
        largest_smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Check whether the left child should replace the root
        if left < n and _out_of_order(items[left], items[largest_smallest], order):
            largest_smallest = left

        # Check whether the right child should replace the current pick
        if right < n and _out_of_order(items[right], items[largest_smallest], order):
            largest_smallest = right

        # Stop once the root is in place; otherwise swap and keep sifting down from the child
        if largest_smallest == i:
            return
        items[i], items[largest_smallest] = items[largest_smallest], items[i]
        i = largest_smallest


def shell_sort(items, order="asc"):
    """Shell Sort, yielding the list after every gap size."""
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
            while j >= gap and _out_of_order(items[j - gap], temp, order):
                items[j] = items[j - gap]
                j -= gap

            # Put temp in its correct location
            items[j] = temp
        yield list(items)
        gap //= 2

    return items
