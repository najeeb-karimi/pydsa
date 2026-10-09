"""A red-black search tree with parent links, duplicate keys and optional fix-up traces."""

from math import isfinite
from collections import deque

from pydsa.algorithms.trace import record
from pydsa.core.errors import InvalidTypeError, NotFoundError
from pydsa.core.tree import BSTNode, BinaryTree


class RedBlackNode(BSTNode):
    def __init__(self, key, parent=None):
        super().__init__(key)
        self.parent = parent
        self.color = "R"


def snapshot(node):
    """Freeze keys, colors and child links; absent leaves count as black."""
    if node is None:
        return None
    return node.key, node.color, snapshot(node.left), snapshot(node.right)


def _color(node):
    return "B" if node is None else node.color


class RedBlackTree(BinaryTree):
    """A balanced multiset of numeric or string keys; deletion removes one occurrence."""

    def __init__(self, data_type="num"):
        super().__init__(data_type)

    def check_type(self, key):
        super().check_type(key)
        if isinstance(key, bool) or isinstance(key, float) and not isfinite(key):
            raise InvalidTypeError("Tree keys must be finite numbers or strings.")

    def _record(self, trace, kind, marks=None, **data):
        if trace is not None:
            record(trace, kind, snapshot(self.root), marks, **data)

    def _paint(self, node, color, trace):
        if node is not None and node.color != color:
            node.color = color
            self._record(trace, "rb_recolor", {node.key: "moved"}, key=node.key, color=color)

    def _rotate(self, node, left, trace):
        """Rotate a subtree and reconnect it immediately to its parent or the root."""
        top = node.right if left else node.left
        middle = top.left if left else top.right
        if left:
            node.right = middle
            top.left = node
        else:
            node.left = middle
            top.right = node
        if middle is not None:
            middle.parent = node
        top.parent = node.parent
        if node.parent is None:
            self.root = top
        elif node is node.parent.left:
            node.parent.left = top
        else:
            node.parent.right = top
        node.parent = top
        self._record(trace, "rb_rotate", {node.key: "moved", top.key: "moved"},
                     node=node.key, top=top.key, direction="left" if left else "right")

    def search(self, key, trace=None):
        """Return a matching node or None, recording the search path when requested."""
        self.check_type(key)
        node = self.root
        while node is not None:
            if node.key == key:
                self._record(trace, "tree_found", {key: "checked"}, key=key)
                return node
            self._step_down(trace, node, key)
            node = node.left if key < node.key else node.right
        self._record(trace, "tree_missing", key=key)
        return None

    def insert(self, key, trace=None):
        """Insert a red leaf, then repair red parents through recoloring and rotations."""
        self.check_type(key)
        parent, node = None, self.root
        while node is not None:
            parent = node
            self._step_down(trace, node, key)
            node = node.left if key < node.key else node.right
        added = RedBlackNode(key, parent)
        if parent is None:
            self.root = added
        elif key < parent.key:
            parent.left = added
        else:
            parent.right = added
        self._record(trace, "rb_insert", {key: "new"}, key=key)
        self._fix_insert(added, trace)

    def _fix_insert(self, node, trace):
        while _color(node.parent) == "R":
            parent, grandparent = node.parent, node.parent.parent
            left = parent is grandparent.left
            uncle = grandparent.right if left else grandparent.left
            if _color(uncle) == "R":
                self._record(trace, "rb_insert_uncle", {grandparent.key: "checked"}, node=grandparent.key)
                self._paint(parent, "B", trace)
                self._paint(uncle, "B", trace)
                self._paint(grandparent, "R", trace)
                node = grandparent
                continue
            if node is (parent.right if left else parent.left):
                self._record(trace, "rb_insert_inner", {parent.key: "checked"}, node=parent.key)
                node = parent
                self._rotate(node, left, trace)
            parent, grandparent = node.parent, node.parent.parent
            self._record(trace, "rb_insert_outer", {grandparent.key: "checked"}, node=grandparent.key)
            self._paint(parent, "B", trace)
            self._paint(grandparent, "R", trace)
            self._rotate(grandparent, not left, trace)
        self._paint(self.root, "B", trace)

    def _transplant(self, node, replacement):
        if node.parent is None:
            self.root = replacement
        elif node is node.parent.left:
            node.parent.left = replacement
        else:
            node.parent.right = replacement
        if replacement is not None:
            replacement.parent = node.parent

    def delete(self, key, trace=None):
        """Remove one matching key and repair any black height lost by the removed node."""
        node = self.search(key, trace)
        if node is None:
            raise NotFoundError(f"Key {key!r} is not in the tree.")
        removed_color = node.color
        if node.left is None:
            child, parent = node.right, node.parent
            self._transplant(node, child)
        elif node.right is None:
            child, parent = node.left, node.parent
            self._transplant(node, child)
        else:
            successor = self._min_value_node(node.right)
            self._record(trace, "rb_successor", {successor.key: "moved"}, key=key, successor=successor.key)
            removed_color, child = successor.color, successor.right
            if successor.parent is node:
                parent = successor
            else:
                parent = successor.parent
                self._transplant(successor, child)
                successor.right = node.right
                successor.right.parent = successor
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            self._paint(successor, node.color, trace)
        self._record(trace, "rb_remove", key=key)
        if removed_color == "B":
            self._fix_delete(child, parent, trace)

    def _fix_delete(self, node, parent, trace):
        while node is not self.root and _color(node) == "B":
            left = node is parent.left
            sibling = parent.right if left else parent.left
            if _color(sibling) == "R":
                self._record(trace, "rb_delete_red_sibling", {parent.key: "checked"}, node=parent.key)
                self._paint(sibling, "B", trace)
                self._paint(parent, "R", trace)
                self._rotate(parent, left, trace)
                sibling = parent.right if left else parent.left
            near = (sibling.left if left else sibling.right) if sibling is not None else None
            far = (sibling.right if left else sibling.left) if sibling is not None else None
            if _color(near) == "B" and _color(far) == "B":
                self._record(trace, "rb_delete_black_children", {parent.key: "checked"}, node=parent.key)
                self._paint(sibling, "R", trace)
                node, parent = parent, parent.parent
                continue
            if _color(far) == "B":
                self._record(trace, "rb_delete_near", {sibling.key: "checked"}, node=sibling.key)
                self._paint(near, "B", trace)
                self._paint(sibling, "R", trace)
                self._rotate(sibling, not left, trace)
                sibling = parent.right if left else parent.left
                far = sibling.right if left else sibling.left
            self._record(trace, "rb_delete_far", {parent.key: "checked"}, node=parent.key)
            self._paint(sibling, parent.color, trace)
            self._paint(parent, "B", trace)
            self._paint(far, "B", trace)
            self._rotate(parent, left, trace)
            node, parent = self.root, None
        self._paint(node, "B", trace)

    def black_height(self):
        """Count black nodes on a root-to-missing-leaf path, including its absent leaf."""
        height, node = 1, self.root
        while node is not None:
            height += node.color == "B"
            node = node.left
        return height

    def _traverse(self, order, trace):
        keys = []
        def collect(node):
            keys.append(node.key)
            if trace is not None:
                self._record(trace, "tree_walk", {node.key: "visited"}, key=node.key, keys=tuple(keys))
        def visit(node):
            if node is None:
                return
            if order == "pre":
                collect(node)
            visit(node.left)
            if order == "in":
                collect(node)
            visit(node.right)
            if order == "post":
                collect(node)
        visit(self.root)
        return keys

    def inorder(self, trace=None):
        """Return every key in sorted order in a single traversal."""
        return self._traverse("in", trace)

    def preorder(self, trace=None):
        return self._traverse("pre", trace)

    def postorder(self, trace=None):
        return self._traverse("post", trace)

    def level_order(self, trace=None):
        keys, queue = [], deque([self.root] if self.root else [])
        while queue:
            node = queue.popleft()
            keys.append(node.key)
            if trace is not None:
                self._record(trace, "tree_walk", {node.key: "visited"}, key=node.key, keys=tuple(keys))
            queue.extend(child for child in (node.left, node.right) if child is not None)
        return keys
