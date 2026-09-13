"""PyDSA entry point: shows the intro and runs the data structure and algorithm category menus."""

from pydsa.ui import render
from pydsa.ui.menu import Menu, Nav, back_option, exit_option
from pydsa.ui.screens import (
    array, deque, disjoint_set, graph, graph_algorithms, hash_table, heap, linked_list, queue,
    searching_algorithms, sorting_algorithms, stack, tree, trie,
)

LINEAR = [("Array", array), ("Stack", stack), ("Queue", queue), ("Deque", deque), ("Linked List", linked_list)]
NON_LINEAR = [
    ("Tree", tree), ("Heap & Priority Queue", heap), ("Trie", trie),
    ("Graph", graph), ("Hash Table", hash_table), ("Disjoint Set", disjoint_set),
]
ALGORITHMS = [("Sorting", sorting_algorithms), ("Searching", searching_algorithms), ("Graph Algorithms", graph_algorithms)]


def open_screen(screen):
    """Run a data structure or algorithm screen, starting it again for as long as it returns Nav.NEW."""
    while True:
        nav = screen.run()
        if nav is not Nav.NEW:
            return nav


def pick_screen(title, screens):
    """Let the user open screens from one category; return Nav.EXIT if they quit the program."""
    menu = Menu(title, [
        [(name, lambda screen=screen: open_screen(screen)) for name, screen in screens],
        [back_option()],
    ])
    # Going back from a screen shows this category again; Go Back and the home option return home
    return Nav.EXIT if menu.open() is Nav.EXIT else None


def run():
    """Show the intro, then keep offering the categories until the user exits."""
    render.main_intro()
    Menu("📂 What do you want to learn?", [
        [("Linear data structures", lambda: pick_screen("🏁 Which linear data structure do you want to learn?", LINEAR)),
         ("Non-linear data structures", lambda: pick_screen("🧭 Which non-linear data structure do you want to learn?", NON_LINEAR)),
         ("Algorithms", lambda: pick_screen("🧮 Which algorithms do you want to learn?", ALGORITHMS))],
        [exit_option()],
    ]).run()
    render.goodbye()
