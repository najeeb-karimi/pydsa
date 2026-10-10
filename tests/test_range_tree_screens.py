"""Range tree navigation, narrated diagrams, practice, bounds and work comparisons."""

import random

import pytest
from rich.cells import cell_len

from pydsa import progress, settings
from pydsa.content import notes, texts
from pydsa.core.fenwick_tree import FenwickTree
from pydsa.core.segment_tree import SegmentTree
from pydsa.practice import challenges, experiments
from pydsa.ui import render, stepper
from pydsa.ui.console import console


def test_segment_all_operations_rebuild_code_restart_and_home(play):
    out = play("2", "1", "1", "3", "2", "4", "4", "3", "1", "10", "3", "2", "4",
               "2", "-1, 5, 9", "3", "0", "2", "5", "6", "1", "6", "2", "6", "3",
               "7", "2", "3", "8", "0", argv=["--topic", "segment-tree"])
    assert "What it is" in out and "Range [2, 4] sum: 12." in out
    assert "Range [2, 4] sum: 19." in out and "Range [0, 2] sum: 13." in out
    assert "Replaced index 3 with 10." in out
    assert "Pseudocode: Build from Array" in out and "Pseudocode: Range Query" in out
    assert "Pseudocode: Point Update" in out and "def query(" in out
    assert "Goodbye!" in out and "segment-tree" in progress.current.visited


def test_fenwick_all_operations_rebuild_code_restart_and_home(play):
    out = play("2", "1", "3", "6", "3", "-1", "4", "2", "4", "5", "4", "1", "-5",
               "4", "2", "4", "2", "3, -4, 2", "4", "0", "2", "6",
               "7", "1", "7", "2", "7", "3", "7", "4", "8", "2", "9", "0",
               argv=["--topic", "fenwick-tree"])
    assert "Prefix [0, 6] sum: 28." in out and "Prefix [0, -1] sum: 0." in out
    assert "Range [2, 4] sum: 12." in out and "Range [2, 4] sum: 3." in out
    assert "Range [0, 2] sum: 1." in out
    assert "lowest set bit" in out and "0111" in out and "Fenwick blocks" in out
    assert all(f"Pseudocode: {label}" in out for label in ("Build from Array", "Prefix Sum", "Range Sum", "Point Update"))
    assert "Goodbye!" in out and "fenwick-tree" in progress.current.visited


@pytest.mark.parametrize("choice,operation,answer", [("2", "min", "1"), ("3", "max", "8")])
def test_segment_creation_aggregate_choices(play, choice, operation, answer):
    out = play("2", choice, "3", "0", "7", "0", argv=["--topic", "segment-tree"])
    assert f"Range [0, 7] {operation}: {answer}." in out


@pytest.mark.parametrize("topic", ["segment-tree", "fenwick-tree"])
def test_typed_numbers_and_invalid_values_ranges_and_updates(play, topic):
    setup = ["1", "1"] if topic == "segment-tree" else ["1"]
    query = "3" if topic == "segment-tree" else "4"
    update = "4" if topic == "segment-tree" else "5"
    out = play(*setup, "a,b", "nan, 2", "inf, 2", ",", "1.5, -2.5, 4",
               query, "-1", "99", "0", "-1", "3", "2",
               update, "True", "3", "0", "2", "nan", "1", "9",
               query, "0", "2", "0", argv=["--topic", topic])
    assert "Range [0, 2] sum: 3.0." in out and "Range [0, 2] sum: 10.5." in out
    assert "finite numbers" in out and "must be at most 2" in out and "must be a whole number" in out


@pytest.mark.parametrize("topic", ["segment-tree", "fenwick-tree"])
def test_random_creation_and_count_limits(play, topic):
    setup = ["3", "2"] if topic == "segment-tree" else ["3"]
    out = play(*setup, "0", "51", "8", "0", argv=["--topic", topic])
    assert "must be at least 1" in out and "must be at most 50" in out and "from 8 numbers" in out


@pytest.mark.parametrize("topic", ["segment-tree", "fenwick-tree"])
@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError, ":b"])
def test_cancelled_or_interrupted_creation(play, topic, interrupt):
    setup = ["1", "1"] if topic == "segment-tree" else ["1"]
    tail = ["0", "0"] if interrupt == ":b" else []
    out = play(*setup, interrupt, *tail, argv=["--topic", topic])
    assert "Goodbye!" in out and "Traceback" not in out


@pytest.mark.parametrize("topic", ["segment-tree", "fenwick-tree"])
def test_cancelled_update_does_not_change_values(play, topic):
    setup = ["2", "1"] if topic == "segment-tree" else ["2"]
    query, update = ("3", "4") if topic == "segment-tree" else ("4", "5")
    out = play(*setup, update, "0", "1", ":b", query, "0", "7", "0", argv=["--topic", topic])
    assert "Cancelled." in out and "Range [0, 7] sum: 36." in out


def test_category_routes_and_aggregate_back(play):
    out = play("2", "6", "2", "0", "0", "7", "2", "0")
    assert "What should each range store?" in out and "Fenwick blocks" in out and "Goodbye!" in out


@pytest.mark.parametrize("topic", ["segment-tree", "fenwick-tree"])
def test_practice_quiz_prediction_and_both_experiments(play, monkeypatch, topic):
    monkeypatch.setattr(random.Random, "shuffle", lambda self, items: None)
    challenge = challenges.make(topic, random.Random(8))
    monkeypatch.setattr(challenges, "make", lambda topic_id: challenge)
    setup = ["2", "1", "9"] if topic == "segment-tree" else ["2", "10"]
    out = play(*setup, "1", "a", "a", "a", "a", "a", "2", repr(challenge.answer),
               "3", "1", "2", "2", "3", "0", "0", "0", argv=["--topic", topic])
    assert "Quiz score: 5/5" in out and "Correct prediction" in out
    assert "Direct range sum" in out and "Ratio" in out
    assert progress.current.quizzes[topic].best == 100 and progress.current.challenges[topic] == 1


@pytest.mark.parametrize("width", [45, 90])
@pytest.mark.parametrize("topic", ["segment-tree", "fenwick-tree"])
def test_guides_operations_code_and_paused_diagrams_fit(play, monkeypatch, capsys, width, topic):
    console.width, console.no_color = width, True
    monkeypatch.setattr(render, "ascii_art", lambda art: None)
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause", colors=False))
    setup = ["2", "1", "s"] if topic == "segment-tree" else ["2", "s"]
    query, update, code = ("3", "4", "6") if topic == "segment-tree" else ("4", "5", "7")
    out = play(*setup, "1", query, "2", "4", "a", update, "3", "1", "10", "a", code, "2", "0",
               argv=["--topic", topic, "--no-color"])
    assert "Step 1:" in out and "\x1b[" not in out and all(cell_len(line) <= width for line in out.splitlines())
    if topic == "segment-tree":
        assert "(inside)" in out and "(partial)" in out and "(outside)" in out
    else:
        assert "0110" in out and "Low bit" in out
    # Larger diagrams and every code view also remain readable when narrow.
    tree = SegmentTree(list(range(50))) if topic == "segment-tree" else FenwickTree(list(range(50)))
    (render.segment_tree if topic == "segment-tree" else render.fenwick_tree)(tree)
    for note in notes.NOTES:
        if note.topic == topic and note.sources:
            render.code(note)
    out = capsys.readouterr().out
    assert all(cell_len(line) <= width for line in out.splitlines())
    if topic == "segment-tree":
        assert "shown as an outline" in out


@pytest.mark.parametrize("topic", ["segment-tree", "fenwick-tree"])
def test_experiments_compare_the_same_range_with_direct_sum(topic):
    fast, direct = experiments.for_topic(topic)
    for mode in experiments.MODES:
        rows = experiments.measure(fast, mode, rng=random.Random(3))
        baseline = experiments.measure(direct, mode, rng=random.Random(3))
        assert [row.work for row in baseline] == [row.n // 2 - 1 for row in baseline]
        assert all(row.work <= 4 * experiments.LOG(row.n) + 1 for row in rows)
        assert rows[-1].work < baseline[-1].work // 4
        for n in fast.sizes:
            tree, left, right = fast.make_input(n, mode, random.Random(3))
            values, a, b = direct.make_input(n, mode, random.Random(3))
            assert (left, right) == (a, b) and tree.items == values
            answer = tree.query(left, right) if isinstance(tree, SegmentTree) else tree.range_sum(left, right)
            assert answer == sum(values[left:right + 1])


def test_range_tree_ascii_titles():
    assert len(texts.SEGMENT_TREE_ASCII.splitlines()) >= 9
    assert len(texts.FENWICK_TREE_ASCII.splitlines()) >= 9
