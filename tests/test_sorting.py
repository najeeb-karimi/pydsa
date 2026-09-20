"""Sorting generators, checked against sorted()."""

import random

import pytest

from pydsa.algorithms import sorting
from pydsa.algorithms.sorting import SortStats
from pydsa.core.errors import InvalidTypeError

ALGORITHMS = [
    sorting.bubble_sort,
    sorting.selection_sort,
    sorting.insertion_sort,
    sorting.quick_sort,
    sorting.heap_sort,
    sorting.shell_sort,
    sorting.merge_sort,
    sorting.counting_sort,
    sorting.radix_sort,
]

def lists(events):
    """Return the list as it was after every step."""
    return [event.snapshot for event in events]


_rng = random.Random(7)
CASES = [
    [],
    [1],
    [2, 1],
    [10, 1987, 672, 8, 2004],
    [5, 5, 3, 3, 1, 9, 0, -4],
    [2.5, -1, 3],
    ["pear", "apple", "fig", "banana"],
] + [[_rng.randint(-50, 50) for _ in range(_rng.randint(0, 25))] for _ in range(100)] \
  + [[_rng.randint(0, 999) for _ in range(_rng.randint(0, 25))] for _ in range(50)]


@pytest.mark.parametrize("order", ["asc", "desc"])
@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda algorithm: algorithm.__name__)
def test_sorts_in_place(algorithm, order):
    for data in CASES:
        if not sorting.accepts(algorithm, data):
            with pytest.raises(InvalidTypeError):
                algorithm(list(data), order)
            continue

        items, stats = list(data), SortStats()
        steps = lists(algorithm(items, order, stats))
        expected = sorted(data, reverse=order == "desc")

        assert items == expected
        assert all(step is not items for step in steps)
        if algorithm is not sorting.counting_sort:
            # Every step holds the same elements; counting sort instead overwrites the list value by value
            assert all(sorted(step) == sorted(data) for step in steps)
        if steps:
            assert steps[-1] == expected
        if algorithm in (sorting.counting_sort, sorting.radix_sort):
            assert stats.comparisons == 0
        # Every value that ends up somewhere else had to be written at least once
        assert stats.writes >= sum(1 for before, after in zip(data, expected) if before != after)


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda algorithm: algorithm.__name__)
def test_returns_the_sorted_list(algorithm):
    items = [3, 1, 2]
    generator = algorithm(items)
    with pytest.raises(StopIteration) as stop:
        while True:
            next(generator)
    assert stop.value.value is items
    assert items == [1, 2, 3]


def test_bubble_sort_yields_after_every_swap():
    assert lists(sorting.bubble_sort([3, 2, 1])) == [[2, 3, 1], [2, 1, 3], [1, 2, 3]]


def test_counters():
    stats = SortStats()
    list(sorting.bubble_sort([3, 2, 1], "asc", stats))
    assert (stats.comparisons, stats.writes) == (3, 6)

    stats = SortStats()
    list(sorting.insertion_sort([1, 2, 3], "asc", stats))
    assert (stats.comparisons, stats.writes) == (2, 2)  # Already sorted: one comparison and one write per insertion

    stats = SortStats()
    list(sorting.radix_sort([170, 45, 75, 90, 802, 24, 2, 66], "asc", stats))
    assert (stats.comparisons, stats.writes) == (0, 24)  # All 8 values are written back once per digit


def test_merge_sort_yields_after_every_merge():
    for n in range(10):
        assert len(list(sorting.merge_sort(list(range(n, 0, -1))))) == max(n - 1, 0)


def test_counting_sort_handles_negative_values():
    items = [3, -2, 0, -2, 5]
    steps = lists(sorting.counting_sort(items))
    assert items == [-2, -2, 0, 3, 5]
    assert steps[0] == [-2, -2, 0, -2, 5]  # Both copies of -2 are written first


def test_radix_sort_yields_after_every_digit():
    assert lists(sorting.radix_sort([170, 45, 75, 90, 802, 24, 2, 66])) == [
        [170, 90, 802, 2, 24, 45, 75, 66],
        [802, 2, 24, 45, 66, 170, 75, 90],
        [2, 24, 45, 66, 75, 90, 170, 802],
    ]


def test_what_counting_and_radix_sort_accept():
    assert not sorting.accepts(sorting.counting_sort, ["a"])
    assert not sorting.accepts(sorting.counting_sort, [1.5])
    assert not sorting.accepts(sorting.counting_sort, [0, sorting.COUNTING_RANGE_LIMIT])
    assert sorting.accepts(sorting.counting_sort, [-5, 5])
    assert not sorting.accepts(sorting.radix_sort, [1, -1])
    assert sorting.accepts(sorting.bubble_sort, ["a", "b"])
    with pytest.raises(InvalidTypeError):
        sorting.radix_sort([-1])
