"""Rich renderers, checked through their plain-text output (tests don't run in a terminal, so there are no colors)."""

from rich.cells import cell_len

from pydsa import __version__
from pydsa.algorithms import sorting
from pydsa.content import complexity, texts
from pydsa.core.deque import Deque
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.hash_set import HashSet
from pydsa.core.hash_table import ChainingHashTable, LinearProbingHashTable
from pydsa.core.heap import MinHeap
from pydsa.core.priority_queue import PriorityQueue
from pydsa.core.queue import Queue
from pydsa.core.stack import Stack
from pydsa.core.tree import AVLTree, BinarySearchTree
from pydsa.core.trie import Trie
from pydsa.ui import render
from pydsa.ui.console import console


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


def test_definition_with_complexity_tables(capsys):
    render.definition(texts.ARRAY_DEFINITION, complexity.ARRAY, complexity.SORTING)
    out = capsys.readouterr().out
    assert "🎯 Definition" in out
    assert "Array operations" in out and "Sorting algorithms" in out
    assert "O(n log n)" in out


def test_main_intro_shows_the_version(capsys):
    render.main_intro()
    out = capsys.readouterr().out
    assert f"⏳ Version {__version__}" in out
    assert "Changelog" in out
