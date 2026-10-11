"""All Phase 6 menu paths, learning tools, size caps, playback and narrow output."""

import random

import pytest
from rich.cells import cell_len

from pydsa import progress, settings
from pydsa.algorithms import backtracking as core, dynamic_programming as dp
from pydsa.content import texts
from pydsa.practice import challenges, experiments
from pydsa.ui import render, stepper
from pydsa.ui.console import console
from pydsa.ui.screens import backtracking, dynamic_programming

CHILDREN = (*dynamic_programming.KINDS, *backtracking.KINDS)
TOPICS = ("dynamic-programming", *(kind.guide for kind in dynamic_programming.KINDS),
          "recursion-backtracking", *(kind.guide for kind in backtracking.KINDS))


def labels(kind):
    return (dynamic_programming.operations(kind, dynamic_programming.example(kind)) if kind in dynamic_programming.KINDS
            else backtracking.operations(kind, backtracking.example(kind)))


@pytest.mark.parametrize("kind", CHILDREN, ids=lambda k: k.guide)
def test_every_operation_guide_code_restart_and_home(play, kind):
    actions = labels(kind)
    script = ["2", "1", *(str(i) for i in range(2, len(actions) + 2))]
    code = len(actions) + 2
    for i in range(1, len(actions)):  # Display is deliberately not a code operation.
        script.extend((str(code), str(i)))
    script.extend((str(code + 1), "2", str(code + 2), "0"))
    out = play(*script, argv=["--topic", kind.guide])
    assert "Loaded the example inputs" in out and "Goodbye!" in out
    assert all(f"Pseudocode: {label}" in out for label, _ in actions[:-1])
    assert kind.guide in progress.current.visited
    if kind.guide == "fibonacci":
        assert "F(5) = 5" in out and "Fibonacci call tree" in out and "Fibonacci call counts" in out
        assert "Plain recursion" in out and "Memoization" in out
    elif kind.guide == "knapsack":
        assert "Best value: 11; chosen item indexes: [0, 3]." in out and "Take item" in out
    elif kind.guide == "longest-common-subsequence":
        assert "Common subsequence: 'BCBA'; length: 4." in out and "↖" in out and "rebuilt subsequence" in out
    elif kind.guide == "coin-change":
        assert "Fewest coins: 2; chosen coins: [3, 3]." in out and "Number of ways: 4" in out
    elif kind.guide == "tower-of-hanoi":
        assert "Total moves: 7 = 2^3 - 1." in out and "Move 7:" in out
    elif kind.guide == "permutations":
        assert "Permutations: 6" in out and "Permutation recursion tree" in out
    else:
        assert "Solutions: 2" in out and "Removed the queen" in out and "Rejected row" in out


@pytest.mark.parametrize("parent,choice", [("dynamic-programming", "1"), ("recursion-backtracking", "1")])
def test_parent_guide_cancel_child_and_restart(play, parent, choice):
    guide = "5" if parent == "dynamic-programming" else "4"
    out = play(guide, choice, "0", choice, "2", "8" if parent == "dynamic-programming" else "5", "2", "0",
               argv=["--topic", parent])
    assert out.count("Loaded the example inputs") == 2 and "Goodbye!" in out


@pytest.mark.parametrize("category,child", [("5", "4"), ("6", "3")])
def test_category_routes_to_new_screens(play, category, child):
    out = play("5", category, child, "2", "2", "0")
    assert "Loaded the example inputs" in out and "Goodbye!" in out


@pytest.mark.parametrize("kind", CHILDREN, ids=lambda k: k.guide)
def test_random_inputs_and_every_solver(play, kind):
    count = len(labels(kind))
    out = play("3", *(str(i) for i in range(2, count + 2)), "0", argv=["--topic", kind.guide])
    assert "Generated small random inputs" in out and "Goodbye!" in out


@pytest.mark.parametrize("kind", CHILDREN, ids=lambda k: k.guide)
@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError, ":b"])
def test_interrupted_typed_inputs(play, kind, interrupt):
    tail = ["0", "0"] if interrupt == ":b" else []
    out = play("1", interrupt, *tail, argv=["--topic", kind.guide])
    assert "Goodbye!" in out and "Traceback" not in out


@pytest.mark.parametrize("topic,data,answer", [
    ("fibonacci", ["0"], "F(0) = 0"),
    ("knapsack", ["", "", "0"], "Best value: 0; chosen item indexes: []."),
    ("longest-common-subsequence", ["", "abc"], "Common subsequence: ''; length: 0."),
    ("coin-change", ["2,4", "3"], "The target cannot be made"),
    ("tower-of-hanoi", ["0"], "Total moves: 0 = 2^0 - 1."),
    ("permutations", [""], "Permutations: 1"),
    ("permutations", ["1,1,2"], "Permutations: 6"),
    ("n-queens", ["2"], "Solutions: 0"),
    ("n-queens", ["0"], "Solutions: 1"),
])
def test_typed_edge_cases(play, topic, data, answer):
    out = play("1", *data, "2", "3" if topic == "coin-change" else "0", *( ["0"] if topic == "coin-change" else []), argv=["--topic", topic])
    assert answer in out and "Goodbye!" in out
    if topic == "coin-change":
        assert "Number of ways: 0" in out


@pytest.mark.parametrize("topic,cap", [("fibonacci", 16), ("tower-of-hanoi", 10), ("n-queens", 8)])
def test_integer_caps_and_recovery(play, topic, cap):
    out = play("1", "oops", "-1", str(cap + 1), "1", "2", "0", argv=["--topic", topic])
    assert "must be a whole number" in out and "must be at least 0" in out and f"must be at most {cap}" in out


def test_knapsack_rejects_invalid_weights_values_and_capacity(play):
    out = play("1", "0", "1.5", "1,2,3,4,5,6,7,8,9", "2,3", "7", "7,8", "31", "4", "2", "0",
               argv=["--topic", "knapsack"])
    assert "Use at most 8 whole numbers" in out and "same length" in out and "at most 30" in out
    assert "Best value: 8" in out


def test_lcs_length_cap_and_preserved_whitespace(play):
    out = play("1", "a" * 13, " a ", " a ", "2", "0", argv=["--topic", "longest-common-subsequence"])
    assert "Use at most 12 characters" in out and "Common subsequence: ' a '; length: 3." in out


def test_coin_deduplication_and_invalid_denominations(play):
    out = play("1", "1,0", "2,2,3", "4", "2", "3", "0", argv=["--topic", "coin-change"])
    assert "Use at most 6 whole numbers" in out and "Coins: [2, 3]" in out and "Number of ways: 1" in out


def test_permutation_size_cap(play):
    out = play("1", "1,2,3,4,5,6,7", "1,2", "2", "0", argv=["--topic", "permutations"])
    assert "Use at most 4 whole numbers" in out and "Permutations: 2" in out


@pytest.mark.parametrize("kind", CHILDREN, ids=lambda k: k.guide)
@pytest.mark.parametrize("width", [45, 90])
def test_guides_code_operations_and_paused_steps_fit_without_color(play, monkeypatch, kind, width):
    console.width = width
    monkeypatch.setattr(render, "ascii_art", lambda art: None)
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause", colors=False))
    count = len(labels(kind))
    out = play("2", "1", "2", "a", str(count + 2), "1", "0", argv=["--topic", kind.guide, "--no-color"])
    assert "Step 1:" in out and "\x1b[" not in out
    assert all(cell_len(line) <= width for line in out.splitlines())
    if kind.guide in ("knapsack", "longest-common-subsequence", "coin-change") and width == 45:
        assert "compact rows" in out


@pytest.mark.parametrize("kind", CHILDREN, ids=lambda k: k.guide)
def test_stop_playback_keeps_completed_answer(play, monkeypatch, kind):
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause"))
    out = play("2", "2", "s", "0", argv=["--topic", kind.guide])
    assert "Stopped after 1 of" in out and "Goodbye!" in out


@pytest.mark.parametrize("topic,code", list(zip(TOPICS, map(str, range(30, 39)))))
def test_quizzes_predictions_and_experiments(play, monkeypatch, topic, code):
    monkeypatch.setattr(random.Random, "shuffle", lambda self, items: None)
    challenge = challenges.make(topic, random.Random(9))
    monkeypatch.setattr(challenges, "make", lambda topic_id: challenge)
    out = play("8", "4", "5", code, "1", "a", "a", "a", "a", "a", "2", repr(challenge.answer),
               "3", "1", "2", "0", "0", "0", "0", "0", "0")
    assert "Quiz score: 5/5" in out and "Correct prediction" in out and "Ratio" in out
    assert progress.current.quizzes[topic].best == 100 and progress.current.challenges[topic] == 1


@pytest.mark.parametrize("kind", CHILDREN, ids=lambda k: k.guide)
def test_operation_menu_practice_route(play, kind):
    count = len(labels(kind))
    out = play("2", str(count + 5), "3", "1", "1", "0", "0", "0", argv=["--topic", kind.guide])
    assert "Ratio" in out and "Goodbye!" in out


@pytest.mark.parametrize("width", [45, 90])
def test_large_compact_states_and_unicode_controls_fit(width, capsys):
    console.width, console.no_color = width, True
    for function, args in ((dp.fibonacci_table, (16,)), (dp.knapsack, ([1] * 8, [2] * 8, 30)),
                           (dp.longest_common_subsequence, ("🦄é\t[red]\n\x1b", "é🦄\t[blue]")),
                           (dp.coin_change_ways, ([1, 2, 3, 4, 5, 6], 30))):
        trace = []
        function(*args, trace=trace)
        render.dp_step(len(trace), trace[-1])
    render.hanoi_pegs((tuple(range(10, 0, -1)), (), ()))
    render.queens_board(8, core.n_queens(8)[0], {(7, 3): "checked"})
    out = capsys.readouterr().out
    assert "compact rows" in out and "\\t" in out
    assert "\x1b[" not in out and all(cell_len(line) <= width for line in out.splitlines())


@pytest.mark.parametrize("width", [45, 90])
def test_lcs_rebuild_captions_escape_control_characters(width, capsys):
    console.width, console.no_color = width, True
    text = "\t\x1b[2J\n[red]"
    trace = []
    assert dp.longest_common_subsequence(text, text, trace).sequence == text
    for number, event in enumerate(trace, 1):
        if event.kind == "dp_lcs_rebuild":
            render.dp_step(number, event)
    out = capsys.readouterr().out
    assert "\\t" in out and "\\x1b" in out and "\\n" in out and "[red]" in out
    assert "\x1b" not in out and "\t" not in out
    assert all(cell_len(line) <= width for line in out.splitlines())


def test_work_growth_counts_actual_operations():
    by_id = {e.id: e for e in experiments.EXPERIMENTS}
    sizes = (4, 8, 12, 16)
    assert [r.work for r in experiments.measure(by_id["fibonacci-recursive"], sizes=sizes)] == [9, 67, 465, 3193]
    assert [r.work for r in experiments.measure(by_id["fibonacci-memoized"], sizes=sizes)] == [2 * n - 1 for n in sizes]
    assert [r.work for r in experiments.measure(by_id["fibonacci-table"], sizes=sizes)] == [n + 1 for n in sizes]
    for identifier in ("knapsack-cells", "lcs-cells", "coin-minimum", "coin-ways"):
        assert [r.work for r in experiments.measure(by_id[identifier], sizes=sizes)] == [n * n for n in sizes]
    assert [r.work for r in experiments.measure(by_id["hanoi-moves"], sizes=(2, 4, 6, 8))] == [3, 15, 63, 255]
    assert len(experiments.for_topic("dynamic-programming")) == 7
    assert len(experiments.for_topic("recursion-backtracking")) == 3


def test_flower_power_titles():
    for topic in TOPICS:
        art = getattr(texts, topic.replace("-", "_").upper() + "_ASCII")
        assert len(art.splitlines()) >= 9 and "(_ o _)" in art
