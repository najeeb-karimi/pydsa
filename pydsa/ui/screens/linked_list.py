"""Linked list screen: singly and doubly linked lists."""

from pydsa.content import texts
from pydsa.core.errors import EmptyError, OutOfBoundsError
from pydsa.core.linked_list import DoublyLinkedList, SinglyLinkedList
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_value
from pydsa.ui.menu import Menu, operation_menu


def run():
    """Show the linked list intro, let the user pick a singly or doubly linked list and run its menu."""
    render.intro(texts.LINKED_LIST_ASCII, texts.LINKED_LIST_DEFINITION)
    return Menu(
        "\n🧪 Which type of linked list do you want?",
        [[("Singly Linked List", singly), ("Doubly Linked List", doubly)]],
        spaced=True,
        invalid="\n🚫 Invalid!",
    ).select()


def singly():
    """Run the singly linked list operation menu on a new, empty list."""
    sll = SinglyLinkedList()

    def show():
        render.linked_list(list(sll), " => ", "\n❌ List is empty.")

    return operation_menu("SINGLY LINKED LIST", texts.LINKED_LIST_DEFINITION, [
        *shared_operations(sll, show),
        ("Traversing/Displaying", show),
        ("Searching", lambda: search(sll, texts.LINKED_LIST_SEARCH_INFO)),
    ], new_label="New Linked List").run()


def doubly():
    """Run the doubly linked list operation menu on a new, empty list."""
    dll = DoublyLinkedList()

    def show():
        render.linked_list(list(dll), " <=> ", "\n👉 List is empty.")

    return operation_menu("DOUBLY LINKED LIST", texts.LINKED_LIST_DEFINITION, [
        *shared_operations(dll, show),
        ("Traversing Forward", show),
        ("Traversing Backward", lambda: render.linked_list(dll.backward(), " <=> ", "\n👉 List is empty.")),
        ("Searching", lambda: search(dll)),
    ], new_label="New Linked List").run()


def shared_operations(linked_list, show):
    """Return the insertion and deletion operations both lists offer; show prints the list."""
    return [
        ("Insertion at the Beginning", lambda: insert(show, linked_list.insert_at_beginning)),
        ("Insertion at a Specific Point", lambda: insert(show, linked_list.insert_at_position, ask_index())),
        ("Insertion at the End", lambda: insert(show, linked_list.insert_at_end)),
        ("Deletion from the Beginning", lambda: delete(show, linked_list.delete_from_beginning)),
        ("Deletion from a Specific Point", lambda: delete(show, linked_list.delete_from_position, ask_index())),
        ("Deletion from the End", lambda: delete(show, linked_list.delete_from_end)),
    ]


def ask_index():
    """Ask for a position until a whole number is entered."""
    return ask_int("\n🔟 Please enter the index.\n>>> ", "\n🚫 Invalid index!")


def insert(show, method, *position):
    """Ask for an item and insert it with method, passing the position first if one is given."""
    item = ask_value()
    if item is None:
        print("\n🚫 Invalid data type; item not inserted.")
        return
    try:
        method(*position, item)
    except OutOfBoundsError:
        print("\n🚫 Position out of bounds. Insertion unsuccessful.")
        return
    print("\n✅ Insertion successful.", end="")
    show()


def delete(show, method, *position):
    """Delete a node with method, passing the position if one is given."""
    try:
        method(*position)
    except EmptyError:
        print("\n🚫 List is empty.")
        return
    except OutOfBoundsError:
        print("\n🚫 Position out of bounds. Deletion unsuccessful.")
        return
    print("\n✅ Deletion successful.", end="")
    show()


def search(linked_list, info=None):
    """Explain the search if info is given, then ask for a target and report its position."""
    if info is not None:
        print(info)
    target = ask_value(msg="target element")
    if target is None:
        print("\n🚫 Invalid data type; nothing to search for.")
        return
    position = linked_list.search(target)
    if position == -1:
        print("\n❌ Item not found.")
    else:
        print(f"\n✅ Item found at position {position}.")
