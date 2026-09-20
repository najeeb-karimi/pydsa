"""Step events: the exact steps small runs take, and a caption for every one of them."""

import pytest

from pydsa.algorithms import graph_algorithms, searching, sorting
from pydsa.content import narration
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.graph import ListGraph
from pydsa.core.hash_table import ChainingHashTable, LinearProbingHashTable
from pydsa.core.heap import MinHeap
from pydsa.core.tree import AVLTree, BinarySearchTree
from pydsa.core.trie import Trie


def kinds(events):
    """Return the kind of every event, which is what the steps of a run come down to."""
    return [event.kind for event in events]


def traced(operation, *arguments, **keywords):
    """Run an operation that takes a trace and return the events it recorded."""
    trace = []
    operation(*arguments, trace=trace, **keywords)
    return trace


def example_graph(directed):
    """Return the example graph of the graph screens, which has the vertices 0 to 4."""
    graph = ListGraph(directed)
    for vertex in range(5):
        graph.add_vertex(vertex)
    edges = ([(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)] if directed else
             [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3), (2, 4, 9)])
    for u, v, weight in edges:
        graph.add_edge(u, v, weight)
    return graph


# ---------------------------------------------------------------------------
# Sorting and searching
# ---------------------------------------------------------------------------

def test_bubble_sort_records_every_swap():
    events = list(sorting.bubble_sort([3, 2, 1]))
    assert kinds(events) == ["swap", "swap", "swap"]
    assert [event.snapshot for event in events] == [[2, 3, 1], [2, 1, 3], [1, 2, 3]]
    assert [event.data for event in events] == [{"a": 2, "b": 3}, {"a": 1, "b": 3}, {"a": 1, "b": 2}]
    assert [sorted(event.marks) for event in events] == [[0, 1], [1, 2], [0, 1]]


def test_insertion_sort_tells_a_move_from_a_value_that_stays():
    events = list(sorting.insertion_sort([2, 1, 3]))
    assert kinds(events) == ["insert", "in_place"]
    assert events[0].data == {"value": 1, "index": 0}
    assert events[1].data == {"value": 3, "index": 2}


def test_quick_sort_marks_the_pivot():
    events = list(sorting.quick_sort([3, 1, 4, 2]))
    assert kinds(events) == ["partition", "partition"]
    assert events[0].data == {"pivot": 2, "index": 1, "low": 0, "high": 3}
    assert events[0].marks == {1: "pivot"}


def test_searches_say_why_they_move_on():
    values = [7, 8, 10, 42, 300]
    assert kinds(traced(searching.linear_search, values, 10)) == ["passed", "passed", "match"]
    assert kinds(traced(searching.binary_search, values, 8)) == ["too_large", "too_small", "match"]
    assert kinds(traced(searching.binary_search, values, 300)) == ["too_small", "too_small", "match"]
    assert kinds(traced(searching.jump_search, values, 300))[-2:] == ["block", "match"]
    assert kinds(traced(searching.exponential_search, values, 5)) == ["passed", "bound"]
    events = traced(searching.binary_search, values, 8)
    assert events[0].data == {"index": 2, "value": 10, "target": 8}
    assert events[0].marks == {2: "checked"}


# ---------------------------------------------------------------------------
# Heaps and trees
# ---------------------------------------------------------------------------

def test_heap_insert_and_extract_record_every_sift():
    heap = MinHeap("num")
    heap.heapify([10, 20, 30])
    assert kinds(heap.insert(5)) == ["add_leaf", "sift_up", "sift_up"]
    assert kinds(heap.extract()[1]) == ["move_last", "sift_down"]


def test_bst_insert_records_the_path():
    tree = BinarySearchTree("num")
    assert kinds(traced(tree.insert, 50)) == ["empty_tree"]
    assert kinds(traced(tree.insert, 30)) == ["go_left", "place_left"]
    assert kinds(traced(tree.insert, 40)) == ["go_left", "go_right", "place_right"]
    assert traced(tree.insert, 45)[-1].snapshot == (50, (30, None, (40, None, (45, None, None))), None)


@pytest.mark.parametrize("keys, case", [
    ([30, 20, 10], "LL"),
    ([10, 20, 30], "RR"),
    ([30, 10, 20], "LR"),
    ([10, 30, 20], "RL"),
], ids=["LL", "RR", "LR", "RL"])
def test_avl_names_every_rotation_case(keys, case):
    tree = AVLTree("num")
    for key in keys[:-1]:
        tree.insert(key)
    events = traced(tree.insert, keys[-1])
    assert kinds(events)[-2:] == ["unbalanced", "rotate"]
    assert events[-1].data == {"case": case, "top": 20}
    assert events[-1].snapshot == (20, (10, None, None), (30, None, None))  # Balanced again
    assert abs(events[-2].data["balance"]) == 2


def test_bst_delete_tells_the_three_cases():
    def tree_of(*keys):
        tree = BinarySearchTree("num")
        for key in keys:
            tree.insert(key)
        return tree

    assert kinds(traced(tree_of(50, 30, 70).delete, 30)) == ["go_left", "delete_leaf"]
    one_child = traced(tree_of(50, 30, 20).delete, 30)
    assert kinds(one_child) == ["go_left", "delete_one_child"]
    assert one_child[-1].data == {"key": 30, "child": 20}
    events = traced(tree_of(50, 30, 70, 60, 80).delete, 50)
    assert kinds(events) == ["successor", "go_left", "delete_leaf"]
    assert events[0].data == {"key": 50, "successor": 60}


# ---------------------------------------------------------------------------
# Hash tables, disjoint sets and tries
# ---------------------------------------------------------------------------

def test_probing_records_every_slot_it_tries():
    # An int hashes to itself, so 0 and 3 both start at slot 0 of a table with three slots
    table = LinearProbingHashTable(3)
    assert kinds(traced(table.insert, 0, "a")) == ["home", "free"]
    events = traced(table.insert, 3, "b")
    assert kinds(events) == ["home", "probe", "free"]
    assert events[1].data == {"key": 0, "index": 0}
    assert events[2].data == {"key": 3, "index": 1}
    assert kinds(traced(table.lookup, 3)) == ["home", "probe", "found"]
    assert kinds(_missing(table.lookup, 6)) == ["home", "probe", "probe", "miss"]
    table.insert(1, "c")
    assert kinds(_missing(table.insert, 9, "d")) == ["home", "probe", "probe", "probe", "full"]


def test_deleting_from_a_probing_table_rehashes_the_cluster():
    table = LinearProbingHashTable(4)
    for key in (0, 4, 1):  # 0 and 4 share a home slot, so they form a cluster with 1
        table.insert(key, str(key))
    events = traced(table.delete, 0)
    assert kinds(events) == ["home", "found", "remove", "rehash", "rehash"]
    assert [event.data for event in events[3:]] == [{"key": 4, "index": 0}, {"key": 1, "index": 1}]


def test_chaining_records_the_bucket_it_used():
    table = ChainingHashTable(3)
    assert kinds(traced(table.insert, 0, 1)) == ["home", "chain"]
    assert kinds(traced(table.insert, 0, 2)) == ["home", "update"]
    assert kinds(traced(table.lookup, 0)) == ["home", "found"]
    assert kinds(_missing(table.lookup, 9)) == ["home", "miss"]


def test_disjoint_set_records_the_walk_and_the_union():
    union_find = DisjointSet(4)
    assert kinds(traced(union_find.union, 0, 1)) == ["root", "root", "attach", "rank_up"]
    assert kinds(traced(union_find.union, 2, 3)) == ["root", "root", "attach", "rank_up"]
    assert kinds(traced(union_find.union, 1, 3)) == ["hop", "root", "hop", "root", "attach", "rank_up"]
    assert kinds(traced(union_find.find, 3)) == ["hop", "hop", "root", "compress"]
    assert kinds(traced(union_find.union, 0, 3)) == ["root", "hop", "root", "same_set"]


def test_trie_records_the_path_through_the_nodes():
    trie = Trie(["car"])
    assert kinds(traced(trie.insert, "card")) == ["follow", "follow", "follow", "new_node", "mark_word"]
    assert kinds(traced(trie.search, "car")) == ["follow", "follow", "follow", "is_word"]
    assert kinds(traced(trie.search, "ca")) == ["follow", "follow", "not_word"]
    assert kinds(traced(trie.search, "dog")) == ["no_link"]
    assert kinds(traced(trie.delete, "card")) == ["unmark", "prune", "keep_node"]
    assert traced(trie.insert, "cat")[-2].snapshot == "cat"


# ---------------------------------------------------------------------------
# Graphs
# ---------------------------------------------------------------------------

def test_traversals_record_what_waits_in_the_queue():
    graph = example_graph(directed=False)
    events = traced(graph.bfs, 0)
    assert kinds(events)[:4] == ["visit", "enqueue", "visit", "enqueue"]
    assert events[1].data == {"vertex": 0, "neighbors": [1, 2]}
    assert events[1].snapshot == {"order": [0], "waiting": [1, 2]}
    assert kinds(traced(graph.dfs, 0))[:2] == ["visit", "visit"]
    assert kinds(traced(graph.dfs, 0))[-1] == "back"


def test_dijkstra_records_settled_and_relaxed_vertices():
    events = traced(graph_algorithms.dijkstra, example_graph(directed=False), 0)
    assert kinds(events)[:5] == ["settle", "relax", "relax", "settle", "relax"]
    assert events[0].data == {"vertex": 0, "distance": 0}
    assert events[4].data == {"vertex": 1, "distance": 3, "through": 2}
    assert "stale" in kinds(events)  # Vertex 1 was reached again, by a longer path
    assert events[-1].snapshot == {0: 0, 1: 3, 2: 1, 3: 8, 4: 10}


def test_topological_sort_records_the_in_degrees():
    events = traced(graph_algorithms.topological_sort, example_graph(directed=True))
    assert kinds(events)[:3] == ["no_incoming", "place", "ready"]
    assert events[0].data == {"vertices": [0]}
    assert events[0].snapshot == {0: 0, 1: 2, 2: 1, 3: 2, 4: 1}


def test_cycle_detection_records_the_path_and_the_groups():
    directed = example_graph(directed=True)
    assert set(kinds(traced(graph_algorithms.find_cycle, directed))) == {"enter", "leave"}
    directed.add_edge(4, 0, 1)
    events = traced(graph_algorithms.find_cycle, directed)
    assert kinds(events)[-1] == "cycle_edge"
    assert events[-1].data == {"u": 4, "v": 0}

    events = traced(graph_algorithms.find_cycle, example_graph(directed=False))
    assert kinds(events) == ["join", "join", "cycle_link"]
    assert events[1].snapshot == [(0, 1), (0, 2)]


def test_spanning_trees_record_the_edges_they_take_and_leave():
    graph = example_graph(directed=False)
    prim = traced(graph_algorithms.prim, graph)
    assert kinds(prim)[:2] == ["start_tree", "accept"]
    assert "skip" in kinds(prim)
    assert prim[1].data == {"u": 0, "v": 2, "weight": 1}
    kruskal = traced(graph_algorithms.kruskal, graph)
    assert kinds(kruskal)[0] == "accept"
    assert [event.data["weight"] for event in kruskal if event.kind == "accept"] == [1, 2, 3, 5]


# ---------------------------------------------------------------------------
# Captions
# ---------------------------------------------------------------------------

def every_run():
    """Yield the events of at least one run of every operation that records its steps."""
    values = [7, 8, 10, 42, 300, 672, 1987, 2004]
    for sort in (sorting.bubble_sort, sorting.selection_sort, sorting.insertion_sort, sorting.quick_sort,
                 sorting.heap_sort, sorting.shell_sort, sorting.merge_sort, sorting.counting_sort,
                 sorting.radix_sort):
        yield list(sort([170, 45, 75, 90, 802, 24, 2, 66]))
    yield list(sorting.insertion_sort([2, 1, 3]))  # A value that stays where it is
    for search in (searching.linear_search, searching.binary_search, searching.jump_search,
                   searching.interpolation_search, searching.exponential_search):
        for target in (10, 2004, 5):
            yield traced(search, values, target)

    heap = MinHeap("num")
    yield heap.heapify([50, 30, 10, 20, 70])
    yield heap.insert(5)
    yield heap.extract()[1]
    yield heap.update(3, 1)

    for tree in (BinarySearchTree("num"), AVLTree("num")):
        for key in (50, 30, 70, 60, 80, 20, 10):
            yield traced(tree.insert, key)
        for key in (10, 30, 50):
            yield traced(tree.delete, key)

    chaining = ChainingHashTable(3)
    yield traced(chaining.insert, 0, 1)
    yield traced(chaining.insert, 0, 2)
    yield traced(chaining.lookup, 0)
    yield traced(chaining.delete, 0)
    yield _missing(chaining.lookup, 0)

    probing = LinearProbingHashTable(3)
    for key in (0, 3, 1):  # Ints hash to themselves, so 0 and 3 collide
        yield traced(probing.insert, key, str(key))
    yield _missing(probing.insert, 9, "9")  # The table is full now
    yield traced(probing.delete, 0)
    yield _missing(probing.lookup, 9)

    union_find = DisjointSet(6)
    for a, b in ((0, 1), (2, 3), (1, 3), (0, 2)):
        yield traced(union_find.union, a, b)
    yield traced(union_find.find, 3)

    trie = Trie(["car"])
    yield traced(trie.insert, "card")
    for word in ("car", "ca", "dog"):
        yield traced(trie.search, word)
    yield traced(trie.delete, "card")

    for directed in (True, False):
        graph = example_graph(directed)
        yield traced(graph.bfs, 0)
        yield traced(graph.dfs, 0)
        yield traced(graph_algorithms.dijkstra, graph, 0)
        yield traced(graph_algorithms.find_cycle, graph)
        if directed:
            yield traced(graph_algorithms.topological_sort, graph)
            graph.add_edge(4, 0, 1)  # Closes a cycle, so the sort can't finish
            yield _missing(graph_algorithms.topological_sort, graph)
            yield traced(graph_algorithms.find_cycle, graph)
        else:
            yield traced(graph_algorithms.prim, graph)
            yield traced(graph_algorithms.kruskal, graph)


def _missing(operation, *arguments):
    """Return the events of an operation that ends in an error, such as a lookup that finds nothing."""
    trace = []
    with pytest.raises(Exception):
        operation(*arguments, trace=trace)
    return trace


ALL_EVENTS = [event for events in every_run() for event in events]


def test_every_step_has_a_caption_that_reads_as_a_sentence():
    for event in ALL_EVENTS:
        sentence = narration.caption(event)
        assert sentence.endswith(".") and sentence[0].isupper() or sentence[0] in "'0123456789", sentence


def test_every_caption_is_used_and_every_kind_has_one():
    used = {event.kind for event in ALL_EVENTS}
    assert used - set(narration.TEMPLATES) == set()
    assert set(narration.TEMPLATES) - used == set()


def test_captions_leave_the_costs_to_the_complexity_tables():
    assert not any("O(" in template for template in narration.TEMPLATES.values())


def test_a_kind_without_a_caption_is_reported():
    with pytest.raises(KeyError):
        narration.caption(ALL_EVENTS[0]._replace(kind="dance"))
