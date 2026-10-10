"""Deterministic salted SHA-256 Bloom filter; membership is possible, never proof."""

from hashlib import sha256
from math import expm1

from pydsa.algorithms.trace import record
from pydsa.core.errors import InvalidTypeError


class BloomFilter:
    """Store strings in m bits with k independent salts; deleting bits is unsupported."""

    def __init__(self, m=64, k=3):
        if type(m) is not int or m < 1 or type(k) is not int or k < 1:
            raise ValueError("Bit count m and hash count k must be positive integers.")
        self.m, self.k = m, k
        self._bits = bytearray(m)
        self.additions = 0

    @property
    def bits(self):
        return tuple(self._bits)

    def positions(self, item):
        """Hash each UTF-8 string with a fixed domain and its hash-number salt."""
        if not isinstance(item, str):
            raise InvalidTypeError("Bloom-filter items must be strings.")
        encoded = item.encode("utf-8")
        return tuple(int.from_bytes(sha256(b"PyDSA-Bloom-v1:" + str(i).encode("ascii") + b":" + encoded).digest(),
                                    "big") % self.m for i in range(self.k))

    def snapshot(self):
        return self.bits, self.m, self.k, self.additions

    def _record(self, trace, kind, at=None, **data):
        if trace is not None:
            record(trace, kind, self.snapshot(), {at: "checked"} if at is not None else None, **data)

    def add(self, item, trace=None):
        """Set each salted hash position; existing bits stay set even for repeated adds."""
        positions = self.positions(item)
        for salt, at in enumerate(positions, 1):
            already = bool(self._bits[at])
            self._bits[at] = 1
            self._record(trace, "bf_set", at, item=item, salt=salt, index=at, already=already)
        self.additions += 1
        self._record(trace, "bf_added", item=item)
        return positions

    def might_contain(self, item, trace=None):
        """A zero bit proves absence; all set bits only indicate possible membership."""
        for salt, at in enumerate(self.positions(item), 1):
            present = bool(self._bits[at])
            self._record(trace, "bf_check", at, item=item, salt=salt, index=at, present=present)
            if not present:
                self._record(trace, "bf_absent", item=item)
                return False
        self._record(trace, "bf_possible", item=item)
        return True

    def estimated_false_positive_rate(self, distinct_items):
        """Usual approximation assuming independent uniform hashes and distinct inserted items."""
        if type(distinct_items) is not int or distinct_items < 0:
            raise ValueError("The distinct-item count must be a non-negative integer.")
        return (-expm1(-self.k * distinct_items / self.m)) ** self.k
