"""Independent cache, sorted-list and membership models, plus seeded level probabilities."""

import math
import os
import random
import subprocess
import sys
from collections import Counter, OrderedDict

import pytest

from pydsa.core.bloom_filter import BloomFilter
from pydsa.core.errors import InvalidTypeError, NotFoundError
from pydsa.core.hash_table import ChainingHashTable
from pydsa.core.linked_list import DoublyLinkedList
from pydsa.core.lru_cache import LRUCache
from pydsa.core.skip_list import SkipList


def cache_invariants(cache, model):
    assert isinstance(cache.table, ChainingHashTable) and isinstance(cache.order, DoublyLinkedList)
    assert cache.items() == list(reversed(model.items()))
    assert len(cache) == len(model) <= cache.capacity
    nodes, node, previous = [], cache.order.head, None
    while node is not None:
        assert node.prev is previous
        assert cache.table.lookup(node.data[0])[1] is node
        nodes.append(node)
        previous, node = node, node.next
    assert previous is cache.tail
    assert sum(len(bucket) for bucket in cache.table.table) == len(nodes)
    backwards, node = [], cache.tail
    while node is not None:
        backwards.append(node.data)
        node = node.prev
    assert backwards == list(model.items())


@pytest.mark.parametrize("capacity", [1, 2, 3, 12])
@pytest.mark.parametrize("seed", range(8))
def test_cache_against_ordered_dict(capacity, seed):
    rng, cache, model = random.Random(seed), LRUCache(capacity), OrderedDict()
    # Small ints and colliding keys exercise bucket chains, hits, misses and replacements.
    keys = [i * cache.table.size for i in range(16)]
    for _ in range(240):
        key, value = rng.choice(keys), rng.randrange(-20, 21)
        if rng.random() < 0.65:
            evicted = None
            if key in model:
                del model[key]
            elif len(model) == capacity:
                evicted = model.popitem(last=False)
            model[key] = value
            assert cache.put(key, value) == evicted
        elif key in model:
            assert cache.get(key) == model[key]
            model.move_to_end(key)
        else:
            with pytest.raises(NotFoundError):
                cache.get(key)
        cache_invariants(cache, model)


def test_cache_invalid_keys_do_not_evict_and_values_can_be_none():
    cache = LRUCache(1)
    cache.put("key", None)
    assert cache.get("key") is None
    for bad in ([], {}, set()):
        with pytest.raises(TypeError):
            cache.put(bad, 4)
        assert cache.items() == [("key", None)]
    for bad in (float("nan"), float("inf"), -float("inf")):
        with pytest.raises(InvalidTypeError):
            cache.put(bad, 4)
        with pytest.raises(InvalidTypeError):
            cache.get(bad)
        assert cache.items() == [("key", None)]
    assert cache.put("new", 0) == ("key", None)
    assert cache.put("new", False) is None and cache.get("new") is False


def skip_invariants(linked, model):
    assert list(linked) == sorted(model) and len(linked) == len(model)
    rows, lanes = linked.snapshot()
    nodes, node = [], linked.head.forward[0]
    while node is not None:
        nodes.append(node)
        node = node.forward[0]
    assert len({node.identity for node in nodes}) == len(nodes)
    assert linked.level == max((len(node.forward) for node in nodes), default=1)
    assert len(lanes) == linked.level
    for level in range(linked.max_level):
        expected = [node for node in nodes if len(node.forward) > level]
        actual, node = [], linked.head.forward[level]
        while node is not None:
            assert len(node.forward) > level
            actual.append(node)
            node = node.forward[level]
        assert actual == expected
    assert [key for _, key, _ in rows] == sorted(model)


@pytest.mark.parametrize("cap", [1, 2, 8, 32])
@pytest.mark.parametrize("seed", range(8))
def test_skip_list_random_multiset_model(cap, seed):
    rng, linked, model = random.Random(seed), SkipList(seed=seed, max_level=cap), []
    for _ in range(140):
        key = rng.randrange(-15, 16)
        if rng.random() < 0.65:
            linked.insert(key)
            model.append(key)
        elif key in model:
            assert linked.delete(key) == key
            model.remove(key)
        else:
            with pytest.raises(NotFoundError):
                linked.delete(key)
        assert (linked.search(key) is not None) == (key in model)
        skip_invariants(linked, model)
    rng.shuffle(model)
    for key in list(model):
        linked.delete(key)
        model.remove(key)
    skip_invariants(linked, [])


def test_skip_strings_duplicates_numeric_validation_and_seed_replay():
    a, b = SkipList("str", seed=5), SkipList("str", seed=5)
    for key in ("pear", "apple", "pear", "", "[word]", "é"):
        ta, tb = [], []
        a.insert(key, ta)
        b.insert(key, tb)
        assert ta == tb and a.snapshot() == b.snapshot()
    assert list(a) == sorted(("pear", "apple", "pear", "", "[word]", "é"))
    a.delete("pear")
    assert list(a).count("pear") == 1
    for linked, invalid in ((a, [1, None, True]), (SkipList(), ["2", True, float("inf"), float("nan")])):
        before, rng_state = linked.snapshot(), linked.rng.getstate()
        for key in invalid:
            for method in (linked.insert, linked.delete, linked.search):
                with pytest.raises(InvalidTypeError):
                    method(key)
            assert linked.snapshot() == before and linked.rng.getstate() == rng_state


def test_skip_level_distribution_over_many_nodes():
    linked = SkipList(seed=721, max_level=16)
    for key in range(16000):
        linked.insert(key)
    heights = Counter(height for _, _, height in linked.snapshot()[0])
    # Geometric heights: P(height == h) = 2^-h below the cap.
    for height in range(1, 8):
        expected = len(linked) / 2**height
        assert abs(heights[height] - expected) < 5 * math.sqrt(expected)
    pointer_count = sum(height * count for height, count in heights.items())
    assert 1.9 * len(linked) < pointer_count < 2.1 * len(linked)


@pytest.mark.parametrize("m,k", [(1, 1), (1, 7), (17, 3), (128, 5), (2048, 3)])
@pytest.mark.parametrize("seed", range(6))
def test_bloom_never_loses_added_items(m, k, seed):
    rng, bloom, model = random.Random(seed), BloomFilter(m, k), set()
    previous_bits = bloom.bits
    for _ in range(70):
        item = f"word:{rng.randrange(100)}"
        bloom.add(item)
        model.add(item)
        assert all(bloom.might_contain(added) for added in model)
        assert all(not before or after for before, after in zip(previous_bits, bloom.bits))
        previous_bits = bloom.bits
    # Positive answers are deliberately not treated as exact membership.
    assert bloom.additions == 70
    assert len(bloom.bits) == m and set(bloom.bits) <= {0, 1}


def test_bloom_empty_unicode_repeats_and_certain_false_positive():
    bloom = BloomFilter(64, 3)
    assert not bloom.might_contain("")
    for item in ("", "é", "你好", "[word]", "a:b", "a\x00b"):
        positions = bloom.add(item)
        assert positions == bloom.positions(item) and bloom.might_contain(item)
    before = bloom.bits
    bloom.add("")
    assert bloom.bits == before
    tiny = BloomFilter(1, 3)
    tiny.add("stored")
    assert tiny.might_contain("never added")
    for bad in (1, True, None, b"word", []):
        before, count = bloom.bits, bloom.additions
        with pytest.raises(InvalidTypeError):
            bloom.add(bad)
        with pytest.raises(InvalidTypeError):
            bloom.might_contain(bad)
        assert (bloom.bits, bloom.additions) == (before, count)


def test_bloom_salted_positions_stay_stable_in_other_processes():
    script = "from pydsa.core.bloom_filter import BloomFilter; print(BloomFilter(101, 5).positions('é:hello'))"
    outputs = []
    for seed in ("1", "98451"):
        env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONIOENCODING="utf-8")
        outputs.append(subprocess.check_output([sys.executable, "-c", script], env=env, text=True).strip())
    assert outputs[0] == outputs[1] == repr(BloomFilter(101, 5).positions("é:hello"))
    assert len(set(BloomFilter(101, 5).positions("é:hello"))) > 1


def test_false_positive_formula_is_a_bounded_approximation():
    bloom = BloomFilter(2048, 3)
    assert bloom.estimated_false_positive_rate(0) == 0
    expected = (1 - math.exp(-3 * 512 / 2048))**3
    assert bloom.estimated_false_positive_rate(512) == pytest.approx(expected)
    assert 0 < bloom.estimated_false_positive_rate(32) < bloom.estimated_false_positive_rate(512) < 1
    for bad in (-1, True, "4", 1.5):
        with pytest.raises(ValueError):
            bloom.estimated_false_positive_rate(bad)


@pytest.mark.parametrize("constructor,args", [(LRUCache, (0,)), (LRUCache, (True,)), (LRUCache, (1.5,)),
    (SkipList, ("words",)), (SkipList, ("num", True)), (SkipList, ("num", 0, 0)),
    (SkipList, ("num", 0, 65)), (BloomFilter, (0, 3)), (BloomFilter, (8, 0)), (BloomFilter, (True, 3))])
def test_constructor_validation(constructor, args):
    with pytest.raises(ValueError):
        constructor(*args)


@pytest.mark.parametrize("kind", ["cache", "skip", "bloom"])
def test_trace_snapshots_stay_independent_and_are_skipped_when_off(kind, monkeypatch):
    if kind == "cache":
        structure = LRUCache(2)
        operation, arguments = structure.put, ("A", 1)
        mutate = lambda: structure.put("B", 2)
    elif kind == "skip":
        structure = SkipList(seed=4)
        operation, arguments = structure.insert, (5,)
        mutate = lambda: structure.insert(9)
    else:
        structure = BloomFilter(32, 3)
        operation, arguments = structure.add, ("apple",)
        mutate = lambda: structure.add("pear")
    trace = []
    operation(*arguments, trace=trace)
    before = repr(trace)
    mutate()
    assert repr(trace) == before
    def unexpected():
        raise AssertionError("Untraced operation copied its snapshot")
    monkeypatch.setattr(structure, "snapshot", unexpected)
    mutate()
    if kind == "cache":
        structure.get("B")
    elif kind == "skip":
        structure.search(9)
        structure.delete(9)
    else:
        structure.might_contain("pear")
