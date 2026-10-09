# B-Tree
> A B-tree stores several sorted keys in each node and keeps every leaf at the same depth. Choose its minimum degree to see how wider nodes make a shorter tree.

## What it is
A B-tree is a search tree whose [nodes](glossary:node) hold several sorted [keys](glossary:key). An internal node with k keys has k + 1 children, one for each range between or beyond the keys. All [leaves](glossary:leaf) are at the same depth.

## How it works
The minimum degree t controls node size. Every node holds at most 2t − 1 keys. A non-root node holds at least t − 1 keys; a nonempty root can hold fewer.

Searching finds the possible child range using the node's sorted keys. Insertion splits a full child before descending: its middle key moves into the parent, and the keys on either side become two nodes. A full root splits into a new level.

Before deletion descends into a minimum-size child, it borrows a key through the parent from a larger sibling, or merges two siblings with their separator key. For an internal key, a predecessor or successor can replace it when that child has enough keys. Otherwise its neighboring children merge. An empty root gives way to its only child.

## Real-life analogy
Think of a library directory with several divider cards in each drawer. Each divider points to a narrower range of drawers. Splitting an overcrowded drawer or combining nearly empty drawers keeps every route to a book equally deep.

## When to use it
Use it to explore how wide search trees work. Grouping many keys into a node is useful for indexes that read data in blocks, such as database or disk indexes.

## When to avoid it
Use a binary search tree to learn one-key decisions first. If you need only equality lookups, a hash table is simpler. This learning implementation keeps everything in memory and does not implement disk storage.

## In PyDSA
Choose finite numbers or strings and a minimum degree from 2 to 10 in the create flow. The example uses degree 2. The core accepts any integer degree of at least 2. Duplicates are retained, and Delete removes one occurrence. Inorder lists every key in sorted order; preorder and postorder list all keys of a node before or after its children, and level order reads whole nodes left to right. Stats distinguish keys from nodes. Search paths, traversals, splits, borrowing and merges are narrated. Examples, random data, practice and an insertion-path experiment are available.
