"""Hash set, checked against Python's built-in set."""

import random

import pytest

from pydsa.core.errors import NotFoundError
from pydsa.core.hash_set import HashSet

WORDS = ["Messi", "Apple", "UFO", "kiwi", "fig"]


def random_item(rng):
    return rng.choice([rng.randint(0, 15), rng.choice(WORDS), rng.choice([1.5, 2.0])])


def test_random_operations_match_a_set():
    rng = random.Random(13)
    for _ in range(300):
        hash_set, model = HashSet(rng.randint(1, 7)), set()
        for _ in range(50):
            op = rng.choice(["add", "add", "remove", "contains"])
            item = random_item(rng)
            if op == "add":
                assert hash_set.add(item) == (item not in model)
                model.add(item)
            elif op == "remove":
                if item in model:
                    hash_set.remove(item)
                    model.discard(item)
                else:
                    with pytest.raises(NotFoundError):
                        hash_set.remove(item)
            else:
                assert (item in hash_set) == (item in model)
            assert set(hash_set) == model
            assert len(hash_set) == len(model)


def test_set_operations_match_python_sets():
    rng = random.Random(14)
    for _ in range(300):
        a_items = [random_item(rng) for _ in range(rng.randint(0, 10))]
        b_items = [random_item(rng) for _ in range(rng.randint(0, 10))]
        a, b = HashSet(rng.randint(1, 7), a_items), HashSet(rng.randint(1, 7), b_items)
        model_a, model_b = set(a_items), set(b_items)
        assert set(a.union(b)) == model_a | model_b
        assert set(a.intersection(b)) == model_a & model_b
        assert set(a.difference(b)) == model_a - model_b
        assert a.is_subset(b) == (model_a <= model_b)
        assert a.is_superset(b) == (model_a >= model_b)


def test_items_are_the_keys_of_a_chaining_hash_table():
    hash_set = HashSet(3, [1, 4, 1])
    assert hash_set.table.table[1] == [[1, None], [4, None]]
    assert len(hash_set) == 2
    assert hash_set.union(HashSet(5)).size == 3
