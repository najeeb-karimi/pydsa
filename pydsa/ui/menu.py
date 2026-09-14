"""Numbered console menus and the navigation results their actions return."""

from enum import Enum, auto
from typing import Callable, NamedTuple

from pydsa.content import registry
from pydsa.ui import render
from pydsa.ui.console import BackRequested, ask_code, clear, info


class Nav(Enum):
    """Where to go once an action is done."""

    BACK = auto()  # Return to the previous menu
    NEW = auto()  # Start the current topic again from scratch
    HOME = auto()  # Return to the main menu
    EXIT = auto()  # Quit the program


class Option(NamedTuple):
    """A menu entry: its label, the action it runs, an optional fixed code and an optional role."""

    label: str
    action: Callable[[], object]
    code: str | None = None
    role: str | None = None  # "back" for the option that leaves this menu for the previous one


def back_option(label="Go Back"):
    """Return the 0 option that leaves a menu for the previous one."""
    return Option(label, lambda: Nav.BACK, "0", "back")


def exit_option():
    """Return the 0 option that quits the program."""
    return Option("Exit", lambda: Nav.EXIT, "0")


class Menu:
    """A title with numbered options, read from the console.

    groups is a list of option lists, shown with a blank line between them. Options can be Option or
    plain (label, action[, code]) tuples; those without a fixed code are numbered in order from 1. By
    convention, the 0 option is the menu's way out and comes last.

    The b shortcut picks the menu's Go Back option, or steps back with Nav.BACK when there is none; can_go_back
    turns that off (for the main menu). compact_repeat shows the options in compact columns, without the
    title, every time after the first.
    """

    def __init__(self, title, groups, *, can_go_back=True, compact_repeat=False):
        self.title = title
        self.groups = []
        self.options = {}
        self.can_go_back = can_go_back
        self.compact_repeat = compact_repeat
        self.shown = False
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
        """Show the menu, ask until a valid code or the back shortcut is typed, and return the chosen option."""
        groups = [[(option.code, option.label) for option in group] for group in self.groups]
        while True:
            try:
                code = ask_code(self.title, groups, compact=self.compact_repeat and self.shown)
            except BackRequested:
                back = self._back_option()
                if back is not None:
                    return back
                info("You're already at the main menu, so there's nowhere to go back to.")
                continue
            finally:
                self.shown = True
            return self.options[code]

    def _back_option(self):
        """Return the option the back shortcut picks, or None if this menu can't be left that way."""
        for option in self.options.values():
            if option.role == "back":
                return option
        return Option("Go Back", lambda: Nav.BACK, None, "back") if self.can_go_back else None

    def select(self):
        """Run the chosen option's action once and return its result, or None if the user cancelled it."""
        option = self.choose()
        try:
            return option.action()
        except BackRequested:
            info("Cancelled.")
            return None

    def open(self):
        """Run the chosen option's action and return its result.

        If the action opened a sub-menu that the user left with Go Back, or the user cancelled it, this menu
        is shown again. Only this menu's own back option passes Nav.BACK on to the caller.
        """
        while True:
            option = self.choose()
            try:
                result = option.action()
            except BackRequested:
                info("Cancelled.")
                continue
            if result is Nav.BACK and option.role != "back":
                continue
            return result

    def run(self):
        """Keep running chosen actions until one returns a Nav, and return that Nav."""
        while True:
            result = self.select()
            if isinstance(result, Nav):
                return result


def read_guide(guides):
    """Show one of guides (topic IDs); when there's more than one, let the user pick which."""
    if len(guides) == 1:
        render.guide(guides[0])
        return
    Menu("📖 Which guide do you want to read?", [
        [(registry.guide(guide).title, lambda guide=guide: render.guide(guide)) for guide in guides],
        [back_option()],
    ]).select()


def operation_menu(name, operations, *, guides, new_label):
    """Build the operation menu of a data structure or an algorithm screen.

    Read the Guide comes first, showing one of guides (topic IDs, the most specific first), followed by
    operations as (label, action) pairs. The last group holds the shared navigation: new_label (start this
    screen again), Main Menu and 0) Exit.
    """

    def start_again():
        clear()
        return Nav.NEW

    def go_home():
        clear()
        render.home()
        return Nav.HOME

    return Menu(
        f"⚔️ What do you want to do with the {name}?",
        [
            [("Read the Guide", lambda: read_guide(guides)), *operations],
            [(new_label, start_again), ("Main Menu", go_home), exit_option()],
        ],
        compact_repeat=True,
    )
