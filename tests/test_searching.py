"""Searching algorithms, checked against list.index()."""

import random

import pytest

from pydsa.algorithms.searching import binary_search, linear_search


@pytest.mark.parametrize("search", [linear_search, binary_search], ids=lambda search: search.__name__)
def test_matches_list_index(search):
    rng = random.Random(3)
    for _ in range(300):
        # Duplicates are allowed: both searches report the first index
        data = [rng.randint(-20, 20) for _ in range(rng.randint(0, 20))]
        for target in set(data) | {100, -100}:
            expected = data.index(target) if target in data else -1
            assert search(data, target) == expected


@pytest.mark.parametrize("search", [linear_search, binary_search], ids=lambda search: search.__name__)
def test_strings(search):
    words = ["pear", "apple", "fig", "banana", "apple"]
    for word in words:
        assert search(words, word) == words.index(word)
    assert search(words, "kiwi") == -1


def test_binary_search_keeps_the_original_order():
    data = [10, 1987, 672, 8, 2004]
    assert binary_search(data, 8) == 3
    assert data == [10, 1987, 672, 8, 2004]
