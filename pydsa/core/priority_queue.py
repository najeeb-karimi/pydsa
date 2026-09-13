"""Priority queue built on the min heap."""

from itertools import count
from typing import Any, NamedTuple

from pydsa.core.errors import EmptyError, NotFoundError
from pydsa.core.heap import MinHeap


class Entry(NamedTuple):
    """An item waiting in the priority queue.

    Entries compare by priority first and then by arrival order, which is unique, so items themselves are
    never compared and equal priorities are served first-in first-out.
    """

    priority: int | float
    order: int
    item: Any


class PriorityQueue:
    """Priority queue where a smaller priority number is served first."""

    def __init__(self):
        self.heap = MinHeap()
        self._arrivals = count()

    def __len__(self):
        return len(self.heap)

    def is_empty(self):
        return self.heap.is_empty()

    def enqueue(self, item, priority):
        """Add item with the given priority; return the heap steps."""
        return self.heap.insert(Entry(priority, next(self._arrivals), item))

    def dequeue(self):
        """Remove the item served next; return it, its priority and the heap steps."""
        if self.heap.is_empty():
            raise EmptyError("The priority queue is empty.")
        entry, steps = self.heap.extract()
        return entry.item, entry.priority, steps

    def peek(self):
        """Return the item served next and its priority, without removing it."""
        if self.heap.is_empty():
            raise EmptyError("The priority queue is empty.")
        entry = self.heap.peek()
        return entry.item, entry.priority

    def change_priority(self, item, priority):
        """Give item a new priority, keeping its place among equal priorities; return the old priority and the steps.

        If item was added more than once, the copy that arrived first is changed.
        """
        matches = [index for index, entry in enumerate(self.heap.items) if entry.item == item]
        if not matches:
            raise NotFoundError(f"{item!r} isn't in the priority queue.")
        index = min(matches, key=lambda index: self.heap.items[index].order)
        entry = self.heap.items[index]
        return entry.priority, self.heap.update(index, entry._replace(priority=priority))

    def in_order(self):
        """Return the entries in the order they will be served."""
        return sorted(self.heap.items)
