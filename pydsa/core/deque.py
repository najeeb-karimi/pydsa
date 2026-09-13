"""Static, dynamically typed double-ended queue (deque) stored in a circular array."""

from pydsa.core.errors import CapacityError, EmptyError


class Deque:
    """Fixed-capacity deque that accepts elements of any type.

    Both ends wrap around the circular array, so no push or pop ever shifts items. As in the circular
    queue, a popped item stays in its slot until a later push overwrites it.
    """

    def __init__(self, capacity):
        """Initialize an empty deque that holds at most capacity items."""
        self.capacity = capacity
        self.slots = [None] * capacity
        self.front = 0  # Slot of the front item
        self.length = 0

    def __len__(self):
        return self.length

    def is_empty(self):
        """Return True if the deque is empty."""
        return self.length == 0

    def is_full(self):
        """Return True if the deque is full."""
        return self.length == self.capacity

    @property
    def back(self):
        """Slot of the back item; only meaningful while the deque isn't empty."""
        return (self.front + self.length - 1) % self.capacity

    def is_live(self, index):
        """Return True if the slot at index holds an item that is still in the deque."""
        return (index - self.front) % self.capacity < self.length

    def push_front(self, item):
        """Add an item before the front."""
        if self.is_full():
            raise CapacityError("Deque is full.")
        self.front = (self.front - 1) % self.capacity  # Step back, wrapping around to the end of the array
        self.slots[self.front] = item
        self.length += 1

    def push_back(self, item):
        """Add an item after the back."""
        if self.is_full():
            raise CapacityError("Deque is full.")
        self.slots[(self.front + self.length) % self.capacity] = item
        self.length += 1

    def pop_front(self):
        """Remove and return the front item."""
        item = self.peek_front()
        self.front = (self.front + 1) % self.capacity
        self.length -= 1
        return item

    def pop_back(self):
        """Remove and return the back item."""
        item = self.peek_back()
        self.length -= 1
        return item

    def peek_front(self):
        """Return the front item without removing it."""
        if self.is_empty():
            raise EmptyError("Deque is empty.")
        return self.slots[self.front]

    def peek_back(self):
        """Return the back item without removing it."""
        if self.is_empty():
            raise EmptyError("Deque is empty.")
        return self.slots[self.back]

    def to_list(self):
        """Return the items from front to back."""
        return [self.slots[(self.front + i) % self.capacity] for i in range(self.length)]
