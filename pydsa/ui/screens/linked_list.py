"""Linked list screen: singly and doubly linked lists."""

from typing import NamedTuple

from pydsa.content import complexity, texts
from pydsa.core.errors import EmptyError, OutOfBoundsError
from pydsa.core.linked_list import DoublyLinkedList, SinglyLinkedList
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_value, error, not_found, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt


class ListKind(NamedTuple):
    """The class and name of one kind of linked list."""

    list_class: type
    name: str
    doubly: bool


SINGLY = ListKind(SinglyLinkedList, "singly linked list", False)
DOUBLY = ListKind(DoublyLinkedList, "doubly linked list", True)

EXAMPLE_ITEMS = [10, "Messi", 2.5]


def show_definition():
    render.definition(texts.LINKED_LIST_DEFINITION, complexity.LINKED_LIST)


def run():
    """Show the linked list intro, let the user pick a kind of list and run its menu."""
    render.intro(texts.LINKED_LIST_ASCII, texts.LINKED_LIST_DEFINITION, complexity.LINKED_LIST)
    return Menu("🧪 Which type of linked list do you want?", [
        [("Singly Linked List", lambda: list_menu(SINGLY)), ("Doubly Linked List", lambda: list_menu(DOUBLY))],
        [back_option()],
    ]).open()


def list_menu(kind):
    """Create a linked list of the given kind and run its operation menu."""
    linked_list = Menu(f"🛠️ Do you want to start with an empty {kind.name} or use the preloaded example?", [
        [("Start with an empty list", lambda: create(kind)), ("Use the example", lambda: example(kind))],
        [back_option()],
    ]).open()
    if linked_list is Nav.BACK:
        return Nav.BACK

    def show():
        render.linked_list(list(linked_list), doubly=kind.doubly)

    if kind.doubly:
        displays = [
            ("Display Forward", show),
            ("Display Backward", lambda: render.linked_list(linked_list.backward(), doubly=True, backward=True)),
        ]
    else:
        displays = [("Display", show)]

    return operation_menu(kind.name, [
        ("Insert at Beginning", lambda: insert(linked_list, show, "beginning")),
        ("Insert at Position", lambda: insert(linked_list, show, "position")),
        ("Insert at End", lambda: insert(linked_list, show, "end")),
        ("Delete from Beginning", lambda: delete(linked_list, show, "beginning")),
        ("Delete from Position", lambda: delete(linked_list, show, "position")),
        ("Delete from End", lambda: delete(linked_list, show, "end")),
        ("Search", lambda: search(linked_list)),
        *displays,
    ], definition=show_definition, new_label="New Linked List").run()


def create(kind):
    success(f"Created an empty {kind.name}.")
    return kind.list_class()


def example(kind):
    linked_list = kind.list_class()
    for item in EXAMPLE_ITEMS:
        linked_list.insert_at_end(item)
    success(f"Loaded the example {kind.name}.")
    render.linked_list(list(linked_list), doubly=kind.doubly)
    return linked_list


def ask_position():
    return ask_int("🔢 Which position?", "position")


def insert(linked_list, show, where):
    """Ask for an item and insert it at the beginning, at a position or at the end (where)."""
    position = ask_position() if where == "position" else None
    item = ask_value()
    try:
        if where == "beginning":
            linked_list.insert_at_beginning(item)
        elif where == "end":
            linked_list.insert_at_end(item)
        else:
            linked_list.insert_at_position(position, item)
    except OutOfBoundsError:
        error(f"Position {position} is out of bounds. Valid positions are 0 to {len(linked_list)}.")
        return
    place = f"position {position}" if where == "position" else f"the {where}"
    success(f"Inserted {fmt(item)} at {place}.")
    show()


def delete(linked_list, show, where):
    """Delete the node at the beginning, at a position or at the end (where)."""
    position = ask_position() if where == "position" else None
    try:
        if where == "beginning":
            item = linked_list.delete_from_beginning()
        elif where == "end":
            item = linked_list.delete_from_end()
        else:
            item = linked_list.delete_from_position(position)
    except EmptyError:
        error("The list is empty, so there's nothing to delete.")
        return
    except OutOfBoundsError:
        error(f"Position {position} is out of bounds. Valid positions are 0 to {len(linked_list) - 1}.")
        return
    place = f"position {position}" if where == "position" else f"the {where}"
    success(f"Deleted {fmt(item)} from {place}.")
    show()


def search(linked_list):
    """Explain linear search, then ask for a target and report its position."""
    render.explanation("How Linear Search Works on a Linked List", texts.LINKED_LIST_SEARCH_INFO)
    target = ask_value(what="target")
    position = linked_list.search(target)
    if position == -1:
        not_found(f"{fmt(target)} isn't in the list.")
    else:
        success(f"Found {fmt(target)} at position {position}.")
