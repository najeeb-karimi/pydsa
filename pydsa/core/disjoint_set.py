"""Disjoint set (Union-Find) with union by rank and path compression."""

from pydsa.core.errors import OutOfBoundsError


class DisjointSet:
    """Union-Find over the elements 0 to size - 1, which start out in sets of their own."""

    def __init__(self, size):
        self.parent = list(range(size))  # Each element starts as the root of its own set
        self.rank = [0] * size  # An upper bound on the height of each root's tree

    def __len__(self):
        return len(self.parent)

    def _check(self, *elements):
        """Raise OutOfBoundsError if any of the elements doesn't exist."""
        for element in elements:
            if not 0 <= element < len(self.parent):
                raise OutOfBoundsError(f"Element {element} doesn't exist.")

    def root_of(self, element):
        """Return the root of element's set without changing any parent links."""
        self._check(element)
        while self.parent[element] != element:
            element = self.parent[element]
        return element

    def find(self, element):
        """Return the root of element's set, pointing every element on the way straight at the root."""
        root = self.root_of(element)
        # Path compression: walk the same path again, relinking each element to the root
        while self.parent[element] != root:
            self.parent[element], element = root, self.parent[element]
        return root

    def union(self, a, b):
        """Merge the sets of a and b; return False if they were already in the same set."""
        self._check(a, b)
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        # Union by rank: attach the root of the shorter tree under the root of the taller one
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True

    def connected(self, a, b):
        """Return True if a and b are in the same set."""
        self._check(a, b)
        return self.find(a) == self.find(b)

    def groups(self):
        """Return a dict mapping each root to the sorted members of its set, without changing any parent links."""
        sets = {}
        for element in range(len(self.parent)):
            sets.setdefault(self.root_of(element), []).append(element)
        return sets
