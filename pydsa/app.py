"""PyDSA entry point: shows the intro and runs the data structure category menus."""

from pydsa.ui import render
from pydsa.ui.menu import Menu, Nav, back_option, exit_option
from pydsa.ui.screens import array, deque, disjoint_set, graph, hash_table, linked_list, queue, stack, tree

LINEAR = [("Array", array), ("Stack", stack), ("Queue", queue), ("Deque", deque), ("Linked List", linked_list)]
NON_LINEAR = [("Tree", tree), ("Graph", graph), ("Hash Table", hash_table), ("Disjoint Set", disjoint_set)]


def open_screen(screen):
    """Run a data structure screen, starting it again for as long as it returns Nav.NEW."""
    while True:
        nav = screen.run()
        if nav is not Nav.NEW:
            return nav


def pick_structure(title, screens):
    """Let the user open data structures from one category; return Nav.EXIT if they quit the program."""
    menu = Menu(title, [
        [(name, lambda screen=screen: open_screen(screen)) for name, screen in screens],
        [back_option()],
    ])
    # Going back from a data structure shows this category again; Go Back and New Data Structure return home
    return Nav.EXIT if menu.open() is Nav.EXIT else None


def run():
    """Show the intro, then keep offering the data structure categories until the user exits."""
    render.main_intro()
    Menu("📂 Which type of data structure do you want to learn?", [
        [("Linear data structures", lambda: pick_structure("🏁 Which linear data structure do you want to learn?", LINEAR)),
         ("Non-linear data structures", lambda: pick_structure("🧭 Which non-linear data structure do you want to learn?", NON_LINEAR))],
        [exit_option()],
    ]).run()
    render.goodbye()
