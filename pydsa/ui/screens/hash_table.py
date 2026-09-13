"""Hash table screen: separate chaining and linear probing."""

from pydsa.content import texts
from pydsa.core.errors import CapacityError, NotFoundError
from pydsa.core.hash_table import ChainingHashTable, LinearProbingHashTable
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_value, value_prompt
from pydsa.ui.menu import Menu, operation_menu

EXAMPLE_PAIRS = [("Messi", "10"), ("Apple", 1976), (2024, -273.15), ("UFO", "Roswell, NM")]


def run():
    """Show the hash table intro, let the user pick a collision resolution technique and run its menu."""
    render.intro(texts.HASH_TABLE_ASCII, texts.HASH_TABLE_DEFINITION)
    return Menu(
        "\n🧪 Which type of collision resolution do you want in the hash table?",
        [[("Separate Chaining (Open Hashing)", chaining_menu),
          ("Linear Probing (from the Open Addressing [Closed Hashing] category)", probing_menu)]],
        invalid="\n🚫 Invalid collision resolution type code!",
    ).select()


# ---------------------------------------------------------------------------
# Shared pieces
# ---------------------------------------------------------------------------

def ask_table_size(unit):
    """Ask for the number of buckets or slots (unit) until an int of at least 1 is entered."""
    return ask_int(value_prompt(f"the total number of {unit} you want; in other words, the size of the hash table", "INT"),
                   "\n🚫 Invalid data type. Hash table size must be an INT of at least 1.", min_value=1)


def create(build, example_count, example_name):
    """Build a hash table from scratch or load the preloaded example.

    build(size) creates and announces an empty table; the example inserts the first example_count pairs.
    """

    def custom():
        table = build(ask_table_size("buckets" if example_name == "Chaining" else "slots"))
        render.indexed_rows(table.table)
        return table

    def example():
        table = build(5)
        # The table can't be filled in directly: Python's hash() for strings changes between runs,
        # so the keys land in different buckets each time and hard-coded positions would be wrong
        for key, value in EXAMPLE_PAIRS[:example_count]:
            table.insert(key, value)
        print(f"👇🏻 Here's an example {example_name} Hash Table:")
        render.indexed_rows(table.table)
        return table

    return Menu(
        "\n🛠️ Do you want to create a hash table yourself or use the preloaded example?",
        [[("Create a hash table", custom), ("Use the example", example)]],
        bullet="●",
    ).select()


def ask_key(msg="key"):
    """Ask for a key of any type until a valid one is entered; msg customizes the prompt."""
    print("\n🔑 Specify the Key:")
    while True:
        key = ask_value(msg=msg)
        if key is not None:
            return key
        print("\n🚫 Invalid data type for the key.")


def ask_pair_value():
    """Ask for a value of any type until a valid one is entered."""
    print("\n🚪 Specify the Value:")
    while True:
        value = ask_value(msg="value")
        if value is not None:
            return value
        print("\n🚫 Invalid data type for the value.")


def insert(table):
    """Insert or update a key-value pair typed by the user."""
    key = ask_key()
    value = ask_pair_value()
    try:
        index, updated = table.insert(key, value)
    except CapacityError:
        print("\n🚫 Insertion unsuccessful. Hash table is full; cannot insert new key.")
        return
    action = "Updated" if updated else "Inserted"
    print(f"\n✅ Insertion successful. {action} key ({key}) with value ({value}) at index {index}.")


def search(table):
    """Look up a key typed by the user."""
    key = ask_key("key that you want to search for")
    try:
        index, value = table.lookup(key)
    except NotFoundError:
        print(f"\n❌ Searching successful. Key ({key}) not found.")
        return
    print(f"\n✅ Searching successful. Key ({key}) found at index {index} with value ({value}).")


def operations(table, delete):
    """Return the operations both hash tables offer; delete is the table-specific deletion action."""

    def display():
        print("\n👇🏻 Here's a display of your Hash Table:")
        render.indexed_rows(table.table)

    return [
        ("Insertion", lambda: insert(table)),
        ("Deletion", delete),
        ("Searching", lambda: search(table)),
        ("Displaying", display),
    ]


# ---------------------------------------------------------------------------
# Separate Chaining
# ---------------------------------------------------------------------------

def build_chaining(size):
    """Return an empty chaining hash table and announce it."""
    table = ChainingHashTable(size)
    print(f"\n✅ Initialized hash table with {size} buckets.")
    print(texts.CHAINING_INFO)
    return table


def chaining_menu():
    """Create a separate chaining hash table and run its operation menu."""
    table = create(build_chaining, 4, "Chaining")

    def delete():
        key = ask_key("key that you want to delete")
        try:
            index = table.delete(key)
        except NotFoundError:
            print(f"\n🚫 Deletion unsuccessful. Key ({key}) not found, nothing to delete.")
            return
        print(f"\n✅ Deletion successful. Deleted key ({key}) from index {index}.")

    return operation_menu("Chaining Hash Table", texts.HASH_TABLE_DEFINITION, operations(table, delete),
                          new_label="New Hash Table", new_intro=False).run()


# ---------------------------------------------------------------------------
# Linear Probing
# ---------------------------------------------------------------------------

def build_probing(size):
    """Return an empty linear probing hash table and announce it."""
    table = LinearProbingHashTable(size)
    print(f"\n✅ Initialized hash table with {size} slots.")
    return table


def probing_menu():
    """Create a linear probing hash table and run its operation menu."""
    table = create(build_probing, 3, "Linear Probing")

    def delete():
        key = ask_key("key that you want to delete")
        try:
            index, rehashed = table.delete(key)
        except NotFoundError:
            print(f"\n🚫 Deletion unsuccessful. Key ({key}) not found, nothing to delete.")
            return
        message = f"\n✅ Deletion successful. Deleted key ({key}) from index {index}."
        if rehashed:
            message += f"\n♻️ Rehashed {rehashed} key(s) from the same cluster."
        print(message)

    return operation_menu("Linear Probing Hash Table", texts.HASH_TABLE_DEFINITION, operations(table, delete),
                          new_label="New Hash Table", new_intro=False).run()
