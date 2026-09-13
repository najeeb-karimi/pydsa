"""Menu rendering, invalid codes and navigation results."""

from pydsa.ui.menu import Menu, Nav, operation_menu


def feed(monkeypatch, *answers):
    """Make input() return the given answers in order."""
    remaining = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(remaining))


def test_prompt_layout():
    menu = Menu("\nTitle?", [[("One", None), ("Two", None)], [("Back", None, "0")]], spaced=True)
    assert menu.prompt() == "\nTitle?\n★1) One\n★2) Two\n\n★0) Back\n\n>>> "
    compact = Menu("\nPick:", [[("A", None), ("B", None)]], bullet="●")
    assert compact.prompt() == "\nPick:\n●1) A\n●2) B\n>>> "


def test_select_retries_until_a_valid_code(monkeypatch, capsys):
    feed(monkeypatch, "9", "x", "2")
    menu = Menu("\nPick:", [[("A", lambda: "a"), ("B", lambda: "b")]], invalid="\nnope")
    assert menu.select() == "b"
    assert capsys.readouterr().out == "\nnope\n\nnope\n"


def test_select_without_retry_gives_up(monkeypatch, capsys):
    feed(monkeypatch, "9")
    menu = Menu("\nPick:", [[("A", lambda: "a")]], invalid="\nnope")
    assert menu.select(retry=False) is None
    assert capsys.readouterr().out == "\nnope\n"


def test_run_stops_at_the_first_nav(monkeypatch):
    calls = []
    feed(monkeypatch, "1", "1", "2")
    menu = Menu("\nPick:", [[("Work", lambda: calls.append("work")), ("Leave", lambda: Nav.BACK)]])
    assert menu.run() is Nav.BACK
    assert calls == ["work", "work"]


def test_operation_menu_navigation_entries(monkeypatch, capsys):
    monkeypatch.setattr("os.system", lambda command: 0)
    menu = operation_menu("THING", "The definition.", [("Poke", lambda: print("poked"))], new_label="New Thing")
    assert "★0) Definition\n★1) Poke\n★2) New Thing\n★3) New Data Structure\n★4) Exiting the Program\n\n>>> " in menu.prompt()

    feed(monkeypatch, "0", "1", "4")
    assert menu.run() is Nav.EXIT
    assert capsys.readouterr().out == "The definition.\npoked\n"

    feed(monkeypatch, "2")
    assert menu.run() is Nav.NEW
    feed(monkeypatch, "3")
    assert menu.run() is Nav.HOME
