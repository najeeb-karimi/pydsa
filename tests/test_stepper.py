"""The step player: the Steps setting, the keys at a pause and what a run shows when nobody watches."""

import pytest

from pydsa import settings
from pydsa.algorithms import sorting
from pydsa.settings import Settings
from pydsa.ui import render, stepper
from pydsa.ui.console import QuitRequested


@pytest.fixture
def watching(monkeypatch):
    """Pretend PyDSA runs in a terminal, where the steps can be watched one at a time."""
    monkeypatch.setattr(stepper, "can_pause", lambda: True)


@pytest.fixture
def typed(monkeypatch):
    """Answer the step player's prompts with scripted answers."""

    def script(*answers):
        remaining = iter(answers)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))

    return script


def steps(count=4):
    """Return the steps of a small sorting run; a reversed list of count values needs count - 1 swaps or more."""
    return list(sorting.bubble_sort(list(range(count, 0, -1))))


def drawn():
    """Return a draw function that remembers the numbers of the steps it drew."""
    numbers = []
    return numbers, lambda number, event: numbers.append(number)


def test_a_scripted_run_never_pauses(capsys):
    numbers, draw = drawn()
    shown = []
    assert len(stepper.play(steps(), draw, shown.append)) == 6
    assert numbers == []  # No terminal, so the steps aren't walked through
    assert len(shown[0]) == 6
    capsys.readouterr()


def test_without_a_summary_the_steps_are_listed(capsys):
    numbers, draw = drawn()
    stepper.play(steps(3), draw)
    out = capsys.readouterr().out
    assert "1. 2 came after 3, so the two swapped places." in out
    assert "3. 1 came after 2, so the two swapped places." in out
    assert numbers == []


def test_an_empty_run_shows_nothing(capsys):
    assert stepper.play([], lambda number, event: None) == []
    assert capsys.readouterr().out == ""


def test_pause_walks_through_every_step(watching, typed, capsys):
    settings.current = Settings(steps="pause")
    numbers, draw = drawn()
    typed("", "", "", "", "")
    stepper.play(steps(), draw)
    assert numbers == [1, 2, 3, 4, 5, 6]
    assert "Step 1 of 6 · Enter: next · a: the rest · s: stop" in capsys.readouterr().out


def test_a_shows_the_rest_and_s_stops(watching, typed, capsys):
    settings.current = Settings(steps="pause")
    numbers, draw = drawn()
    typed("a")
    stepper.play(steps(), draw)
    assert numbers == [1, 2, 3, 4, 5, 6]

    numbers, draw = drawn()
    typed("s")
    stepper.play(steps(), draw)
    assert numbers == [1]
    assert "Stopped after 1 of 6 steps." in capsys.readouterr().out


def test_quitting_at_a_pause(watching, typed):
    settings.current = Settings(steps="pause")
    typed(":q")
    with pytest.raises(QuitRequested):
        stepper.play(steps(), lambda number, event: None)


def test_ask_asks_first_and_enter_shows_everything_at_once(watching, typed, capsys):
    settings.current = Settings(steps="ask")
    numbers, draw = drawn()
    typed("")  # Enter: don't watch
    shown = []
    stepper.play(steps(), draw, shown.append)
    assert numbers == [] and len(shown) == 1
    assert "👀 Watch it step by step?" in capsys.readouterr().out

    numbers, draw = drawn()
    typed("y", "a")
    stepper.play(steps(), draw, shown.append)
    assert numbers == [1, 2, 3, 4, 5, 6]


def test_cancelling_the_question_only_skips_the_steps(watching, typed, capsys):
    settings.current = Settings(steps="ask")
    numbers, draw = drawn()
    typed(":b")
    stepper.play(steps(), draw)
    assert numbers == []
    capsys.readouterr()


def test_all_never_asks(watching, typed):
    settings.current = Settings(steps="all")
    numbers, draw = drawn()
    typed()  # Any prompt would raise StopIteration
    shown = []
    stepper.play(steps(), draw, shown.append)
    assert numbers == [] and len(shown) == 1


def test_a_single_step_is_never_worth_a_question(watching, typed, capsys):
    settings.current = Settings(steps="pause")
    numbers, draw = drawn()
    typed()
    stepper.play(steps(2), draw)
    assert numbers == []
    assert "1. 1 came after 2, so the two swapped places." in capsys.readouterr().out


def test_a_long_run_offers_the_short_version(watching, typed, capsys):
    settings.current = Settings(steps="pause")
    many = steps(25)
    assert len(many) > stepper.MANY_STEPS
    numbers, draw = drawn()
    typed("")  # Enter: the short version
    shown = []
    stepper.play(many, draw, shown.append)
    out = capsys.readouterr().out
    assert f"This run takes {len(many)} steps, which is a lot to watch one at a time." in out
    assert f"👀 Watch all {len(many)} steps anyway?" in out
    assert numbers == [] and len(shown) == 1


def test_drawing_a_step_writes_its_caption_and_its_state(capsys):
    render.list_step(2, steps(3)[1])
    out = capsys.readouterr().out
    assert "Step 2: 1 came after 3, so the two swapped places." in out
    assert "List: [2, 1*, 3*]" in out
