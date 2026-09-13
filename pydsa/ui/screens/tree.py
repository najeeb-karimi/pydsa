"""Tree screen: binary search tree and AVL tree."""

from typing import NamedTuple

from pydsa.content import complexity, texts
from pydsa.core.errors import NotFoundError
from pydsa.core.tree import AVLTree, BinarySearchTree
from pydsa.ui import render
from pydsa.ui.console import ask_value, info, not_found, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt


class TreeKind(NamedTuple):
    """The class and wording for one kind of tree."""

    tree_class: type
    info: str
    name: str  # As in "Loaded the example BST"
    with_article: str  # As in "create a BST yourself"


BST = TreeKind(BinarySearchTree, texts.BST_INFO, "BST", "a BST")
AVL = TreeKind(AVLTree, texts.AVL_INFO, "AVL tree", "an AVL tree")

EXAMPLE_KEYS = [50, 30, 10, 20, 70, 60, 80]


def show_definition():
    render.definition(texts.TREE_DEFINITION, complexity.TREE)


def run():
    """Show the tree intro, let the user pick a BST or an AVL tree and run its menu."""
    render.intro(texts.TREE_ASCII, texts.TREE_DEFINITION, complexity.TREE)
    return Menu("🧪 Which type of tree do you want?", [
        [("BST (Binary Search Tree)", lambda: tree_menu(BST)),
         ("AVL Tree (Adelson-Velsky and Landis)", lambda: tree_menu(AVL))],
        [back_option()],
    ]).open()


def tree_menu(kind):
    """Create a tree of the given kind and run its operation menu."""
    info(kind.info)
    tree = Menu(f"🛠️ Do you want to create {kind.with_article} yourself or use the preloaded example?", [
        [(f"Create {kind.with_article}", lambda: create(kind)), ("Use the example", lambda: example(kind))],
        [back_option()],
    ]).open()
    if tree is Nav.BACK:
        return Nav.BACK

    return operation_menu(kind.name, [
        ("Insert", lambda: insert(tree)),
        ("Delete", lambda: delete(tree)),
        ("Search", lambda: search(tree)),
        ("Traversals", lambda: traversals(tree)),
        ("Tree Stats", lambda: render.tree_stats(tree)),
        ("Display", lambda: show(tree)),
    ], definition=show_definition, new_label="New Tree").run()


def show(tree):
    """Draw the tree, with balance factors for an AVL tree."""
    render.binary_tree(tree, balance=isinstance(tree, AVLTree))


def create(kind):
    """Ask whether the tree holds numbers or strings and return an empty tree."""
    data_type = Menu(f"🤔 Which type of data do you want to store in the {kind.name}?", [
        [("Numbers (int or float)", lambda: "num"), ("Strings", lambda: "str")],
        [back_option()],
    ]).open()
    if data_type is Nav.BACK:
        return Nav.BACK
    success(f"Created an empty {kind.name} for {'numbers' if data_type == 'num' else 'strings'}.")
    return kind.tree_class(data_type)


def example(kind):
    """Return the preloaded example tree."""
    tree = kind.tree_class("num")
    for key in EXAMPLE_KEYS:
        tree.insert(key)
    success(f"Loaded the example {kind.name}.")
    show(tree)
    return tree


def ask_key(tree):
    """Ask for a key of the tree's data type."""
    return ask_value(tree.data_type, "key")


def insert(tree):
    key = ask_key(tree)
    tree.insert(key)
    success(f"Inserted {fmt(key)}.")
    show(tree)


def delete(tree):
    key = ask_key(tree)
    try:
        tree.delete(key)
    except NotFoundError:
        not_found(f"{fmt(key)} isn't in the tree, so nothing was deleted.")
        return
    success(f"Deleted {fmt(key)}.")
    show(tree)


def search(tree):
    key = ask_key(tree)
    if key in tree:
        success(f"Found {fmt(key)} in the tree.")
    else:
        not_found(f"{fmt(key)} isn't in the tree.")


def traversals(tree):
    """Let the user pick a traversal and show the keys in that order."""
    Menu("🗂️ Which traversal do you want?", [
        [("Inorder (left, node, right)", lambda: render.traversal("Inorder", tree.inorder())),
         ("Preorder (node, left, right)", lambda: render.traversal("Preorder", tree.preorder())),
         ("Postorder (left, right, node)", lambda: render.traversal("Postorder", tree.postorder())),
         ("Level order (level by level, left to right)", lambda: render.traversal("Level order", tree.level_order()))],
        [back_option()],
    ]).select()
