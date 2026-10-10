"""Graph Algorithms II: menus, errors, creation, practice, paused steps and compact drawings."""

import random

import pytest
from rich.cells import cell_len

from pydsa import progress, settings
from pydsa.algorithms import graph_algorithms
from pydsa.content import notes, texts
from pydsa.core.graph import ListGraph
from pydsa.practice import challenges, experiments
from pydsa.ui import render, stepper
from pydsa.ui.console import console


def test_negative_example_both_algorithms_guides_code_restart_and_home(play):
    out = play("4", "2", "0", "5", "0", "6", "0", "4", "6", "4", "0",
               "1", "7", "1", "8", "1", "9", "9", "4", "9", "5", "9", "6",
               "8", "10", "1", "11", "0", argv=["--topic", "graph-algorithms"])
    assert "Try Bellman-Ford" in out and "Relaxation pass" in out
    assert "All-pairs distances" in out and "Distance: 6; path: 0 → 1 → 2 → 3 → 4" in out
    assert "Vertex 0 is unreachable from 4." in out
    assert "Pseudocode: Bellman-Ford" in out and "Pseudocode: Floyd-Warshall" in out
    assert "Pseudocode: A* on a Grid" in out and "Goodbye!" in out
    assert {"bellman-ford", "floyd-warshall", "a-star"} <= progress.current.visited.keys()


@pytest.mark.parametrize("representation", ["adjacency-list-graph", "adjacency-matrix-graph"])
def test_graph_menu_negative_cycles_are_drawn_and_missing_sources_are_clean(play, representation):
    out = play("2", "1", "4", "4", "0", "-20", "8", "4", "0", "8", "5",
               "8", "4", "99", "0", argv=["--topic", representation])
    assert "Negative cycle: 0 → 2 → 1 → 3 → 4 → 0" in out
    assert "Negative diagonal vertices:" in out and "shortest paths through them are undefined" in out
    assert "Vertex 99" in out and "Goodbye!" in out


def test_graph_menu_grid_back_new_home_and_exit_propagate(play):
    out = play("2", "1", "8", "0", "9", "0", argv=["--topic", "adjacency-list-graph"])
    assert "Goodbye!" in out
    out = play("2", "1", "8", "6", "0", "9", "8", "6", "2", "6", "2", "7", "0",
               argv=["--topic", "adjacency-list-graph"])
    assert "What do you want to do with the grid?" in out and "Goodbye!" in out
    out = play("2", "2", "8", "7", "2", "0", argv=["--topic", "adjacency-matrix-graph"])
    assert "Goodbye!" in out


def test_grid_example_all_operations_code_and_restart(play):
    out = play("2", "1", "2", "3", "4", "5", "1", "5", "2", "6", "2", "7", "0",
               argv=["--topic", "a-star"])
    assert "Shortest path: 10 moves." in out
    assert "A* (Manhattan): 10 moves; expanded 11 cells." in out
    assert "Dijkstra (zero heuristic)" in out and "Pseudocode: Run A*" in out
    assert "Pseudocode: Compare with Dijkstra" in out and "Goodbye!" in out


def test_grid_typed_rows_bounds_walls_and_unreachable_goal(play):
    out = play("1", "0", "3", "11", "3", "?", "...", "###", "...",
               "1", "0", "0", "0", "3", "2", "2", "2", "2", "3", "0", argv=["--topic", "a-star"])
    assert "Use exactly 3 dots or # characters." in out and "That cell is a wall" in out
    assert "must be at least 1" in out and "must be at most 10" in out
    assert "Goal is unreachable. Expanded 3 cells." in out and "Dijkstra (zero heuristic): unreachable" in out


def test_grid_rejects_all_walls_and_accepts_shared_endpoint(play):
    out = play("1", "1", "1", "#", ".", "0", "0", "0", "0", "2", "3", "0",
               argv=["--topic", "a-star"])
    assert "The grid needs at least one open cell" in out and "Shortest path: 0 moves." in out
    assert "expanded 1 cells" in out and "Dijkstra expansions minus A*: 0" in out


def test_random_grid_and_graph_creation(play, monkeypatch):
    monkeypatch.setattr(random, "random", lambda: 0)  # All walls initially; creation must leave an open cell.
    out = play("3", "2", "2", "0", "0", "0", "0", "2", "0", argv=["--topic", "a-star"])
    assert "Shortest path: 0 moves." in out
    out = play("3", "1", "4", "1", "4", "5", "0", "6", "0", "3", "0",
               argv=["--topic", "graph-algorithms"])
    assert "random edges" in out and "Relaxation pass" in out and "All-pairs distances" in out


@pytest.mark.parametrize("topic,code", [("bellman-ford", "23"), ("floyd-warshall", "24"), ("a-star", "25")])
def test_new_practice_banks_predictions_and_experiments(play, monkeypatch, topic, code):
    monkeypatch.setattr(random.Random, "shuffle", lambda self, values: None)
    challenge = challenges.make(topic, random.Random(6))
    monkeypatch.setattr(challenges, "make", lambda topic_id: challenge)
    out = play("8", "4", "5", code, "1", "a", "a", "a", "a", "a", "2", repr(challenge.answer),
               "3", "1", "2", "0", "0", "0", "0", "0", "0")
    assert "Quiz score: 5/5" in out and "Correct prediction" in out and "Ratio" in out
    assert progress.current.quizzes[topic].best == 100 and progress.current.challenges[topic] == 1


@pytest.mark.parametrize("width", [45, 90])
@pytest.mark.parametrize("topic", ["bellman-ford", "floyd-warshall", "a-star"])
def test_guides_code_and_paused_states_fit_without_color(play, monkeypatch, capsys, width, topic):
    console.width = width
    monkeypatch.setattr(render, "ascii_art", lambda art: None)
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause", colors=False))
    if topic == "bellman-ford":
        answers = ["4", "1", "7", "5", "0", "a", "9", "4", "0"]
    elif topic == "floyd-warshall":
        answers = ["4", "1", "8", "6", "a", "0", "4", "9", "5", "0"]
    else:
        answers = ["2", "1", "2", "a", "3", "5", "1", "0"]
    out = play(*answers, argv=["--topic", topic, "--no-color"])
    assert "Step 1:" in out and "*" in out and "\x1b[" not in out
    assert all(cell_len(line) <= width for line in out.splitlines())
    graph = ListGraph()
    for vertex in range(10):
        graph.add_vertex(vertex)
    for vertex in range(9):
        graph.add_edge(vertex, vertex + 1, 100000)
    trace = []
    graph_algorithms.floyd_warshall(graph, trace)
    for i, event in enumerate(trace, 1):
        render.floyd_step(i, event)
    for note in notes.NOTES:
        if note.sources and (note.topic == "a-star" or note.operation in ("Bellman-Ford", "Floyd-Warshall", "A* on a Grid")):
            render.code(note)
    out = capsys.readouterr().out
    assert all(cell_len(line) <= width for line in out.splitlines())
    assert "From" in out and "To" in out


@pytest.mark.parametrize("topic,answers", [("bellman-ford", ["4", "5", "0", "s", "0"]),
                                         ("floyd-warshall", ["4", "6", "s", "0", "4", "0"]),
                                         ("a-star", ["2", "2", "s", "0"])])
def test_paused_steps_can_stop(play, monkeypatch, topic, answers):
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause"))
    out = play(*answers, argv=["--topic", topic])
    assert "Stopped after 1 of" in out and "Goodbye!" in out


@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError, ":b"])
def test_grid_interrupted_creation_is_clean(play, interrupt):
    tail = ["0", "0"] if interrupt == ":b" else []
    out = play("1", "2", "2", interrupt, *tail, argv=["--topic", "a-star"])
    assert "Goodbye!" in out and "Traceback" not in out


def test_work_experiments_count_actual_growth_and_grid_savings():
    by_id = {e.id: e for e in experiments.EXPERIMENTS}
    sizes = (8, 16, 32)
    for name, expected in (("bellman-passes", [(n - 1) ** 2 for n in sizes]),
                           ("floyd-pairs", [n ** 3 for n in sizes]),
                           ("grid-a-star", [2 * n - 1 for n in sizes]),
                           ("grid-dijkstra", [n * n for n in sizes])):
        assert [r.work for r in experiments.measure(by_id[name], sizes=sizes)] == expected


def test_grid_predictions_include_short_routes_and_detours():
    answers = {challenges.make("a-star", random.Random(seed)).answer for seed in range(30)}
    assert 8 in answers and max(answers) > 8


def test_ascii_titles_are_flower_power():
    for art in (texts.BELLMAN_FORD_ASCII, texts.FLOYD_WARSHALL_ASCII, texts.A_STAR_ASCII):
        assert len(art.splitlines()) >= 9 and "(_ o _)" in art
