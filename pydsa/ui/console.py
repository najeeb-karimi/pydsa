"""Console input helpers: screen clearing and validated prompts."""

import os


def clear():
    """Clear the terminal screen."""
    # Windows
    if os.name == "nt":
        os.system("cls")
    # macOS and Linux (os.name is "posix")
    else:
        os.system("clear")


def value_prompt(msg, label):
    """Return the standard prompt for entering a value of the labeled type, e.g. "(INT)"."""
    return f"\n✍️ Please enter the {msg}. ({label})\n>>> "


def ask_choice(prompt, codes, invalid):
    """Ask with prompt until one of codes is entered and return it; invalid is printed otherwise."""
    while True:
        choice = input(prompt)
        if choice in codes:
            return choice
        print(invalid)


def ask_int(prompt, invalid, min_value=None, too_small=None):
    """Ask with prompt until a whole number of at least min_value is entered and return it.

    invalid is printed when the input isn't an int, and too_small (invalid by default) when it's
    below min_value.
    """
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print(invalid)
            continue
        if min_value is not None and value < min_value:
            print(invalid if too_small is None else too_small)
            continue
        return value


def _convert(text, data_type):
    """Return text converted to data_type, or None if it can't be converted."""
    try:
        return data_type(text)
    except ValueError:
        return None


def ask_value(kind="all", msg="item"):
    """Ask for a value and return it, or None if it can't be converted to the requested type.

    kind is "all" (the user picks str, int or float), "str", "num" (the user picks int or float),
    "int" or "float"; msg names the value in the prompts.
    """
    # Any of str, int or float, picked by the user
    if kind == "all":
        choice = ask_choice(
            f"""\n🤔 Please specify the data type of the {msg}:
•1) str
•2) int
•3) float
>>> """,
            ("1", "2", "3"),
            "\n🚫 Invalid code number! Please use code numbers 1–3.",
        )
        text = input(f"\n✍️ Please enter the {msg}.\n>>> ")
        return _convert(text, {"1": str, "2": int, "3": float}[choice])

    # String input only
    if kind == "str":
        return input(value_prompt(msg, "STRING"))

    # Numeric input only, with int or float picked by the user
    if kind == "num":
        choice = ask_choice(
            """\n🤔 Please specify the type of NUMERAL data you want to enter:
•1) int
•2) float
>>> """,
            ("1", "2"),
            "\n🚫 Invalid code number! Please use code numbers 1 or 2.",
        )
        kind = "int" if choice == "1" else "float"

    if kind == "int":
        return _convert(input(value_prompt(msg, "INT")), int)
    if kind == "float":
        return _convert(input(value_prompt(msg, "FLOAT")), float)
    raise ValueError(f"Unknown value kind: {kind}")


def ask_item():
    """Ask for a stack or queue item; numeric input can be kept as an int or turned into a str."""
    item = input("\n✍️ Please write the item.\n>>> ")
    try:
        number = int(item)
    except ValueError:
        return item
    choice = input("\n🤔 Do you want to add the item as an int or str? Type 1 for int or anything else for str.\n>>> ")
    return number if choice == "1" else str(number)


def ask_order():
    """Ask for a sorting order and return "asc" or "desc"."""
    order = ask_choice(
        """\n🤔 Please specify the order.
•1) Ascending
•2) Descending
>>> """,
        ("1", "2"),
        "\n🚫 Invalid code number.",
    )
    return "asc" if order == "1" else "desc"
