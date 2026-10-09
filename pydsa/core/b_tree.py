"""A B-tree multiset using top-down splits and deletion repairs, with optional traces."""

from bisect import bisect_left, bisect_right
from collections import deque
from math import isfinite

from pydsa.algorithms.trace import record
from pydsa.core.errors import EmptyError, InvalidTypeError, NotFoundError
from pydsa.core.tree import BinaryTree


class BNode:
    def __init__(self, keys=(), children=()):
        self.keys = list(keys)
        self.children = list(children)

    @property
    def leaf(self):
        return not self.children


def snapshot(node):
    if node is None:
        return None
    return tuple(node.keys), tuple(snapshot(child) for child in node.children)


class BTree(BinaryTree):
    """Nodes hold up to 2t - 1 keys; all leaves have the same depth. Duplicates are retained."""

    def __init__(self, t=2, data_type="num"):
        if type(t) is not int or t < 2:
            raise ValueError("The minimum degree must be an integer of at least 2.")
        super().__init__(data_type)
        self.t = t
        self.root = None

    def check_type(self, key):
        super().check_type(key)
        if isinstance(key, bool) or isinstance(key, float) and not isfinite(key):
            raise InvalidTypeError("Tree keys must be finite numbers or strings.")

    def _record(self, trace, kind, marks=None, **data):
        if trace is not None:
            record(trace, kind, snapshot(self.root), marks, **data)

    def search(self, key, trace=None):
        """Return the node containing key or None, tracing each node and child choice."""
        self.check_type(key)
        node = self.root
        while node is not None:
            index = bisect_left(node.keys, key)
            self._record(trace, "bt_visit", {key: "checked"}, key=key, keys=tuple(node.keys))
            if index < len(node.keys) and node.keys[index] == key:
                self._record(trace, "tree_found", {key: "checked"}, key=key)
                return node
            if node.leaf:
                break
            self._record(trace, "bt_descend", key=key, index=index)
            node = node.children[index]
        self._record(trace, "tree_missing", key=key)
        return None

    def __contains__(self, key):
        return self.search(key) is not None

    def _split(self, parent, index, trace):
        child = parent.children[index]
        middle = child.keys[self.t - 1]
        right = BNode(child.keys[self.t:], child.children[self.t:] if not child.leaf else ())
        child.keys = child.keys[:self.t - 1]
        child.children = child.children[:self.t]
        parent.keys.insert(index, middle)
        parent.children.insert(index + 1, right)
        self._record(trace, "bt_split", {middle: "moved"}, key=middle)

    def insert(self, key, trace=None):
        """Split full nodes before descending, then insert into a non-full leaf."""
        self.check_type(key)
        if self.root is None:
            self.root = BNode([key])
            self._record(trace, "bt_insert", {key: "new"}, key=key)
            return
        if len(self.root.keys) == 2 * self.t - 1:
            self.root = BNode(children=[self.root])
            self._split(self.root, 0, trace)
        node = self.root
        while not node.leaf:
            index = bisect_right(node.keys, key)
            if len(node.children[index].keys) == 2 * self.t - 1:
                self._split(node, index, trace)
                if key >= node.keys[index]:
                    index += 1
            self._record(trace, "bt_descend", key=key, index=index)
            node = node.children[index]
        node.keys.insert(bisect_right(node.keys, key), key)
        self._record(trace, "bt_insert", {key: "new"}, key=key)

    def _merge(self, parent, index, trace):
        left, right = parent.children[index:index + 2]
        key = parent.keys.pop(index)
        left.keys.extend([key, *right.keys])
        left.children.extend(right.children)
        parent.children.pop(index + 1)
        if parent is self.root and not parent.keys:
            self.root = left
        self._record(trace, "bt_merge", {key: "moved"}, key=key)
        return left

    def _fill(self, parent, index, trace):
        """Give a minimum-size child another key before walking into it."""
        child = parent.children[index]
        if index > 0 and len(parent.children[index - 1].keys) >= self.t:
            sibling = parent.children[index - 1]
            key = parent.keys[index - 1]
            child.keys.insert(0, key)
            parent.keys[index - 1] = sibling.keys.pop()
            if not sibling.leaf:
                child.children.insert(0, sibling.children.pop())
            self._record(trace, "bt_borrow_left", {key: "moved"}, key=key)
        elif index < len(parent.keys) and len(parent.children[index + 1].keys) >= self.t:
            sibling = parent.children[index + 1]
            key = parent.keys[index]
            child.keys.append(key)
            parent.keys[index] = sibling.keys.pop(0)
            if not sibling.leaf:
                child.children.append(sibling.children.pop(0))
            self._record(trace, "bt_borrow_right", {key: "moved"}, key=key)
        else:
            if index == len(parent.keys):
                index -= 1
            child = self._merge(parent, index, trace)
        return child

    def delete(self, key, trace=None):
        """Remove one occurrence, borrowing or merging before entering a minimum-size child."""
        if self.search(key, trace) is None:
            raise NotFoundError(f"Key {key!r} is not in the tree.")
        self._delete(self.root, key, trace)
        if self.root is not None and not self.root.keys:
            self.root = self.root.children[0] if self.root.children else None
        self._record(trace, "bt_done", key=key)

    def _delete(self, node, key, trace):
        index = bisect_left(node.keys, key)
        if index < len(node.keys) and node.keys[index] == key:
            if node.leaf:
                node.keys.pop(index)
                if node is self.root and not node.keys:
                    self.root = None
                self._record(trace, "bt_remove", key=key)
            elif len(node.children[index].keys) >= self.t:
                previous = node.children[index]
                while not previous.leaf:
                    previous = previous.children[-1]
                replacement = previous.keys[-1]
                node.keys[index] = replacement
                self._record(trace, "bt_replace", {replacement: "moved"}, key=key, value=replacement)
                self._delete(node.children[index], replacement, trace)
            elif len(node.children[index + 1].keys) >= self.t:
                following = node.children[index + 1]
                while not following.leaf:
                    following = following.children[0]
                replacement = following.keys[0]
                node.keys[index] = replacement
                self._record(trace, "bt_replace", {replacement: "moved"}, key=key, value=replacement)
                self._delete(node.children[index + 1], replacement, trace)
            else:
                self._delete(self._merge(node, index, trace), key, trace)
        else:
            child = node.children[index]
            if len(child.keys) == self.t - 1:
                child = self._fill(node, index, trace)
            if child is not self.root:
                self._record(trace, "bt_descend", key=key, index=node.children.index(child))
            self._delete(child, key, trace)

    def _collect(self, keys, values, trace):
        for key in values:
            keys.append(key)
            if trace is not None:
                self._record(trace, "tree_walk", {key: "visited"}, key=key, keys=tuple(keys))

    def inorder(self, trace=None):
        """Visit each child before the separator key to its right, producing sorted keys."""
        keys = []
        def visit(node):
            if node.leaf:
                self._collect(keys, node.keys, trace)
            else:
                for index, key in enumerate(node.keys):
                    visit(node.children[index])
                    self._collect(keys, [key], trace)
                visit(node.children[-1])
        if self.root:
            visit(self.root)
        return keys

    def preorder(self, trace=None):
        keys = []
        def visit(node):
            self._collect(keys, node.keys, trace)
            for child in node.children:
                visit(child)
        if self.root:
            visit(self.root)
        return keys

    def postorder(self, trace=None):
        keys = []
        def visit(node):
            for child in node.children:
                visit(child)
            self._collect(keys, node.keys, trace)
        if self.root:
            visit(self.root)
        return keys

    def level_order(self, trace=None):
        keys, queue = [], deque([self.root] if self.root else [])
        while queue:
            node = queue.popleft()
            self._collect(keys, node.keys, trace)
            queue.extend(node.children)
        return keys

    def __len__(self):
        def count(node):
            return len(node.keys) + sum(count(child) for child in node.children)
        return count(self.root) if self.root else 0

    def node_count(self):
        def count(node):
            return 1 + sum(count(child) for child in node.children)
        return count(self.root) if self.root else 0

    def height(self):
        height, node = 0, self.root
        while node:
            height += 1
            node = node.children[0] if node.children else None
        return height

    def leaf_count(self):
        def count(node):
            return 1 if node.leaf else sum(count(child) for child in node.children)
        return count(self.root) if self.root else 0

    def min(self):
        if self.root is None:
            raise EmptyError("The tree is empty.")
        node = self.root
        while node.children:
            node = node.children[0]
        return node.keys[0]

    def max(self):
        if self.root is None:
            raise EmptyError("The tree is empty.")
        node = self.root
        while node.children:
            node = node.children[-1]
        return node.keys[-1]
