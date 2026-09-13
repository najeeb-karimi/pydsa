"""Array screen."""

from pydsa.content import complexity, texts
from pydsa.core.array import Array
from pydsa.core.errors import OutOfBoundsError
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_value, error, plural, result, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt
from pydsa.ui.screens.searching_algorithms import SEARCHES, run_search
from pydsa.ui.screens.sorting_algorithms import SORTS, run_sort


def show_definition():
    render.definition(texts.ARRAY_DEFINITION, complexity.ARRAY, complexity.SORTING)


def run():
    """Create an array and run the array operation menu."""
    render.intro(texts.ARRAY_ASCII, texts.ARRAY_DEFINITION, complexity.ARRAY, complexity.SORTING)
    array = Menu("🛠️ Do you want to create an array yourself or use the preloaded example?", [
        [("Create an array", create), ("Use the example", example)],
        [back_option()],
    ]).open()
    if array is Nav.BACK:
        return Nav.BACK

    return operation_menu("array", [
        ("Insert", lambda: insert(array)),
        ("Delete", lambda: delete(array)),
        ("Get by Index", lambda: get(array)),
        ("Sort", lambda: sort(array)),
        ("Search", lambda: search(array)),
        ("Size", lambda: result(f"The array has {plural(array.size, 'element')}.")),
        ("Data Type", lambda: result(f"The array holds {array.data_type.__name__} values.")),
        ("Display", lambda: render.array(array.items)),
    ], definition=show_definition, new_label="New Array").run()


# ---------------------------------------------------------------------------
# Creation
# ---------------------------------------------------------------------------

def create():
    """Ask for the data type and size, then return an array filled with that type's default value."""
    data_type = Menu("🤔 Which data type should the array hold?", [
        [("int", lambda: int), ("str", lambda: str)],
        [back_option()],
    ]).open()
    if data_type is Nav.BACK:
        return Nav.BACK
    size = ask_int("↔️ How many elements should the array have?", "size", min_value=1)
    array = Array(size, data_type, data_type())
    success(f"Created a {data_type.__name__} array with {plural(size, 'element')}.")
    render.array(array.items)
    return array


def example():
    """Return the preloaded example array."""
    array = Array(5, int, 0)
    array.items = [10, 1987, 672, 8, 2004]
    success("Loaded the example array.")
    render.array(array.items)
    return array


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def ask_index():
    return ask_int("🔢 Which index?", "index")


def out_of_bounds(array, index):
    error(f"Index {index} is out of bounds. Valid indexes are 0 to {array.size - 1}.")


def insert(array):
    """Insert one item at a chosen index, or fill up the whole array."""
    Menu("➕ How do you want to insert?", [
        [("Insert one item", lambda: insert_one(array)), ("Fill the whole array", lambda: fill(array))],
        [back_option()],
    ]).select()


def insert_one(array):
    item = ask_value(array.data_type.__name__)
    index = ask_index()
    try:
        array.insert(index, item)
    except OutOfBoundsError:
        out_of_bounds(array, index)
        return
    success(f"Inserted {fmt(item)} at index {index}.")
    render.array(array.items)


def fill(array):
    kind = array.data_type.__name__
    for index in range(array.size):
        array.insert(index, ask_value(kind, f"item for index {index}"))
    success("Filled the whole array.")
    render.array(array.items)


def delete(array):
    """Reset the item at a chosen index to the default value."""
    index = ask_index()
    try:
        item = array.get(index)
        array.remove(index)
    except OutOfBoundsError:
        out_of_bounds(array, index)
        return
    success(f"Deleted {fmt(item)} from index {index}, which now holds {fmt(array.default_value)} again.")
    render.array(array.items)


def get(array):
    """Show the item at a chosen index."""
    index = ask_index()
    try:
        result(f"Index {index} holds {fmt(array.get(index))}.")
    except OutOfBoundsError:
        out_of_bounds(array, index)


def sort(array):
    """Let the user pick a sorting algorithm and sort the array with it, showing every step."""
    Menu("🗂️ Which sorting algorithm do you want to use?", [
        [(sort.name, lambda sort=sort: sort_array(array, sort)) for sort in SORTS],
        [back_option()],
    ]).select()


def sort_array(array, sort):
    if run_sort(array.items, sort, "the array"):
        render.array(array.items)


def search(array):
    """Let the user pick a searching algorithm and search the array with it."""
    Menu("🔍 Which searching algorithm do you want to use?", [
        [(search.name, lambda search=search: run_search(array.items, search, array.data_type.__name__, "the array"))
         for search in SEARCHES],
        [back_option()],
    ]).select()
