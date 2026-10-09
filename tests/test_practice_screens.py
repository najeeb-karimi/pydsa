"""End-to-end practice navigation, persistence, cancellation and screen widths."""

import random

import pytest
from rich.cells import cell_len

from pydsa import progress
from pydsa.practice import challenges
from pydsa.ui import render
from pydsa.ui.console import console
from pydsa.ui.menu import operation_menu
from pydsa.ui.screens import practice


@pytest.fixture
def ordered_choices(monkeypatch):
    monkeypatch.setattr(random.Random, "shuffle", lambda self, values: None)


def test_topic_quiz_saves_and_returns_to_operations(play, ordered_choices):
    out = play("2", "12", "1", "a", "a", "a", "a", "a", "0", "0", argv=["--topic", "stack"])
    assert "Practice: Stack" in out and "Quiz score: 5/5 (100%)" in out
    assert progress.load()[0].quizzes["stack"] == progress.QuizScore(100, 1)
    assert "Goodbye!" in out


def test_wrong_quiz_answers_can_be_retried(play, ordered_choices):
    out = play("2", "12", "1", "b", "a", "a", "a", "a", "1", "a", "0", "0",
               argv=["--topic", "stack"])
    assert "The correct answer is:" in out and "Quiz score: 4/5 (80%)" in out
    assert "Retry score: 1/1" in out
    assert progress.load()[0].quizzes["stack"] == progress.QuizScore(80, 1)


def test_prediction_uses_fresh_data_and_keeps_live_stack(play, monkeypatch):
    challenge = challenges.make("stack", random.Random(3))
    monkeypatch.setattr(challenges, "make", lambda topic: challenge)
    out = play("2", "12", "2", repr(challenge.answer), "0", "3", "0", argv=["--topic", "stack"])
    assert "Correct prediction." in out
    assert "Popped 'Messi' from the top." in out
    assert progress.load()[0].challenges == {"stack": 1}


def test_incorrect_and_cancelled_predictions_are_not_counted(play):
    out = play("2", "12", "2", "wrong", "2", ":b", "0", "0", argv=["--topic", "stack"])
    assert "The result is" in out and "Cancelled." in out
    assert not progress.current.challenges


def test_new_user_practice_and_experiment_navigation(play):
    out = play("8", "1", "2", "3", "1", "2", "0", "5", "0", "0")
    assert out.count("Visit a topic first") == 2
    assert "Ratio" in out and "Milliseconds" in out and "best completed first-round score" in out
    assert "bubble-sort" in progress.current.visited


def test_practice_browser_quiz_and_mixed_session(play, ordered_choices):
    out = play("8", "4", "1", "2", "1", "a", "a", "a", "a", "a", "0", "0", "0", "0", "0")
    assert "Quiz score: 5/5" in out and "✓ Stack" in out
    progress.visit("queue")
    out = play("8", "1", *("a" for _ in range(10)), "0", "0")
    assert "Quiz score: 10/10" in out
    assert set(progress.current.quizzes) == {"stack", "queue"}
    assert progress.current.quizzes["stack"].attempts == 2


def test_mixed_prediction_only_uses_visited_topics(monkeypatch):
    progress.visit("queue")
    seen = []
    monkeypatch.setattr(practice, "prediction", seen.append)
    practice.mixed_prediction()
    assert seen == ["queue"]


def test_mixed_quiz_does_not_repeat_shared_foundation_questions(monkeypatch):
    progress.visit("bst")
    progress.visit("avl-tree")
    selected = []
    monkeypatch.setattr(practice.quiz, "run", lambda questions, rng: selected.extend(questions))
    practice.mixed_quiz()
    assert len({question.prompt for question in selected}) == len(selected)
    assert {question.topic for question in selected} <= progress.current.visited.keys()


def test_visited_labels_refresh_when_returning_to_topic_list(play):
    out = play("1", "2", "0", "0", "0")
    assert "2) ✓ Stack" in out


def test_reset_progress_requires_confirmation(play):
    progress.visit("stack")
    progress.record_quiz("stack", 4, 5)
    out = play("7", "7", "0", "0", "0")
    assert "stack" in progress.current.visited and "Reset your progress." not in out
    out = play("7", "7", "1", "0", "0")
    assert "Reset your progress." in out
    assert progress.load()[0] == progress.Progress()


@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError])
def test_interrupted_quiz_exits_cleanly_without_a_score(play, interrupt):
    out = play("2", "12", "1", interrupt, argv=["--topic", "stack"])
    assert "Goodbye!" in out and not progress.current.quizzes


def test_quiz_back_and_quit_shortcuts(play):
    assert "Cancelled." in play("2", "12", "1", ":b", "0", "0", argv=["--topic", "stack"])
    assert "Goodbye!" in play("2", "12", "1", "q", argv=["--topic", "stack"])


def test_invalid_quiz_letter_and_help(play, ordered_choices):
    out = play("2", "12", "1", "x", "h", "a", "a", "a", "a", "a", "0", "0",
               argv=["--topic", "stack"])
    assert "Invalid choice." in out and "❓ Help" in out and "Quiz score: 5/5" in out


def test_every_operation_menu_has_topic_practice():
    from tests.test_notes import menus
    for topic_id, operations in menus():
        menu = operation_menu("structure", topic_id, operations, new_label="New Structure")
        assert sum(option.label == "Practice" for option in menu.options.values()) == 1


@pytest.mark.parametrize("width", [45, 90])
def test_practice_screens_fit_narrow_terminals(play, monkeypatch, capsys, width, ordered_choices):
    console.width = width
    monkeypatch.setattr(render, "ascii_art", lambda art: None)
    out = play("8", "4", "1", "2", "1", "a", "a", "a", "a", "a", "0", "0", "0", "5", "0", "0",
               argv=["--no-color"])
    assert all(cell_len(line) <= width for line in out.splitlines()), [(cell_len(line), line) for line in out.splitlines() if cell_len(line) > width]


def test_progress_survives_new_app_sessions(play, ordered_choices):
    play("2", "12", "1", "a", "a", "a", "a", "a", "0", "0", argv=["--topic", "stack"])
    progress.current = progress.Progress()
    out = play("0")
    assert "1 of 49 topics visited" in out and "quiz average 100%" in out
