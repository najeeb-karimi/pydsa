"""Binary min heap and max heap stored in an array."""

from typing import NamedTuple

from pydsa.core.errors import EmptyError, InvalidTypeError
from pydsa.core.tree import DATA_TYPES


class HeapStep(NamedTuple):
    """A snapshot of the heap's array during an operation.

    moved holds the indexes to point out: the key that was just placed, or the two keys that were just swapped,
    as (where the sifting key was, where it went).
    """

    items: list
    moved: tuple = ()


class Heap:
    """Binary heap stored in a list; subclasses decide which of two keys belongs closer to the root.

    The children of the node at index i are at 2i + 1 and 2i + 2, and its parent is at (i - 1) // 2.
    Operations that move keys return the list of HeapSteps they went through.
    """

    kind = None  # "min" or "max"

    def __init__(self, data_type=None):
        """Initialize an empty heap of "num" (int or float) or "str" keys; None accepts any comparable keys."""
        if data_type is not None and data_type not in DATA_TYPES:
            raise ValueError(f"data_type must be one of: {', '.join(DATA_TYPES)}")
        self.data_type = data_type
        self.items = []

    def _above(self, a, b):
        """Return True if key a must sit above key b."""
        raise NotImplementedError

    def check_type(self, key):
        """Raise InvalidTypeError if key doesn't match the heap's data type."""
        if self.data_type is not None and not isinstance(key, DATA_TYPES[self.data_type]):
            raise InvalidTypeError(f"This heap only holds {self.data_type} keys.")

    def __len__(self):
        return len(self.items)

    def is_empty(self):
        return not self.items

    def peek(self):
        """Return the root key without removing it."""
        if not self.items:
            raise EmptyError("The heap is empty.")
        return self.items[0]

    def insert(self, key):
        """Add key as the last leaf and sift it up; return the steps."""
        self.check_type(key)
        self.items.append(key)
        return [self._snapshot((len(self.items) - 1,))] + self._sift_up(len(self.items) - 1)

    def extract(self):
        """Remove and return the root key and the steps: the last leaf moves to the root and sifts down."""
        root = self.peek()
        last = self.items.pop()
        if not self.items:
            return root, []
        self.items[0] = last
        return root, [self._snapshot((0,))] + self._sift_down(0)

    def heapify(self, keys):
        """Replace the heap's keys with keys and sift down every parent, from the last one to the root; return the steps."""
        keys = list(keys)
        for key in keys:
            self.check_type(key)
        self.items = keys
        steps = [self._snapshot()]
        for index in range(len(self.items) // 2 - 1, -1, -1):
            steps += self._sift_down(index)
        return steps

    def update(self, index, key):
        """Replace the key at index and sift it up or down to its place; return the steps."""
        self.check_type(key)
        self.items[index] = key
        steps = [self._snapshot((index,))]
        if index and self._above(key, self.items[(index - 1) // 2]):
            return steps + self._sift_up(index)
        return steps + self._sift_down(index)

    def _snapshot(self, moved=()):
        return HeapStep(list(self.items), moved)

    def _swap(self, index, other):
        """Swap the sifting key at index with the key at other and return the step."""
        self.items[index], self.items[other] = self.items[other], self.items[index]
        return self._snapshot((index, other))

    def _sift_up(self, index):
        steps = []
        while index:
            parent = (index - 1) // 2
            if not self._above(self.items[index], self.items[parent]):
                break
            steps.append(self._swap(index, parent))
            index = parent
        return steps

    def _sift_down(self, index):
        steps = []
        while True:
            top = index
            for child in (2 * index + 1, 2 * index + 2):
                if child < len(self.items) and self._above(self.items[child], self.items[top]):
                    top = child
            if top == index:
                return steps
            steps.append(self._swap(index, top))
            index = top

    # Tree extras: a heap is a complete binary tree, so its shape follows from its size alone

    def level_order(self):
        """Return the keys level by level, which is simply the array's order."""
        return list(self.items)

    def height(self):
        """Return the number of levels."""
        return len(self.items).bit_length()

    def leaf_count(self):
        """Return the number of leaves: every node from index n // 2 on has no children."""
        return len(self.items) - len(self.items) // 2

    def _leaves(self):
        if not self.items:
            raise EmptyError("The heap is empty.")
        return self.items[len(self.items) // 2:]


class MinHeap(Heap):
    """Heap whose root holds the smallest key."""

    kind = "min"

    def _above(self, a, b):
        return a < b

    def min(self):
        return self.peek()

    def max(self):
        """The largest key is always a leaf, so only the leaves are checked."""
        return max(self._leaves())


class MaxHeap(Heap):
    """Heap whose root holds the largest key."""

    kind = "max"

    def _above(self, a, b):
        return a > b

    def min(self):
        """The smallest key is always a leaf, so only the leaves are checked."""
        return min(self._leaves())

    def max(self):
        return self.peek()
