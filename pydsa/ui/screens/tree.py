"""Tree screen: binary search tree and AVL tree."""

from typing import NamedTuple

from pydsa.content import texts
from pydsa.core.errors import NotFoundError
from pydsa.core.tree import AVLTree, BinarySearchTree
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_value, not_found, plural, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt


class TreeKind(NamedTuple):
    """The class and wording for one kind of tree."""

    tree_class: type
    guide: str  # The ID of its guide and topic
    name: str  # As in "Loaded the example BST"
    with_article: str  # As in "create a BST yourself"


BST = TreeKind(BinarySearchTree, "bst", "BST", "a BST")
AVL = TreeKind(AVLTree, "avl-tree", "AVL tree", "an AVL tree")

EXAMPLE_KEYS = [50, 30, 10, 20, 70, 60, 80]


def run():
    """Show the tree intro, let the user pick a BST or an AVL tree and run its menu."""
    render.intro(texts.TREE_ASCII, "tree")
    return Menu("🧪 Which type of tree do you want?", [
        [("BST (Binary Search Tree)", lambda: tree_menu(BST)),
         ("AVL Tree (Adelson-Velsky and Landis)", lambda: tree_menu(AVL))],
        [back_option()],
    ]).open()


def run_kind(kind):
    """Show the tree intro and run the menu of one kind of tree, skipping the choice of kind."""
    render.intro(texts.TREE_ASCII, "tree")
    return tree_menu(kind)


def tree_menu(kind):
    """Show the summary of a kind of tree, then create one and run its operation menu."""
    render.summary(kind.guide)
    tree = Menu(f"🛠️ Do you want to create {kind.with_article} yourself or use the preloaded example?", [
        [(f"Create {kind.with_article}", lambda: create(kind)), ("Use the example", lambda: example(kind)),
         ("Fill with random values", lambda: fill_random(kind))],
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
    ], guides=[kind.guide, "tree"], new_label="New Tree").run()


def show(tree):
    """Draw the tree, with balance factors for an AVL tree."""
    render.binary_tree(tree, balance=isinstance(tree, AVLTree))


def ask_data_type(kind):
    """Ask whether the tree holds numbers or strings; return "num", "str" or Nav.BACK."""
    return Menu(f"🤔 Which type of data do you want to store in the {kind.name}?", [
        [("Numbers (int or float)", lambda: "num"), ("Strings", lambda: "str")],
        [back_option()],
    ]).open()


def create(kind):
    """Ask whether the tree holds numbers or strings and return an empty tree."""
    data_type = ask_data_type(kind)
    if data_type is Nav.BACK:
        return Nav.BACK
    success(f"Created an empty {kind.name} for {'numbers' if data_type == 'num' else 'strings'}.")
    return kind.tree_class(data_type)


def fill_random(kind):
    """Ask for the data type and how many random keys to insert, and return the tree."""
    data_type = ask_data_type(kind)
    if data_type is Nav.BACK:
        return Nav.BACK
    count = random_data.ask_count("keys")
    tree = kind.tree_class(data_type)
    for key in random_data.values(data_type, count):
        tree.insert(key)
    success(f"Created {kind.with_article} with {plural(count, 'random key')}.")
    show(tree)
    return tree


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
