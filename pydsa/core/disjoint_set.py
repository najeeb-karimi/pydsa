"""Disjoint set (Union-Find) with union by rank and path compression.

find() and union() take an optional trace list and record every hop up to a root, every element that path
compression relinked and how two trees were joined, as TraceEvents whose snapshot is a copy of the parent
and rank arrays.
"""

from pydsa.algorithms.trace import record
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

    def _snapshot(self):
        """Return a copy of the parent and rank arrays, so a recorded step keeps them as they were."""
        return list(self.parent), list(self.rank)

    def _record(self, trace, kind, marks=None, **data):
        if trace is not None:
            record(trace, kind, self._snapshot(), marks, **data)

    def root_of(self, element, trace=None):
        """Return the root of element's set without changing any parent links."""
        self._check(element)
        while self.parent[element] != element:
            self._record(trace, "hop", {element: "checked"}, element=element, parent=self.parent[element])
            element = self.parent[element]
        self._record(trace, "root", {element: "root"}, element=element)
        return element

    def find(self, element, trace=None):
        """Return the root of element's set, pointing every element on the way straight at the root."""
        root = self.root_of(element, trace)
        # Path compression: walk the same path again, relinking each element to the root
        while self.parent[element] != root:
            relinked = element
            self.parent[element], element = root, self.parent[element]
            self._record(trace, "compress", {relinked: "moved"}, element=relinked, root=root)
        return root

    def union(self, a, b, trace=None):
        """Merge the sets of a and b; return False if they were already in the same set."""
        self._check(a, b)
        root_a, root_b = self.find(a, trace), self.find(b, trace)
        if root_a == root_b:
            self._record(trace, "same_set", {root_a: "root"}, a=a, b=b, root=root_a)
            return False
        # Union by rank: attach the root of the shorter tree under the root of the taller one
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self._record(trace, "attach", {root_b: "moved", root_a: "root"}, child=root_b, parent=root_a)
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
            self._record(trace, "rank_up", {root_a: "root"}, root=root_a)
        return True

    def connected(self, a, b, trace=None):
        """Return True if a and b are in the same set."""
        self._check(a, b)
        return self.find(a, trace) == self.find(b, trace)

    def groups(self):
        """Return a dict mapping each root to the sorted members of its set, without changing any parent links."""
        sets = {}
        for element in range(len(self.parent)):
            sets.setdefault(self.root_of(element), []).append(element)
        return sets
