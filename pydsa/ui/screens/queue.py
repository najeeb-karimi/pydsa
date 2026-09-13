"""Queue screen."""

from pydsa.content import texts
from pydsa.core.errors import CapacityError, EmptyError
from pydsa.core.queue import Queue
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_item
from pydsa.ui.menu import Menu, operation_menu


def run():
    """Create a queue and run the queue operation menu."""
    render.intro(texts.QUEUE_ASCII, texts.QUEUE_DEFINITION)
    queue = Menu(
        "\n🛠️ Do you want to create a queue yourself or use the preloaded example?",
        [[("Create a queue", create), ("Use the example", example)]],
        bullet="●",
    ).select()

    return operation_menu("QUEUE", texts.QUEUE_DEFINITION, [
        ("Enqueue", lambda: enqueue(queue)),
        ("Dequeue", lambda: dequeue(queue)),
        ("Front", lambda: show_end(queue.get_front, "Front")),
        ("Rear", lambda: show_end(queue.get_rear, "Rear")),
        ("isEmpty", lambda: print(f"\n👉 isEmpty: {queue.is_empty()}.")),
        ("isFull", lambda: print(f"\n👉 isFull: {queue.is_full()}.")),
        ("Size Check", lambda: print(f"\n👉 Queue size: {len(queue)}/{queue.capacity}")),
        ("Displaying", lambda: render.queue_slots(queue)),
    ], new_label="New Queue", exit_label="Exit the Program").run()


def create():
    """Ask for the queue size and return an empty queue."""
    size = ask_int("\n↔️ Please specify the size of the queue.\n>>> ",
                   "\n❌ Invalid, the size can only be an integer!",
                   min_value=1, too_small="\n❌ Invalid, the size must be at least 1!")
    queue = Queue(size)
    print("\n✅ Here's your queue:", end="")
    render.queue_slots(queue)
    return queue


def example():
    """Return the preloaded example queue."""
    queue = Queue(5)
    print("\n✅ Here's an example queue with size 5:", end="")
    render.queue_slots(queue)
    return queue


def enqueue(queue):
    """Enqueue an item typed by the user."""
    item = ask_item()
    try:
        queue.enqueue(item)
    except CapacityError:
        print("\n🚫 Queue is full; item not enqueued.", end="")
    render.queue_slots(queue)


def dequeue(queue):
    """Dequeue the front item."""
    try:
        queue.dequeue()
    except EmptyError:
        print("\n🚫 Queue is empty.", end="")
    render.queue_slots(queue)


def show_end(get_item, name):
    """Show the front or rear item, using get_item to fetch it."""
    try:
        print(f"\n👉 {name} item: {get_item()}")
    except EmptyError:
        print("\n🚫 Queue is empty.")
