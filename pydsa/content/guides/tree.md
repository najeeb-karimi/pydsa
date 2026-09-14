# Tree
> A tree stores items as nodes connected in a hierarchy that starts from a single root at the top. Each node can have children, and every node except the root has exactly one parent.

## What it is
A tree is a [data structure](glossary:data-structure) made of [nodes](glossary:node) joined by [edges](glossary:edge). The top node is the [root](glossary:root). The nodes directly below a node are its children, and the node directly above it is its [parent](glossary:parent-and-child). Nodes without children are called [leaves](glossary:leaf). A tree never contains a [cycle](glossary:cycle), so following edges downward can never lead you back to a node you already passed.

In a [binary tree](glossary:binary-tree), each node has at most two children: a left one and a right one. PyDSA has two binary trees, the binary search tree (BST) and the AVL tree.

## How it works
In a binary search tree, every key in a node's left [subtree](glossary:subtree) is smaller than the node's key, and every key in its right subtree is larger. To find a key, you start at the root and go left or right depending on whether the key is smaller or larger, ruling out a whole subtree at every step. Inserting follows the same path and adds the new key as a leaf where the path ends.

How quick that is depends on the tree's [height](glossary:height). A tree with full levels is short and bushy, so every path is short. But a tree can also grow into one long chain, and then a search visits almost every node. An AVL tree prevents that by [rotating](glossary:rotation) nodes to stay balanced.

A [traversal](glossary:traversal) visits every node in a set order:
- Inorder visits the left subtree, then the node, then the right subtree. In a binary search tree, that lists the keys in sorted order.
- Preorder visits a node before its subtrees, and postorder visits it after them.
- Level order visits the tree one [level](glossary:level) at a time, from the root down.

## Real-life analogy
The folders on your computer. One folder at the top holds other folders, which hold more folders and files, and every file sits in exactly one folder.

## When to use it
- Your data is naturally a hierarchy, like folders, a company's org chart or the parts of a web page.
- You want to keep keys sorted while you add and remove them, and still find any key quickly.
- You need the smallest or largest key, or every key between two values.

## When to avoid it
- You only need to know whether a key exists and don't care about order; a hash table is usually faster.
- Your data is a simple list that you go through from start to end.

## In PyDSA
- After the tree opens, you choose a BST or an AVL tree. You can also open one directly with its topic ID, `bst` or `avl-tree`.
- Both trees hold keys of one data type, numbers or strings, and both allow duplicate keys.
- Trees are drawn from the top down. A tree too wide for the terminal is shown as an outline instead.
- `Tree Stats` shows the height, the number of nodes and leaves, and the smallest and largest keys.
