"""Linked list screen: singly, doubly, singly circular and doubly circular linked lists."""

from typing import NamedTuple

from pydsa.content import texts
from pydsa.core.errors import EmptyError, OutOfBoundsError
from pydsa.core.linked_list import DoublyCircularLinkedList, DoublyLinkedList, SinglyCircularLinkedList, SinglyLinkedList
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_int, ask_value, error, info, not_found, plural, result, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt


class ListKind(NamedTuple):
    """The class and shape of one kind of linked list."""

    list_class: type
    name: str
    doubly: bool
    circular: bool
    guide: str  # The ID of its guide and topic


SINGLY = ListKind(SinglyLinkedList, "singly linked list", False, False, "singly-linked-list")
DOUBLY = ListKind(DoublyLinkedList, "doubly linked list", True, False, "doubly-linked-list")
SINGLY_CIRCULAR = ListKind(SinglyCircularLinkedList, "singly circular linked list", False, True, "singly-circular-linked-list")
DOUBLY_CIRCULAR = ListKind(DoublyCircularLinkedList, "doubly circular linked list", True, True, "doubly-circular-linked-list")

EXAMPLE_ITEMS = [10, "Messi", 2.5]


def run():
    """Show the linked list intro, let the user pick a kind of list and run its menu."""
    render.intro(texts.LINKED_LIST_ASCII, "linked-list")
    return Menu("🧪 Which type of linked list do you want?", [
        [(kind.name.title(), lambda kind=kind: list_menu(kind)) for kind in (SINGLY, DOUBLY, SINGLY_CIRCULAR, DOUBLY_CIRCULAR)],
        [back_option()],
    ]).open()


def run_kind(kind):
    """Show the linked list intro and run the menu of one kind of list, skipping the choice of kind."""
    render.intro(texts.LINKED_LIST_ASCII, "linked-list")
    return list_menu(kind)


def list_menu(kind):
    """Show the summary of a kind of linked list, then create one and run its operation menu."""
    render.summary(kind.guide)
    linked_list = Menu(f"🛠️ Do you want to start with an empty {kind.name} or use the preloaded example?", [
        [("Start with an empty list", lambda: create(kind)), ("Use the example", lambda: example(kind)),
         ("Fill with random values", lambda: fill_random(kind))],
        [back_option()],
    ]).open()
    if linked_list is Nav.BACK:
        return Nav.BACK

    def show():
        render.linked_list(list(linked_list), doubly=kind.doubly, circular=kind.circular)

    operations = [
        ("Insert at Beginning", lambda: insert(linked_list, show, "beginning")),
        ("Insert at Position", lambda: insert(linked_list, show, "position")),
        ("Insert at End", lambda: insert(linked_list, show, "end")),
        ("Delete from Beginning", lambda: delete(linked_list, show, "beginning")),
        ("Delete from Position", lambda: delete(linked_list, show, "position")),
        ("Delete from End", lambda: delete(linked_list, show, "end")),
        ("Search", lambda: search(linked_list)),
    ]
    if kind.doubly:
        operations += [
            ("Display Forward", show),
            ("Display Backward", lambda: render.linked_list(linked_list.backward(), doubly=True,
                                                            circular=kind.circular, backward=True)),
        ]
    else:
        operations.append(("Display", show))
    if kind.circular:
        operations.append(("Walk Around the Loop", lambda: walk(linked_list, kind)))

    return operation_menu(kind.name, operations, guides=[kind.guide, "linked-list"], new_label="New Linked List").run()


def create(kind):
    success(f"Created an empty {kind.name}.")
    return kind.list_class()


def example(kind):
    linked_list = kind.list_class()
    for item in EXAMPLE_ITEMS:
        linked_list.insert_at_end(item)
    success(f"Loaded the example {kind.name}.")
    render.linked_list(list(linked_list), doubly=kind.doubly, circular=kind.circular)
    return linked_list


def fill_random(kind):
    """Ask how many random nodes to add and return a list holding them."""
    count = random_data.ask_count("nodes")
    linked_list = kind.list_class()
    for item in random_data.values("any", count):
        linked_list.insert_at_end(item)
    success(f"Created a {kind.name} with {plural(count, 'random node')}.")
    render.linked_list(list(linked_list), doubly=kind.doubly, circular=kind.circular)
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
    render.explanation("linear-search")
    target = ask_value(what="target")
    position = linked_list.search(target)
    if position == -1:
        not_found(f"{fmt(target)} isn't in the list.")
    else:
        success(f"Found {fmt(target)} at position {position}.")


def walk(linked_list, kind):
    """Visit a chosen number of nodes around a circular list, in either direction for a doubly circular list."""
    if linked_list.is_empty():
        error("The list is empty, so there's nothing to walk around.")
        return
    backward = False
    if kind.doubly:
        backward = Menu("↔️ Which way do you want to walk?", [
            [("Forward, following the next links", lambda: False),
             ("Backward, following the prev links", lambda: True)],
            [back_option()],
        ]).select()
        if backward is Nav.BACK:
            return
    steps = ask_int("🔢 How many nodes do you want to visit?", "number of nodes", min_value=1)
    items = linked_list.walk(steps, backward=backward) if kind.doubly else linked_list.walk(steps)
    start = "tail" if backward else "head"
    result(f"Visited {plural(steps, 'node')} starting from the {start}: {' → '.join(fmt(item) for item in items)}")
    if steps > len(linked_list):
        info(f"The list only has {plural(len(linked_list), 'node')}, so the walk went around the loop more than once.")
