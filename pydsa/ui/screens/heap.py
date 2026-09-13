"""Heap screen: min heap, max heap and the priority queue built on the min heap."""

from typing import NamedTuple

from pydsa.content import complexity, texts
from pydsa.core.errors import EmptyError, NotFoundError
from pydsa.core.heap import MaxHeap, MinHeap
from pydsa.core.priority_queue import PriorityQueue
from pydsa.ui import render
from pydsa.ui.console import ask_int, ask_list, ask_value, error, info, not_found, plural, result, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import entry, fmt


class HeapKind(NamedTuple):
    """The class and wording for one kind of heap."""

    heap_class: type
    name: str
    root: str  # Which key sits at the root, as in "the smallest key"
    short: str  # As in "Extract Min"


MIN = HeapKind(MinHeap, "min heap", "smallest", "Min")
MAX = HeapKind(MaxHeap, "max heap", "largest", "Max")

EXAMPLE_KEYS = [50, 30, 10, 20, 70, 60, 80]
EXAMPLE_QUEUE = [("Fix bug", 1), ("Write docs", 3), ("Reply", 2), ("Deploy", 1)]


def show_definition():
    render.definition(texts.HEAP_DEFINITION, complexity.HEAP, complexity.PRIORITY_QUEUE)


def run():
    """Show the heap intro, let the user pick a heap or the priority queue and run its menu."""
    render.intro(texts.HEAP_ASCII, texts.HEAP_DEFINITION, complexity.HEAP, complexity.PRIORITY_QUEUE)
    return Menu("🧪 Which one do you want?", [
        [("Min Heap", lambda: heap_menu(MIN)),
         ("Max Heap", lambda: heap_menu(MAX)),
         ("Priority Queue (built on a min heap)", queue_menu)],
        [back_option()],
    ]).open()


# ---------------------------------------------------------------------------
# Min and max heaps
# ---------------------------------------------------------------------------

def heap_menu(kind):
    """Create a heap of the given kind and run its operation menu."""
    info(texts.HEAP_INFO)
    heap = Menu(f"🛠️ Do you want to create a {kind.name} yourself or use the preloaded example?", [
        [(f"Create a {kind.name}", lambda: create(kind)), ("Use the example", lambda: example(kind))],
        [back_option()],
    ]).open()
    if heap is Nav.BACK:
        return Nav.BACK

    return operation_menu(kind.name, [
        ("Insert", lambda: insert(heap)),
        (f"Extract {kind.short}", lambda: extract(heap, kind)),
        (f"Peek {kind.short}", lambda: peek(heap, kind)),
        ("Build from a List", lambda: build(heap, kind)),
        ("Level Order", lambda: level_order(heap)),
        ("Tree Stats", lambda: render.tree_stats(heap, "heap")),
        ("Display", lambda: render.heap(heap)),
    ], definition=show_definition, new_label="New Heap").run()


def create(kind):
    """Ask whether the heap holds numbers or strings and return an empty heap."""
    data_type = Menu(f"🤔 Which type of data do you want to store in the {kind.name}?", [
        [("Numbers (int or float)", lambda: "num"), ("Strings", lambda: "str")],
        [back_option()],
    ]).open()
    if data_type is Nav.BACK:
        return Nav.BACK
    success(f"Created an empty {kind.name} for {'numbers' if data_type == 'num' else 'strings'}.")
    return kind.heap_class(data_type)


def example(kind):
    """Return the preloaded example heap."""
    heap = kind.heap_class("num")
    heap.heapify(EXAMPLE_KEYS)
    keys = ", ".join(fmt(key) for key in EXAMPLE_KEYS[:-1])
    success(f"Loaded the example {kind.name}, built from {keys} and {fmt(EXAMPLE_KEYS[-1])}.")
    render.heap(heap)
    return heap


def insert(heap):
    key = ask_value(heap.data_type, "key")
    steps = heap.insert(key)
    success(f"Inserted {fmt(key)} with {plural(len(steps) - 1, 'swap')}.")
    render.heap_steps(steps, f"Added {fmt(key)} as the last leaf.")


def extract(heap, kind):
    try:
        key, steps = heap.extract()
    except EmptyError:
        error("The heap is empty, so there's nothing to extract.")
        return
    success(f"Extracted the {kind.root} key, {fmt(key)}.")
    if steps:
        render.heap_steps(steps, f"Moved the last leaf, {fmt(steps[0].items[0])}, to the root.")
    else:
        info("That was the only key, so the heap is empty now.")


def peek(heap, kind):
    try:
        result(f"The {kind.root} key is {fmt(heap.peek())}.")
    except EmptyError:
        error("The heap is empty, so there's nothing to peek at.")


def build(heap, kind):
    """Ask for a list of keys and heapify them, replacing the heap's keys."""
    keys = ask_list("✍️ Enter the keys, separated by commas (they replace the heap's current keys):", heap.data_type)
    steps = heap.heapify(keys)
    success(f"Built a {kind.name} from {plural(len(keys), 'key')} with {plural(len(steps) - 1, 'swap')}.")
    render.heap_steps(steps, "Started from the keys in the order you typed them.")


def level_order(heap):
    render.traversal("Level order", heap.level_order())
    if not heap.is_empty():
        info("In a heap, the level order is simply the array from left to right.")


# ---------------------------------------------------------------------------
# Priority queue
# ---------------------------------------------------------------------------

def queue_menu():
    """Create a priority queue and run its operation menu."""
    info(texts.PRIORITY_QUEUE_INFO)
    queue = Menu("🛠️ Do you want to start with an empty priority queue or use the preloaded example?", [
        [("Start with an empty priority queue", create_queue), ("Use the example", example_queue)],
        [back_option()],
    ]).open()
    if queue is Nav.BACK:
        return Nav.BACK

    return operation_menu("priority queue", [
        ("Enqueue", lambda: enqueue(queue)),
        ("Dequeue", lambda: dequeue(queue)),
        ("Peek", lambda: peek_queue(queue)),
        ("Change Priority", lambda: change_priority(queue)),
        ("Size", lambda: result(f"The priority queue holds {plural(len(queue), 'item')}.")),
        ("Display", lambda: render.priority_queue(queue)),
    ], definition=show_definition, new_label="New Heap").run()


def create_queue():
    success("Created an empty priority queue.")
    return PriorityQueue()


def example_queue():
    """Return the preloaded example priority queue."""
    queue = PriorityQueue()
    for item, priority in EXAMPLE_QUEUE:
        queue.enqueue(item, priority)
    success("Loaded the example priority queue.")
    info("'Deploy' has the same priority as 'Fix bug' but arrived later, so it's served second.")
    render.priority_queue(queue)
    return queue


def ask_priority():
    return ask_int("🔢 What's the priority? A smaller number is served first.", "priority")


def enqueue(queue):
    item = ask_value()
    priority = ask_priority()
    steps = queue.enqueue(item, priority)
    success(f"Enqueued {fmt(item)} with priority {priority}.")
    render.heap_steps(steps, f"Added {entry(steps[0].items[-1])} as the last leaf.", entry)


def dequeue(queue):
    try:
        item, priority, steps = queue.dequeue()
    except EmptyError:
        error("The priority queue is empty, so there's nothing to dequeue.")
        return
    success(f"Dequeued {fmt(item)}, which had priority {priority}.")
    if steps:
        render.heap_steps(steps, f"Moved the last leaf, {entry(steps[0].items[0])}, to the root.", entry)
    else:
        info("That was the only item, so the priority queue is empty now.")


def peek_queue(queue):
    try:
        item, priority = queue.peek()
    except EmptyError:
        error("The priority queue is empty, so there's nothing to peek at.")
        return
    result(f"The next item is {fmt(item)}, with priority {priority}.")


def change_priority(queue):
    item = ask_value()
    priority = ask_priority()
    try:
        old, steps = queue.change_priority(item, priority)
    except NotFoundError:
        not_found(f"{fmt(item)} isn't in the priority queue, so nothing changed.")
        return
    success(f"Changed the priority of {fmt(item)} from {old} to {priority}.")
    render.heap_steps(steps, f"Set the priority of {fmt(item)} to {priority}.", entry)
