"""Binary search tree and AVL tree.

insert() and delete() take an optional trace list and record the path they walked, the case they ran into
and, for an AVL tree, every rotation, as TraceEvents whose snapshot is the tree as nested tuples.
"""

from collections import deque

from pydsa.algorithms.trace import record
from pydsa.algorithms.trace import tree as tree_snapshot
from pydsa.core.errors import EmptyError, InvalidTypeError, NotFoundError

# Python types each tree data type accepts
DATA_TYPES = {"num": (int, float), "str": (str,)}


class BSTNode:
    """Node of a binary search tree."""

    def __init__(self, key):
        self.key = key  # Value of the node
        self.left = None  # Left child
        self.right = None  # Right child


class AVLNode(BSTNode):
    """Node of an AVL tree, which also tracks its height."""

    def __init__(self, key):
        super().__init__(key)
        self.height = 1  # Height of the node; a new node is a leaf


class BinaryTree:
    """Searching and traversals shared by the binary search trees below."""

    def __init__(self, data_type):
        """Initialize an empty tree that holds "num" (int or float) or "str" keys."""
        if data_type not in DATA_TYPES:
            raise ValueError(f"data_type must be one of: {', '.join(DATA_TYPES)}")
        self.root = None  # The tree starts empty
        self.data_type = data_type  # The tree only holds one kind of data

    def check_type(self, key):
        """Raise InvalidTypeError if key doesn't match the tree's data type."""
        if not isinstance(key, DATA_TYPES[self.data_type]):
            raise InvalidTypeError(f"This tree only holds {self.data_type} keys.")

    def _record(self, trace, kind, marks=None, **data):
        """Record one step of an operation, with the whole tree as the state it left behind."""
        if trace is not None:
            record(trace, kind, tree_snapshot(self.root), marks, **data)

    def _step_down(self, trace, node, key):
        """Record the step that goes from node to one of its children while looking for key."""
        side = "go_left" if key < node.key else "go_right"
        self._record(trace, side, {node.key: "checked"}, key=key, node=node.key)

    def search(self, key):
        """Return the node holding key, or None if it isn't in the tree."""
        self.check_type(key)
        node = self.root
        while node is not None and node.key != key:
            node = node.left if key < node.key else node.right
        return node

    def __contains__(self, key):
        return self.search(key) is not None

    def inorder(self):
        """Return the keys in in-order (left, node, right)."""
        return self._inorder(self.root)

    def _inorder(self, node):
        """Recursively collect keys in in-order."""
        if node is None:
            return []
        return self._inorder(node.left) + [node.key] + self._inorder(node.right)

    def preorder(self):
        """Return the keys in pre-order (node, left, right)."""
        return self._preorder(self.root)

    def _preorder(self, node):
        """Recursively collect keys in pre-order."""
        if node is None:
            return []
        return [node.key] + self._preorder(node.left) + self._preorder(node.right)

    def postorder(self):
        """Return the keys in post-order (left, right, node)."""
        return self._postorder(self.root)

    def _postorder(self, node):
        """Recursively collect keys in post-order."""
        if node is None:
            return []
        return self._postorder(node.left) + self._postorder(node.right) + [node.key]

    def level_order(self):
        """Return the keys level by level from the root down, each level from left to right (breadth-first)."""
        keys, queue = [], deque([self.root] if self.root is not None else [])
        while queue:
            node = queue.popleft()
            keys.append(node.key)
            queue.extend(child for child in (node.left, node.right) if child is not None)
        return keys

    def __len__(self):
        """Return the number of nodes."""
        return self._count(self.root)

    def _count(self, node):
        if node is None:
            return 0
        return 1 + self._count(node.left) + self._count(node.right)

    def height(self):
        """Return the number of levels, which is 0 for an empty tree and 1 for a lone root."""
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def leaf_count(self):
        """Return the number of nodes without children."""
        return self._leaf_count(self.root)

    def _leaf_count(self, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        return self._leaf_count(node.left) + self._leaf_count(node.right)

    def min(self):
        """Return the smallest key, found by always going left."""
        if self.root is None:
            raise EmptyError("The tree is empty.")
        return self._min_value_node(self.root).key

    def max(self):
        """Return the largest key, found by always going right."""
        if self.root is None:
            raise EmptyError("The tree is empty.")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.key

    @staticmethod
    def _min_value_node(node):
        """Return the node with the smallest key in the subtree rooted at node."""
        current = node
        while current.left is not None:
            current = current.left
        return current


def _removal(node):
    """Return the kind, marks and data of the step that takes a node without a left child out of the tree."""
    if node.right is None:
        return "delete_leaf", {node.key: "removed"}, {}
    return "delete_one_child", {node.key: "removed", node.right.key: "moved"}, {"child": node.right.key}


# ---------------------------------------------------------------------------
# BST (Binary Search Tree)
# ---------------------------------------------------------------------------

class BinarySearchTree(BinaryTree):
    """Binary search tree that holds either numbers or strings; duplicates go to the right subtree."""

    def insert(self, key, trace=None):
        """Insert a new key into the BST."""
        self.check_type(key)
        if self.root is None:
            self.root = BSTNode(key)  # An empty tree gets the key as its root
            self._record(trace, "empty_tree", {key: "new"}, key=key)
        else:
            self._insert(self.root, key, trace)

    def _insert(self, node, key, trace=None):
        """Recursively find the right spot for a new key and insert it."""
        self._step_down(trace, node, key)
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
                self._record(trace, "place_left", {key: "new", node.key: "checked"}, key=key, node=node.key)
            else:
                self._insert(node.left, key, trace)
        else:
            if node.right is None:
                node.right = BSTNode(key)
                self._record(trace, "place_right", {key: "new", node.key: "checked"}, key=key, node=node.key)
            else:
                self._insert(node.right, key, trace)

    def delete(self, key, trace=None):
        """Delete one occurrence of key from the BST."""
        if key not in self:
            raise NotFoundError(f"Key {key!r} is not in the tree.")
        self.root = self._delete(self.root, key, trace)

    def _delete(self, node, key, trace=None):
        """Recursively delete a key from the subtree rooted at node and return the new subtree root."""
        if node is None:
            return node
        if key < node.key or key > node.key:
            self._step_down(trace, node, key)
        if key < node.key:
            node.left = self._delete(node.left, key, trace)
        elif key > node.key:
            node.right = self._delete(node.right, key, trace)
        else:
            # Node with one child or no child
            if node.left is None:
                kind, marks, extra = _removal(node)
                self._record(trace, kind, marks, key=key, **extra)
                return node.right
            elif node.right is None:
                self._record(trace, "delete_one_child", {key: "removed", node.left.key: "moved"},
                             key=key, child=node.left.key)
                return node.left
            # Node with two children: replace it with its in-order successor (smallest key in the right subtree)
            temp = self._min_value_node(node.right)
            self._record(trace, "successor", {key: "removed", temp.key: "moved"}, key=key, successor=temp.key)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key, trace)
        return node


# ---------------------------------------------------------------------------
# AVL Tree
# ---------------------------------------------------------------------------

class AVLTree(BinaryTree):
    """Self-balancing binary search tree that holds either numbers or strings."""

    def insert(self, key, trace=None):
        """Insert a new key into the AVL tree."""
        self.check_type(key)
        if self.root is None:
            self.root = AVLNode(key)  # An empty tree gets the key as its root
            self._record(trace, "empty_tree", {key: "new"}, key=key)
            return
        self.root = self._insert(self.root, key, trace)

    def _insert(self, node, key, trace=None):
        """Recursively insert a key, rebalance on the way back up and return the new subtree root."""
        if not node:
            return AVLNode(key)

        self._step_down(trace, node, key)
        # The new node is recorded once it hangs in the tree, so the step shows it
        if key < node.key:
            empty = not node.left
            node.left = self._insert(node.left, key, trace)
            if empty:
                self._record(trace, "place_left", {key: "new", node.key: "checked"}, key=key, node=node.key)
        else:
            empty = not node.right
            node.right = self._insert(node.right, key, trace)
            if empty:
                self._record(trace, "place_right", {key: "new", node.key: "checked"}, key=key, node=node.key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        # Rotate to restore the balance
        if balance > 1 and key < node.left.key:
            return self._rebalance(node, "LL", trace)
        if balance < -1 and key >= node.right.key:
            return self._rebalance(node, "RR", trace)
        if balance > 1 and key >= node.left.key:
            return self._rebalance(node, "LR", trace)
        if balance < -1 and key < node.right.key:
            return self._rebalance(node, "RL", trace)

        return node

    def delete(self, key, trace=None):
        """Delete one occurrence of key from the AVL tree."""
        if key not in self:
            raise NotFoundError(f"Key {key!r} is not in the tree.")
        self.root = self._delete(self.root, key, trace)

    def _delete(self, node, key, trace=None):
        """Recursively delete a key, rebalance on the way back up and return the new subtree root."""
        if not node:
            return node

        if key < node.key or key > node.key:
            self._step_down(trace, node, key)
        if key < node.key:
            node.left = self._delete(node.left, key, trace)
        elif key > node.key:
            node.right = self._delete(node.right, key, trace)
        else:
            if not node.left:
                kind, marks, extra = _removal(node)
                self._record(trace, kind, marks, key=key, **extra)
                return node.right  # Only a right child, or no child
            elif not node.right:
                self._record(trace, "delete_one_child", {key: "removed", node.left.key: "moved"},
                             key=key, child=node.left.key)
                return node.left  # Only a left child

            # Two children: replace the key with its in-order successor's key, then delete the successor
            temp = self._min_value_node(node.right)
            self._record(trace, "successor", {key: "removed", temp.key: "moved"}, key=key, successor=temp.key)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key, trace)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        # Rotate to restore the balance
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rebalance(node, "LL", trace)
        if balance > 1 and self._get_balance(node.left) < 0:
            return self._rebalance(node, "LR", trace)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rebalance(node, "RR", trace)
        if balance < -1 and self._get_balance(node.right) > 0:
            return self._rebalance(node, "RL", trace)

        return node

    def _rebalance(self, node, case, trace=None):
        """Rotate the subtree at node back into balance and return its new root.

        The four cases are named after where the subtree grew too tall: LL and RR need one rotation, and LR
        and RL need one rotation of the child first, which turns them into an LL or RR case.
        """
        if trace is not None:
            record(trace, "unbalanced", tree_snapshot(node), {node.key: "checked"},
                   node=node.key, balance=self._get_balance(node))
        if case == "LR":
            node.left = self._left_rotate(node.left)
        elif case == "RL":
            node.right = self._right_rotate(node.right)
        top = self._right_rotate(node) if case in ("LL", "LR") else self._left_rotate(node)
        if trace is not None:
            record(trace, "rotate", tree_snapshot(top), {top.key: "moved"}, case=case, top=top.key)
        return top

    def _left_rotate(self, z):
        """Rotate the subtree rooted at z to the left and return its new root."""
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, z):
        """Rotate the subtree rooted at z to the right and return its new root."""
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def height(self):
        """Return the number of levels, which every AVL node already stores."""
        return self._get_height(self.root)

    def balance_factor(self, node):
        """Return the balance factor of a node (left height minus right height), always -1, 0 or 1."""
        return self._get_balance(node)

    @staticmethod
    def _get_height(node):
        """Return the height of a node, or 0 for an empty subtree."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Return the balance factor of a node (left height minus right height)."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
