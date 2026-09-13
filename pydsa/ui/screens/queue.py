"""Queue screen."""

from pydsa.content import complexity, texts
from pydsa.core.errors import CapacityError, EmptyError
from pydsa.core.queue import Queue
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_int, ask_item, error, plural, result, success, yes_no
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt


def show(queue):
    render.circular_slots(queue, {"front": queue.front, "rear": queue.rear})


def run():
    """Create a queue and run the queue operation menu."""
    render.intro(texts.QUEUE_ASCII, texts.QUEUE_DEFINITION, complexity.QUEUE)
    queue = Menu("🛠️ Do you want to create a queue yourself or use the preloaded example?", [
        [("Create a queue", create), ("Use the example", example), ("Fill with random values", fill_random)],
        [back_option()],
    ]).open()
    if queue is Nav.BACK:
        return Nav.BACK

    return operation_menu("queue", [
        ("Enqueue", lambda: enqueue(queue)),
        ("Dequeue", lambda: dequeue(queue)),
        ("Peek Front", lambda: peek(queue.get_front, "front")),
        ("Peek Rear", lambda: peek(queue.get_rear, "rear")),
        ("Check if Empty", lambda: result(f"Is the queue empty? {yes_no(queue.is_empty())}.")),
        ("Check if Full", lambda: result(f"Is the queue full? {yes_no(queue.is_full())}.")),
        ("Size", lambda: result(f"The queue holds {len(queue)} of {plural(queue.capacity, 'item')}.")),
        ("Display", lambda: show(queue)),
    ], definition=lambda: render.definition(texts.QUEUE_DEFINITION, complexity.QUEUE), new_label="New Queue").run()


def create():
    """Ask for the capacity and return an empty queue."""
    capacity = ask_int("↔️ How many items should the queue be able to hold?", "size", min_value=1)
    queue = Queue(capacity)
    success(f"Created an empty queue that holds up to {plural(capacity, 'item')}.")
    show(queue)
    return queue


def example():
    """Return the preloaded example queue."""
    queue = Queue(5)
    for item in (10, "Messi", 2.5):
        queue.enqueue(item)
    queue.dequeue()
    success("Loaded the example queue. Its first item, 10, was already dequeued.")
    show(queue)
    return queue


def fill_random():
    """Ask for the capacity and the number of random items, and return a queue holding them."""
    capacity, count = random_data.ask_capacity_and_count("queue")
    queue = Queue(capacity)
    for item in random_data.values("any", count):
        queue.enqueue(item)
    success(f"Created a queue that holds up to {plural(capacity, 'item')}, with {plural(count, 'random item')} enqueued.")
    show(queue)
    return queue


def enqueue(queue):
    item = ask_item()
    try:
        queue.enqueue(item)
    except CapacityError:
        error(f"The queue is full, so {fmt(item)} wasn't enqueued.")
        return
    success(f"Enqueued {fmt(item)} at the rear.")
    show(queue)


def dequeue(queue):
    try:
        item = queue.dequeue()
    except EmptyError:
        error("The queue is empty, so there's nothing to dequeue.")
        return
    success(f"Dequeued {fmt(item)} from the front.")
    show(queue)


def peek(get_item, end):
    """Show the item at the front or rear (end), using get_item to fetch it."""
    try:
        result(f"The {end} item is {fmt(get_item())}.")
    except EmptyError:
        error("The queue is empty, so there's nothing to peek at.")
