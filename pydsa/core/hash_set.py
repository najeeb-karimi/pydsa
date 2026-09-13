"""Hash set built on the separate chaining hash table."""

from pydsa.core.errors import NotFoundError
from pydsa.core.hash_table import ChainingHashTable


class HashSet:
    """Set of unique items, stored as the keys of a separate chaining hash table."""

    def __init__(self, size=8, items=()):
        """Initialize a set with the given number of buckets, holding items."""
        self.table = ChainingHashTable(size)
        for item in items:
            self.add(item)

    @property
    def size(self):
        """The number of buckets."""
        return self.table.size

    def __iter__(self):
        """Yield the items bucket by bucket."""
        for bucket in self.table.table:
            for item, _ in bucket:
                yield item

    def __len__(self):
        return sum(len(bucket) for bucket in self.table.table)

    def __contains__(self, item):
        try:
            self.table.lookup(item)
        except NotFoundError:
            return False
        return True

    def add(self, item):
        """Add item to the set; return False if it was already there."""
        _, already_there = self.table.insert(item, None)
        return not already_there

    def remove(self, item):
        """Remove item from the set."""
        self.table.delete(item)

    def union(self, other):
        """Return a new set with every item that is in this set or in other."""
        return HashSet(self.size, [*self, *other])

    def intersection(self, other):
        """Return a new set with the items that are in both this set and other."""
        return HashSet(self.size, [item for item in self if item in other])

    def difference(self, other):
        """Return a new set with the items that are in this set but not in other."""
        return HashSet(self.size, [item for item in self if item not in other])

    def is_subset(self, other):
        """Return True if every item of this set is also in other."""
        return all(item in other for item in self)

    def is_superset(self, other):
        """Return True if every item of other is also in this set."""
        return other.is_subset(self)
