"""Hash tables with two collision resolution techniques.

Separate chaining (open hashing) and linear probing, from the open addressing (closed hashing) family.
"""

from pydsa.core.errors import CapacityError, NotFoundError


# ---------------------------------------------------------------------------
# Hash table with Separate Chaining (Open Hashing)
# ---------------------------------------------------------------------------

class ChainingHashTable:
    """Hash table where each bucket is a list, so colliding keys are chained in the same bucket."""

    def __init__(self, size):
        """Initialize the hash table with the given number of empty buckets."""
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        """Return the bucket index for a key: its hash code modulo the table size."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert a key-value pair, or update the value if the key already exists.

        Return (index, updated), where updated is True if the key was already in the table.
        """
        index = self.hash_function(key)
        # Update the value if the key is already in the bucket
        for kv in self.table[index]:
            if kv[0] == key:
                kv[1] = value
                return index, True
        # Otherwise, append a new key-value pair to the bucket
        self.table[index].append([key, value])
        return index, False

    def lookup(self, key):
        """Return (index, value) for a key."""
        index = self.hash_function(key)
        for kv in self.table[index]:
            if kv[0] == key:
                return index, kv[1]
        raise NotFoundError(f"Key {key!r} not found.")

    def delete(self, key):
        """Delete a key-value pair and return the index it was deleted from."""
        index = self.hash_function(key)
        for i, kv in enumerate(self.table[index]):
            if kv[0] == key:
                del self.table[index][i]
                return index
        raise NotFoundError(f"Key {key!r} not found.")


# ---------------------------------------------------------------------------
# Hash table with Linear Probing (Open Addressing / Closed Hashing)
# ---------------------------------------------------------------------------

class LinearProbingHashTable:
    """Hash table with one pair per slot; a collision moves on to the next free slot (linear probing)."""

    def __init__(self, size):
        """Initialize the hash table with the given number of empty slots."""
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        """Return the home slot index for a key: its hash code modulo the table size."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert a key-value pair, or update the value if the key already exists.

        Return (index, updated), where updated is True if the key was already in the table.
        """
        index = self.hash_function(key)
        original_index = index
        # Probe forward until an empty slot or the same key is found
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return index, True
            index = (index + 1) % self.size
            # Coming back around to the starting slot means every slot is taken
            if index == original_index:
                raise CapacityError("Hash table is full; cannot insert new key.")
        self.table[index] = (key, value)
        return index, False

    def _find(self, key):
        """Return the slot index holding key."""
        index = self.hash_function(key)
        original_index = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return index
            index = (index + 1) % self.size
            if index == original_index:
                break
        raise NotFoundError(f"Key {key!r} not found.")

    def lookup(self, key):
        """Return (index, value) for a key."""
        index = self._find(key)
        return index, self.table[index][1]

    def delete(self, key):
        """Delete a key-value pair and rehash the rest of its cluster.

        Return (index, rehashed): the slot the pair was deleted from and how many keys were rehashed.
        """
        index = self._find(key)
        self.table[index] = None
        # Take out every pair that follows in the same cluster and insert it again,
        # so later lookups don't stop at the gap left by the deleted pair
        cluster = []
        next_index = (index + 1) % self.size
        while self.table[next_index] is not None:
            cluster.append(self.table[next_index])
            self.table[next_index] = None
            next_index = (next_index + 1) % self.size
        for rehash_key, rehash_value in cluster:
            self.insert(rehash_key, rehash_value)
        return index, len(cluster)
