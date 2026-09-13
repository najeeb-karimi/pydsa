"""Console output for the intro and the data structures."""

from pydsa import __version__
from pydsa.content import texts


def main_intro():
    """Print the PyDSA banner, welcome message, version, changelog and data structure overview."""
    print(texts.BANNER)
    print(texts.WELCOME)
    print(f"⏳ Version {__version__}")
    print(texts.CHANGELOG)
    print(texts.SOURCE_CODE)
    print(texts.OVERVIEW)


def intro(ascii_art, definition):
    """Print a data structure's ASCII title followed by its definition."""
    print(ascii_art)
    print(definition)


def values(items):
    """Print a list of values (array, stack) on one line."""
    print(f"\n👉 {items}")


STRIKE = chr(0x0336)  # Combining long stroke overlay


def strike(value):
    """Return value as a string with every character struck out."""
    return "".join(char + STRIKE for char in str(value))


def queue_slots(queue):
    """Print every slot of a circular queue, striking out items that were already dequeued."""
    slots = [
        slot if slot is None or queue.is_live(index) else strike(slot)
        for index, slot in enumerate(queue.slots)
    ]
    values(slots)


def sorting_steps(steps):
    """Print each intermediate state yielded by a sorting generator."""
    for step in steps:
        print("🔹", step)


def linked_list(items, separator, empty_message):
    """Print linked list items joined by separator, or empty_message if there are none."""
    if not items:
        print(empty_message)
        return
    print("\n👉", separator.join(str(item) for item in items))


def tree_traversal(keys, name):
    """Print the keys of a tree traversal and label it."""
    print(f"\n👉🏻 {keys}\nℹ️ {name} Traversal")


def vertex_order(order, name):
    """Print the vertices of a graph traversal and label it."""
    print("".join(f"{vertex} " for vertex in order), end="")
    print(f"\nℹ️ {name} Traversal")


def indexed_rows(rows):
    """Print one numbered line per row: adjacency matrix rows, hash table buckets or slots."""
    for index, row in enumerate(rows):
        print("🔹", index, row)


def adjacency_list(adj_list):
    """Print each vertex followed by its (neighbor, weight) edges."""
    for vertex, edges in adj_list.items():
        print("🔹", vertex, edges)
