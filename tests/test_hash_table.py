"""Separate chaining and linear probing hash tables, checked against a dict."""

import random

import pytest

from pydsa.core.errors import CapacityError, NotFoundError
from pydsa.core.hash_table import ChainingHashTable, LinearProbingHashTable


def random_key(rng):
    return rng.choice([rng.randint(-20, 40), rng.choice(["Messi", "Apple", "UFO", "kiwi", "fig"]), rng.choice([1.5, -273.15])])


@pytest.mark.parametrize("table_class", [ChainingHashTable, LinearProbingHashTable], ids=lambda cls: cls.__name__)
def test_random_operations_match_a_dict(table_class):
    rng = random.Random(11)
    probing = table_class is LinearProbingHashTable
    for _ in range(300):
        size = rng.randint(1, 7)
        table, model = table_class(size), {}
        for _ in range(50):
            op = rng.choice(["insert", "insert", "delete", "lookup"])
            key, value = random_key(rng), rng.randint(0, 99)
            if op == "insert":
                if probing and key not in model and len(model) == size:
                    with pytest.raises(CapacityError):
                        table.insert(key, value)
                else:
                    index, updated = table.insert(key, value)
                    assert updated == (key in model)
                    model[key] = value
            elif op == "delete":
                if key in model:
                    table.delete(key)
                    del model[key]
                else:
                    with pytest.raises(NotFoundError):
                        table.delete(key)
            elif key in model:
                index, found = table.lookup(key)
                assert found == model[key]
            else:
                with pytest.raises(NotFoundError):
                    table.lookup(key)

            if probing:
                assert {slot[0]: slot[1] for slot in table.table if slot is not None} == model
            else:
                # Every pair sits in the bucket its hash points to
                assert {kv[0]: kv[1] for i, bucket in enumerate(table.table) for kv in bucket if hash(kv[0]) % size == i} == model
                assert sum(len(bucket) for bucket in table.table) == len(model)
            # Every remaining key can still be found, including after cluster rehashing
            assert all(table.lookup(k)[1] == v for k, v in model.items())


def test_chaining_reports_the_bucket():
    table = ChainingHashTable(3)
    assert table.insert(7, "a") == (1, False)
    assert table.insert(10, "b") == (1, False)
    assert table.insert(7, "c") == (1, True)
    assert table.table[1] == [[7, "c"], [10, "b"]]
    assert table.delete(10) == 1


def test_probing_delete_rehashes_the_rest_of_the_cluster():
    table = LinearProbingHashTable(5)
    for key in (1, 6, 11):  # All three start at slot 1
        table.insert(key, str(key))
    assert [slot and slot[0] for slot in table.table] == [None, 1, 6, 11, None]
    assert table.delete(1) == (1, 2)
    assert [slot and slot[0] for slot in table.table] == [None, 6, 11, None, None]
    assert table.lookup(11) == (2, "11")


def test_probing_full_table():
    table = LinearProbingHashTable(2)
    table.insert(0, "a")
    table.insert(1, "b")
    with pytest.raises(CapacityError):
        table.insert(2, "c")
    assert table.insert(1, "B") == (1, True)
