"""Hash table screen: separate chaining and linear probing."""

from typing import Callable, NamedTuple

from pydsa.content import complexity, texts
from pydsa.core.errors import CapacityError, NotFoundError
from pydsa.core.hash_table import ChainingHashTable, LinearProbingHashTable
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_value, error, info, not_found, plural, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt


class TableKind(NamedTuple):
    """The class, wording and renderer for one kind of hash table."""

    table_class: type
    name: str
    unit: str  # What a position in the table is called: bucket or slot
    show: Callable
    example_pairs: int  # How many of EXAMPLE_PAIRS the example holds


CHAINING = TableKind(ChainingHashTable, "chaining hash table", "bucket", render.chaining_table, 4)
PROBING = TableKind(LinearProbingHashTable, "linear probing hash table", "slot", render.probing_table, 3)

EXAMPLE_PAIRS = [("Messi", "10"), ("Apple", 1976), (2024, -273.15), ("UFO", "Roswell, NM")]


def show_definition():
    render.definition(texts.HASH_TABLE_DEFINITION, complexity.HASH_TABLE)


def run():
    """Show the hash table intro, let the user pick a collision resolution technique and run its menu."""
    render.intro(texts.HASH_TABLE_ASCII, texts.HASH_TABLE_DEFINITION, complexity.HASH_TABLE)
    return Menu("🧪 Which collision resolution technique do you want?", [
        [("Separate Chaining (Open Hashing)", lambda: table_menu(CHAINING)),
         ("Linear Probing (Open Addressing)", lambda: table_menu(PROBING))],
        [back_option()],
    ]).open()


def table_menu(kind):
    """Create a hash table of the given kind and run its operation menu."""
    table = Menu(f"🛠️ Do you want to create a {kind.name} yourself or use the preloaded example?", [
        [("Create a hash table", lambda: create(kind)), ("Use the example", lambda: example(kind))],
        [back_option()],
    ]).open()
    if table is Nav.BACK:
        return Nav.BACK

    return operation_menu(kind.name, [
        ("Insert", lambda: insert(kind, table)),
        ("Delete", lambda: delete(kind, table)),
        ("Search", lambda: search(kind, table)),
        ("Display", lambda: kind.show(table)),
    ], definition=show_definition, new_label="New Hash Table").run()


def create(kind):
    """Ask for the number of buckets or slots and return an empty hash table."""
    size = ask_int(f"🔢 How many {kind.unit}s should the table have?", f"number of {kind.unit}s", min_value=1)
    table = kind.table_class(size)
    success(f"Created an empty hash table with {plural(size, kind.unit)}.")
    if kind is CHAINING:
        info(texts.CHAINING_INFO)
    kind.show(table)
    return table


def example(kind):
    """Return the preloaded example hash table."""
    table = kind.table_class(5)
    # The table can't be filled in directly: Python's hash() for strings changes between runs,
    # so the keys land in different buckets each time and hard-coded positions would be wrong
    for key, value in EXAMPLE_PAIRS[:kind.example_pairs]:
        table.insert(key, value)
    success("Loaded the example hash table.")
    kind.show(table)
    return table


def insert(kind, table):
    key = ask_value(what="key")
    value = ask_value(what="value")
    try:
        index, updated = table.insert(key, value)
    except CapacityError:
        error(f"The table is full, so key {fmt(key)} wasn't inserted.")
        return
    action = "Updated" if updated else "Inserted"
    success(f"{action} key {fmt(key)} with value {fmt(value)} in {kind.unit} {index}.")
    kind.show(table)


def delete(kind, table):
    key = ask_value(what="key")
    try:
        if kind is PROBING:
            index, rehashed = table.delete(key)
        else:
            index, rehashed = table.delete(key), 0
    except NotFoundError:
        not_found(f"Key {fmt(key)} isn't in the table, so nothing was deleted.")
        return
    success(f"Deleted key {fmt(key)} from {kind.unit} {index}.")
    if rehashed:
        info(f"Rehashed {plural(rehashed, 'key')} from the same cluster, so they can still be found.")
    kind.show(table)


def search(kind, table):
    key = ask_value(what="key")
    try:
        index, value = table.lookup(key)
    except NotFoundError:
        not_found(f"Key {fmt(key)} isn't in the table.")
        return
    success(f"Found key {fmt(key)} in {kind.unit} {index} with value {fmt(value)}.")
