# AVL Tree
> An AVL tree is a binary search tree that rebalances itself after every insert and delete. It keeps the heights of every node's two subtrees within one of each other, so the tree always stays short.

## What it is
An AVL tree, named after its inventors Adelson-Velsky and Landis, is a binary search tree that balances itself. Every [node](glossary:node) has a [balance factor](glossary:balance-factor): the [height](glossary:height) of its left [subtree](glossary:subtree) minus the height of its right subtree. In an AVL tree, every balance factor is -1, 0 or 1.

## How it works
Inserting and deleting start exactly as in a binary search tree. Then, on the way back up to the [root](glossary:root), each node on the path updates its height and checks its balance factor. If the balance factor has reached 2 or -2, the node is out of balance, and a [rotation](glossary:rotation) fixes it. A rotation turns a small part of the tree, lifting a child up and moving the node down, while keeping every key in the right order.

There are four cases, named after where the extra height is:
- Left Left: the left child's left side is too tall. One right rotation fixes it.
- Right Right: the right child's right side is too tall. One left rotation fixes it.
- Left Right: the left child's right side is too tall. A left rotation on the child turns it into a Left Left case, and a right rotation on the node finishes the job.
- Right Left: the mirror image, fixed by a right rotation on the child and then a left rotation on the node.

Each rotation changes only a few links. Because the tree never gets out of balance, the path from the root to any [leaf](glossary:leaf) always stays short.

## Real-life analogy
A hanging mobile. When one side gets heavier and the mobile starts to tilt, you rehang a piece so it levels out again. An AVL tree does the same whenever one side grows too tall.

## When to use it
- Keys can arrive in any order, including sorted order, and searches must stay quick.
- You search more often than you insert or delete, since the tree is kept strictly balanced.
- You need a sorted collection where inserts, deletes and lookups are always quick, not just usually.

## When to avoid it
- You insert and delete far more often than you search. Rotations add work, and more loosely balanced trees, such as red-black trees, rotate less often.
- You don't need the keys in order; a hash table is simpler and usually faster.

## In PyDSA
- You choose whether the tree holds numbers or strings, and duplicate keys are allowed.
- Every node stores its own height, so the tree's height is read straight from the root.
- The display shows each node's balance factor in parentheses, so you can check that it stays between -1 and 1.
- Try inserting 1, 2, 3, 4 and 5 in that order, as with the BST, and compare the two shapes.
