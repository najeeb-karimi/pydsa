"""New balanced tree menus, narrated operations, practice and narrow diagrams."""

import random

import pytest
from rich.cells import cell_len

from pydsa import progress, settings
from pydsa.content import narration, texts
from pydsa.core.b_tree import BTree
from pydsa.core.red_black_tree import RedBlackTree
from pydsa.practice import challenges, experiments
from pydsa.ui import render, stepper
from pydsa.ui.console import console


@pytest.mark.parametrize("topic", ["red-black-tree", "b-tree"])
def test_example_all_operations_code_restart_and_home(play, topic):
    out = play("2", "1", "2", "1", "60", "3", "1", "10", "3", "1", "999",
               "4", "1", "25", "4", "1", "999", "5", "1", "5", "2", "5", "3", "5", "4",
               "6", "7", "8", "1", "9", "2", "10", "0", argv=["--topic", topic])
    assert "What it is" in out and "Inserted 60." in out and "Deleted 10." in out
    assert "nothing was deleted" in out and "Found 25 in the tree." in out
    assert all(f"{name} traversal" in out for name in ("Inorder", "Preorder", "Postorder", "Level order"))
    assert "Pseudocode: Insert" in out and "def insert(self, key, trace=None):" in out
    assert "Tree stats" in out and "Goodbye!" in out
    assert topic in progress.current.visited


def test_b_tree_creation_degree_validation_and_word_keys(play):
    out = play("1", "2", "1", "11", "3", "2", "pear", "2", "apple", "2", "pear",
               "3", "pear", "4", "pear", "5", "1", "6", "0", argv=["--topic", "b-tree"])
    assert "minimum degree" in out and "Minimum degree t = 3" in out
    assert "Inorder traversal: 'apple', 'pear'" in out
    assert "Found 'pear' in the tree" in out and "Keys" in out and "Nodes" in out


@pytest.mark.parametrize("topic,answers", [
    ("red-black-tree", ("3", "1", "8", "0")),
    ("red-black-tree", ("3", "2", "8", "0")),
    ("b-tree", ("3", "1", "2", "8", "0")),
    ("b-tree", ("3", "2", "3", "8", "0")),
])
def test_random_create_flows(play, topic, answers):
    out = play(*answers, argv=["--topic", topic])
    assert "8 random keys" in out and "Goodbye!" in out


@pytest.mark.parametrize("topic", ["red-black-tree", "b-tree"])
@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError, ":b"])
def test_interrupted_creation_is_clean(play, topic, interrupt):
    answers = ("1", "1", interrupt, "0", "0") if interrupt == ":b" else ("1", "1", interrupt)
    # B-tree creation has a typed degree prompt; a Red-Black tree goes straight to its operation menu.
    if topic == "red-black-tree":
        answers = ("1", "1", "2", "1", interrupt, "0") if interrupt == ":b" else ("1", "1", "2", "1", interrupt)
    out = play(*answers, argv=["--topic", topic])
    assert "Traceback" not in out and "Goodbye!" in out


@pytest.mark.parametrize("topic", ["red-black-tree", "b-tree"])
def test_practice_quiz_prediction_and_experiment(play, monkeypatch, topic):
    monkeypatch.setattr(random.Random, "shuffle", lambda self, items: None)
    challenge = challenges.make(topic, random.Random(4))
    monkeypatch.setattr(challenges, "make", lambda topic_id: challenge)
    out = play("2", "11", "1", "a", "a", "a", "a", "a", "2", repr(challenge.answer),
               "3", "1", "2", "0", "0", "0", argv=["--topic", topic])
    assert "Quiz score: 5/5" in out and "Correct prediction" in out and "Ratio" in out
    assert progress.current.quizzes[topic].best == 100
    assert progress.current.challenges[topic] == 1


@pytest.mark.parametrize("topic", ["red-black-tree", "b-tree"])
@pytest.mark.parametrize("answer", ["a", "s"])
def test_paused_steps_show_states_and_can_skip(play, monkeypatch, topic, answer):
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause"))
    out = play("2", "2", "1", "60", answer, "0", argv=["--topic", topic])
    assert "Step 1:" in out and "Goodbye!" in out and "Inserted 60." in out
    assert "Stopped after" in out if answer == "s" else "Step 2:" in out


@pytest.mark.parametrize("width", [45, 90])
def test_all_new_views_fit_without_color(play, monkeypatch, capsys, width):
    console.width = width
    monkeypatch.setattr(render, "ascii_art", lambda art: None)
    out = play("2", "1", "2", "1", "60", "3", "1", "10", "4", "1", "50", "6", "8", "2", "0",
               argv=["--no-color", "--topic", "red-black-tree"])
    assert "(R)" in out and "(B)" in out and "\x1b[" not in out
    assert all(cell_len(line) <= width for line in out.splitlines())
    out = play("2", "1", "2", "1", "60", "3", "1", "10", "4", "1", "50", "6", "8", "2", "0",
               argv=["--no-color", "--topic", "b-tree"])
    assert "[" in out and " | " in out and all(cell_len(line) <= width for line in out.splitlines())
    tree = BTree(3, "str")
    for i in range(60):
        tree.insert(f"long-key-{i:03d}")
    render.b_tree(tree)
    out = capsys.readouterr().out
    assert "shown as an outline" in out and all(cell_len(line) <= width for line in out.splitlines())


def test_b_tree_diagram_has_all_children_and_equal_width_rows():
    tree = BTree(3)
    for i in range(36):
        tree.insert(i)
    children = lambda node: node.children
    label = lambda node: render.Text("[" + " | ".join(map(str, node.keys)) + "]")
    lines, _ = render._diagram(tree.root, children, label)
    assert len({cell_len(line.plain) for line in lines}) == 1
    assert all(str(i) in "\n".join(line.plain for line in lines) for i in range(36))
    assert len(tree.root.children) > 2


@pytest.mark.parametrize("keys,direction", [([30, 20, 10], "right"), ([10, 20, 30], "left"),
                                          ([30, 10, 20], "left"), ([10, 30, 20], "right")])
def test_red_black_rotation_sequences(keys, direction):
    tree, trace = RedBlackTree(), []
    for key in keys[:-1]:
        tree.insert(key)
    tree.insert(keys[-1], trace)
    rotations = [event for event in trace if event.kind == "rb_rotate"]
    assert rotations[0].data["direction"] == direction
    assert len(rotations) == (2 if keys[1] != 20 else 1)
    assert trace[-1].snapshot == (20, "B", (10, "R", None, None), (30, "R", None, None))
    assert all(narration.caption(event).endswith(".") for event in trace)


def test_new_experiments_keep_ordered_insertions_short():
    for topic in ("red-black-tree", "b-tree"):
        experiment, = experiments.for_topic(topic)
        for mode in experiments.MODES:
            rows = experiments.measure(experiment, mode, sizes=(16, 32, 64, 128), rng=random.Random(2))
            assert all(0 < row.work <= 2 * experiments.LOG(row.n) for row in rows)


def test_new_ascii_titles_are_present():
    assert len(texts.RED_BLACK_TREE_ASCII.splitlines()) >= 9
    assert len(texts.B_TREE_ASCII.splitlines()) >= 9
