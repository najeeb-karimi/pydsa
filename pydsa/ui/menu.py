"""Numbered console menus and the navigation results their actions return."""

from enum import Enum, auto
from typing import Callable, NamedTuple

from pydsa.ui import render
from pydsa.ui.console import clear


class Nav(Enum):
    """Where to go once an action is done."""

    BACK = auto()  # Return to the previous menu
    NEW = auto()  # Start the current data structure again from scratch
    HOME = auto()  # Return to the data structure categories
    EXIT = auto()  # Quit the program


class Option(NamedTuple):
    """A menu entry: its label, the action it runs and an optional fixed code."""

    label: str
    action: Callable[[], object]
    code: str | None = None


class Menu:
    """A title followed by numbered options, read from the console.

    groups is a list of option lists, separated by a blank line when shown. Options can be given as
    Option or plain (label, action[, code]) tuples; those without a fixed code are numbered in order
    from start. spaced adds a blank line before the >>> prompt.
    """

    def __init__(self, title, groups, *, bullet="★", start=1, spaced=False, invalid="\n❌ Invalid code number!"):
        self.title = title
        self.bullet = bullet
        self.spaced = spaced
        self.invalid = invalid
        self.groups = []
        self.options = {}
        next_code = start
        for group in groups:
            entries = []
            for entry in group:
                option = Option(*entry)
                code = option.code
                if code is None:
                    code = str(next_code)
                    next_code += 1
                entries.append((code, option))
                self.options[code] = option
            self.groups.append(entries)

    def prompt(self):
        """Return the menu text, ending with the >>> prompt."""
        body = "\n\n".join(
            "\n".join(f"{self.bullet}{code}) {option.label}" for code, option in group)
            for group in self.groups
        )
        gap = "\n\n" if self.spaced else "\n"
        return f"{self.title}\n{body}{gap}>>> "

    def select(self, retry=True):
        """Ask for a code, run the chosen option's action and return its result.

        An invalid code prints the invalid message, then asks again, or returns None if retry is False.
        """
        while True:
            code = input(self.prompt())
            if code in self.options:
                return self.options[code].action()
            print(self.invalid)
            if not retry:
                return None

    def run(self):
        """Keep selecting options until an action returns a Nav, and return that Nav."""
        while True:
            result = self.select()
            if isinstance(result, Nav):
                return result


def operation_menu(name, definition, operations, *, new_label, new_intro=True,
                   exit_label="Exiting the Program", invalid="\n🚫 Invalid operation code!"):
    """Build the operation menu of a data structure.

    The menu starts with Definition (code 0, printing definition), then lists operations as
    (label, action) pairs, and ends with the shared navigation entries: new_label (start this data
    structure again, showing the main intro first if new_intro is True), New Data Structure and
    exit_label.
    """

    def start_again():
        clear()
        if new_intro:
            render.main_intro()
        return Nav.NEW

    def go_home():
        clear()
        render.main_intro()
        return Nav.HOME

    options = [
        ("Definition", lambda: print(definition)),
        *operations,
        (new_label, start_again),
        ("New Data Structure", go_home),
        (exit_label, lambda: Nav.EXIT),
    ]
    return Menu(f"\n⚔️ Which operation do you want to perform with the {name}?", [options],
                start=0, spaced=True, invalid=invalid)
