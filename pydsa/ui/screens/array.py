"""Array screen."""

from pydsa.algorithms import searching, sorting
from pydsa.content import texts
from pydsa.core.array import Array
from pydsa.core.errors import InvalidTypeError, OutOfBoundsError
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_order, ask_value
from pydsa.ui.menu import Menu, operation_menu

SORTS = [
    ("Bubble sort", sorting.bubble_sort, texts.BUBBLE_SORT_INFO),
    ("Selection sort", sorting.selection_sort, texts.SELECTION_SORT_INFO),
    ("Insertion sort", sorting.insertion_sort, texts.INSERTION_SORT_INFO),
    ("Quick sort", sorting.quick_sort, texts.QUICK_SORT_INFO),
    ("Heap sort", sorting.heap_sort, texts.HEAP_SORT_INFO),
    ("Shell sort", sorting.shell_sort, texts.SHELL_SORT_INFO),
]

SEARCHES = [
    ("Linear search", searching.linear_search, texts.LINEAR_SEARCH_INFO),
    ("Binary search", searching.binary_search, texts.BINARY_SEARCH_INFO),
]


def run():
    """Create an array and run the array operation menu."""
    render.intro(texts.ARRAY_ASCII, texts.ARRAY_DEFINITION)
    array = Menu(
        "\n🛠️ Do you want to create an array yourself or use the preloaded example?",
        [[("Create an array", create), ("Use the example", example)]],
        bullet="●",
    ).select()

    return operation_menu("ARRAY", texts.ARRAY_DEFINITION, [
        ("Insertion", lambda: insert(array)),
        ("Deletion", lambda: delete(array)),
        ("Indexing", lambda: get(array)),
        ("Sorting", lambda: sort(array)),
        ("Searching", lambda: search(array)),
        ("Size Check", lambda: print(f"\n👉 Array size: {array.size}")),
        ("Type Check", lambda: print(f"\n👉 Array Data Type: {array.data_type.__name__}")),
        ("Displaying", lambda: render.values(array.items)),
    ], new_label="New Array", exit_label="Exit the Program", invalid="\n❌️ Invalid code number.").run()


# ---------------------------------------------------------------------------
# Creation
# ---------------------------------------------------------------------------

def create():
    """Ask for the array type and size, then return an array filled with default values."""
    while True:
        array_type = input("\n🤔 Please specify the type of array. Write either str or int.\n>>> ")
        if array_type in ("str", "int"):
            break
        print("\n❌️ Either str or int!")

    size = ask_int("\n↔️ Please specify the size of the array.\n>>> ",
                   "\n❌ Invalid, the size can only be an integer!",
                   min_value=1, too_small="\n❌ Invalid, the size must be at least 1!")

    array = Array(size, str, "") if array_type == "str" else Array(size, int, 0)
    print(f"\n✅️ Here's your {array_type} array.", end="")
    render.values(array.items)
    return array


def example():
    """Return the preloaded example array."""
    array = Array(5, int, 0)
    array.items = [10, 1987, 672, 8, 2004]
    print("\n✅️ Here's an example int array with size 5.", end="")
    render.values(array.items)
    return array


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def ask_index(prompt):
    """Ask for an array index with the given prompt until a whole number is entered."""
    return ask_int(prompt, "\n🚫 Invalid, the index can only be an integer!")


def store(array, index, text):
    """Store the typed text at index, converted to an int first for int arrays."""
    item = text
    if array.data_type is int:
        try:
            item = int(text)
        except ValueError:
            pass
    try:
        array.insert(index, item)
    except InvalidTypeError:
        print(f"\n🚫 TypeError(Array can only contain elements of type {array.data_type.__name__}; item not inserted.)")
    except OutOfBoundsError:
        print("\n🚫 IndexError(Array index out of bounds; item not inserted.)")


def insert(array):
    """Insert one item at a chosen index, or fill up the entire array."""
    choice = input("\n➕️ Type 1 for adding one item or anything else for filling up the entire array.\n>>> ")

    # Add a single item
    if choice == "1":
        item = input("\n✍️ Please write the item.\n>>> ")
        index = ask_index("\n✍️ Please provide the index.\n>>> ")
        store(array, index, item)

    # Fill the entire array
    else:
        for i in range(array.size):
            item = input(f"\n✍️ Please write the item for index {i}: ")
            store(array, i, item)

    render.values(array.items)


def delete(array):
    """Remove the item at a chosen index."""
    index = ask_index("\n✍️ Please provide the index of the item you want to remove.\n>>> ")
    try:
        array.remove(index)
    except OutOfBoundsError:
        print("\n🚫 IndexError(Array index out of bounds. Deletion unsuccessful.)")
    render.values(array.items)


def get(array):
    """Show the item at a chosen index."""
    index = ask_index("\n✍️ Please provide the index of the item you want to get.\n>>> ")
    try:
        print(f"\n👉 {array.get(index)}")
    except OutOfBoundsError:
        print("\n🚫 IndexError(Array index out of bounds.)")


def sort(array):
    """Let the user pick a sorting algorithm and sort the array with it, showing every step."""
    Menu(
        "\n🗂️ Which sorting algorithm do you want to use?",
        [[(label, lambda algorithm=algorithm, info=info: run_sort(array, algorithm, info))
          for label, algorithm, info in SORTS]],
        bullet="●",
        invalid="\n🚫 Invalid code number.",
    ).select(retry=False)


def run_sort(array, algorithm, info):
    """Ask for the order, explain the algorithm and print the array before, during and after sorting."""
    order = ask_order()
    print(info)
    print("\n📌 Initial array:", end="")
    render.values(array.items)
    print("\n🪜 Sorting Steps:")
    render.sorting_steps(algorithm(array.items, order))
    print("\n♻️ Sorted array:", end="")
    render.values(array.items)


def search(array):
    """Let the user pick a searching algorithm and search the array with it."""
    Menu(
        "\n🔍 Which searching algorithm do you want to use?",
        [[(label, lambda algorithm=algorithm, info=info: run_search(array, algorithm, info))
          for label, algorithm, info in SEARCHES]],
        bullet="●",
        invalid="\n🚫 Invalid code number!",
    ).select(retry=False)


def run_search(array, algorithm, info):
    """Explain the algorithm, ask for a target of the array's type and report where it was found."""
    print(info)
    target = ask_value(array.data_type.__name__, "target element")
    if target is None:
        print("\n🚫 Invalid data type!")
        return
    index = algorithm(array.items, target)
    if index == -1:
        print("\n❌ Element not found.")
    else:
        print(f"\n✅ Element found at index: {index}.")
