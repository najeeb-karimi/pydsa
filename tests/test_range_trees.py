"""Range trees checked against direct array aggregates, including updates and rebuilds."""

import random

import pytest

from pydsa.core import segment_tree
from pydsa.core.errors import InvalidTypeError, OutOfBoundsError
from pydsa.core.fenwick_tree import FenwickTree
from pydsa.core.segment_tree import SegmentTree


FACTORIES = [lambda values: SegmentTree(values, "sum"), lambda values: SegmentTree(values, "min"),
             lambda values: SegmentTree(values, "max"), FenwickTree]


def check_structure(tree, values):
    assert tree.items == values and len(tree) == len(values)
    if isinstance(tree, FenwickTree):
        assert tree.blocks[0] == 0
        for i, value in enumerate(tree.blocks[1:], 1):
            assert value == pytest.approx(sum(values[i - (i & -i):i]))
    else:
        aggregate = {"sum": sum, "min": min, "max": max}[tree.operation]

        def check(node, low, high):
            assert (node.low, node.high) == (low, high)
            assert node.value == pytest.approx(aggregate(values[low:high + 1]))
            if low == high:
                assert node.left is None and node.right is None
            else:
                assert node.left.low == low and node.right.high == high
                assert node.left.high + 1 == node.right.low
                check(node.left, low, node.left.high)
                check(node.right, node.right.low, high)
        if values:
            check(tree.root, 0, len(values) - 1)
        else:
            assert tree.root is None


@pytest.mark.parametrize("factory", FACTORIES, ids=["sum", "min", "max", "fenwick"])
@pytest.mark.parametrize("seed", range(12))
def test_random_queries_updates_and_rebuilds(factory, seed):
    rng = random.Random(seed)
    values = [rng.randrange(-100, 101) for _ in range(rng.randrange(1, 65))]
    tree = factory(iter(values))
    for _ in range(160):
        if rng.random() < 0.08:
            values = [rng.randrange(-100, 101) for _ in range(rng.randrange(1, 65))]
            tree.build(iter(values))
        elif rng.random() < 0.5:
            position, value = rng.randrange(len(values)), rng.randrange(-100, 101)
            tree.update(position, value)
            values[position] = value
        left = rng.randrange(len(values))
        right = rng.randrange(left, len(values))
        if isinstance(tree, FenwickTree):
            assert tree.range_sum(left, right) == sum(values[left:right + 1])
            assert tree.prefix_sum(right) == sum(values[:right + 1])
        else:
            reference = {"sum": sum, "min": min, "max": max}[tree.operation]
            assert tree.query(left, right) == reference(values[left:right + 1])
        check_structure(tree, values)


@pytest.mark.parametrize("factory", FACTORIES)
@pytest.mark.parametrize("values", [[], [0], [-9], [3, 3, 3], [1.25, -2.5, 4.75], [10**100, -10**100, 7]])
def test_boundaries_and_owned_arrays(factory, values):
    source = list(values)
    tree = factory(source)
    source.append(99)
    copy = tree.items
    copy.append(123)
    check_structure(tree, values)
    if isinstance(tree, FenwickTree):
        assert tree.prefix_sum(-1) == 0
        blocks = tree.blocks
        blocks[0] = 999
        assert tree.blocks[0] == 0
    if values:
        for left in range(len(values)):
            for right in range(left, len(values)):
                if isinstance(tree, FenwickTree):
                    assert tree.range_sum(left, right) == pytest.approx(sum(values[left:right + 1]))
                else:
                    reference = {"sum": sum, "min": min, "max": max}[tree.operation]
                    assert tree.query(left, right) == pytest.approx(reference(values[left:right + 1]))
        tree.update(0, -4.5)
        values = [-4.5, *values[1:]]
        check_structure(tree, values)
    else:
        with pytest.raises(OutOfBoundsError):
            tree.update(0, 1)
        with pytest.raises(OutOfBoundsError):
            (tree.query if isinstance(tree, SegmentTree) else tree.range_sum)(0, 0)
    tree.build([])
    check_structure(tree, [])


@pytest.mark.parametrize("factory", FACTORIES)
def test_invalid_values_and_ranges_leave_state_unchanged(factory):
    tree = factory([4, -3, 7])
    query = tree.query if isinstance(tree, SegmentTree) else tree.range_sum
    for bad in (True, "4", None, [], float("nan"), float("inf"), -float("inf")):
        trace = []
        with pytest.raises(InvalidTypeError):
            tree.update(1, bad, trace)
        with pytest.raises(InvalidTypeError):
            tree.build([10, bad], trace)
        assert trace == []
        check_structure(tree, [4, -3, 7])
    for left, right in ((-1, 1), (0, 3), (2, 1), (True, 2), (0, False), (1.0, 2), (0, "2")):
        with pytest.raises(OutOfBoundsError):
            query(left, right)
    for position in (-1, 3, True, 1.5, "1"):
        with pytest.raises(OutOfBoundsError):
            tree.update(position, 9)
    check_structure(tree, [4, -3, 7])
    if isinstance(tree, FenwickTree):
        for end in (-2, 3, True, 1.0, "1"):
            with pytest.raises(OutOfBoundsError):
                tree.prefix_sum(end)


def test_unknown_aggregate_is_rejected():
    for operation in ("average", None, "SUM"):
        with pytest.raises(ValueError):
            SegmentTree([1, 2], operation)


def test_fenwick_replacement_preserves_small_decimal_after_large_value():
    tree = FenwickTree([10**100])
    tree.update(0, 1.25)
    assert tree.prefix_sum(0) == 1.25
    assert tree.range_sum(0, 0) == 1.25


@pytest.mark.parametrize("factory", FACTORIES)
def test_random_decimal_queries_and_replacements(factory):
    rng = random.Random(21)
    values = [rng.uniform(-100, 100) for _ in range(31)]
    tree = factory(values)
    for _ in range(100):
        position, value = rng.randrange(len(values)), rng.uniform(-100, 100)
        tree.update(position, value)
        values[position] = value
        left, right = sorted(rng.sample(range(len(values)), 2))
        if isinstance(tree, FenwickTree):
            assert tree.range_sum(left, right) == pytest.approx(sum(values[left:right + 1]))
        else:
            reference = {"sum": sum, "min": min, "max": max}[tree.operation]
            assert tree.query(left, right) == pytest.approx(reference(values[left:right + 1]))
        check_structure(tree, values)


def test_segment_query_classification_and_pruning():
    tree, trace = SegmentTree([2, 1, 5, 3, 4, 7, 6, 8]), []
    assert tree.query(2, 4, trace) == 12
    classifications = {event.kind for event in trace}
    assert {"sg_inside", "sg_partial", "sg_outside"} <= classifications
    covered = []
    for event in trace:
        low, high = event.data["low"], event.data["high"]
        if event.kind == "sg_inside":
            assert 2 <= low <= high <= 4
            covered.extend(range(low, high + 1))
        if event.kind == "sg_outside":
            assert high < 2 or low > 4
    assert sorted(covered) == [2, 3, 4]
    trace.clear()
    assert tree.query(0, 7, trace) == 36
    assert [event.kind for event in trace] == ["sg_inside", "sg_result"]


def test_fenwick_binary_query_and_update_paths():
    tree, trace = FenwickTree(range(1, 9)), []
    assert tree.prefix_sum(6, trace) == 28
    takes = [event for event in trace if event.kind == "fw_take"]
    assert [event.data["i"] for event in takes] == [7, 6, 4]
    assert [event.data["binary"] for event in takes] == ["0111", "0110", "0100"]
    jumps = [event for event in trace if event.kind == "fw_query_jump"]
    assert [event.data["next"] for event in jumps] == [6, 4, 0]
    trace.clear()
    tree.update(4, -5, trace)
    assert [event.data["i"] for event in trace if event.kind == "fw_add"] == [5, 6, 8]
    assert [event.data["delta"] for event in trace if event.kind == "fw_add"] == [-10] * 3
    for event in trace:
        assert int(event.data["binary"], 2) == event.data["i"]
        assert int(event.data["bit_binary"], 2) == event.data["bit"]
        if "next" in event.data:
            assert int(event.data["next_binary"], 2) == event.data["next"]
    check_structure(tree, [1, 2, 3, 4, -5, 6, 7, 8])


@pytest.mark.parametrize("factory", FACTORIES)
def test_trace_snapshots_are_independent_and_untraced_work_skips_them(factory, monkeypatch):
    tree, trace = factory([]), []
    tree.build([2, 1, 5, 3, 4], trace)
    tree.update(3, -8, trace)
    (tree.query if isinstance(tree, SegmentTree) else tree.range_sum)(1, 4, trace)
    before = repr(trace)
    tree.build([99])
    tree.update(0, 7)
    assert repr(trace) == before
    def unexpected(*args, **kwargs):
        raise AssertionError("An untraced operation copied a snapshot")
    if isinstance(tree, SegmentTree):
        monkeypatch.setattr(segment_tree, "snapshot", unexpected)
    else:
        # Recording would expose a broken guard even if a snapshot was not retained.
        monkeypatch.setattr("pydsa.core.fenwick_tree.record", unexpected)
    tree.build([1, 2, 3])
    tree.update(1, 4)
    assert (tree.query if isinstance(tree, SegmentTree) else tree.range_sum)(0, 2) == (
        {"sum": 8, "min": 1, "max": 4}[tree.operation] if isinstance(tree, SegmentTree) else 8)
