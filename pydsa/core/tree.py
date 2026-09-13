"""Binary search tree and AVL tree."""

from pydsa.core.errors import InvalidTypeError, NotFoundError

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

    @staticmethod
    def _min_value_node(node):
        """Return the node with the smallest key in the subtree rooted at node."""
        current = node
        while current.left is not None:
            current = current.left
        return current


# ---------------------------------------------------------------------------
# BST (Binary Search Tree)
# ---------------------------------------------------------------------------

class BinarySearchTree(BinaryTree):
    """Binary search tree that holds either numbers or strings; duplicates go to the right subtree."""

    def insert(self, key):
        """Insert a new key into the BST."""
        self.check_type(key)
        if self.root is None:
            self.root = BSTNode(key)  # An empty tree gets the key as its root
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        """Recursively find the right spot for a new key and insert it."""
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = BSTNode(key)
            else:
                self._insert(node.right, key)

    def delete(self, key):
        """Delete one occurrence of key from the BST."""
        if key not in self:
            raise NotFoundError(f"Key {key!r} is not in the tree.")
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """Recursively delete a key from the subtree rooted at node and return the new subtree root."""
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node with one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node with two children: replace it with its in-order successor (smallest key in the right subtree)
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return node


# ---------------------------------------------------------------------------
# AVL Tree
# ---------------------------------------------------------------------------

class AVLTree(BinaryTree):
    """Self-balancing binary search tree that holds either numbers or strings."""

    def insert(self, key):
        """Insert a new key into the AVL tree."""
        self.check_type(key)
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Recursively insert a key, rebalance on the way back up and return the new subtree root."""
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        # Rotate to restore the balance
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)  # Left Left case
        if balance < -1 and key >= node.right.key:
            return self._left_rotate(node)  # Right Right case
        if balance > 1 and key >= node.left.key:
            node.left = self._left_rotate(node.left)  # Left Right case
            return self._right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)  # Right Left case
            return self._left_rotate(node)

        return node

    def delete(self, key):
        """Delete one occurrence of key from the AVL tree."""
        if key not in self:
            raise NotFoundError(f"Key {key!r} is not in the tree.")
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """Recursively delete a key, rebalance on the way back up and return the new subtree root."""
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right  # Only a right child, or no child
            elif not node.right:
                return node.left  # Only a left child

            # Two children: replace the key with its in-order successor's key, then delete the successor
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        # Rotate to restore the balance
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)  # Left Left case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)  # Left Right case
            return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)  # Right Right case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)  # Right Left case
            return self._left_rotate(node)

        return node

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
