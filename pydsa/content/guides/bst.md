# Binary Search Tree (BST)
> A binary search tree keeps every smaller key to the left of a node and every larger key to the right. Each comparison rules out a whole side of the tree, so finding a key is quick as long as the tree stays short.

## What it is
A binary search tree, or BST, is a [binary tree](glossary:binary-tree) with one rule that holds at every [node](glossary:node): all the keys in its left [subtree](glossary:subtree) are smaller than its [key](glossary:key), and all the keys in its right subtree are larger or equal. Because of that rule, an inorder [traversal](glossary:traversal) always lists the keys in sorted order.

## How it works
- Searching starts at the [root](glossary:root). If the key you want is smaller than the node's key, you go left, and otherwise you go right. You stop when you find the key or run out of nodes.
- Inserting follows the same path as a search and attaches the new key as a [leaf](glossary:leaf) where the path ends.
- Deleting depends on how many children the node has. A leaf is simply removed, and a node with one child is replaced by that child. A node with two children takes the key of its [in-order successor](glossary:in-order-successor), the smallest key in its right subtree, and the successor's old node is deleted instead.
- The smallest key is found by going left until you can't anymore, and the largest by going right.

A BST doesn't balance itself, so its shape depends on the order the keys arrive in. A random order usually gives a bushy tree. Keys that arrive already sorted build a tree where every node has only a right child, which is really a linked list, and searching it checks every node.

## Real-life analogy
Guessing a number between 1 and 100 while someone tells you "higher" or "lower" after each guess. Every answer rules out part of the range, just as every comparison in a BST rules out one side of a node.

## When to use it
- You want to understand ordered trees: the BST is the base that balanced trees build on.
- Keys arrive in a fairly random order, and you need them kept sorted while you add and remove them.
- You need sorted output, the smallest or largest key, or the keys in a range.

## When to avoid it
- Keys may arrive sorted or nearly sorted, which makes the tree tall and slow. Use a self-balancing tree, such as the AVL tree.
- You only need to know whether a key exists; a hash table is faster on average.

## In PyDSA
- You choose whether the BST holds numbers or strings, and every key must be of that type.
- Duplicate keys are allowed and go into the right subtree.
- `Delete` removes one copy of a key.
- Try inserting 1, 2, 3, 4 and 5 in that order, then display the tree to watch a BST turn into a chain.
