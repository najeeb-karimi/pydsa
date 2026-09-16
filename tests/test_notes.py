"""Operation notes: every menu operation has one, and their costs and code references are real."""

import inspect
import re

import pytest

from pydsa.content import complexity, notes
from pydsa.core.array import Array
from pydsa.core.deque import Deque
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.graph import ListGraph, MatrixGraph
from pydsa.core.hash_set import HashSet
from pydsa.core.priority_queue import PriorityQueue
from pydsa.core.queue import Queue
from pydsa.core.stack import Stack
from pydsa.core.trie import Trie
from pydsa.ui.screens import (
    array, deque, disjoint_set, graph, graph_algorithms, hash_set, hash_table, heap, linked_list, queue,
    searching_algorithms, sorting_algorithms, stack, tree, trie,
)


def menus():
    """Yield (topic, operations) for every operation menu and algorithm sub-menu, built without running them."""
    yield "array", array.operations(Array(3, int, 0))
    yield "stack", stack.operations(Stack(3))
    yield "queue", queue.operations(Queue(3))
    yield "deque", deque.operations(Deque(3))
    for kind in (linked_list.SINGLY, linked_list.DOUBLY, linked_list.SINGLY_CIRCULAR, linked_list.DOUBLY_CIRCULAR):
        yield kind.guide, linked_list.operations(kind.list_class(), kind)
    for kind in (tree.BST, tree.AVL):
        yield kind.guide, tree.operations(kind.tree_class("num"))
    for kind in (heap.MIN, heap.MAX):
        yield kind.guide, heap.operations(kind.heap_class("num"), kind)
    yield "priority-queue", heap.queue_operations(PriorityQueue())
    yield "trie", trie.operations(Trie())
    yield "adjacency-matrix-graph", graph.operations(MatrixGraph(2))
    yield "adjacency-list-graph", graph.operations(ListGraph())
    for directed in (True, False):  # Each direction offers different algorithms
        yield "graph-algorithms", graph_algorithms.operations(ListGraph(directed))
        yield "graph-algorithms", graph.algorithm_options(ListGraph(directed))
    for kind in (hash_table.CHAINING, hash_table.PROBING):
        yield kind.guide, hash_table.operations(kind.table_class(3), kind)
    yield "hash-set", hash_set.operations({"A": HashSet(3), "B": HashSet(3)})
    yield "disjoint-set", disjoint_set.operations(DisjointSet(3))
    yield "sorting", sorting_algorithms.operations([3, 1, 2])
    yield "sorting", [(sort.name, None) for sort in sorting_algorithms.SORTS]  # The array's Sort menu
    yield "searching", searching_algorithms.operations([3, 1, 2])


def test_every_operation_has_exactly_one_note_and_every_note_is_used():
    used = set()
    for topic, operations in menus():
        for label, _ in operations:
            used.add((notes.find(topic, label).topic, label))
    keys = [(note.topic, note.operation) for note in notes.NOTES]
    assert len(keys) == len(set(keys))
    assert set(keys) == used


def test_missing_notes_are_reported():
    with pytest.raises(KeyError, match="no note for 'Fly' in the 'stack' menu"):
        notes.find("stack", "Fly")


@pytest.mark.parametrize("note", notes.NOTES, ids=lambda note: f"{note.topic}:{note.operation}")
def test_note_contents(note):
    assert note.summary.endswith(".") and len(re.findall(r"[.!?](?=\s|$)", note.summary)) == 1, note.summary
    assert all(step.endswith(".") for step in note.steps)
    words = " ".join((note.summary, *note.steps, *note.pseudocode))
    assert "O(" not in words  # Costs come from the complexity tables
    assert bool(note.pseudocode) == bool(note.sources)
    if note.sources and not note.explained:
        assert note.steps
    for row in note.complexity_rows:
        values = complexity.cost(note.topic, row)
        assert values and all(value != "—" for _, value in values)
    for reference in note.sources:
        function = notes.resolve(reference)
        assert inspect.isfunction(function), reference
        assert inspect.getsource(function)


def test_costs_keep_only_the_topics_own_columns():
    assert complexity.cost("stack", "Push") == [("Time", "O(1)"), ("Extra space", "O(1)")]
    assert complexity.cost("doubly-circular-linked-list", "Delete from end") == [("Doubly circular", "O(1)")]
    assert complexity.cost("bst", "Search") == [("BST (average)", "O(log n)"), ("BST (worst)", "O(n)")]
    with pytest.raises(KeyError):
        complexity.cost("stack", "Fly")
