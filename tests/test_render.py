"""Rich renderers, checked through their plain-text output (tests don't run in a terminal, so there are no colors)."""

from rich.cells import cell_len

from pydsa.algorithms import sorting
from pydsa.content import complexity, texts
from pydsa.core.hash_table import ChainingHashTable, LinearProbingHashTable
from pydsa.core.queue import Queue
from pydsa.core.stack import Stack
from pydsa.core.tree import BinarySearchTree
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
    render.queue(queue)
    out = capsys.readouterr().out
    assert "front" in out and "rear" in out
    assert render.strike("1") in out
    assert "Struck-out items" in out


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


def test_binary_tree_labels_children(capsys):
    tree = BinarySearchTree("num")
    for key in (50, 30, 70, 60):
        tree.insert(key)
    render.binary_tree(tree)
    out = capsys.readouterr().out
    assert "root 50" in out
    assert "L 30" in out and "R 70" in out and "L 60" in out

    render.binary_tree(BinarySearchTree("str"))
    assert "The tree is empty." in capsys.readouterr().out


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
    assert "⏳ Version 3.1" in out
    assert "Changelog" in out
