"""Tree implementations: binary search tree and AVL tree."""

import utility


# ---------------------------------------------------------------------------
# BST (Binary Search Tree)
# ---------------------------------------------------------------------------

class Node:
    """Node of a binary search tree."""

    def __init__(self, key):
        self.key = key  # Value of the node
        self.left = None  # Left child
        self.right = None  # Right child


class BinarySearchTree:
    """Binary search tree that holds either numbers or strings."""

    def __init__(self, type):
        self.root = None  # The tree starts empty
        self.data_type = type  # "num" or "str", so the tree only holds one kind of data

    def insert(self, key):
        """Insert a new key into the BST."""
        if self.root is None:
            self.root = Node(key)  # An empty tree gets the key as its root
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        """Recursively find the right spot for a new key and insert it."""
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert(node.right, key)

    def search(self, key):
        """Search for a key in the BST and return its node, or None if it isn't there."""
        return self._search(self.root, key)

    def _search(self, node, key):
        """Recursively search the subtree rooted at node for a key."""
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def delete(self, key):
        """Delete a key from the BST."""
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

    def _min_value_node(self, node):
        """Return the node with the smallest key in the subtree rooted at node."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        """Return the keys in in-order (left, node, right)."""
        return self._inorder(self.root)

    def _inorder(self, node):
        """Recursively collect keys in in-order."""
        res = []
        if node:
            res = self._inorder(node.left)
            res.append(node.key)
            res = res + self._inorder(node.right)
        return res

    def preorder(self):
        """Return the keys in pre-order (node, left, right)."""
        return self._preorder(self.root)

    def _preorder(self, node):
        """Recursively collect keys in pre-order."""
        res = []
        if node:
            res.append(node.key)
            res = res + self._preorder(node.left)
            res = res + self._preorder(node.right)
        return res

    def postorder(self):
        """Return the keys in post-order (left, right, node)."""
        return self._postorder(self.root)

    def _postorder(self, node):
        """Recursively collect keys in post-order."""
        res = []
        if node:
            res = self._postorder(node.left)
            res = res + self._postorder(node.right)
            res.append(node.key)
        return res


def bst_main():
    """Create a binary search tree and run the BST operation menu."""
    print("\nℹ️ This program implements a BST that allows nodes of the same general data type & allows duplicates on the right subtree of the root.")

    # Type selection loop; the tree holds either numbers or strings
    while True:
        type = input("""\n🤔 Which type of data do you want store in the BST?
★1) Numbers (int or float)
★2) Strings
>>> """)
        match type:
            case "1":
                bst = BinarySearchTree("num")
                break
            case "2":
                bst = BinarySearchTree("str")
                break
            case _:
                print("Invalid code number!")
                continue

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the BST?
★0) Definition
★1) Insertion
★2) Deletion
★3) Searching
★4) Traversals
★5) New Tree
★6) New Data Structure
★7) Exiting the Program

>>> """)
        match opr:

            # Definition
            case "0":
                tree_intro("def")

            # Insertion
            case "1":
                data_type = bst.data_type
                if data_type == "str":
                    item = utility.input_verify("str")
                elif data_type == "num":
                    item = utility.input_verify("num")

                if item != None:
                    bst.insert(item)
                    print("\n✅ Successfully inserted.", end="")
                    print(f"\n👉🏻 {bst.inorder()}\nℹ️ Inorder Traversal")
                else:
                    print("\n🚫 Invalid data type; item not inserted.")

            # Deletion
            case "2":
                data_type = bst.data_type
                if data_type == "str":
                    item = utility.input_verify("str")
                elif data_type == "num":
                    item = utility.input_verify("num")

                if item != None:
                    # Look the item up in the in-order traversal first, so a missing node can be reported
                    nodes = bst.inorder()
                    if item not in nodes:
                        print("\n❌ Node not found. Deletion unsuccessful.")
                    else:
                        bst.delete(item)
                        print("\n✅ Successfully deleted.", end="")
                        print(f"\n👉🏻 {bst.inorder()}\nℹ️ Inorder Traversal")
                else:
                    print("\n🚫 Invalid data type. Deletion unsuccessful.")

            # Searching
            case "3":
                data_type = bst.data_type
                if data_type == "str":
                    item = utility.input_verify("str")
                elif data_type == "num":
                    item = utility.input_verify("num")

                    if item != None:
                        result = bst.search(item)
                        if result != None:
                            print("\n✅ Node available.", end="")
                            print(f"\n👉🏻 {bst.inorder()}\nℹ️ Inorder Traversal")
                        else:
                            print("\n❌ Node not found.", end=" ")
                            print(f"\n👉🏻 {bst.inorder()}\nℹ️ Inorder Traversal")
                    else:
                        print("\n🚫 Invalid data type. Deletion unsuccessful.")

            # Traversals
            case "4":

                # Traversal type selection loop
                while True:
                    traversal_type = input("""\n🗂️ Which traversal do you want?
●1) Inorder Traversal
●2) Preorder Traversal
●3) Postorder Traversal
>>> """)
                    match traversal_type:

                        # Inorder
                        case "1":
                            print(f"\n👉🏻 {bst.inorder()}\nℹ️ Inorder Traversal")
                            break

                        # Preorder
                        case "2":
                            print(f"\n👉🏻 {bst.preorder()}\nℹ️ Preorder Traversal")
                            break

                        # Postorder
                        case "3":
                            print(f"\n👉🏻 {bst.postorder()}\nℹ️ Postorder Traversal")
                            break

                        # Invalid
                        case _:
                            print("\n❌ Invalid code number!")
                            continue

            # New tree
            case "5":
                utility.clear()
                tree_intro("full")
                tree_main()
                break

            # New data structure
            case "6":
                utility.clear()
                utility.main_intro()
                break

            # Exit the program
            case "7":
                exit()

            # Invalid
            case _:
                print("\n🚫 Invalid operation code!")


# ---------------------------------------------------------------------------
# AVL Tree
# ---------------------------------------------------------------------------

class Node:
    """Node of an AVL tree, which also tracks its height."""

    def __init__(self, key):
        self.key = key  # Value of the node
        self.left = None  # Left child
        self.right = None  # Right child
        self.height = 1  # Height of the node; a new node is a leaf


class AVLTree:
    """Self-balancing binary search tree that holds either numbers or strings."""

    def __init__(self, type):
        self.root = None  # The tree starts empty
        self.data_type = type  # "num" or "str", so the tree only holds one kind of data

    def insert(self, key):
        """Insert a new key into the AVL tree."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Recursively insert a key, rebalance on the way back up and return the new subtree root."""
        if not node:
            return Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        # Rotate to restore the balance
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)  # Left Left case
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)  # Right Right case
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)  # Left Right case
            return self._right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)  # Right Left case
            return self._left_rotate(node)

        return node

    def delete(self, key):
        """Delete a key from the AVL tree."""
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

    def search(self, key):
        """Search for a key in the AVL tree and return its node, or None if it isn't there."""
        return self._search(self.root, key)

    def _search(self, node, key):
        """Recursively search the subtree rooted at node for a key."""
        if not node or node.key == key:
            return node

        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder(self):
        """Return the keys in in-order (left, node, right)."""
        return self._inorder(self.root)

    def _inorder(self, node):
        """Recursively collect keys in in-order."""
        res = []
        if node:
            res = self._inorder(node.left)
            res.append(node.key)
            res = res + self._inorder(node.right)
        return res

    def preorder(self):
        """Return the keys in pre-order (node, left, right)."""
        return self._preorder(self.root)

    def _preorder(self, node):
        """Recursively collect keys in pre-order."""
        res = []
        if node:
            res.append(node.key)
            res = res + self._preorder(node.left)
            res = res + self._preorder(node.right)
        return res

    def postorder(self):
        """Return the keys in post-order (left, right, node)."""
        return self._postorder(self.root)

    def _postorder(self, node):
        """Recursively collect keys in post-order."""
        res = []
        if node:
            res = self._postorder(node.left)
            res = res + self._postorder(node.right)
            res.append(node.key)
        return res

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

    def _get_height(self, node):
        """Return the height of a node, or 0 for an empty subtree."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Return the balance factor of a node (left height minus right height)."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _min_value_node(self, node):
        """Return the node with the smallest key in the subtree rooted at node."""
        current = node
        while current.left is not None:
            current = current.left
        return current


def avl_main():
    """Create an AVL tree and run the AVL operation menu."""
    print("\nℹ️ This program implements an AVL that allows nodes of the same general data type & allows duplicates on the right subtree of the root.")

    # Type selection loop; the tree holds either numbers or strings
    while True:
        type = input("""\n🤔 Which type of data do you want store in the AVL?
★1) Numbers (int or float)
★2) Strings
>>> """)
        match type:
            case "1":
                avl = AVLTree("num")
                break
            case "2":
                bst = AVLTree("str")
                break
            case _:
                print("Invalid code number!")
                continue

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the AVL TREE?
★0) Definition
★1) Insertion
★2) Deletion
★3) Searching
★4) Traversals
★5) New Tree
★6) New Data Structure
★7) Exiting the Program

>>> """)
        match opr:

            # Definition
            case "0":
                tree_intro("def")

            # Insertion
            case "1":
                data_type = avl.data_type
                if data_type == "str":
                    item = utility.input_verify("str")
                elif data_type == "num":
                    item = utility.input_verify("num")

                if item != None:
                    avl.insert(item)
                    print("\n✅ Successfully inserted.", end="")
                    print(f"\n👉🏻 {avl.inorder()}\nℹ️ Inorder Traversal")
                else:
                    print("\n🚫 Invalid data type; item not inserted.")

            # Deletion
            case "2":
                data_type = avl.data_type
                if data_type == "str":
                    item = utility.input_verify("str")
                elif data_type == "num":
                    item = utility.input_verify("num")

                if item != None:
                    # Look the item up in the in-order traversal first, so a missing node can be reported
                    nodes = avl.inorder()
                    if item not in nodes:
                        print("\n❌ Node not found. Deletion unsuccessful.")
                    else:
                        avl.delete(item)
                        print("\n✅ Successfully deleted.", end="")
                        print(f"\n👉🏻 {avl.inorder()}\nℹ️ Inorder Traversal")
                else:
                    print("\n🚫 Invalid data type. Deletion unsuccessful.")

            # Searching
            case "3":
                data_type = avl.data_type
                if data_type == "str":
                    item = utility.input_verify("str")
                elif data_type == "num":
                    item = utility.input_verify("num")

                    if item != None:
                        result = avl.search(item)
                        if result != None:
                            print("\n✅ Node available.", end="")
                            print(f"\n👉🏻 {avl.inorder()}\nℹ️ Inorder Traversal")
                        else:
                            print("\n❌ Node not found.", end=" ")
                            print(f"\n👉🏻 {avl.inorder()}\nℹ️ Inorder Traversal")
                    else:
                        print("\n🚫 Invalid data type. Deletion unsuccessful.")

            # Traversals
            case "4":

                # Traversal type selection loop
                while True:
                    traversal_type = input("""\n🗂️ Which traversal do you want?
●1) Inorder Traversal
●2) Preorder Traversal
●3) Postorder Traversal
>>> """)
                    match traversal_type:

                        # Inorder
                        case "1":
                            print(f"\n👉🏻 {avl.inorder()}\nℹ️ Inorder Traversal")
                            break

                        # Preorder
                        case "2":
                            print(f"\n👉🏻 {avl.preorder()}\nℹ️ Preorder Traversal")
                            break

                        # Postorder
                        case "3":
                            print(f"\n👉🏻 {avl.postorder()}\nℹ️ Postorder Traversal")
                            break

                        # Invalid
                        case _:
                            print("\n❌ Invalid code number!")
                            continue

            # New tree
            case "5":
                utility.clear()
                tree_intro("full")
                tree_main()
                break

            # New data structure
            case "6":
                utility.clear()
                utility.main_intro()
                break

            # Exit the program
            case "7":
                exit()

            # Invalid
            case _:
                print("\n🚫 Invalid operation code!")


# ---------------------------------------------------------------------------
# Tree main and intro functions
# ---------------------------------------------------------------------------

def tree_main():
    """Show the tree intro and let the user pick a BST or an AVL tree.

    Once the chosen tree's menu returns, control goes back to the main menu in main.py.
    """
    tree_intro("full")

    # Tree type selection loop
    while True:
        tree_type = input("""\n🧪 Which type of tree do you want?
★1) BST (Binary Search Tree)
★2) AVL (Adelson-Velsky and Evgenii Landis)  
>>> """)

        match tree_type:
            # BST
            case "1":
                bst_main()
                break

            # AVL
            case "2":
                avl_main()
                break

            # Invalid
            case _:
                print("\n🚫 Invalid type code!")


def tree_intro(condition):
    """Print the ASCII art and definition ("full") or only the definition ("def")."""
    tree_ascii = """\n
,---------. .-------.        .-''-.      .-''-.   
\          \|  _ _   \     .'_ _   \   .'_ _   \  
 `--.  ,---'| ( ' )  |    / ( ` )   ' / ( ` )   ' 
    |   \   |(_ o _) /   . (_ o _)  |. (_ o _)  | 
    :_ _:   | (_,_).' __ |  (_,_)___||  (_,_)___| 
    (_I_)   |  |\ \  |  |'  \   .---.'  \   .---. 
   (_(=)_)  |  | \ `'   / \  `-'    / \  `-'    / 
    (_I_)   |  |  \    /   \       /   \       /  
    '---'   ''-'   `'-'     `'-..-'     `'-..-'\n"""

    tree_def = """\n🎯 A specialized type of graph, the tree is a hierarchical, non-linear data structure consisting of nodes connected by edges. It starts with a single node called the root, from which all other nodes branch out. Each node can have zero or more child nodes, and nodes with no children are called leaf nodes. Trees are used to represent hierarchical relationships and are fundamental in various applications such as file systems, databases, and network routing. They facilitate efficient data retrieval and manipulation through various traversal methods like in-order, pre-order, and post-order traversal.
🎯 Trees have many different types the most important of which is the Binary Tree which in which each node has at most 2 children. The binary tree can also be classified further down the line with the most popular ones being the BST & the AVL trees. PyDSA implements these two types of binary trees. 

🌟 A Binary Search Tree (BST) is a specialized type of binary tree where each node has at most two children, referred to as the left and right child. The key property of a BST is that for any given node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater. This property allows for efficient searching, insertion, and deletion operations, typically with a time complexity of (O(log n)) if the tree is balanced. If not balanced, it's possible for the BST to develop a big difference between its left & right subtrees in which case the time complexity will degrade to (O(n)). That's why self-balancing BSTs like AVL & Red-Black tree are used. BSTs are widely used in applications that require dynamic data sets and quick lookups, such as databases and search engines.

🌟 An AVL tree is a self-balancing binary search tree named after its inventors, Georgy Adelson-Velsky and Evgenii Landis. In an AVL tree, the heights of the left and right subtrees of any node differ by at most one, ensuring the tree remains balanced. This balance is maintained through rotations during insertion and deletion operations. The AVL tree's balanced nature guarantees that operations such as search, insertion, and deletion have a time complexity of (O(log n)), making it highly efficient for applications requiring frequent data modifications and lookups."""

    if condition == "full":
        print(tree_ascii)
        print(tree_def)
    elif condition == "def":
        print(tree_def)


# Run the tree module on its own
if __name__ == "__main__":
    tree_main()
