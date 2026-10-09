"""Balanced tree updates checked against a multiset and independently checked invariants."""

import math
import random

import pytest

from pydsa.core.b_tree import BTree, snapshot as b_snapshot
from pydsa.core.errors import EmptyError, InvalidTypeError, NotFoundError
from pydsa.core.red_black_tree import RedBlackTree, snapshot as rb_snapshot


def red_black_rules(tree):
    if tree.root is not None:
        assert tree.root.color == "B" and tree.root.parent is None

    def check(node, parent, low, high):
        if node is None:
            return 1
        assert node.parent is parent
        assert node.color in ("R", "B")
        assert low is None or low <= node.key
        assert high is None or node.key <= high
        if node.color == "R":
            assert node.left is None or node.left.color == "B"
            assert node.right is None or node.right.color == "B"
        left = check(node.left, node, low, node.key)
        right = check(node.right, node, node.key, high)
        assert left == right
        return left + (node.color == "B")

    assert check(tree.root, None, None, None) == tree.black_height()
    assert tree.height() <= 2 * math.log2(len(tree) + 1) if len(tree) else tree.height() == 0


def b_tree_rules(tree):
    depths = set()

    def check(node, depth, low, high):
        assert node.keys == sorted(node.keys)
        assert (1 if node is tree.root else tree.t - 1) <= len(node.keys) <= 2 * tree.t - 1
        assert low is None or low <= node.keys[0]
        assert high is None or node.keys[-1] <= high
        if node.leaf:
            depths.add(depth)
        else:
            assert len(node.children) == len(node.keys) + 1
            bounds = [low, *node.keys, high]
            for index, child in enumerate(node.children):
                check(child, depth + 1, bounds[index], bounds[index + 1])

    if tree.root is not None:
        check(tree.root, 1, None, None)
        assert depths == {tree.height()}
    else:
        assert tree.height() == 0


FACTORIES = [RedBlackTree, *(lambda t=t: BTree(t) for t in (2, 3, 5, 10))]


@pytest.mark.parametrize("factory", FACTORIES, ids=["red-black", "b-2", "b-3", "b-5", "b-10"])
@pytest.mark.parametrize("seed", range(12))
def test_mixed_updates_match_a_sorted_multiset(factory, seed):
    rng = random.Random(seed)
    tree, model = factory(), []
    for _ in range(220):
        key = rng.randrange(-25, 26)
        if rng.random() < 0.58:
            tree.insert(key)
            model.append(key)
        elif key in model:
            tree.delete(key)
            model.remove(key)
        else:
            with pytest.raises(NotFoundError):
                tree.delete(key)
        assert tree.inorder() == sorted(model)
        assert len(tree) == len(model)
        assert (key in tree) == (key in model)
        for walk in (tree.preorder, tree.postorder, tree.level_order):
            assert sorted(walk()) == sorted(model)
        red_black_rules(tree) if isinstance(tree, RedBlackTree) else b_tree_rules(tree)
        if model:
            assert tree.min() == min(model) and tree.max() == max(model)
    rng.shuffle(model)
    for key in model:
        tree.delete(key)
        red_black_rules(tree) if isinstance(tree, RedBlackTree) else b_tree_rules(tree)
    assert tree.root is None and len(tree) == tree.leaf_count() == 0


@pytest.mark.parametrize("tree", [RedBlackTree("str"), BTree(2, "str")])
def test_words_duplicates_errors_and_empty_stats(tree):
    for word in ("pear", "apple", "pear", "fig", "banana", "cherry", "date"):
        tree.insert(word)
    tree.delete("pear")
    assert tree.inorder() == ["apple", "banana", "cherry", "date", "fig", "pear"]
    assert tree.search("missing") is None
    with pytest.raises(InvalidTypeError):
        tree.insert(3)
    for word in tree.inorder():
        tree.delete(word)
    assert tree.inorder() == tree.level_order() == []
    for operation in (tree.min, tree.max):
        with pytest.raises(EmptyError):
            operation()


@pytest.mark.parametrize("key", [True, float("inf"), float("nan"), "word", None])
@pytest.mark.parametrize("factory", [RedBlackTree, BTree])
def test_invalid_numeric_keys_are_rejected_without_changes(factory, key):
    tree = factory()
    for operation in (tree.insert, tree.search, tree.delete):
        with pytest.raises(InvalidTypeError):
            operation(key)
    assert tree.root is None


@pytest.mark.parametrize("degree", [True, 1, 0, -1, 2.5, "2"])
def test_b_tree_degree_must_be_an_integer_at_least_two(degree):
    with pytest.raises(ValueError):
        BTree(degree)


@pytest.mark.parametrize("factory,freeze", [(RedBlackTree, rb_snapshot), (BTree, b_snapshot)])
def test_traces_capture_changes_without_mutable_links(factory, freeze):
    tree, trace = factory(), []
    for key in range(40):
        tree.insert(key, trace)
    assert trace[-1].snapshot == freeze(tree.root)
    saved = repr(trace)
    for key in range(40):
        tree.delete(key)
    assert repr(trace) == saved
    missing = []
    assert tree.search(10, missing) is None
    assert missing[-1].kind == "tree_missing"


@pytest.mark.parametrize("factory", [RedBlackTree, BTree])
@pytest.mark.parametrize("method", ["inorder", "preorder", "postorder", "level_order"])
def test_each_traversal_traces_the_real_visit_order(factory, method):
    tree = factory()
    for key in (9, 3, 15, 1, 7, 12, 20, 7):
        tree.insert(key)
    trace = []
    result = getattr(tree, method)(trace)
    assert [event.data["key"] for event in trace] == result
    assert [event.data["keys"] for event in trace] == [tuple(result[:i]) for i in range(1, len(result) + 1)]
    assert all(event.kind == "tree_walk" for event in trace)


@pytest.mark.parametrize("factory", [RedBlackTree, BTree])
def test_invalid_data_types_are_rejected(factory):
    with pytest.raises(ValueError):
        factory(data_type="any")


@pytest.mark.parametrize("factory", FACTORIES, ids=["red-black", "b-2", "b-3", "b-5", "b-10"])
@pytest.mark.parametrize("values", [list(range(64)), list(range(63, -1, -1)), [7] * 64],
                         ids=["ascending", "descending", "all-equal"])
def test_ordered_and_equal_keys_stay_balanced_until_empty(factory, values):
    tree = factory()
    for key in values:
        tree.insert(key)
        red_black_rules(tree) if isinstance(tree, RedBlackTree) else b_tree_rules(tree)
    remaining = sorted(values)
    for key in values:
        tree.delete(key)
        remaining.remove(key)
        assert tree.inorder() == remaining
        red_black_rules(tree) if isinstance(tree, RedBlackTree) else b_tree_rules(tree)
