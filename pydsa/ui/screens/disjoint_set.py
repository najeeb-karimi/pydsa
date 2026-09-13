"""Disjoint set (Union-Find) screen."""

from pydsa.content import complexity, texts
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.errors import OutOfBoundsError
from pydsa.ui import render
from pydsa.ui.console import ask_int, error, info, plural, result, success, yes_no
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu

EXAMPLE_UNIONS = [(0, 1), (2, 3), (1, 3), (4, 5), (6, 7)]


def run():
    """Create a disjoint set and run the disjoint set operation menu."""
    render.intro(texts.DISJOINT_SET_ASCII, texts.DISJOINT_SET_DEFINITION, complexity.DISJOINT_SET)
    union_find = Menu("🛠️ Do you want to create a disjoint set yourself or use the preloaded example?", [
        [("Create a disjoint set", create), ("Use the example", example)],
        [back_option()],
    ]).open()
    if union_find is Nav.BACK:
        return Nav.BACK

    return operation_menu("disjoint set", [
        ("Union", lambda: union(union_find)),
        ("Find", lambda: find(union_find)),
        ("Check if Connected", lambda: connected(union_find)),
        ("List Sets", lambda: render.disjoint_sets(union_find)),
        ("Display", lambda: render.disjoint_set(union_find)),
    ], definition=lambda: render.definition(texts.DISJOINT_SET_DEFINITION, complexity.DISJOINT_SET),
       new_label="New Disjoint Set").run()


def create():
    """Ask for the number of elements and return a disjoint set where each element is in a set of its own."""
    size = ask_int("🔢 How many elements should the disjoint set have?", "number of elements", min_value=1)
    union_find = DisjointSet(size)
    success(f"Created a disjoint set of {plural(size, 'element')}, numbered 0 to {size - 1}, each in a set of its own.")
    render.disjoint_set(union_find)
    return union_find


def example():
    """Return the preloaded example disjoint set."""
    union_find = DisjointSet(8)
    for a, b in EXAMPLE_UNIONS:
        union_find.union(a, b)
    pairs = [f"{a} and {b}" for a, b in EXAMPLE_UNIONS]
    success(f"Loaded the example: 8 elements after merging the sets of {', '.join(pairs[:-1])}, and {pairs[-1]}.")
    render.disjoint_set(union_find)
    return union_find


def ask_pair():
    return ask_int("🔢 What's the first element?", "element"), ask_int("🔢 What's the second element?", "element")


def missing_element(union_find, *elements):
    """Report the first of elements that doesn't exist."""
    element = next(e for e in elements if not 0 <= e < len(union_find))
    error(f"Element {element} doesn't exist. Valid elements are 0 to {len(union_find) - 1}.")


def union(union_find):
    a, b = ask_pair()
    try:
        merged = union_find.union(a, b)
    except OutOfBoundsError:
        missing_element(union_find, a, b)
        return
    if not merged:
        info(f"{a} and {b} are already in the same set, so nothing changed.")
        return
    success(f"Merged the sets of {a} and {b}. Their root is now {union_find.root_of(a)}.")
    render.disjoint_set(union_find)


def find(union_find):
    element = ask_int("🔢 Which element's root do you want to find?", "element")
    parents_before = list(union_find.parent)
    try:
        root = union_find.find(element)
    except OutOfBoundsError:
        missing_element(union_find, element)
        return
    result(f"The root of {element} is {root}.")
    relinked = sum(1 for before, after in zip(parents_before, union_find.parent) if before != after)
    if relinked:
        info(f"Path compression pointed {plural(relinked, 'element')} straight at the root.")
        render.disjoint_set(union_find)


def connected(union_find):
    a, b = ask_pair()
    try:
        same_set = union_find.connected(a, b)
    except OutOfBoundsError:
        missing_element(union_find, a, b)
        return
    result(f"Are {a} and {b} connected? {yes_no(same_set)}.")
