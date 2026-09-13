"""Stack screen."""

from pydsa.content import texts
from pydsa.core.errors import CapacityError, EmptyError
from pydsa.core.stack import Stack
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_item
from pydsa.ui.menu import Menu, operation_menu


def run():
    """Create a stack and run the stack operation menu."""
    render.intro(texts.STACK_ASCII, texts.STACK_DEFINITION)
    stack = Menu(
        "\n🛠️ Do you want to create a stack yourself or use the preloaded example?",
        [[("Create a stack", create), ("Use the example", example)]],
        bullet="●",
    ).select()

    return operation_menu("STACK", texts.STACK_DEFINITION, [
        ("Pushing", lambda: push(stack)),
        ("Popping", lambda: pop(stack)),
        ("Top/Peek", lambda: peek(stack)),
        ("isEmpty", lambda: print(f"\n👉 isEmpty: {stack.is_empty()}")),
        ("isFull", lambda: print(f"\n👉 isFull: {stack.is_full()}")),
        ("Size Check", lambda: print(f"\n👉 Stack size: {len(stack)}/{stack.capacity}")),
        ("Displaying", lambda: render.values(stack.items)),
    ], new_label="New Stack", exit_label="Exit the Program").run()


def create():
    """Ask for the stack size and return an empty stack."""
    size = ask_int("\n↔️ Please specify the size of the stack.\n>>> ",
                   "\n🚫 Invalid, the size can only be an integer!",
                   min_value=1, too_small="\n🚫 Invalid, the size must be at least 1!")
    stack = Stack(size)
    print("\n✅ Here's your stack:", end="")
    render.values(stack.items)
    return stack


def example():
    """Return the preloaded example stack."""
    stack = Stack(5)
    print("\n✅ Here's an example stack with size 5:", end="")
    stack.push(10)
    stack.push("Messi")
    render.values(stack.items)
    return stack


def push(stack):
    """Push an item typed by the user."""
    item = ask_item()
    try:
        stack.push(item)
    except CapacityError:
        print("\n🚫 Stack is full; item not pushed.", end="")
    render.values(stack.items)


def pop(stack):
    """Pop the top item and show what was removed."""
    try:
        item = stack.pop()
        print(f"\n👋 Item removed: {item}", end="")
    except EmptyError:
        print("\n🚫 Stack is empty.", end="")
    render.values(stack.items)


def peek(stack):
    """Show the top item."""
    try:
        print(f"\n👉 Top item: {stack.peek()}")
    except EmptyError:
        print("\n🚫 Stack is empty.")
