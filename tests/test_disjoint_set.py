"""Disjoint set (Union-Find), checked against naive grouping."""

import math
import random

import pytest

from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.errors import OutOfBoundsError


def naive_groups(size, unions):
    """Merge plain Python sets for every union and return the groups as sorted lists."""
    groups = [{element} for element in range(size)]
    for a, b in unions:
        group_a = next(group for group in groups if a in group)
        group_b = next(group for group in groups if b in group)
        if group_a is not group_b:
            group_a |= group_b
            groups.remove(group_b)
    return sorted(sorted(group) for group in groups)


def test_random_unions_match_naive_grouping():
    rng = random.Random(15)
    for _ in range(300):
        size = rng.randint(1, 12)
        union_find, unions = DisjointSet(size), []
        for _ in range(rng.randint(0, 20)):
            a, b = rng.randrange(size), rng.randrange(size)
            already_together = any(a in group and b in group for group in naive_groups(size, unions))
            assert union_find.union(a, b) == (not already_together)
            unions.append((a, b))
            if rng.random() < 0.3:
                element = rng.randrange(size)
                root = union_find.find(element)
                assert union_find.parent[element] == root  # Path compression links it straight to the root

        expected = naive_groups(size, unions)
        assert sorted(union_find.groups().values()) == expected
        for a in range(size):
            for b in range(size):
                assert union_find.connected(a, b) == any(a in group and b in group for group in expected)
        assert all(union_find.parent[root] == root for root in union_find.groups())
        # Union by rank keeps every tree, and so every rank, at most log2(size) tall
        assert max(union_find.rank) <= math.log2(size)


def test_find_compresses_the_path():
    union_find = DisjointSet(4)
    union_find.parent = [0, 0, 1, 2]  # A chain: 3 → 2 → 1 → 0
    assert union_find.root_of(3) == 0
    assert union_find.parent == [0, 0, 1, 2]  # root_of doesn't change anything
    assert union_find.find(3) == 0
    assert union_find.parent == [0, 0, 0, 0]


def test_union_by_rank_attaches_the_shorter_tree():
    union_find = DisjointSet(3)
    union_find.union(0, 1)  # Equal ranks: 1 goes under 0, whose rank grows to 1
    assert union_find.parent == [0, 0, 2] and union_find.rank == [1, 0, 0]
    union_find.union(2, 0)  # 2's tree is shorter, so it goes under 0 even though 2 came first
    assert union_find.parent == [0, 0, 0] and union_find.rank == [1, 0, 0]


def test_elements_out_of_bounds():
    union_find = DisjointSet(3)
    with pytest.raises(OutOfBoundsError):
        union_find.find(3)
    with pytest.raises(OutOfBoundsError):
        union_find.union(0, -1)
    with pytest.raises(OutOfBoundsError):
        union_find.connected(5, 0)
    assert union_find.parent == [0, 1, 2]
