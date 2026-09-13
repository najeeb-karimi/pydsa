"""Console input and output built on rich: prompts, status messages and screen clearing."""

from rich.console import Console
from rich.text import Text
from rich.theme import Theme

PROMPT = ">>> "

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
    }),
    highlight=False,
)


def clear():
    """Clear the terminal screen (does nothing when the output isn't a terminal)."""
    console.clear()


def plural(count, singular, plural_form=None):
    """Return the count with the right form of the noun, e.g. "1 item" or "3 items"."""
    word = singular if count == 1 else plural_form or f"{singular}s"
    return f"{count} {word}"


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


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

def ask(question):
    """Show question on its own line and return what the user types at the >>> prompt."""
    console.print()
    console.print(Text(question, style="title"))
    return input(PROMPT)


def ask_code(title, groups):
    """Show title with numbered options and ask until one of their codes is typed; return that code.

    groups is a list of (code, label) lists, shown with a blank line between them.
    """
    codes = [code for group in groups for code, _ in group]
    width = max(len(code) for code in codes)
    while True:
        console.print()
        console.print(Text(title, style="title"))
        for position, group in enumerate(groups):
            if position:
                console.print()
            for code, label in group:
                console.print(Text.assemble("  ", (f"{code:>{width}})", "code"), " ", label))
        choice = input(PROMPT).strip()
        if choice in codes:
            return choice
        error("Invalid choice. Please type one of the numbers shown.")


def ask_int(question, what, min_value=None):
    """Ask until a whole number of at least min_value is typed; what names the value in error messages."""
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
