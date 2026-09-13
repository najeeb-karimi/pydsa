"""Sorting generators, checked against sorted()."""

import random

import pytest

from pydsa.algorithms import sorting

ALGORITHMS = [
    sorting.bubble_sort,
    sorting.selection_sort,
    sorting.insertion_sort,
    sorting.quick_sort,
    sorting.heap_sort,
    sorting.shell_sort,
]

_rng = random.Random(7)
CASES = [
    [],
    [1],
    [2, 1],
    [10, 1987, 672, 8, 2004],
    [5, 5, 3, 3, 1, 9, 0, -4],
    ["pear", "apple", "fig", "banana"],
] + [[_rng.randint(-50, 50) for _ in range(_rng.randint(0, 25))] for _ in range(100)]


@pytest.mark.parametrize("order", ["asc", "desc"])
@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda algorithm: algorithm.__name__)
def test_sorts_in_place(algorithm, order):
    for data in CASES:
        items = list(data)
        steps = list(algorithm(items, order))
        expected = sorted(data, reverse=order == "desc")

        assert items == expected
        # Every step is a copy holding the same elements, and the last one is the sorted list
        assert all(step is not items and sorted(step) == sorted(data) for step in steps)
        if steps:
            assert steps[-1] == expected


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
    assert list(sorting.bubble_sort([3, 2, 1])) == [[2, 3, 1], [2, 1, 3], [1, 2, 3]]
