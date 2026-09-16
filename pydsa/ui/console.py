"""Console input and output built on rich: prompts, shortcuts, help, status messages and screen clearing."""

import sys

from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.segment import SegmentLines
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from pydsa import settings

PROMPT = ">>> "
MENU_HINT = "h help · b back · q quit"

# Writes to whatever sys.stdout is at the time. Colors are dropped automatically when the output
# isn't a terminal or NO_COLOR is set.
console = Console(
    theme=Theme({
        "title": "bold",
        "code": "bold cyan",
        "accent": "magenta",
        "muted": "dim",
        "result": "bold",
        "success": "green",
        "error": "red",
        "warning": "yellow",
        "info": "cyan",
        "changed": "bold reverse",
        "markdown.code": "bold cyan",
    }),
    highlight=False,
)

_ENV_NO_COLOR = console.no_color  # Set when the NO_COLOR environment variable asks for plain output
_flag_no_color = False  # Set by the --no-color option


class QuitRequested(Exception):
    """The user typed the quit shortcut."""


class BackRequested(Exception):
    """The user typed the back shortcut at a prompt, cancelling what they were doing."""


def clear():
    """Clear the terminal when the Clear the Screen setting is on (does nothing when the output isn't a terminal)."""
    if settings.current.clear_screen:
        console.clear()


def colors_forced_off():
    """Return True if NO_COLOR or --no-color keeps colors off, whatever the Colors setting says."""
    return _ENV_NO_COLOR or _flag_no_color


def force_colors_off(off):
    """Keep colors off for this run (the --no-color option), or stop doing so."""
    global _flag_no_color
    _flag_no_color = off
    apply_colors()


def apply_colors():
    """Turn colors on or off to match the Colors setting, unless they're forced off."""
    console.no_color = colors_forced_off() or not settings.current.colors


def plural(count, singular, plural_form=None):
    """Return the count with the right form of the noun, e.g. "1 item" or "3 items"."""
    word = singular if count == 1 else plural_form or f"{singular}s"
    return f"{count} {word}"


def yes_no(value):
    """Return "Yes" or "No" for a boolean answer."""
    return "Yes" if value else "No"


# ---------------------------------------------------------------------------
# Status messages
# ---------------------------------------------------------------------------

def _message(emoji, text, style):
    console.print()
    console.print(Text(f"{emoji} {text}", style=style))


def success(text):
    """Report an operation that worked."""
    _message("✅", text, "success")


def error(text):
    """Report invalid input or an operation that was rejected."""
    _message("🚫", text, "error")


def not_found(text):
    """Report something that was looked for but isn't there."""
    _message("❌", text, "warning")


def info(text):
    """Show a note or tip."""
    _message("ℹ️", text, "info")


def result(text):
    """Show the answer to a question such as a size check or a traversal."""
    _message("👉", text, "result")


def show_help(location):
    """Show the shortcuts and where the user is (location is the menu title or question on screen)."""
    shortcuts = Table(box=None, header_style="muted", padding=(0, 2))
    shortcuts.add_column("In a menu", style="code", no_wrap=True)
    shortcuts.add_column("Typing a value", style="code", no_wrap=True)
    shortcuts.add_column("What it does")
    shortcuts.add_row("h or ?", ":h", "Show this help")
    shortcuts.add_row("b", ":b", "Go back to the previous menu, cancelling what you were typing")
    shortcuts.add_row("q", ":q", "Quit PyDSA")
    body = Group(
        Text("Type the number of an option and press Enter. These shortcuts work everywhere:"),
        Text(),
        shortcuts,
        Text(),
        Text.assemble(("You're at: ", "muted"), location),
        Text("Choose Read the Guide in a topic's menu to read its guide, and Show the Code to see how an operation "
             "is written. On the main menu, Learning Tools has an overview and a glossary, and Settings changes how "
             "PyDSA behaves.", style="muted"),
    )
    console.print()
    console.print(Panel(body, title="❓ Help", title_align="left", border_style="info", padding=(0, 1)))


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

def ask(question):
    """Show question and return what the user types at the >>> prompt.

    :h shows help and asks again, :b raises BackRequested and :q raises QuitRequested.
    """
    while True:
        console.print()
        console.print(Text(question, style="title"))
        text = input(PROMPT)
        command = text.strip().lower()
        if command in (":h", ":?"):
            show_help(question)
            continue
        if command == ":b":
            raise BackRequested
        if command == ":q":
            raise QuitRequested
        return text


def _print_menu(title, groups, compact):
    """Print a menu: the title with one option per line, or (compact) just the options in columns."""
    codes = [code for group in groups for code, _ in group]
    width = max(len(code) for code in codes)
    console.print()
    if compact:
        options = [Text.assemble((f"{code})", "code"), " ", label) for group in groups for code, label in group]
        console.print(Columns(options, padding=(0, 4), column_first=True))
    else:
        console.print(Text(title, style="title"))
        for position, group in enumerate(groups):
            if position:
                console.print()
            for code, label in group:
                console.print(Text.assemble("  ", (f"{code:>{width}})", "code"), " ", label))
    console.print(Text(MENU_HINT, style="muted"))


def ask_code(title, groups, compact=False):
    """Show title with numbered options and ask until one of their codes is typed; return that code.

    groups is a list of (code, label) lists, shown with a blank line between them; compact shows only the
    options, in columns. h or ? shows help, b raises BackRequested and q raises QuitRequested.
    """
    codes = [code for group in groups for code, _ in group]
    while True:
        _print_menu(title, groups, compact)
        choice = input(PROMPT).strip()
        if choice in codes:
            return choice
        command = choice.lower()
        if command in ("h", "?"):
            show_help(title)
        elif command == "b":
            raise BackRequested
        elif command == "q":
            raise QuitRequested
        else:
            error("Invalid choice. Please type one of the numbers shown, or h for help.")


def ask_int(question, what, min_value=None, max_value=None):
    """Ask until a whole number between min_value and max_value is typed; what names the value in error messages."""
    while True:
        text = ask(question)
        try:
            value = int(text)
        except ValueError:
            error(f"The {what} must be a whole number.")
            continue
        if min_value is not None and value < min_value:
            error(f"The {what} must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            error(f"The {what} must be at most {max_value}.")
            continue
        return value


TYPES = {"str": str, "int": int, "float": float}


def ask_value(kind="any", what="item"):
    """Ask for a value of the given kind, asking again until the typed text converts to it.

    kind is "any" (the user picks str, int or float), "num" (the user picks int or float), "str",
    "int" or "float"; what names the value in the prompts.
    """
    if kind in ("any", "num"):
        names = ["str", "int", "float"] if kind == "any" else ["int", "float"]
        code = ask_code(f"🤔 Which data type is the {what}?", [[(str(i), name) for i, name in enumerate(names, start=1)]])
        kind = names[int(code) - 1]
    convert = TYPES[kind]
    while True:
        text = ask(f"✍️ Enter the {what} ({kind}):")
        try:
            return convert(text)
        except ValueError:
            error(f"{text!r} isn't a valid {kind}. Please try again.")


def ask_list(question, kind, what="keys"):
    """Ask for comma-separated values until every one of them is valid; return them as a list.

    kind is "num" (each value becomes an int, or a float if it has a decimal point) or "str" (each value is
    kept as typed, without the spaces around it); what names the values in error messages.
    """
    while True:
        parts = [part.strip() for part in ask(question).split(",")]
        if not all(parts):
            error(f"Some of the {what} are empty. Put a value between every two commas.")
            continue
        if kind == "str":
            return parts
        try:
            return [_number(part) for part in parts]
        except ValueError as problem:
            error(f"{problem.args[0]!r} isn't a valid number. Please try again.")


def _number(text):
    """Convert text to an int, or to a float if it isn't a whole number; raise ValueError(text) otherwise."""
    for convert in (int, float):
        try:
            return convert(text)
        except ValueError:
            pass
    raise ValueError(text)


def ask_item():
    """Ask for a stack or queue item; a whole number can be kept as an int or stored as a str."""
    text = ask("✍️ Enter the item:")
    try:
        number = int(text)
    except ValueError:
        return text
    code = ask_code(f"🤔 Should {text} be stored as an int or a str?", [[("1", "int"), ("2", "str")]])
    return number if code == "1" else text


def ask_order():
    """Ask for a sorting order and return "asc" or "desc"."""
    code = ask_code("↕️ Which order do you want?", [[("1", "Ascending"), ("2", "Descending")]])
    return "asc" if code == "1" else "desc"


# ---------------------------------------------------------------------------
# Paging
# ---------------------------------------------------------------------------

def page_height():
    """Return the terminal's height when long output should pause between screenfuls, or None when it shouldn't.

    Output that isn't a terminal and input that isn't typed live, such as a piped script, never pause.
    """
    if console.is_terminal and sys.stdin.isatty():
        return console.size.height
    return None


def page(renderable):
    """Print a blank line and renderable, pausing after every screenful when it's taller than the terminal.

    At a pause, Enter shows the next screenful, a shows the rest and s stops; :q quits PyDSA.
    """
    console.print()
    height = page_height()
    lines = console.render_lines(renderable, console.options, pad=False) if height else []
    if height is None or len(lines) < height:
        console.print(renderable)
        return

    size = max(height - 3, 5)  # Leave room for the hint, which can wrap, and the prompt
    shown = 0
    while True:
        chunk = lines[shown:shown + size]
        console.print(SegmentLines(chunk, new_lines=True), end="")
        shown += len(chunk)
        if shown >= len(lines):
            return
        console.print(Text(f"{shown} of {len(lines)} lines · Enter: more · a: all · s: stop", style="muted"))
        answer = input(PROMPT).strip().lower()
        if answer == ":q":
            raise QuitRequested
        if answer in ("s", "q", "b", ":b"):
            return
        if answer == "a":
            size = len(lines)
