"""Random data generators: every one returns the shape its create flow expects."""

import random
from collections import deque

import pytest

from pydsa.ui import random_data


def test_values_match_the_kind():
    rng = random.Random(1)
    assert all(isinstance(value, int) and 1 <= value <= 99 for value in random_data.values("int", 30, rng))
    assert all(isinstance(value, int) for value in random_data.values("num", 30, rng))
    assert all(value in random_data.WORDS for value in random_data.values("str", 30, rng))
    mixed = random_data.values("any", 200, rng)
    assert {type(value) for value in mixed} == {int, str}


def test_words_stay_different_while_possible():
    rng = random.Random(2)
    assert len(set(random_data.words(len(random_data.WORDS), rng))) == len(random_data.WORDS)
    assert len(random_data.words(40, rng)) == 40
    assert len(set(random_data.trie_words(10, rng))) == 10


@pytest.mark.parametrize("arrangement", random_data.ARRANGEMENTS)
def test_number_lists(arrangement):
    rng = random.Random(3)
    for count in (1, 2, 9, random_data.MAX_ITEMS):
        numbers = random_data.number_list(count, arrangement, rng)
        assert len(numbers) == count and all(isinstance(number, int) for number in numbers)
        if arrangement == "sorted":
            assert numbers == sorted(numbers)
        elif arrangement == "reversed":
            assert numbers == sorted(numbers, reverse=True)
        elif arrangement == "duplicates" and count >= 9:
            assert len(set(numbers)) < count


def test_pairs_and_unions():
    rng = random.Random(4)
    pairs = random_data.key_value_pairs(random_data.MAX_ITEMS, rng)
    assert len({key for key, _ in pairs}) == random_data.MAX_ITEMS
    assert all(1 <= priority <= 5 for _, priority in random_data.priority_items(20, rng))
    unions = random_data.unions(6, 30, rng)
    assert len(unions) == 30 and all(0 <= a < 6 and 0 <= b < 6 for a, b in unions)


def reachable(start, edges, directed):
    neighbors = {}
    for u, v, _ in edges:
        neighbors.setdefault(u, []).append(v)
        if not directed:
            neighbors.setdefault(v, []).append(u)
    seen, queue = {start}, deque([start])
    while queue:
        for v in neighbors.get(queue.popleft(), []):
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen


@pytest.mark.parametrize("directed", [True, False], ids=["directed", "undirected"])
@pytest.mark.parametrize("connected", [True, False], ids=["connected", "anywhere"])
def test_edges(directed, connected):
    rng = random.Random(5)
    for vertex_count in range(1, 8):
        vertices = rng.sample(range(20), vertex_count)
        fewest, most = random_data.edge_limits(vertex_count, directed, connected)
        for count in range(fewest, most + 1):
            edges = random_data.edges(vertices, count, directed, connected, rng)
            pairs = [(u, v) if directed else frozenset((u, v)) for u, v, _ in edges]
            assert len(edges) == count
            assert len(set(pairs)) == count  # No pair repeats
            assert all(u != v and u in vertices and v in vertices for u, v, _ in edges)
            assert all(1 <= weight <= random_data.MAX_WEIGHT for _, _, weight in edges)
            if connected:
                assert reachable(vertices[0], edges, directed) == set(vertices)
