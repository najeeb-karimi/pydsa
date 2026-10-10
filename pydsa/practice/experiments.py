"""Bounded experiments that count actual operations; timings are secondary to work counts."""

import math
import random
from dataclasses import dataclass
from time import perf_counter
from typing import Callable

from pydsa.algorithms import searching, sorting
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.b_tree import BTree
from pydsa.core.hash_table import LinearProbingHashTable
from pydsa.core.heap import MinHeap
from pydsa.core.red_black_tree import RedBlackTree
from pydsa.core.segment_tree import SegmentTree
from pydsa.core.fenwick_tree import FenwickTree
from pydsa.core.tree import AVLTree, BinarySearchTree

MODES = ("random", "sorted", "reversed")


@dataclass(frozen=True)
class Experiment:
    id: str
    topic: str
    name: str
    expected: Callable[[int], float]
    sizes: tuple[int, ...]
    make_input: Callable[[int, str, random.Random], object]
    run: Callable[[object], int]
    growth: str
    note: str


@dataclass(frozen=True)
class Measurement:
    n: int
    work: int
    ratio: float
    milliseconds: float


def ordered_input(n, mode, rng):
    if mode not in MODES:
        raise ValueError(f"Unknown input order: {mode!r}")
    values = list(range(n))
    if mode == "random":
        rng.shuffle(values)
    elif mode == "reversed":
        values.reverse()
    return values


def _sort(algorithm):
    def run(items):
        stats = sorting.SortStats()
        for _ in algorithm(items, stats=stats):
            pass  # Consume events without retaining their snapshots.
        return stats.comparisons + stats.writes
    return run


def _search(algorithm):
    def run(items):
        trace = []
        algorithm(items, len(items), trace)  # Missing target forces a complete unsuccessful search.
        return len(trace)
    return run


def _heap(items):
    heap = MinHeap("num")
    heap.heapify(items[:-1])
    return heap


def _heap_run(heap):
    return sum(event.kind == "sift_up" for event in heap.insert(-1))


def _tree(tree_class):
    def make(n, mode, rng):
        values = ordered_input(n, mode, rng)
        tree = tree_class("num")
        for value in values[:-1]:
            tree.insert(value)
        return tree, values[-1]
    return make


def _tree_run(data):
    tree, key = data
    trace = []
    tree.insert(key, trace)
    return sum(event.kind in ("go_left", "go_right") for event in trace)


def _hash(n, mode, rng):
    ordered_input(n, mode, rng)  # Validate the mode; collisions are controlled independently of order.
    table = LinearProbingHashTable(2 * n + 1)
    for i in range(n - 1):
        table.insert(i * table.size, i)
    return table, (n - 1) * table.size


def _b_tree_run(data):
    tree, key = data
    trace = []
    tree.insert(key, trace)
    return sum(event.kind in ("bt_descend", "bt_insert") for event in trace)


def _hash_run(data):
    table, key = data
    trace = []
    table.insert(key, key, trace)
    return sum(event.kind == "probe" for event in trace)


def _unions(n, mode, rng):
    values = ordered_input(n, mode, rng)
    union_find = DisjointSet(n)
    groups = [[value] for value in values]
    while len(groups) > 1:
        next_groups = []
        for i in range(0, len(groups), 2):
            a = groups[i]
            if i + 1 < len(groups):
                b = groups[i + 1]
                union_find.union(a[0], b[0])
                a += b
            next_groups.append(a)
        groups = next_groups
    deepest = max(values, key=lambda v: _hops(union_find, v))
    return union_find, deepest


def _hops(union_find, element):
    trace = []
    union_find.root_of(element, trace)
    return sum(event.kind == "hop" for event in trace)


def _find_run(data):
    union_find, element = data
    trace = []
    union_find.find(element, trace)
    return sum(event.kind == "hop" for event in trace)


def _compressed_run(data):
    union_find, element = data
    union_find.find(element)
    return _find_run(data)


def _range_input(tree_class=None):
    def make(n, mode, rng):
        values = ordered_input(n, mode, rng)
        # A growing range with an unaligned end avoids the whole-root shortcut.
        return (tree_class(values) if tree_class else values), n // 4, 3 * n // 4 - 2
    return make


def _range_work(data):
    tree, left, right = data
    trace = []
    if isinstance(tree, SegmentTree):
        tree.query(left, right, trace)
        return sum(event.kind in ("sg_inside", "sg_partial", "sg_outside") for event in trace)
    tree.range_sum(left, right, trace)
    return sum(event.kind == "fw_take" for event in trace)


def _direct_sum(data):
    values, left, right = data
    total, work = 0, 0
    for i in range(left, right + 1):
        total += values[i]
        work += 1
    return work


LOG = lambda n: max(math.log2(n), 1)
SMALL = (16, 32, 64, 128, 256)
LARGE = (32, 64, 128, 256, 512)

EXPERIMENTS = (
    *(Experiment(name.replace("_", "-"), name.replace("_", "-"), name.replace("_", " ").title(),
                 (lambda n: n * LOG(n)) if name in ("merge_sort", "heap_sort", "quick_sort") else (lambda n: n * n),
                 SMALL, ordered_input, _sort(getattr(sorting, name)),
                 "n × log2(n)" if name in ("merge_sort", "heap_sort", "quick_sort") else "n²",
                 "Work counts comparisons plus writes. Input order can change the growth; bubble and insertion sorts benefit from sorted data, and this quicksort uses the last value as its pivot.")
      for name in ("bubble_sort", "selection_sort", "insertion_sort", "quick_sort", "heap_sort", "merge_sort")),
    Experiment("linear-search", "linear-search", "Linear search: missing target", lambda n: n, LARGE,
               ordered_input, _search(searching.linear_search), "n",
               "Work counts probes. The missing target makes linear search check every position."),
    Experiment("binary-search", "binary-search", "Binary search: missing target", LOG, LARGE,
               ordered_input, _search(searching.binary_search), "log2(n)",
               "Work counts only probes of the sorted copy. Copying, sorting and mapping original indexes are excluded from this count, but included in elapsed time."),
    Experiment("heap-insert", "heap", "Heap insertion: a new smallest key", LOG, LARGE,
               lambda n, mode, rng: _heap(ordered_input(n, mode, rng)), _heap_run, "log2(n)",
               "Work counts sift-up swaps for one insertion into a heap holding n − 1 keys."),
    Experiment("bst-insert", "bst", "BST insertion path", LOG, SMALL, _tree(BinarySearchTree), _tree_run,
               "log2(n)", "Work counts nodes visited in the final insertion. Ordered input makes the BST a chain, so its ratio against the logarithmic reference grows."),
    Experiment("avl-insert", "avl-tree", "AVL insertion path", LOG, SMALL, _tree(AVLTree), _tree_run,
               "log2(n)", "Work counts nodes visited in the final insertion; rotations keep paths short even for ordered inputs."),
    Experiment("red-black-insert", "red-black-tree", "Red-Black insertion path", LOG, SMALL,
               _tree(RedBlackTree), _tree_run, "log2(n)",
               "Work counts existing nodes compared in the final insertion. Recoloring and rotations are excluded; the color rules keep paths short for ordered inputs too."),
    Experiment("b-tree-insert", "b-tree", "B-tree insertion path (minimum degree 3)", LOG, SMALL,
               _tree(lambda data_type: BTree(3, data_type)), _b_tree_run, "log2(n)",
               "Work counts node visits in the final insertion, including its leaf. Degree stays at 3; comparisons inside nodes and splits are excluded from this count."),
    Experiment("hash-probes", "linear-probing-hash-table", "Hash insertion: colliding integer keys", lambda n: n,
               SMALL, _hash, _hash_run, "n", "All keys share a home slot. Work counts occupied slots probed during the final insertion; this deliberately shows collisions rather than average behavior."),
    Experiment("find-hops", "disjoint-set", "Find before path compression", LOG, LARGE, _unions, _find_run,
               "log2(n)", "Balanced unions create rank trees. Work counts parent hops from a deepest element."),
    Experiment("compressed-find", "disjoint-set", "Find after path compression", lambda n: 1, LARGE,
               _unions, _compressed_run, "1", "One earlier find compresses the path. Work counts the next find's parent hops, not the setup work."),
    *(Experiment(f"{topic}-query", topic, f"{name}: range sum", LOG, LARGE,
                 _range_input(tree_class), _range_work, "log2(n)",
                 "The inclusive range is [n // 4, 3n // 4 - 2], about half the array. Work counts " +
                 ("visited nodes, including outside nodes." if tree_class is SegmentTree else
                  "blocks added in the two prefix queries; subtraction is excluded.") +
                 " Compare with this topic's direct range sum. Construction is excluded; trace snapshots affect elapsed time.")
      for topic, name, tree_class in (("segment-tree", "Segment tree", SegmentTree),
                                     ("fenwick-tree", "Fenwick tree", FenwickTree))),
    *(Experiment(f"{topic}-direct-sum", topic, "Direct range sum: read every value", lambda n: n, LARGE,
                 _range_input(), _direct_sum, "n",
                 "Reads the same inclusive range [n // 4, 3n // 4 - 2] as the tree experiment. "
                 "Work counts array values added, about half of n; input construction is excluded.")
      for topic in ("segment-tree", "fenwick-tree")),
)


def for_topic(topic):
    families = {
        "array": {"sorting", "searching"}, "sorting": {"sorting"}, "searching": {"searching"},
        "tree": {"bst", "avl-tree"}, "min-heap": {"heap"}, "max-heap": {"heap"},
        "priority-queue": {"heap"}, "hash-table": {"linear-probing-hash-table"},
    }
    allowed = {topic, *families.get(topic, ())}
    if "sorting" in allowed:
        allowed.update(experiment.topic for experiment in EXPERIMENTS if experiment.id.endswith("-sort"))
    if "searching" in allowed:
        allowed.update(("linear-search", "binary-search"))
    return tuple(experiment for experiment in EXPERIMENTS if experiment.topic in allowed)


def measure(experiment, mode="random", sizes=None, rng=None):
    """Keep input construction outside the timed operation and enforce the experiment's size cap."""
    if mode not in MODES:
        raise ValueError(f"Unknown input order: {mode!r}")
    sizes = experiment.sizes if sizes is None else tuple(sizes)
    if any(type(n) is not int or n < 2 or n > max(experiment.sizes) for n in sizes):
        raise ValueError("Experiment sizes must be between 2 and the experiment's maximum.")
    rng = rng or random.Random()
    results = []
    for n in sizes:
        data = experiment.make_input(n, mode, rng)
        start = perf_counter()
        work = experiment.run(data)
        elapsed = (perf_counter() - start) * 1000
        results.append(Measurement(n, work, work / experiment.expected(n), elapsed))
    return results
