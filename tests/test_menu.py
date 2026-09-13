"""Menu rendering, invalid codes, shortcuts and navigation results."""

import pytest

from pydsa.ui.console import QuitRequested, ask
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu


def feed(monkeypatch, *answers):
    """Make input() return the given answers in order."""
    remaining = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))


def test_options_are_numbered_with_zero_last(monkeypatch, capsys):
    feed(monkeypatch, "2")
    menu = Menu("Title?", [[("One", lambda: 1), ("Two", lambda: 2)], [back_option()]])
    assert menu.select() == 2
    assert capsys.readouterr().out == "\nTitle?\n  1) One\n  2) Two\n\n  0) Go Back\nh help · b back · q quit\n"


def test_codes_are_right_aligned(capsys, monkeypatch):
    feed(monkeypatch, "10")
    menu = Menu("Pick:", [[(str(n), lambda n=n: n) for n in range(10)], [back_option()]])
    assert menu.select() == 9
    out = capsys.readouterr().out
    assert "   1) 0\n" in out
    assert "  10) 9\n" in out
    assert "   0) Go Back\n" in out


def test_invalid_codes_ask_again(monkeypatch, capsys):
    feed(monkeypatch, "9", "x", " 1 ")
    assert Menu("Pick:", [[("A", lambda: "a")]]).select() == "a"
    assert capsys.readouterr().out.count("🚫 Invalid choice. Please type one of the numbers shown, or h for help.") == 2


def test_open_shows_the_menu_again_when_a_sub_menu_goes_back(monkeypatch):
    visits = []

    def sub_menu():
        visits.append("sub")
        return Nav.BACK

    feed(monkeypatch, "1", "1", "2")
    menu = Menu("Pick:", [[("Sub-menu", sub_menu), ("Value", lambda: 42)], [back_option()]])
    assert menu.open() == 42
    assert visits == ["sub", "sub"]

    feed(monkeypatch, "0")
    assert menu.open() is Nav.BACK


def test_run_stops_at_the_first_nav(monkeypatch):
    calls = []
    feed(monkeypatch, "1", "1", "2")
    menu = Menu("Pick:", [[("Work", lambda: calls.append("work")), ("Leave", lambda: Nav.HOME)]])
    assert menu.run() is Nav.HOME
    assert calls == ["work", "work"]


def test_operation_menu_layout_and_navigation(monkeypatch, capsys):
    menu = operation_menu("thing", [("Poke", lambda: print("poked"))],
                          definition=lambda: print("defined"), new_label="New Thing")

    feed(monkeypatch, "1", "2", "0")
    assert menu.run() is Nav.EXIT
    out = capsys.readouterr().out
    assert "⚔️ What do you want to do with the thing?\n  1) Definition\n  2) Poke\n\n  3) New Thing\n  4) Main Menu\n  0) Exit\n" in out
    assert "defined\n" in out and "poked\n" in out
    # After the first time, the options are shown in compact columns without the title
    assert out.count("What do you want to do with the thing?") == 1
    assert out.count("h help · b back · q quit") == 3

    feed(monkeypatch, "3")
    assert menu.run() is Nav.NEW
    feed(monkeypatch, "4")
    assert menu.run() is Nav.HOME


def test_help_shortcut_shows_help_and_asks_again(monkeypatch, capsys):
    feed(monkeypatch, "h", "?", "1")
    assert Menu("Pick:", [[("A", lambda: "a")]]).select() == "a"
    out = capsys.readouterr().out
    assert out.count("❓ Help") == 2
    assert "You're at: Pick:" in out


def test_back_shortcut(monkeypatch, capsys):
    feed(monkeypatch, "b")
    assert Menu("Pick:", [[("A", lambda: "a")], [back_option("Leave")]]).select() is Nav.BACK

    # Without a Go Back option, b still steps back
    feed(monkeypatch, "b")
    assert Menu("Pick:", [[("A", lambda: "a")]]).run() is Nav.BACK

    # ...unless the menu can't be left that way, like the main menu
    feed(monkeypatch, "b", "1")
    assert Menu("Pick:", [[("A", lambda: "a")]], can_go_back=False).select() == "a"
    assert "You're already at the main menu" in capsys.readouterr().out


def test_quit_shortcuts(monkeypatch):
    feed(monkeypatch, "q")
    with pytest.raises(QuitRequested):
        Menu("Pick:", [[("A", lambda: "a")]]).select()
    feed(monkeypatch, ":Q")
    with pytest.raises(QuitRequested):
        ask("Name?")


def test_cancelling_at_a_prompt(monkeypatch, capsys):
    visits = []

    def ask_twice():
        visits.append("asked")
        return ask("Name?")

    # select and run report the cancellation and go back to the menu
    feed(monkeypatch, "1", ":b", "2")
    assert Menu("Pick:", [[("Ask", ask_twice), ("Leave", lambda: Nav.HOME)]]).run() is Nav.HOME
    assert "Cancelled." in capsys.readouterr().out

    # open shows its menu again
    feed(monkeypatch, "1", ":b", "1", "Ada")
    assert Menu("Pick:", [[("Ask", ask_twice)], [back_option()]]).open() == "Ada"
    assert visits == ["asked", "asked", "asked"]

    # :h shows help and asks the same question again
    feed(monkeypatch, ":h", "Ada")
    assert ask("Name?") == "Ada"
    assert "You're at: Name?" in capsys.readouterr().out
