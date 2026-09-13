"""Shared helpers for PyDSA: screen clearing and the intro text."""

import os


def clear():
    """Clear the terminal screen."""
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # macOS and Linux (os.name is 'posix')
    else:
        os.system('clear')


def input_verify(condition, msg="item"):
    """Prompt for a value of the given type and return it, or None if the conversion fails.

    condition is "str", "int" or "float"; msg names the value in the prompt.
    """

    # String input only; used in the array implementation
    if condition == "str":
        item = input(f"\n✍️ Please enter the {msg}. (STRING)\n>>> ")
        return item

    # Integer input only; used in the array implementation
    elif condition == "int":
        item = input(f"\n✍️ Please enter the {msg}. (INT)\n>>> ")
        try:
            item = int(item)
        except ValueError:
            return None
        else:
            return item

    # Float input only; used in the array implementation
    elif condition == "float":
        item = input(f"\n✍️ Please enter the {msg}. (FLOAT)\n>>> ")
        try:
            item = float(item)
        except ValueError:
            return None
        else:
            return item


def order_verify():
    """Ask for a sorting order and return "asc" or "desc"."""
    while True:
        order = input("""\n🤔 Please specify the order.
•1) Ascending
•2) Descending
>>> """)
        if order not in ("1", "2"):
            print("\n🚫 Invalid code number.")
            continue
        if order == "1":
            return "asc"
        else:
            return "desc"


def main_intro():
    """Print the PyDSA banner, welcome message and version info."""
    print("""\n
.-------.  ____     __  ______        .-'''-.    ____     
\  _(`)_ \ \   \   /  /|    _ `''.   / _     \ .'  __ `.  
| (_ o._)|  \  _. /  ' | _ | ) _  \ (`' )/`--'/   '  \  \ 
|  (_,_) /   _( )_ .'  |( ''_'  ) |(_ o _).   |___|  /  | 
|   '-.-'___(_ o _)'   | . (_) `. | (_,_). '.    _.-`   | 
|   |   |   |(_,_)'    |(_    ._) '.---.  \  :.'   _    | 
|   |   |   `-'  /     |  (_.\.' / \    `-'  ||  _( )_  | 
/   )    \      /      |       .'   \       / \ (_ o _) / 
`---'     `-..-'       '-----'`      `-...-'   '.(_,_).'\n\n
""")

    print("💻 Welcome to PyDSA, a console-based Python app that strives to assist you in learning data structures! The app is designed to give you a good tour of the 4 major linear DSes, giving you an opportunity to wrap your head around their distinctions while on the go! All interaction with the app is based on typing the related number & letter codes in the terminal.\n")
    print("⏳ Version 1.0")
    print("""🌐 All the source code & future updates are available in this GitHub repo under MIT license:
   ★ https://github.com/masi-karimi/pydsa
""")
