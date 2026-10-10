"""Sorted multiset with seeded geometric levels and traced express-lane searches."""

import random
from math import isfinite

from pydsa.algorithms.trace import record
from pydsa.core.errors import InvalidTypeError, NotFoundError
from pydsa.core.tree import DATA_TYPES


class SkipNode:
    def __init__(self, key, level, identity):
        self.key, self.identity = key, identity
        self.forward = [None] * level


class SkipList:
    def __init__(self, data_type="num", seed=0, max_level=32):
        if data_type not in DATA_TYPES:
            raise ValueError("Keys must be numbers or strings.")
        if type(seed) is not int:
            raise ValueError("The seed must be an integer.")
        if type(max_level) is not int or not 1 <= max_level <= 64:
            raise ValueError("The maximum level must be an integer from 1 to 64.")
        self.data_type, self.seed, self.max_level = data_type, seed, max_level
        self.rng = random.Random(seed)
        self.head = SkipNode(None, max_level, 0)
        self.level = 1
        self._count, self._identity = 0, 0

    def __len__(self):
        return self._count

    def __iter__(self):
        node = self.head.forward[0]
        while node is not None:
            yield node.key
            node = node.forward[0]

    def _check(self, key):
        if (not isinstance(key, DATA_TYPES[self.data_type]) or isinstance(key, bool)
                or isinstance(key, float) and not isfinite(key)):
            raise InvalidTypeError(f"Skip-list keys must be finite {self.data_type} values, without booleans.")

    def snapshot(self):
        rows, node = [], self.head.forward[0]
        while node is not None:
            rows.append((node.identity, node.key, len(node.forward)))
            node = node.forward[0]
        lanes = []
        for level in range(self.level):
            lane, node = [], self.head.forward[level]
            while node is not None:
                lane.append(node.identity)
                node = node.forward[level]
            lanes.append(tuple(lane))
        return tuple(rows), tuple(lanes)

    def _record(self, trace, kind, at=None, **data):
        if trace is not None:
            record(trace, kind, self.snapshot(), {at.identity: "checked"} if at else None, **data)

    def _path(self, key, trace):
        previous = [self.head] * self.max_level
        node = self.head
        for level in range(self.level - 1, -1, -1):
            while node.forward[level] is not None and node.forward[level].key < key:
                following = node.forward[level]
                self._record(trace, "sk_right", following, node="HEAD" if node is self.head else node.key,
                             key=following.key, level=level + 1)
                node = following
            previous[level] = node
            if level:
                self._record(trace, "sk_down", node, level=level + 1, next=level)
        return previous

    def search(self, key, trace=None):
        """Return the first matching node, or None, after moving right and down."""
        self._check(key)
        node = self._path(key, trace)[0].forward[0]
        found = node is not None and node.key == key
        self._record(trace, "sk_found" if found else "sk_missing", node if found else None, key=key)
        return node if found else None

    def _random_level(self, key, trace):
        level = 1
        while level < self.max_level:
            heads = self.rng.random() < 0.5
            self._record(trace, "sk_flip", key=key, outcome="heads" if heads else "tails",
                         level=level, next=level + 1 if heads else level)
            if not heads:
                break
            level += 1
        if level == self.max_level:
            self._record(trace, "sk_cap", key=key, level=level)
        return level

    def insert(self, key, trace=None):
        """Retain duplicates, flipping a seeded coin for each promotion."""
        self._check(key)
        previous = self._path(key, trace)
        height = self._random_level(key, trace)
        self.level = max(self.level, height)
        self._identity += 1
        node = SkipNode(key, height, self._identity)
        # Link the base first so every traced upper-lane node exists in the base snapshot.
        for level in range(height):
            node.forward[level] = previous[level].forward[level]
            previous[level].forward[level] = node
            self._record(trace, "sk_link", node, key=key, level=level + 1)
        self._count += 1
        return node

    def delete(self, key, trace=None):
        """Remove one occurrence from every lane containing it."""
        self._check(key)
        previous = self._path(key, trace)
        node = previous[0].forward[0]
        if node is None or node.key != key:
            self._record(trace, "sk_missing", key=key)
            raise NotFoundError(f"Key {key!r} is not in the skip list.")
        for level in range(len(node.forward) - 1, -1, -1):
            previous[level].forward[level] = node.forward[level]
            self._record(trace, "sk_unlink", key=key, level=level + 1)
        self._count -= 1
        old_level = self.level
        while self.level > 1 and self.head.forward[self.level - 1] is None:
            self.level -= 1
        if self.level != old_level:
            self._record(trace, "sk_shrink", level=self.level)
        return key
