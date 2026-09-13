"""PyDSA entry point: shows the intro and runs the data structure category menus."""

from pydsa.ui import render
from pydsa.ui.menu import Menu, Nav
from pydsa.ui.screens import array, graph, hash_table, linked_list, queue, stack, tree

LINEAR = [("Array", array), ("Stack", stack), ("Queue", queue), ("Linked List", linked_list)]
NON_LINEAR = [("Tree", tree), ("Graph", graph), ("Hash Table", hash_table)]


def open_screen(screen):
    """Run a data structure screen, starting it again for as long as it returns Nav.NEW."""
    while True:
        nav = screen.run()
        if nav is not Nav.NEW:
            return nav


def pick_structure(title, screens):
    """Let the user open a data structure from one category; return Nav.EXIT if they quit the program."""
    menu = Menu(
        title,
        [[(name, lambda screen=screen: open_screen(screen)) for name, screen in screens],
         [("Go Back", lambda: Nav.BACK, "0")]],
        spaced=True,
    )
    # Going back and New Data Structure both return to the category menu
    return Nav.EXIT if menu.select() is Nav.EXIT else None


def run():
    """Show the intro, then keep offering the data structure categories until the user exits."""
    render.main_intro()
    Menu(
        "\n📂 Which type of data structure do you want to learn?",
        [[("Linear data structures", lambda: pick_structure("\n🏁 Which Linear Data Structure do you want to learn?", LINEAR)),
          ("Non-linear data structures", lambda: pick_structure("\n🧭 Which Non-linear Data Structure do you want to learn?", NON_LINEAR))]],
        spaced=True,
    ).run()
