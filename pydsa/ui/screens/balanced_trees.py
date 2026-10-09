"""Balanced tree screens, sharing create flows, operations and traversal menus."""

from typing import Callable, NamedTuple

from pydsa.content import texts
from pydsa.core.b_tree import BTree
from pydsa.core.errors import InvalidTypeError, NotFoundError
from pydsa.core.red_black_tree import RedBlackTree
from pydsa.ui import random_data, render, stepper
from pydsa.ui.console import ask_int, error, not_found, plural, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.screens import tree as tree_screen


class TreeKind(NamedTuple):
    guide: str
    name: str
    tree_class: type
    draw: Callable
    draw_step: Callable


RED_BLACK = TreeKind("red-black-tree", "Red-Black tree", RedBlackTree, render.red_black_tree, render.red_black_step)
B_TREE = TreeKind("b-tree", "B-tree", BTree, render.b_tree, render.b_tree_step)
EXAMPLE_KEYS = (10, 20, 30, 15, 25, 5, 1, 7, 40, 50)


def run_red_black():
    return run(RED_BLACK)


def run_b_tree():
    return run(B_TREE)


def run(kind):
    art = texts.RED_BLACK_TREE_ASCII if kind is RED_BLACK else texts.B_TREE_ASCII
    render.intro(art, kind.guide)
    tree = Menu(f"🛠️ How do you want to create the {kind.name}?", [
        [("Create an empty tree", lambda: create(kind)),
         ("Use the example", lambda: example(kind)),
         ("Fill with random values", lambda: create(kind, random=True))],
        [back_option()],
    ]).open()
    if tree is Nav.BACK:
        return Nav.BACK
    return operation_menu(kind.name, kind.guide, operations(tree, kind), new_label=f"New {kind.name}").run()


def create(kind, random=False):
    data_type = Menu("🤔 Which type of keys do you want to store?", [
        [("Numbers (int or float)", lambda: "num"), ("Strings", lambda: "str")],
        [back_option()],
    ]).open()
    if data_type is Nav.BACK:
        return Nav.BACK
    if kind is B_TREE:
        degree = ask_int("🔢 Minimum degree t (2–10)? A node holds at most 2t − 1 keys:",
                         "minimum degree", min_value=2, max_value=10)
        tree = BTree(degree, data_type)
    else:
        tree = RedBlackTree(data_type)
    if random:
        count = random_data.ask_count("keys")
        for key in random_data.values(data_type, count):
            tree.insert(key)
        success(f"Created the {kind.name} with {plural(count, 'random key')}.")
    else:
        success(f"Created an empty {kind.name}.")
    kind.draw(tree)
    return tree


def example(kind):
    tree = BTree(2) if kind is B_TREE else RedBlackTree()
    for key in EXAMPLE_KEYS:
        tree.insert(key)
    success(f"Loaded the example {kind.name}" + (" with minimum degree 2." if kind is B_TREE else "."))
    kind.draw(tree)
    return tree


def operations(tree, kind):
    return [
        ("Insert", lambda: change(tree, kind, "insert")),
        ("Delete", lambda: change(tree, kind, "delete")),
        ("Search", lambda: search(tree, kind)),
        ("Traversals", lambda: traversals(tree, kind)),
        ("Tree Stats", lambda: render.tree_stats(tree, kind.name)),
        ("Display", lambda: kind.draw(tree)),
    ]


def change(tree, kind, operation):
    key, trace = tree_screen.ask_key(tree), []
    try:
        getattr(tree, operation)(key, trace)
    except NotFoundError:
        not_found(f"{render.fmt(key)} isn't in the tree, so nothing was deleted.")
        return
    except InvalidTypeError as problem:
        error(str(problem))
        return
    stepper.play(trace, kind.draw_step)
    success(f"{'Inserted' if operation == 'insert' else 'Deleted'} {render.fmt(key)}.")
    kind.draw(tree)


def search(tree, kind):
    key, trace = tree_screen.ask_key(tree), []
    try:
        node = tree.search(key, trace)
    except InvalidTypeError as problem:
        error(str(problem))
        return
    stepper.play(trace, kind.draw_step)
    if node is None:
        not_found(f"{render.fmt(key)} isn't in the tree.")
    else:
        success(f"Found {render.fmt(key)} in the tree.")


def traversals(tree, kind):
    def walk(name, method):
        trace = []
        keys = method(trace)
        stepper.play(trace, kind.draw_step)
        render.traversal(name, keys)

    Menu("🗂️ Which traversal do you want?", [
        [(name, lambda name=name, method=method: walk(name, method)) for name, method in (
            ("Inorder", tree.inorder), ("Preorder", tree.preorder),
            ("Postorder", tree.postorder), ("Level order", tree.level_order))],
        [back_option()],
    ]).select()
