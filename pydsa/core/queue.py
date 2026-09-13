"""Static, dynamically typed circular queue."""

from pydsa.core.errors import CapacityError, EmptyError


class Queue:
    """Fixed-capacity circular queue that accepts elements of any type.

    Like a real circular buffer, a dequeued item stays in its slot until a later enqueue overwrites
    it, so the console can still show it (struck out) next to the live items.
    """

    def __init__(self, capacity):
        """Initialize an empty queue that holds at most capacity items."""
        self.capacity = capacity
        self.slots = [None] * capacity
        self.front = 0
        self.rear = -1
        self.length = 0

    def __len__(self):
        return self.length

    def is_empty(self):
        """Return True if the queue is empty."""
        return self.length == 0

    def is_full(self):
        """Return True if the queue is full."""
        return self.length == self.capacity

    def is_live(self, index):
        """Return True if the slot at index holds an item that is still in the queue."""
        return (index - self.front) % self.capacity < self.length

    def enqueue(self, item):
        """Add an item at the rear of the queue."""
        if self.is_full():
            raise CapacityError("Queue is full.")
        self.rear = (self.rear + 1) % self.capacity  # Wrap around to the start when the end is reached
        self.slots[self.rear] = item
        self.length += 1

    def dequeue(self):
        """Remove and return the item at the front of the queue."""
        if self.is_empty():
            raise EmptyError("Queue is empty.")
        item = self.slots[self.front]
        self.front = (self.front + 1) % self.capacity
        self.length -= 1
        return item

    def get_front(self):
        """Return the item at the front of the queue."""
        if self.is_empty():
            raise EmptyError("Queue is empty.")
        return self.slots[self.front]

    def get_rear(self):
        """Return the item at the rear of the queue."""
        if self.is_empty():
            raise EmptyError("Queue is empty.")
        return self.slots[self.rear]

    def to_list(self):
        """Return the live items from front to rear."""
        return [self.slots[(self.front + i) % self.capacity] for i in range(self.length)]
