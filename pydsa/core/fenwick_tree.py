"""A linear-built Fenwick tree: zero-based public indexes, one-based binary jumps."""

from pydsa.algorithms.trace import record
from pydsa.core.errors import OutOfBoundsError
from pydsa.core.segment_tree import index, interval, number, numbers


class FenwickTree:
    """Store sums of blocks ending at i, whose size is the lowest set bit of i."""

    def __init__(self, values=()):
        self.build(values)

    @property
    def items(self):
        return list(self._items)

    @property
    def blocks(self):
        return list(self._blocks)

    def __len__(self):
        return len(self._items)

    def _record(self, trace, kind, i=None, **data):
        if trace is not None:
            if i is not None:
                bit = i & -i
                width = max(1, (len(self) + 1).bit_length())
                data.update(i=i, binary=format(i, f"0{width}b"), bit=bit, bit_binary=format(bit, f"0{width}b"))
                if "next" in data:
                    data["next_binary"] = format(data["next"], f"0{width}b")
            record(trace, kind, (tuple(self._items), tuple(self._blocks)), {i: kind} if i else None, **data)

    def build(self, values, trace=None):
        """Initialize each block with its item, then pass completed blocks to their parents."""
        self._items = numbers(values)
        self._blocks = [0, *self._items]
        for i in range(1, len(self) + 1):
            self._record(trace, "fw_block", i, value=self._blocks[i])
            parent = i + (i & -i)
            if parent <= len(self):
                self._blocks[parent] += self._blocks[i]
                self._record(trace, "fw_build_jump", i, next=parent, value=self._blocks[i])

    def prefix_sum(self, end, trace=None):
        """Sum indexes 0 through end; -1 represents the empty prefix."""
        if type(end) is not int or not -1 <= end < len(self):
            raise OutOfBoundsError(f"The prefix end must be a whole number from -1 to {len(self) - 1}.")
        i, total = end + 1, 0
        while i > 0:
            total += self._blocks[i]
            self._record(trace, "fw_take", i, value=self._blocks[i], total=total)
            following = i - (i & -i)
            self._record(trace, "fw_query_jump", i, next=following)
            i = following
        self._record(trace, "fw_prefix", end=end, total=total)
        return total

    def range_sum(self, left, right, trace=None):
        """Subtract the prefix before left from the prefix ending at right."""
        interval(left, right, len(self))
        a = self.prefix_sum(right, trace)
        b = self.prefix_sum(left - 1, trace)
        total = a - b
        self._record(trace, "fw_range", left=left, right=right, a=a, b=b, total=total)
        return total

    def update(self, position, value, trace=None):
        """Replace an item, adding the difference to each block that contains it."""
        index(position, len(self))
        number(value)
        old = self._items[position]
        delta = value - old
        self._items[position] = value
        i = position + 1
        while i <= len(self):
            # Subtract first so a large old value does not swallow a small replacement
            # when computing the difference (especially for a single-value block).
            self._blocks[i] = (self._blocks[i] - old) + value
            self._record(trace, "fw_add", i, delta=delta, value=self._blocks[i])
            following = i + (i & -i)
            self._record(trace, "fw_update_jump", i, next=following)
            i = following
