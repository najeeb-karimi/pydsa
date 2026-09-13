"""Static, dynamically typed stack."""

from pydsa.core.errors import CapacityError, EmptyError


class Stack:
    """Fixed-capacity stack that accepts elements of any type."""

    def __init__(self, capacity):
        """Initialize an empty stack that holds at most capacity items."""
        self.capacity = capacity
        self.items = []

    def __len__(self):
        return len(self.items)

    def is_empty(self):
        """Return True if the stack is empty."""
        return not self.items

    def is_full(self):
        """Return True if the stack is full."""
        return len(self.items) == self.capacity

    def push(self, item):
        """Push an item onto the top of the stack."""
        if self.is_full():
            raise CapacityError("Stack is full.")
        self.items.append(item)

    def pop(self):
        """Remove and return the item at the top of the stack."""
        if self.is_empty():
            raise EmptyError("Stack is empty.")
        return self.items.pop()

    def peek(self):
        """Return the item at the top of the stack without removing it."""
        if self.is_empty():
            raise EmptyError("Stack is empty.")
        return self.items[-1]
