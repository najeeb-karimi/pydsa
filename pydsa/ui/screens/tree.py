"""Tree screen: binary search tree and AVL tree."""

from typing import NamedTuple

from pydsa.content import texts
from pydsa.core.errors import NotFoundError
from pydsa.core.tree import AVLTree, BinarySearchTree
from pydsa.ui import render
from pydsa.ui.console import ask_value
from pydsa.ui.menu import Menu, operation_menu


class TreeKind(NamedTuple):
    """The class and wording for one kind of tree."""

    tree_class: type
    info: str
    name: str  # As in "create a BST yourself"
    short_name: str  # As in "store in the BST"
    title: str  # Name in the operation menu title


BST = TreeKind(BinarySearchTree, texts.BST_INFO, "a BST", "BST", "BST")
AVL = TreeKind(AVLTree, texts.AVL_INFO, "an AVL tree", "AVL", "AVL TREE")

EXAMPLE_KEYS = [50, 30, 10, 20, 70, 60, 80]


def run():
    """Show the tree intro, let the user pick a BST or an AVL tree and run its menu."""
    render.intro(texts.TREE_ASCII, texts.TREE_DEFINITION)
    return Menu(
        "\n🧪 Which type of tree do you want?",
        [[("BST (Binary Search Tree)", lambda: tree_menu(BST)),
          ("AVL (Adelson-Velsky and Evgenii Landis)", lambda: tree_menu(AVL))]],
        invalid="\n🚫 Invalid type code!",
    ).select()


def tree_menu(kind):
    """Create a tree of the given kind and run its operation menu."""
    print(kind.info)
    tree = Menu(
        f"\n🛠️ Do you want to create {kind.name} yourself or use the preloaded example?",
        [[(f"Create {kind.name}", lambda: create(kind)), ("Use the example", lambda: example(kind))]],
        bullet="●",
    ).select()

    return operation_menu(kind.title, texts.TREE_DEFINITION, [
        ("Insertion", lambda: insert(tree)),
        ("Deletion", lambda: delete(tree)),
        ("Searching", lambda: search(tree)),
        ("Traversals", lambda: traversals(tree)),
    ], new_label="New Tree", new_intro=False).run()


def create(kind):
    """Ask whether the tree holds numbers or strings and return an empty tree."""
    return Menu(
        f"\n🤔 Which type of data do you want to store in the {kind.short_name}?",
        [[("Numbers (int or float)", lambda: kind.tree_class("num")),
          ("Strings", lambda: kind.tree_class("str"))]],
    ).select()


def example(kind):
    """Return the preloaded example tree."""
    tree = kind.tree_class("num")
    for key in EXAMPLE_KEYS:
        tree.insert(key)
    print(f"\n✅ Here's an example {kind.short_name}.", end="")
    show(tree)
    return tree


def show(tree):
    """Print the in-order traversal, which lists the keys in sorted order."""
    render.tree_traversal(tree.inorder(), "Inorder")


def ask_key(tree):
    """Ask for a key of the tree's data type; return None if the input doesn't match it."""
    return ask_value(tree.data_type)


def insert(tree):
    """Insert a key typed by the user."""
    key = ask_key(tree)
    if key is None:
        print("\n🚫 Invalid data type; item not inserted.")
        return
    tree.insert(key)
    print("\n✅ Successfully inserted.", end="")
    show(tree)


def delete(tree):
    """Delete a key typed by the user."""
    key = ask_key(tree)
    if key is None:
        print("\n🚫 Invalid data type. Deletion unsuccessful.")
        return
    try:
        tree.delete(key)
    except NotFoundError:
        print("\n❌ Node not found. Deletion unsuccessful.")
        return
    print("\n✅ Successfully deleted.", end="")
    show(tree)


def search(tree):
    """Report whether a key typed by the user is in the tree."""
    key = ask_key(tree)
    if key is None:
        print("\n🚫 Invalid data type. Searching unsuccessful.")
        return
    if key in tree:
        print("\n✅ Node available.", end="")
    else:
        print("\n❌ Node not found.", end=" ")
    show(tree)


def traversals(tree):
    """Let the user pick a traversal and print it."""
    Menu(
        "\n🗂️ Which traversal do you want?",
        [[("Inorder Traversal", lambda: render.tree_traversal(tree.inorder(), "Inorder")),
          ("Preorder Traversal", lambda: render.tree_traversal(tree.preorder(), "Preorder")),
          ("Postorder Traversal", lambda: render.tree_traversal(tree.postorder(), "Postorder"))]],
        bullet="●",
    ).select()
