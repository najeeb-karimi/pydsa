"""Stack screen."""

from pydsa.content import texts
from pydsa.core.errors import CapacityError, EmptyError
from pydsa.core.stack import Stack
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_int, ask_item, error, plural, result, success, yes_no
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt


def run():
    """Create a stack and run the stack operation menu."""
    render.intro(texts.STACK_ASCII, "stack")
    stack = Menu("🛠️ Do you want to create a stack yourself or use the preloaded example?", [
        [("Create a stack", create), ("Use the example", example), ("Fill with random values", fill_random)],
        [back_option()],
    ]).open()
    if stack is Nav.BACK:
        return Nav.BACK

    return operation_menu("stack", [
        ("Push", lambda: push(stack)),
        ("Pop", lambda: pop(stack)),
        ("Peek", lambda: peek(stack)),
        ("Check if Empty", lambda: result(f"Is the stack empty? {yes_no(stack.is_empty())}.")),
        ("Check if Full", lambda: result(f"Is the stack full? {yes_no(stack.is_full())}.")),
        ("Size", lambda: result(f"The stack holds {len(stack)} of {plural(stack.capacity, 'item')}.")),
        ("Display", lambda: render.stack(stack)),
    ], guides=["stack"], new_label="New Stack").run()


def create():
    """Ask for the capacity and return an empty stack."""
    capacity = ask_int("↔️ How many items should the stack be able to hold?", "size", min_value=1)
    stack = Stack(capacity)
    success(f"Created an empty stack that holds up to {plural(capacity, 'item')}.")
    render.stack(stack)
    return stack


def example():
    """Return the preloaded example stack."""
    stack = Stack(5)
    stack.push(10)
    stack.push("Messi")
    success("Loaded the example stack.")
    render.stack(stack)
    return stack


def fill_random():
    """Ask for the capacity and the number of random items, and return a stack holding them."""
    capacity, count = random_data.ask_capacity_and_count("stack")
    stack = Stack(capacity)
    for item in random_data.values("any", count):
        stack.push(item)
    success(f"Created a stack that holds up to {plural(capacity, 'item')}, with {plural(count, 'random item')} pushed onto it.")
    render.stack(stack)
    return stack


def push(stack):
    item = ask_item()
    try:
        stack.push(item)
    except CapacityError:
        error(f"The stack is full, so {fmt(item)} wasn't pushed.")
        return
    success(f"Pushed {fmt(item)} onto the stack.")
    render.stack(stack)


def pop(stack):
    try:
        item = stack.pop()
    except EmptyError:
        error("The stack is empty, so there's nothing to pop.")
        return
    success(f"Popped {fmt(item)} from the top.")
    render.stack(stack)


def peek(stack):
    try:
        result(f"The top item is {fmt(stack.peek())}.")
    except EmptyError:
        error("The stack is empty, so there's nothing to peek at.")
