"""Bounded experiments that count actual operations; timings are secondary to work counts."""

import math
import random
from dataclasses import dataclass
from time import perf_counter
from typing import Callable

from pydsa.algorithms import graph_algorithms, grid_search, searching, sorting, string_search
from pydsa.core.graph import ListGraph
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.b_tree import BTree
from pydsa.core.hash_table import LinearProbingHashTable
from pydsa.core.heap import MinHeap
from pydsa.core.red_black_tree import RedBlackTree
from pydsa.core.segment_tree import SegmentTree
from pydsa.core.fenwick_tree import FenwickTree
from pydsa.core.skip_list import SkipList
from pydsa.core.bloom_filter import BloomFilter
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
    kind: str = "work"


@dataclass(frozen=True)
class Measurement:
    n: int
    work: int
    ratio: float
    milliseconds: float


@dataclass(frozen=True)
class RateMeasurement(Measurement):
    trials: int
    measured: float
    expected: float

    @property
    def false_positives(self):
        return self.work


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


def _skip_input(n, mode, rng):
    linked = SkipList(seed=rng.randrange(2**32))
    for value in ordered_input(n, mode, rng):
        linked.insert(value)
    return linked


def _skip_search(linked):
    trace = []
    linked.search(len(linked), trace)
    return sum(event.kind in ("sk_right", "sk_down") for event in trace)


BLOOM_BITS, BLOOM_HASHES, BLOOM_TRIALS = 2048, 3, 2000


def _bloom_input(n, mode, rng):
    bloom = BloomFilter(BLOOM_BITS, BLOOM_HASHES)
    for value in ordered_input(n, mode, rng):
        bloom.add(f"added:{value}")
    queries = tuple(f"absent:{i}:{rng.getrandbits(64)}" for i in range(BLOOM_TRIALS))
    return bloom, queries


def _bloom_rate(data):
    bloom, queries = data
    return sum(bloom.might_contain(item) for item in queries)


def _graph_input(n, mode, rng):
    ordered_input(n, mode, rng)
    graph = ListGraph()
    # Reverse adapter order makes each Bellman-Ford pass advance one edge.
    for vertex in reversed(range(n)):
        graph.add_vertex(vertex)
    for vertex in range(n - 1):
        graph.add_edge(vertex, vertex + 1, 1)
    return graph


def _bellman_work(graph):
    trace = []
    graph_algorithms.bellman_ford(graph, 0, trace)
    return sum(event.data["checks"] for event in trace)


def _floyd_work(graph):
    trace = []
    graph_algorithms.floyd_warshall(graph, trace)
    return sum(event.data["checks"] for event in trace)


def _grid_input(n, mode, rng):
    ordered_input(n, mode, rng)
    return grid_search.Grid(n, n)


def _string_input(n, mode, rng):
    ordered_input(n, mode, rng)  # Validate the mode; all modes keep this repeated-prefix workload.
    return "a" * n, "a" * (max(2, n // 4) - 1) + "b"


def _string_work(algorithm):
    def run(data):
        stats = string_search.SearchStats()
        algorithm(*data, stats=stats)
        if algorithm is string_search.rabin_karp:
            return stats.total + stats.hash_characters + stats.windows
        return stats.total
    return run


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
    Experiment("skip-search", "skip-list", "Skip-list search: missing key", LOG, LARGE,
               _skip_input, _skip_search, "log2(n)",
               "Work counts right moves and level drops when searching just beyond the largest key. "
               "Seeded fair coins choose levels; layouts vary with seeds and insertion order. "
               "Input construction is excluded; trace snapshots affect elapsed time."),
    Experiment("bloom-false-positives", "bloom-filter", "Bloom filter: measured false positive rate",
               lambda n: BLOOM_TRIALS * BloomFilter(BLOOM_BITS, BLOOM_HASHES).estimated_false_positive_rate(n),
               LARGE, _bloom_input, _bloom_rate, "false positive rate",
               "Fixed m = 2048 bits and k = 3 hashes. Each row adds n distinct strings and checks "
               "2000 distinct strings known to be absent. Insertion order does not change the bits; "
               "construction is excluded. Formula values are approximate, so measured rates need not match exactly.",
               kind="bloom-rate"),
    Experiment("bellman-passes", "bellman-ford", "Bellman-Ford: reverse-ordered chain", lambda n: n * n,
               (4, 8, 16, 32, 64), _graph_input, _bellman_work, "n²",
               "n vertices and n - 1 edges are scanned in reverse vertex order, requiring n - 1 passes. "
               "Work counts relaxation edge checks, excluding the final cycle check and setup. Trace snapshots affect timing. "
               "Input-order choices keep this deliberately difficult graph order fixed."),
    Experiment("floyd-pairs", "floyd-warshall", "Floyd-Warshall: every pair for each intermediate", lambda n: n ** 3,
               (4, 8, 16, 32), _graph_input, _floyd_work, "n³",
               "n vertices. Work counts every candidate pair checked in each of n passes, even if a route is unreachable. "
               "Graph construction is excluded; matrix snapshots affect timing. Input-order choices keep the same chain."),
    *(Experiment(f"grid-{topic_id}", "a-star", f"Open square grid: {name}", expected, (4, 8, 16, 32),
                 _grid_input, lambda board, heuristic=heuristic: len(grid_search.a_star(
                     board, (0, 0), (board.rows - 1, board.columns - 1), heuristic=heuristic).expanded), growth,
                 "n is side length, so there are n² cells. Start and goal are opposite corners with no walls. "
                 "Work counts expanded cells including the goal; heap operations and construction are excluded. "
                 "Compare Manhattan A* with a zero heuristic on this same grid; walls can change the benefit.")
      for topic_id, name, heuristic, expected, growth in (
          ("a-star", "A*", grid_search.manhattan, lambda n: n, "n"),
          ("dijkstra", "Dijkstra", None, lambda n: n * n, "n²"))),
    *(Experiment(f"{topic}-work", topic, f"{name}: repeated prefix, missing match", expected,
                 (32, 64, 128, 256), _string_input, _string_work(algorithm), growth,
                 "n is text length; the pattern length is about n / 4. Text is all a and pattern ends in b. "
                 "Input-order choices keep the same workload; construction is excluded. " +
                 ("Work counts character comparisons, including KMP preprocessing." if topic != "rabin-karp" else
                  "Work counts characters read for hashing, window hash checks and verification comparisons. "
                  "Modulus 101 rejects these windows; collisions on other inputs can erase the benefit."))
      for topic, name, algorithm, expected, growth in (
          ("naive-string-search", "Naive search", string_search.naive_search, lambda n: n * n, "n²"),
          ("kmp", "KMP", string_search.kmp_search, lambda n: n, "n"),
          ("rabin-karp", "Rabin-Karp", string_search.rabin_karp, lambda n: n, "n"))),
)


def for_topic(topic):
    families = {
        "array": {"sorting", "searching"}, "sorting": {"sorting"}, "searching": {"searching"},
        "tree": {"bst", "avl-tree"}, "min-heap": {"heap"}, "max-heap": {"heap"},
        "priority-queue": {"heap"}, "hash-table": {"linear-probing-hash-table"},
        "graph-algorithms": {"bellman-ford", "floyd-warshall", "a-star"},
        "string-algorithms": {"naive-string-search", "kmp", "rabin-karp"},
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
        expected = experiment.expected(n)
        if experiment.kind == "bloom-rate":
            results.append(RateMeasurement(n, work, work / expected, elapsed, BLOOM_TRIALS,
                                           work / BLOOM_TRIALS, expected / BLOOM_TRIALS))
        else:
            results.append(Measurement(n, work, work / expected, elapsed))
    return results
