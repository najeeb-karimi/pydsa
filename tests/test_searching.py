"""Searching algorithms, checked against list.index()."""

import random

import pytest

from pydsa.algorithms import searching
from pydsa.core.errors import InvalidTypeError

SEARCHES = [
    searching.linear_search,
    searching.binary_search,
    searching.jump_search,
    searching.interpolation_search,
    searching.exponential_search,
]

# The most positions each search may check in a list of n values
PROBE_LIMITS = {
    searching.linear_search: lambda n: n,
    searching.binary_search: lambda n: n.bit_length(),
    searching.jump_search: lambda n: 2 * int(n ** 0.5) + 2,
    searching.exponential_search: lambda n: 2 * n.bit_length() + 1,
}


@pytest.mark.parametrize("search", SEARCHES, ids=lambda search: search.__name__)
def test_matches_list_index(search):
    rng = random.Random(3)
    for _ in range(300):
        # Duplicates are allowed: every search reports the first index
        data = [rng.randint(-20, 20) for _ in range(rng.randint(0, 20))]
        if rng.random() < 0.3:
            data = [rng.choice([-2.5, 0.5, 1.25, 3.0, 7.75]) for _ in data]
        for target in set(data) | {100, -100, 0.75}:
            expected = data.index(target) if target in data else -1
            trace = []
            assert search(data, target, trace) == expected
            probes = searching.positions(trace)
            assert all(0 <= position < len(data) for position in probes)
            if search in PROBE_LIMITS:
                assert len(probes) <= PROBE_LIMITS[search](len(data))


@pytest.mark.parametrize("search", [s for s in SEARCHES if s is not searching.interpolation_search],
                         ids=lambda search: search.__name__)
def test_strings(search):
    words = ["pear", "apple", "fig", "banana", "apple"]
    for word in words:
        assert search(words, word) == words.index(word)
    assert search(words, "kiwi") == -1


def test_interpolation_search_needs_numbers():
    assert not searching.accepts(searching.interpolation_search, ["pear", "fig"])
    assert searching.accepts(searching.binary_search, ["pear", "fig"])
    with pytest.raises(InvalidTypeError):
        searching.interpolation_search(["pear", "fig"], "fig")
    with pytest.raises(InvalidTypeError):
        searching.interpolation_search([1, 2], "2")


def test_probes_show_the_path_through_the_sorted_copy():
    data = [10, 1987, 672, 8, 2004, 42, 7, 300]  # Sorted: [7, 8, 10, 42, 300, 672, 1987, 2004]
    trace = []
    assert searching.jump_search(data, 300, trace) == 7
    assert searching.positions(trace) == [1, 3, 5, 4]
    assert [event.kind for event in trace] == ["too_small", "too_small", "block", "match"]
    trace = []
    assert searching.exponential_search(data, 5, trace) == -1
    assert searching.positions(trace) == [0, 1]
    assert [event.kind for event in trace] == ["passed", "bound"]


def test_binary_search_keeps_the_original_order():
    data = [10, 1987, 672, 8, 2004]
    assert searching.binary_search(data, 8) == 3
    assert data == [10, 1987, 672, 8, 2004]
