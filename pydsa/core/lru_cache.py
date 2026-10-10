"""Least-recently-used cache using the existing chaining table and doubly linked nodes."""

from math import isfinite

from pydsa.algorithms.trace import record
from pydsa.core.errors import InvalidTypeError, NotFoundError
from pydsa.core.hash_table import ChainingHashTable
from pydsa.core.linked_list import DLLNode, DoublyLinkedList


class LRUCache:
    def __init__(self, capacity=3):
        if type(capacity) is not int or capacity < 1:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        self.table = ChainingHashTable(2 * capacity + 1)
        self.order = DoublyLinkedList()
        self.tail = None
        self._count = 0

    def __len__(self):
        return self._count

    def items(self):
        """Return key-value pairs from most to least recently used."""
        return list(self.order)

    def snapshot(self):
        buckets = tuple(tuple(node.data for _, node in bucket) for bucket in self.table.table)
        return buckets, tuple(self.order), self.capacity

    def _record(self, trace, kind, key, **data):
        if trace is not None:
            record(trace, kind, self.snapshot(), {key: "checked"}, key=key, **data)

    def _unlink(self, node):
        """Unlink a known node without searching through the list."""
        if node.prev is None:
            self.order.head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        node.prev = node.next = None

    def _prepend(self, node):
        node.next = self.order.head
        if node.next is not None:
            node.next.prev = node
        else:
            self.tail = node
        self.order.head = node

    def _recent(self, node, trace):
        if node is not self.order.head:
            self._unlink(node)
            self._prepend(node)
            self._record(trace, "lru_recent", node.data[0])
        else:
            self._record(trace, "lru_stays", node.data[0])

    def _bucket(self, key):
        if isinstance(key, float) and not isfinite(key):
            raise InvalidTypeError("Numeric cache keys must be finite.")
        return self.table.hash_function(key)

    def get(self, key, trace=None):
        """Return a value and mark its key most recent; a miss does not change the cache."""
        bucket = self._bucket(key)
        self._record(trace, "lru_lookup", key, index=bucket)
        try:
            _, node = self.table.lookup(key)
        except NotFoundError:
            self._record(trace, "lru_miss", key)
            raise
        self._record(trace, "lru_hit", key, value=node.data[1])
        self._recent(node, trace)
        return node.data[1]

    def put(self, key, value, trace=None):
        """Insert or replace a key, evicting the tail only for a new key at capacity."""
        bucket = self._bucket(key)  # Validate the key before evicting anything.
        self._record(trace, "lru_lookup", key, index=bucket)
        try:
            _, node = self.table.lookup(key)
        except NotFoundError:
            node = None
        if node is not None:
            node.data = (node.data[0], value)
            self._record(trace, "lru_replace", key, value=value)
            self._recent(node, trace)
            return None
        evicted = None
        if len(self) == self.capacity:
            evicted = self.tail.data
            self.table.delete(evicted[0])
            self._unlink(self.tail)
            self._count -= 1
            self._record(trace, "lru_evict", evicted[0], value=evicted[1])
        node = DLLNode((key, value))
        self._prepend(node)
        self.table.insert(key, node)
        self._count += 1
        self._record(trace, "lru_put", key, value=value)
        return evicted
