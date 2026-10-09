"""Saved learning records, corrupt files, resets and writes isolated under tmp_path."""

import json

import pytest

from pydsa import progress, settings


def test_progress_round_trips_and_keeps_best_scores(tmp_path):
    assert progress.path().is_relative_to(tmp_path)
    assert progress.load() == (progress.Progress(), None)
    assert progress.visit("avl-tree") is None
    assert {"avl-tree", "tree"} <= progress.current.visited.keys()
    timestamp = progress.current.visited["avl-tree"]
    assert progress.visit("avl-tree") is None
    assert progress.current.visited["avl-tree"] >= timestamp
    progress.record_quiz("avl-tree", 4, 5)
    progress.record_quiz("avl-tree", 1, 5)
    progress.record_challenge("avl-tree")
    loaded, notice = progress.load()
    assert notice is None and loaded == progress.current
    assert loaded.quizzes["avl-tree"] == progress.QuizScore(80, 2)
    assert loaded.challenges["avl-tree"] == 1
    assert "quiz average 80%" in progress.summary()
    assert not progress.path().with_suffix(".tmp").exists()


@pytest.mark.parametrize("text", ["{", "[]", "null", '{"version": 999}', '{"version": true}',
                                 '{"version": 1, "visited": []}',
                                 '{"version": 1, "visited": {"stack": "yesterday"}}',
                                 '{"version": 1, "quizzes": {"stack": {"best": 101, "attempts": 1}}}',
                                 '{"version": 1, "quizzes": {"stack": {"best": NaN, "attempts": 1}}}',
                                 '{"version": 1, "challenges": {"stack": -1}}'])
def test_corrupt_progress_is_ignored(text):
    progress.path().parent.mkdir(parents=True)
    progress.path().write_text(text, encoding="utf-8")
    loaded, notice = progress.load()
    assert loaded == progress.Progress() and notice


def test_valid_records_survive_invalid_and_unknown_records():
    progress.path().parent.mkdir(parents=True)
    data = {"version": 1, "quizzes": {"stack": {"best": 60, "attempts": 2},
                                      "queue": {"best": 50, "attempts": True}},
            "challenges": {"stack": 3, "future-topic": 9}}
    progress.path().write_text(json.dumps(data), encoding="utf-8")
    loaded, notice = progress.load()
    assert notice
    assert loaded.quizzes == {"stack": progress.QuizScore(60, 2)}
    assert loaded.challenges == {"stack": 3}


def test_save_failure_keeps_session_progress(monkeypatch, tmp_path):
    blocker = tmp_path / "file"
    blocker.write_text("not a directory", encoding="utf-8")
    monkeypatch.setenv("PYDSA_HOME", str(blocker))
    assert progress.visit("stack")
    assert "stack" in progress.current.visited
    assert progress.record_quiz("stack", 2, 5)
    assert progress.current.quizzes["stack"].best == 40


def test_failed_replacement_preserves_previous_file(monkeypatch):
    progress.visit("stack")
    before = progress.path().read_bytes()
    monkeypatch.setattr(type(progress.path()), "replace", lambda *args: (_ for _ in ()).throw(OSError()))
    assert progress.record_challenge("stack")
    assert progress.path().read_bytes() == before


def test_reset_leaves_settings_alone():
    settings.save(settings.Settings(detail="detailed"))
    before = settings.path().read_bytes()
    progress.visit("stack")
    progress.record_quiz("stack", 5, 5)
    assert progress.reset() is None
    assert progress.load() == (progress.Progress(), None)
    assert settings.path().read_bytes() == before


@pytest.mark.parametrize("correct,total", [(-1, 5), (6, 5), (0, 0), (True, 5), (1, 2.5)])
def test_invalid_quiz_scores_are_refused(correct, total):
    with pytest.raises(ValueError):
        progress.record_quiz("stack", correct, total)
