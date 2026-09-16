"""Rich renderers, checked through their plain-text output (tests don't run in a terminal, so there are no colors)."""

import pytest
from rich.cells import cell_len

from pydsa import __version__, settings
from pydsa.algorithms import graph_algorithms, sorting
from pydsa.content import notes, registry, texts
from pydsa.core.deque import Deque
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.graph import ListGraph
from pydsa.core.hash_set import HashSet
from pydsa.core.hash_table import ChainingHashTable, LinearProbingHashTable
from pydsa.core.heap import MinHeap
from pydsa.core.priority_queue import PriorityQueue
from pydsa.core.queue import Queue
from pydsa.core.stack import Stack
from pydsa.core.tree import AVLTree, BinarySearchTree
from pydsa.core.trie import Trie
from pydsa.settings import Settings
from pydsa.ui import render
from pydsa.ui.console import QuitRequested, console


def test_array_cells_under_their_indexes(capsys):
    render.array([10, "a"])
    out = capsys.readouterr().out
    assert "│ 10 │ 'a' │" in out
    assert "Index" not in out


def test_array_switches_to_rows_when_too_wide(capsys):
    console.width = 30
    render.array(list(range(100, 115)))
    out = capsys.readouterr().out
    assert "Index" in out
    assert all(cell_len(line) <= 30 for line in out.splitlines())


def test_values_are_never_read_as_markup(capsys):
    render.array(["[bold]x[/bold]"])
    assert "'[bold]x[/bold]'" in capsys.readouterr().out


def test_stack_marks_the_top_and_summarizes_empty_slots(capsys):
    stack = Stack(10)
    stack.push(1)
    stack.push("two")
    render.stack(stack)
    out = capsys.readouterr().out
    assert out.count("← top") == 1
    assert "'two'" in out.split("← top")[0].splitlines()[-1]
    assert "8 empty slots" in out

    small = Stack(3)
    small.push(1)
    render.stack(small)
    assert capsys.readouterr().out.count("empty") == 2


def test_queue_markers_and_struck_out_leftovers(capsys):
    queue = Queue(3)
    for item in (1, 2, 3):
        queue.enqueue(item)
    queue.dequeue()
    render.circular_slots(queue, {"front": queue.front, "rear": queue.rear})
    out = capsys.readouterr().out
    assert "front" in out and "rear" in out
    assert render.strike("1") in out
    assert "Struck-out items" in out


def test_deque_marks_both_ends(capsys):
    deque = Deque(3)
    deque.push_front("a")
    render.circular_slots(deque, {"front": deque.front, "back": deque.back})
    out = capsys.readouterr().out
    assert "front/back" in out
    assert out.count("empty") == 2


def test_circular_linked_lists_loop_back(capsys):
    render.linked_list([1, "a"], circular=True)
    out = capsys.readouterr().out
    assert "│ 1 │ → │ 'a' │ → back to the head" in out
    assert "the tail links back to the head" in out

    render.linked_list(["a", 1], doubly=True, circular=True, backward=True)
    out = capsys.readouterr().out
    assert "│ 'a' │ ⇄ │ 1 │ ⇄ back to the tail" in out
    assert "None" not in out


def test_hash_sets_side_by_side(capsys):
    render.hash_sets({"A": HashSet(3, [1, "b", 2.5]), "B": HashSet(3)})
    out = capsys.readouterr().out
    assert "Set A" in out and "Set B" in out
    assert "A = {1, 2.5, 'b'}" in out
    assert "B = ∅ (the empty set)" in out


def test_disjoint_set_arrays_and_groups(capsys):
    union_find = DisjointSet(5)
    union_find.union(0, 1)
    union_find.union(3, 4)
    render.disjoint_set(union_find)
    out = capsys.readouterr().out
    assert "Parent and Rank Arrays" in out
    assert "3 sets" in out
    assert "{0, 1}" in out and "{2}" in out and "{3, 4}" in out

    console.width = 20
    render.disjoint_set(DisjointSet(12))
    assert "Rank" in capsys.readouterr().out


def test_linked_lists_as_boxed_nodes(capsys):
    render.linked_list([1, "a"])
    out = capsys.readouterr().out
    assert "│ 1 │ → │ 'a' │ → None" in out
    assert "2 nodes" in out

    render.linked_list([1, "a"], doubly=True, backward=True)
    out = capsys.readouterr().out
    assert "None ← │ 1 │ ⇄ │ 'a' │ → None" in out
    assert "tail back to the head" in out

    render.linked_list([])
    assert "The list is empty." in capsys.readouterr().out


def test_long_linked_lists_wrap(capsys):
    console.width = 40
    render.linked_list(list(range(1000, 1012)))
    out = capsys.readouterr().out
    assert all(cell_len(line) <= 40 for line in out.splitlines())
    assert out.count("┌") == 12


def test_binary_tree_drawn_top_down(capsys):
    tree = BinarySearchTree("num")
    for key in (50, 30, 70, 60):
        tree.insert(key)
    render.binary_tree(tree)
    assert "   50\n┌──┴──┐\n30    70\n    ┌─┘\n    60\n" in capsys.readouterr().out

    render.binary_tree(BinarySearchTree("str"))
    assert "The tree is empty." in capsys.readouterr().out


def test_avl_tree_shows_balance_factors(capsys):
    tree = AVLTree("num")
    for key in (1, 2, 3, 4):
        tree.insert(key)
    render.binary_tree(tree, balance=True)
    out = capsys.readouterr().out
    assert "2 (-1)" in out and "3 (-1)" in out and "4 (0)" in out
    assert "balance factor" in out


def test_wide_trees_fall_back_to_an_outline(capsys):
    console.width = 24
    tree = AVLTree("num")
    for key in range(1000, 1015):
        tree.insert(key)
    render.binary_tree(tree)
    out = capsys.readouterr().out
    assert "root 1007" in out and "L 1003" in out and "R 1011" in out
    assert "┴" not in out


def test_tree_stats(capsys):
    tree = BinarySearchTree("str")
    for key in ("m", "c", "x", "a"):
        tree.insert(key)
    render.tree_stats(tree)
    out = capsys.readouterr().out
    assert "Height (levels)" in out and "Leaves" in out
    assert "'a'" in out and "'x'" in out

    render.tree_stats(MinHeap("num"), "heap")
    assert "The heap is empty." in capsys.readouterr().out


def test_heap_steps_show_the_tree_and_the_array(capsys):
    heap = MinHeap("num")
    heap.heapify([10, 20, 30])
    render.heap_steps(heap.insert(5), "Added 5 as the last leaf.")
    out = capsys.readouterr().out
    assert "Step 0: Added 5 as the last leaf." in out
    assert "Step 1: Moved 5 up, swapping it with its parent 20." in out
    assert "Step 2: Moved 5 up, swapping it with its parent 10." in out
    assert "Array: [5*, 10*, 30, 20]" in out
    assert "* marks the keys that moved" in out
    assert out.count("┴") == 3  # One tree diagram per step

    render.heap(heap)
    out = capsys.readouterr().out
    assert "│ 5 │ 10 │ 30 │ 20 │" in out
    assert "2i + 1 and 2i + 2" in out


def test_priority_queue_serving_order(capsys):
    queue = PriorityQueue()
    queue.enqueue("b", 2)
    queue.enqueue("a", 1)
    queue.enqueue("c", 2)
    render.priority_queue(queue)
    out = capsys.readouterr().out
    assert "1: 'a'" in out
    assert "Serving order" in out
    assert out.index("'b'  ") < out.index("'c'  ")  # Equal priorities in arrival order


def test_trie_marks_word_ends(capsys):
    render.trie(Trie(["car", "cat", "do"]))
    out = capsys.readouterr().out
    assert "✓ 'car'" in out and "✓ 'cat'" in out and "✓ 'do'" in out
    assert "3 words in 6 nodes" in out

    render.trie(Trie())
    assert "The trie is empty." in capsys.readouterr().out


def test_graphs(capsys):
    render.adjacency_matrix([[0, 5], [7, 0]])
    out = capsys.readouterr().out
    assert "Adjacency Matrix" in out and "from \\ to" in out

    render.adjacency_list({0: [(1, 5), (2, 30)], 1: []})
    out = capsys.readouterr().out
    assert "→ 1 (5)   → 2 (30)" in out
    assert "no edges" in out


def test_undirected_graphs(capsys):
    render.adjacency_list({0: [(1, 5)], 1: [(0, 5)]}, directed=False)
    out = capsys.readouterr().out
    assert "— 1 (5)" in out and "under both of its vertices" in out

    render.adjacency_matrix([[0, 5], [5, 0]], directed=False)
    assert "symmetric" in capsys.readouterr().out


def test_sort_comparison(capsys):
    stats = sorting.SortStats()
    stats.comparisons, stats.writes = 3, 6
    render.sort_comparison([("Bubble Sort", stats, 3), ("Radix Sort", None, 0)])
    out = capsys.readouterr().out
    assert "Sorting algorithms compared" in out
    assert "Bubble Sort" in out and "—" in out
    assert "can't sort this list" in out


def test_search_probes_are_numbered_under_the_values(capsys):
    render.search_probes([1, 2, 3], [1, 2, 1], "Checked 3 positions.")
    out = capsys.readouterr().out
    assert "1,3" in out
    assert "Checked 3 positions." in out


def test_shortest_paths_and_spanning_forests(capsys):
    graph = ListGraph()
    for vertex in range(3):
        graph.add_vertex(vertex)
    graph.add_edge(0, 1, 5)
    paths = graph_algorithms.dijkstra(graph, 0)
    render.shortest_paths(paths, {vertex: graph_algorithms.shortest_path(paths, vertex) for vertex in graph.vertices()})
    out = capsys.readouterr().out
    assert "Shortest paths" in out
    assert "0 → 1" in out and "unreachable" in out
    assert "Every path starts at vertex 0. The distances became final in this order: 0, 1." in out

    triangle = ListGraph(directed=False)
    for vertex in range(3):
        triangle.add_vertex(vertex)
    for u, v, weight in [(0, 1, 1), (1, 2, 2), (0, 2, 3)]:
        triangle.add_edge(u, v, weight)
    render.spanning_forest(graph_algorithms.kruskal(triangle))
    out = capsys.readouterr().out
    assert "Chosen edges" in out
    assert "0 — 1" in out and "1 — 2" in out
    assert "Left out, because they would close a cycle: 0 — 2 (3)." in out


def test_hash_tables(capsys):
    chaining = ChainingHashTable(3)
    chaining.insert(1, "a")
    chaining.insert(4, "b")
    render.chaining_table(chaining)
    assert "1: 'a' → 4: 'b'" in capsys.readouterr().out

    probing = LinearProbingHashTable(3)
    probing.insert(1, "a")
    probing.insert(4, "b")
    render.probing_table(probing)
    out = capsys.readouterr().out
    assert "Home slot" in out
    assert out.count("empty") == 1


def test_sorting_steps_mark_moved_values(capsys):
    items = [3, 2, 1]
    count = render.sorting_steps(items, sorting.bubble_sort(items))
    out = capsys.readouterr().out
    assert count == 3
    assert any("start" in line and "[3, 2, 1]" in line for line in out.splitlines())
    assert "[2*, 3*, 1]" in out
    assert "* marks the values that moved" in out
    assert items == [1, 2, 3]


def test_intro_shows_the_summary_and_complexity_tables(capsys):
    render.intro(texts.ARRAY_ASCII, "array")
    out = capsys.readouterr().out
    assert "🎯 Array" in out and "numbered boxes" in out
    assert "Choose Read the Guide" in out
    assert "Array operations" in out and "Sorting algorithms" in out and "O(n log n)" in out
    assert "What it is" not in out


def test_guides_show_every_section_and_their_tables(capsys):
    render.guide("stack")
    out = capsys.readouterr().out
    assert "📖 Stack" in out
    assert all(heading in out for heading in registry.SECTIONS)
    assert "⏱️ Stack operations" in out
    assert "(glossary:" not in out
    assert "Words in bold are explained in the Glossary" in out


def test_explanations_follow_the_detail_setting(capsys):
    render.explanation("bubble-sort")
    out = capsys.readouterr().out
    assert "ℹ️ How Bubble Sort Works" in out
    assert "bubbled" in out  # The summary
    assert "early" not in out  # Not the How it works section
    assert "set Explanations to Detailed" in out

    settings.current = Settings(detail="detailed")
    render.explanation("bubble-sort")
    out = capsys.readouterr().out
    assert "early" in out and "bubbled" not in out
    assert "set Explanations to Detailed" not in out


def test_documents_and_glossary_terms(capsys):
    render.document("choosing", "🧭")
    out = capsys.readouterr().out
    assert "🧭 Which Data Structure Should I Use?" in out and "🔹 Model connections" in out

    render.glossary(registry.find_terms("heap"))
    out = capsys.readouterr().out
    assert "📘 Glossary" in out and "🔹 Heap property" in out and "🔹 Heapify" in out


def test_long_output_pauses_between_screenfuls(monkeypatch, capsys):
    monkeypatch.setattr("pydsa.ui.console.page_height", lambda: 10)

    answers = iter(["", "s"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    render.guide("stack")
    out = capsys.readouterr().out
    assert out.count("Enter: more · a: all · s: stop") == 2
    assert "In PyDSA" not in out  # Stopped before the end

    answers = iter(["a"])
    render.guide("stack")
    out = capsys.readouterr().out
    assert out.count("Enter: more") == 1 and "In PyDSA" in out

    answers = iter([":q"])
    with pytest.raises(QuitRequested):
        render.guide("stack")
    capsys.readouterr()

    # Output that fits never pauses
    monkeypatch.setattr("pydsa.ui.console.page_height", lambda: 1000)
    render.guide("stack")
    assert "Enter: more" not in capsys.readouterr().out


def test_home_shows_the_full_intro_once_per_session(capsys):
    render.start_session()
    render.home()
    render.home()
    out = capsys.readouterr().out
    assert out.count("Changelog") == 1
    assert f"PyDSA {__version__}  ·  type h in any menu for help" in out


def test_operation_notes_follow_the_detail_setting(capsys):
    push = notes.find("stack", "Push")
    render.operation_note(push)
    out = capsys.readouterr().out
    assert "💡 Push: Puts an item on top of the stack. · Cost: Time O(1) · Extra space O(1)" in out
    assert "1." not in out

    settings.current = Settings(detail="detailed")
    render.operation_note(push)
    out = capsys.readouterr().out
    assert "  1. If the stack is full, refuse the item." in out
    assert "  Cost: Time O(1) · Extra space O(1)" in out

    render.operation_note(notes.find("singly-linked-list", "Delete from End"))
    assert "Cost: O(n)" in capsys.readouterr().out  # Only the singly linked list's column

    render.operation_note(notes.find("sorting", "Bubble Sort"))
    out = capsys.readouterr().out
    assert "⏱️ Cost: Best O(n) · Average O(n²) · Worst O(n²) · Extra space O(1)" in out
    assert "💡" not in out  # The algorithm explains itself

    render.operation_note(notes.find("stack", "Display"))
    assert "💡 Display: Draws the stack from the top down, marking the top item.\n" in capsys.readouterr().out


def test_code_shows_the_pseudocode_and_the_real_source(capsys):
    render.code(notes.find("stack", "Pop"))
    out = capsys.readouterr().out
    assert "📝 Pseudocode: Pop" in out and "remove the top item and return it" in out
    assert "🐍 Stack.pop" in out and "pydsa/core/stack.py" in out
    assert "def pop(self):" in out
    assert "raises EmptyError" in out

    render.code(notes.find("sorting", "Bubble Sort"))
    out = capsys.readouterr().out
    assert "def bubble_sort(" in out and "follows the pseudocode closely" in out


def test_main_intro_shows_the_version(capsys):
    render.main_intro()
    out = capsys.readouterr().out
    assert f"⏳ Version {__version__}" in out
    assert "Changelog" in out
