"""Regressions for gaps found while auditing all five phases of the v4 roadmap."""

import json
import os
import subprocess
import sys
from dataclasses import replace

import pytest
from rich.cells import cell_len

from pydsa import settings, topics
from pydsa.algorithms import graph_algorithms, searching, sorting
from pydsa.algorithms.trace import tree as snapshot
from pydsa.content import narration, notes
from pydsa.core.graph import ListGraph
from pydsa.core.hash_table import ChainingHashTable
from pydsa.core.tree import AVLTree, BinarySearchTree
from pydsa.practice import challenges
from pydsa.ui import render, stepper
from pydsa.ui.console import console, force_colors_off


@pytest.mark.parametrize("search", [searching.binary_search, searching.jump_search,
                                   searching.interpolation_search, searching.exponential_search])
def test_sorted_search_steps_include_valid_active_bounds(search):
    values = [2, 6, 10, 17, 25, 31, 42]
    for target in (2, 17, 42, 19):
        trace = []
        assert search(values, target, trace) == (values.index(target) if target in values else -1)
        for event in trace:
            assert 0 <= event.data["low"] <= event.data["index"] <= event.data["high"] < len(values)
            assert "Active range: low" in narration.caption(event)
            if search is searching.binary_search:
                assert event.data["mid"] == (event.data["low"] + event.data["high"]) // 2


def test_linear_search_without_tracing_does_not_copy_the_input():
    class CountedList(list):
        def __iter__(self):
            self.iterations += 1
            return super().__iter__()

    values = CountedList(range(100))
    values.iterations = 0
    assert searching.linear_search(values, -1) == -1
    assert values.iterations == 1


@pytest.mark.parametrize("sort", [sorting.bubble_sort, sorting.selection_sort, sorting.insertion_sort,
                                 sorting.quick_sort, sorting.heap_sort, sorting.shell_sort,
                                 sorting.merge_sort, sorting.counting_sort, sorting.radix_sort])
@pytest.mark.parametrize("order", ["asc", "desc"])
def test_sort_steps_account_for_all_work(sort, order):
    stats = sorting.SortStats()
    for values in ([1, 2, 3, 4], [4, 3, 2, 1], [3, 1, 3, 2]):
        before = stats.comparisons, stats.writes
        items = list(values)
        events = list(sort(items, order, stats))
        assert items == sorted(values, reverse=order == "desc")
        assert sum(event.data["comparisons"] for event in events) == stats.comparisons - before[0]
        assert sum(event.data["writes"] for event in events) == stats.writes - before[1]
        assert all("Work since the previous step:" in narration.caption(event) for event in events)


def test_swap_caption_describes_the_values_before_the_swap():
    event = next(sorting.bubble_sort([3, 2]))
    assert narration.caption(event).startswith("3 came after 2, so the two swapped places.")
    assert event.snapshot == [2, 3]


def test_descending_partition_caption_and_marks_match_its_state():
    before = [1, 4, 2, 3]
    event = next(sorting.quick_sort(list(before), "desc"))
    pivot = event.data["index"]
    assert all(value >= event.data["pivot"] for value in event.snapshot[:pivot])
    assert all(value <= event.data["pivot"] for value in event.snapshot[pivot + 1:])
    assert {i for i, value in enumerate(before) if value != event.snapshot[i]} <= set(event.marks)
    assert "smaller values sit before" not in narration.caption(event)


@pytest.mark.parametrize("tree_type", [BinarySearchTree, AVLTree])
@pytest.mark.parametrize("keys,key", [([50, 30, 70], 30), ([50, 30, 70, 20], 30),
                                    ([50, 30, 70, 40], 30), ([50], 50),
                                    ([50, 30], 50), ([50, 70], 50),
                                    ([50, 30, 70, 60, 80], 50)])
def test_deletion_snapshot_shows_the_replacement(tree_type, keys, key):
    tree = tree_type("num")
    for value in keys:
        tree.insert(value)
    trace = []
    tree.delete(key, trace)
    removed = next(event for event in reversed(trace) if event.kind in ("delete_leaf", "delete_one_child"))
    # These cases do not need a later rotation: the deletion itself must show the final state.
    assert removed.snapshot == snapshot(tree.root)
    assert tree.inorder() == sorted(value for value in keys if value != key)
    frozen = removed.snapshot
    tree.insert(99)
    assert removed.snapshot == frozen


def test_chaining_records_each_collision_for_insert_lookup_and_delete():
    table = ChainingHashTable(3)
    table.insert(0, "a")
    table.insert(3, "b")
    for operation, arguments in ((table.insert, (6, "c")), (table.lookup, (6,)), (table.delete, (6,))):
        trace = []
        operation(*arguments, trace=trace)
        collisions = [event for event in trace if event.kind == "chain_probe"]
        assert [event.data["key"] for event in collisions] == [0, 3]
        assert [event.data["position"] for event in collisions] == [0, 1]
        assert all(event.data["target"] == 6 for event in collisions)


def test_topological_sort_records_degrees_before_they_reach_zero():
    graph = ListGraph(True)
    for vertex in range(3):
        graph.add_vertex(vertex)
    graph.add_edge(0, 2, 1)
    graph.add_edge(1, 2, 1)
    trace = []
    assert graph_algorithms.topological_sort(graph, trace) == [0, 1, 2]
    updates = [event for event in trace if event.kind == "edge_removed"]
    assert [event.snapshot[2] for event in updates] == [1, 0]
    assert [event.data["degree"] for event in updates] == [1, 0]


def test_graph_operations_without_tracing_do_not_build_step_snapshots(monkeypatch):
    from pydsa.core import graph as graph_module

    graph = ListGraph(True)
    for vertex in range(3):
        graph.add_vertex(vertex)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 1)

    def unexpected(*args, **kwargs):
        pytest.fail("An untraced operation constructed a step snapshot")

    monkeypatch.setattr(graph_module, "_walk", unexpected)
    monkeypatch.setattr(graph_algorithms, "record", unexpected)
    assert graph.bfs(0) == [0, 1, 2]
    assert graph.dfs(0) == [0, 1, 2]
    assert graph_algorithms.topological_sort(graph) == [0, 1, 2]
    assert graph_algorithms.dijkstra(graph, 0).distances[2] == 2
    assert graph_algorithms.find_cycle(graph) is None


@pytest.mark.parametrize("width", [45, 90])
def test_long_scripted_run_shows_only_six_captions(width, capsys):
    console.width = width
    events = list(sorting.bubble_sort(list(range(25, 0, -1))))
    shown = []
    assert stepper.play(events, lambda *_: pytest.fail("Cannot pause"), shown.append) == events
    out = capsys.readouterr().out
    assert shown == []
    assert "Showing 6 of 300 steps" in out
    assert " ".join(out.split()).count("the two swapped places") == 6
    assert "300." in out
    assert all(len(line) <= width for line in out.splitlines())


def test_caption_table_preserves_brackets_in_user_values(capsys):
    render.step_captions(list(sorting.bubble_sort(["[red]", "[blue]"])))
    out = capsys.readouterr().out
    assert "[red]" in out and "[blue]" in out


@pytest.mark.parametrize("version", [0, 2, True, "1", None])
def test_unsupported_settings_version_uses_defaults(version):
    settings.path().parent.mkdir(parents=True)
    settings.path().write_text(json.dumps({"version": version, "steps": "pause"}), encoding="utf-8")
    loaded, notice = settings.load()
    assert loaded == settings.Settings()
    assert "version isn't supported" in notice


def test_prediction_does_not_accept_booleans_in_numeric_lists():
    challenge = replace(challenges.make("sorting"), answer=[1, 2, 3])
    assert challenge.check("1, 2, 3")
    assert challenge.check("[1.0, 2, 3]")
    assert not challenge.check("[True, 2, 3]")
    nested = replace(challenge, answer=[[0, 1]])
    assert nested.check("[[0, 1]]")
    assert not nested.check("[[False, True]]")


def test_search_summary_explains_bounds_and_moves(play):
    out = play("3", "3", "1", "8", "0", argv=("--topic", "searching"))
    assert "Active range: low" in out
    assert "further left" in out
    assert "Found 8 at index 3" in out


@pytest.mark.parametrize("topic,label", [("tree", "BST (Binary Search Tree)"),
                                       ("heap", "Min Heap"),
                                       ("hash-table", "Separate Chaining (Open Hashing)"),
                                       ("graph", "Adjacency Matrix"),
                                       ("linked-list", "Singly Linked List")])
def test_nested_topic_visits_refresh_on_return(play, topic, label):
    out = play("1", "0", "0", "0", argv=("--topic", topic))
    assert f"1) ✓ {label}" in out


def test_guide_browser_visit_marks_refresh(play):
    out = play("6", "2", "1", "2", "0", "0", "0", "0")
    assert "2) ✓ Stack" in out


@pytest.mark.parametrize("width", [45, 90])
def test_all_guides_notes_and_code_fit_without_color(width, capsys):
    console.width = width
    force_colors_off(True)
    settings.current = settings.Settings(detail="detailed", colors=False)
    for topic in topics.TOPICS:
        render.guide(topic.id)
    for note in notes.NOTES:
        render.operation_note(note)
        if note.sources:
            render.code(note)
    out = capsys.readouterr().out
    assert "\x1b[" not in out
    assert all(cell_len(line) <= width for line in out.splitlines())


def test_piped_cli_handles_a_legacy_windows_encoding():
    environment = {**os.environ, "PYTHONIOENCODING": "cp1252", "NO_COLOR": "1"}
    result = subprocess.run([sys.executable, "-m", "pydsa", "--list-topics"],
                            env=environment, capture_output=True, check=True)
    out = result.stdout.decode("utf-8")
    assert "avl-tree" in out and "dijkstra" in out
    assert "Traceback" not in result.stderr.decode("utf-8")
