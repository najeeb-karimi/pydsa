"""Range aggregates over an array, with point replacement and optional immutable traces."""

from dataclasses import dataclass
from math import isfinite

from pydsa.algorithms.trace import record
from pydsa.core.errors import InvalidTypeError, OutOfBoundsError


def numbers(values):
    """Copy and validate the entire input before changing a tree."""
    values = list(values)
    for value in values:
        number(value)
    return values


def number(value):
    if type(value) not in (int, float) or isinstance(value, float) and not isfinite(value):
        raise InvalidTypeError("Values must be finite numbers, without booleans.")


def index(position, size):
    if type(position) is not int or not 0 <= position < size:
        raise OutOfBoundsError(f"The index must be a whole number from 0 to {size - 1}.")


def interval(left, right, size):
    index(left, size)
    index(right, size)
    if left > right:
        raise OutOfBoundsError("The range start must not be greater than its end.")


@dataclass
class SegmentNode:
    low: int
    high: int
    value: int | float | None = None
    left: "SegmentNode | None" = None
    right: "SegmentNode | None" = None


def snapshot(node):
    if node is None:
        return None
    return node.low, node.high, node.value, snapshot(node.left), snapshot(node.right)


class SegmentTree:
    """Inclusive zero-based ranges; the aggregation is fixed at creation."""

    def __init__(self, values=(), operation="sum"):
        if operation not in ("sum", "min", "max"):
            raise ValueError("The operation must be sum, min or max.")
        self.operation = operation
        self._combine = {"sum": lambda a, b: a + b, "min": min, "max": max}[operation]
        self.build(values)

    @property
    def items(self):
        return list(self._items)

    def __len__(self):
        return len(self._items)

    def _record(self, trace, kind, node, **data):
        if trace is not None:
            record(trace, kind, snapshot(self.root), {(node.low, node.high): kind.removeprefix("sg_")},
                   low=node.low, high=node.high, **data)

    def build(self, values, trace=None):
        """Build leaves from a validated copy, combining children from the bottom up."""
        values = numbers(values)
        self._items = values
        self.root = SegmentNode(0, len(values) - 1) if values else None

        def fill(node):
            if node.low == node.high:
                node.value = values[node.low]
                self._record(trace, "sg_leaf", node, value=node.value)
            else:
                middle = (node.low + node.high) // 2
                node.left = SegmentNode(node.low, middle)
                node.right = SegmentNode(middle + 1, node.high)
                fill(node.left)
                fill(node.right)
                node.value = self._combine(node.left.value, node.right.value)
                self._record(trace, "sg_combine", node, value=node.value, operation=self.operation)
        if self.root is not None:
            fill(self.root)

    def query(self, left, right, trace=None):
        """Combine fully covered nodes, descending only through partial overlaps."""
        interval(left, right, len(self))

        def visit(node):
            if node.high < left or node.low > right:
                self._record(trace, "sg_outside", node)
                return None
            if left <= node.low and node.high <= right:
                self._record(trace, "sg_inside", node, value=node.value)
                return node.value
            self._record(trace, "sg_partial", node)
            a, b = visit(node.left), visit(node.right)
            return b if a is None else a if b is None else self._combine(a, b)
        value = visit(self.root)
        self._record(trace, "sg_result", self.root, left=left, right=right, value=value, operation=self.operation)
        return value

    def update(self, position, value, trace=None):
        """Replace one array value and recompute just its ancestors."""
        index(position, len(self))
        number(value)
        self._items[position] = value
        node, parents = self.root, []
        while node.low != node.high:
            self._record(trace, "sg_descend", node, index=position)
            parents.append(node)
            node = node.left if position <= node.left.high else node.right
        node.value = value
        self._record(trace, "sg_leaf", node, value=value)
        for node in reversed(parents):
            node.value = self._combine(node.left.value, node.right.value)
            self._record(trace, "sg_combine", node, value=node.value, operation=self.operation)
