"""Min and max heaps, checked against heapq."""

import heapq
import random

import pytest

from pydsa.core.errors import EmptyError, InvalidTypeError
from pydsa.core.heap import MaxHeap, MinHeap


def holds_heap_property(heap):
    """No child may belong above its parent."""
    items = heap.items
    return all(not heap._above(items[child], items[(child - 1) // 2]) for child in range(1, len(items)))


def check_steps(steps, final):
    """Every step after the first swaps exactly the two keys it marks, and the last step is the final heap."""
    for previous, step in zip(steps, steps[1:]):
        was, went = step.moved
        expected = list(previous.items)
        expected[was], expected[went] = expected[went], expected[was]
        assert step.items == expected
    assert steps[-1].items == final


@pytest.mark.parametrize("heap_class, sign", [(MinHeap, 1), (MaxHeap, -1)], ids=["min", "max"])
def test_random_operations_match_heapq(heap_class, sign):
    rng = random.Random(16)
    for _ in range(300):
        heap, model = heap_class("num"), []  # heapq is a min heap, so a max heap is modeled with negated keys
        for _ in range(40):
            op = rng.choices(["insert", "extract", "peek", "heapify"], weights=[5, 3, 1, 1])[0]
            if op == "insert":
                key = rng.randint(-20, 20)
                steps = heap.insert(key)
                heapq.heappush(model, sign * key)
                assert steps[0].moved == (len(heap) - 1,)
                check_steps(steps, heap.items)
            elif op == "extract":
                if model:
                    key, steps = heap.extract()
                    assert key == sign * heapq.heappop(model)
                    if steps:
                        check_steps(steps, heap.items)
                else:
                    with pytest.raises(EmptyError):
                        heap.extract()
            elif op == "peek":
                if model:
                    assert heap.peek() == sign * model[0]
                else:
                    with pytest.raises(EmptyError):
                        heap.peek()
            else:
                keys = [rng.randint(-20, 20) for _ in range(rng.randint(0, 15))]
                steps = heap.heapify(keys)
                model = [sign * key for key in keys]
                heapq.heapify(model)
                assert steps[0].items == keys
                check_steps(steps, heap.items)
                assert len(steps) - 1 <= 2 * len(keys)  # Heapify needs only O(n) swaps

            assert holds_heap_property(heap)
            assert sorted(heap.items) == sorted(sign * key for key in model)
            assert len(heap) == len(model)


def depth(index):
    """Count the parent hops from index up to the root."""
    hops = 0
    while index:
        index = (index - 1) // 2
        hops += 1
    return hops


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap], ids=["min", "max"])
def test_tree_metrics_match_brute_force(heap_class):
    rng = random.Random(17)
    for size in range(40):
        keys = [rng.randint(0, 99) for _ in range(size)]
        heap = heap_class("num")
        heap.heapify(keys)
        assert heap.height() == max((depth(index) + 1 for index in range(size)), default=0)
        assert heap.leaf_count() == sum(1 for index in range(size) if 2 * index + 1 >= size)
        assert heap.level_order() == heap.items
        if keys:
            assert heap.min() == min(keys) and heap.max() == max(keys)
        else:
            with pytest.raises(EmptyError):
                heap.min()
            with pytest.raises(EmptyError):
                heap.max()


def test_update_sifts_up_or_down():
    heap = MinHeap("num")
    heap.heapify([10, 20, 30, 40, 50])
    steps = heap.update(4, 5)  # 5 climbs past 20 and 10
    assert [step.moved for step in steps] == [(4,), (4, 1), (1, 0)]
    assert heap.items[0] == 5 and holds_heap_property(heap)
    heap.update(0, 45)
    assert holds_heap_property(heap)
    assert sorted(heap.items) == [10, 20, 30, 40, 45]


def test_insert_and_extract_steps():
    heap = MinHeap("num")
    heap.heapify([10, 20, 30])
    steps = heap.insert(5)
    assert [step.items for step in steps] == [[10, 20, 30, 5], [10, 5, 30, 20], [5, 10, 30, 20]]
    key, steps = heap.extract()
    assert key == 5
    assert steps[0] == ([20, 10, 30], (0,))
    assert heap.items == [10, 20, 30]
    single = MaxHeap("num")
    single.insert(1)
    assert single.extract() == (1, []) and single.is_empty()


def test_keys_must_match_the_data_type():
    with pytest.raises(InvalidTypeError):
        MinHeap("num").insert("5")
    heap = MaxHeap("str")
    heap.heapify(["pear", "apple", "fig"])
    with pytest.raises(InvalidTypeError):
        heap.heapify(["kiwi", 1])
    assert heap.peek() == "pear" and len(heap) == 3  # The rejected list didn't replace the keys
    with pytest.raises(ValueError):
        MinHeap("list")
