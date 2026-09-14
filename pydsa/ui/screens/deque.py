"""Deque screen."""

from pydsa.content import texts
from pydsa.core.deque import Deque
from pydsa.core.errors import CapacityError, EmptyError
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_int, ask_item, error, plural, result, success, yes_no
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt


def show(deque):
    render.circular_slots(deque, {"front": deque.front, "back": deque.back})


def run():
    """Create a deque and run the deque operation menu."""
    render.intro(texts.DEQUE_ASCII, "deque")
    deque = Menu("🛠️ Do you want to create a deque yourself or use the preloaded example?", [
        [("Create a deque", create), ("Use the example", example), ("Fill with random values", fill_random)],
        [back_option()],
    ]).open()
    if deque is Nav.BACK:
        return Nav.BACK

    return operation_menu("deque", [
        ("Push Front", lambda: push(deque, "front")),
        ("Push Back", lambda: push(deque, "back")),
        ("Pop Front", lambda: pop(deque, "front")),
        ("Pop Back", lambda: pop(deque, "back")),
        ("Peek Front", lambda: peek(deque, "front")),
        ("Peek Back", lambda: peek(deque, "back")),
        ("Check if Empty", lambda: result(f"Is the deque empty? {yes_no(deque.is_empty())}.")),
        ("Check if Full", lambda: result(f"Is the deque full? {yes_no(deque.is_full())}.")),
        ("Size", lambda: result(f"The deque holds {len(deque)} of {plural(deque.capacity, 'item')}.")),
        ("Display", lambda: show(deque)),
    ], guides=["deque"], new_label="New Deque").run()


def create():
    """Ask for the capacity and return an empty deque."""
    capacity = ask_int("↔️ How many items should the deque be able to hold?", "size", min_value=1)
    deque = Deque(capacity)
    success(f"Created an empty deque that holds up to {plural(capacity, 'item')}.")
    show(deque)
    return deque


def example():
    """Return the preloaded example deque."""
    deque = Deque(6)
    deque.push_back(10)
    deque.push_back("Messi")
    deque.push_front(2.5)
    success("Loaded the example deque. Pushing 2.5 onto the front wrapped it around to the last slot.")
    show(deque)
    return deque


def fill_random():
    """Ask for the capacity and the number of random items, and return a deque holding them."""
    capacity, count = random_data.ask_capacity_and_count("deque")
    deque = Deque(capacity)
    for item in random_data.values("any", count):
        deque.push_back(item)
    success(f"Created a deque that holds up to {plural(capacity, 'item')}, with {plural(count, 'random item')} pushed onto the back.")
    show(deque)
    return deque


def push(deque, end):
    """Push an item typed by the user onto the front or back (end)."""
    item = ask_item()
    try:
        getattr(deque, f"push_{end}")(item)
    except CapacityError:
        error(f"The deque is full, so {fmt(item)} wasn't pushed.")
        return
    success(f"Pushed {fmt(item)} onto the {end}.")
    show(deque)


def pop(deque, end):
    """Pop the item at the front or back (end)."""
    try:
        item = getattr(deque, f"pop_{end}")()
    except EmptyError:
        error("The deque is empty, so there's nothing to pop.")
        return
    success(f"Popped {fmt(item)} from the {end}.")
    show(deque)


def peek(deque, end):
    """Show the item at the front or back (end)."""
    try:
        result(f"The {end} item is {fmt(getattr(deque, f'peek_{end}')())}.")
    except EmptyError:
        error("The deque is empty, so there's nothing to peek at.")
