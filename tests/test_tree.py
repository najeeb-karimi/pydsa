"""Binary search tree and AVL tree: ordering, balance and type checks."""

import random

import pytest

from pydsa.core.errors import EmptyError, InvalidTypeError, NotFoundError
from pydsa.core.tree import AVLTree, BinarySearchTree


def is_ordered(node, low=None, high=None):
    """Left subtree keys <= node key <= right subtree keys (duplicates may sit on either side after rotations)."""
    if node is None:
        return True
    if (low is not None and node.key < low) or (high is not None and node.key > high):
        return False
    return is_ordered(node.left, low, node.key) and is_ordered(node.right, node.key, high)


def avl_height(node):
    """Return the real height, or -1 if a balance factor or stored height is wrong."""
    if node is None:
        return 0
    left, right = avl_height(node.left), avl_height(node.right)
    if left < 0 or right < 0 or abs(left - right) > 1 or node.height != 1 + max(left, right):
        return -1
    return 1 + max(left, right)


@pytest.mark.parametrize("tree_class", [BinarySearchTree, AVLTree], ids=lambda cls: cls.__name__)
def test_random_operations_match_a_sorted_list(tree_class):
    rng = random.Random(8)
    for _ in range(300):
        tree, model = tree_class("num"), []
        for _ in range(60):
            op = rng.choice(["insert", "insert", "delete", "search"])
            key = rng.randint(0, 30)  # A small range, so there are plenty of duplicates
            if op == "insert":
                tree.insert(key)
                model.append(key)
            elif op == "delete":
                if key in model:
                    tree.delete(key)
                    model.remove(key)
                else:
                    with pytest.raises(NotFoundError):
                        tree.delete(key)
            else:
                node = tree.search(key)
                assert (node is not None) == (key in model)
                assert node is None or node.key == key

            assert tree.inorder() == sorted(model)
            assert sorted(tree.preorder()) == sorted(model)
            assert sorted(tree.postorder()) == sorted(model)
            assert is_ordered(tree.root)
            if tree_class is AVLTree:
                assert avl_height(tree.root) >= 0


@pytest.mark.parametrize("tree_class", [BinarySearchTree, AVLTree], ids=lambda cls: cls.__name__)
def test_string_trees(tree_class):
    tree = tree_class("str")
    words = ["pear", "apple", "fig", "banana", "apple"]
    for word in words:
        tree.insert(word)
    assert tree.inorder() == sorted(words)
    assert "fig" in tree
    assert "kiwi" not in tree


@pytest.mark.parametrize("tree_class", [BinarySearchTree, AVLTree], ids=lambda cls: cls.__name__)
def test_rejects_keys_of_the_other_type(tree_class):
    with pytest.raises(InvalidTypeError):
        tree_class("num").insert("50")
    with pytest.raises(InvalidTypeError):
        tree_class("str").search(50)
    with pytest.raises(ValueError):
        tree_class("list")


def test_traversal_orders():
    tree = BinarySearchTree("num")
    for key in [50, 30, 10, 20, 70, 60, 80]:
        tree.insert(key)
    assert tree.inorder() == [10, 20, 30, 50, 60, 70, 80]
    assert tree.preorder() == [50, 30, 10, 20, 70, 60, 80]
    assert tree.postorder() == [20, 10, 30, 60, 80, 70, 50]


@pytest.mark.parametrize("tree_class", [BinarySearchTree, AVLTree], ids=lambda cls: cls.__name__)
def test_tree_metrics_match_brute_force(tree_class):
    rng = random.Random(9)
    for _ in range(200):
        tree, keys = tree_class("num"), [rng.randint(0, 50) for _ in range(rng.randint(0, 25))]
        for key in keys:
            tree.insert(key)
        for key in rng.sample(keys, len(keys) // 3):
            tree.delete(key)
            keys.remove(key)

        nodes = []  # (depth, node) in preorder, which visits each level from left to right

        def walk(node, depth):
            if node is not None:
                nodes.append((depth, node))
                walk(node.left, depth + 1)
                walk(node.right, depth + 1)

        walk(tree.root, 0)
        by_level = sorted(nodes, key=lambda pair: pair[0])  # A stable sort keeps the left-to-right order
        assert tree.level_order() == [node.key for _, node in by_level]
        assert tree.height() == max((depth + 1 for depth, _ in nodes), default=0)
        assert len(tree) == len(keys)
        assert tree.leaf_count() == sum(1 for _, node in nodes if node.left is None and node.right is None)
        if keys:
            assert tree.min() == min(keys) and tree.max() == max(keys)
        else:
            with pytest.raises(EmptyError):
                tree.min()
            with pytest.raises(EmptyError):
                tree.max()
        if tree_class is AVLTree:
            assert all(tree.balance_factor(node) in (-1, 0, 1) for _, node in nodes)


def test_avl_rotates_a_sorted_insertion_into_balance():
    tree = AVLTree("num")
    for key in range(1, 8):
        tree.insert(key)
    assert tree.preorder() == [4, 2, 1, 3, 6, 5, 7]
    assert tree.root.height == 3
