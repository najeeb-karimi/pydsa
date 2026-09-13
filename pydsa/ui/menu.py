"""Numbered console menus and the navigation results their actions return."""

from enum import Enum, auto
from typing import Callable, NamedTuple

from pydsa.ui import render
from pydsa.ui.console import ask_code, clear


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


def back_option(label="Go Back"):
    """Return the 0 option that leaves a menu for the previous one."""
    return Option(label, lambda: Nav.BACK, "0")


def exit_option():
    """Return the 0 option that quits the program."""
    return Option("Exit", lambda: Nav.EXIT, "0")


class Menu:
    """A title with numbered options, read from the console.

    groups is a list of option lists, shown with a blank line between them. Options can be Option or
    plain (label, action[, code]) tuples; those without a fixed code are numbered in order from 1. By
    convention, the 0 option is the menu's way out and comes last.
    """

    def __init__(self, title, groups):
        self.title = title
        self.groups = []
        self.options = {}
        next_code = 1
        for group in groups:
            entries = []
            for entry in group:
                option = Option(*entry)
                if option.code is None:
                    option = option._replace(code=str(next_code))
                    next_code += 1
                entries.append(option)
                self.options[option.code] = option
            self.groups.append(entries)

    def choose(self):
        """Show the menu, ask until a valid code is typed and return the chosen option."""
        code = ask_code(self.title, [[(option.code, option.label) for option in group] for group in self.groups])
        return self.options[code]

    def select(self):
        """Run the chosen option's action once and return its result."""
        return self.choose().action()

    def open(self):
        """Run the chosen option's action and return its result.

        If the action opened a sub-menu that the user left with Go Back, this menu is shown again. Only
        this menu's own 0 option passes Nav.BACK on to the caller.
        """
        while True:
            option = self.choose()
            result = option.action()
            if result is Nav.BACK and option.code != "0":
                continue
            return result

    def run(self):
        """Keep running chosen actions until one returns a Nav, and return that Nav."""
        while True:
            result = self.select()
            if isinstance(result, Nav):
                return result


def operation_menu(name, operations, *, definition, new_label, home_label="New Data Structure"):
    """Build the operation menu of a data structure or an algorithm screen.

    Definition comes first, followed by operations as (label, action) pairs. The last group holds the
    shared navigation: new_label (start this screen again), home_label (back to the categories) and 0) Exit.
    """

    def start_again():
        clear()
        return Nav.NEW

    def go_home():
        clear()
        render.main_intro()
        return Nav.HOME

    return Menu(
        f"⚔️ What do you want to do with the {name}?",
        [
            [("Definition", definition), *operations],
            [(new_label, start_again), (home_label, go_home), exit_option()],
        ],
    )
