# Red-Black Tree
> A Red-Black Tree keeps keys sorted and its branches short by coloring nodes red or black. You can watch recoloring and rotations restore its rules after an insertion or deletion.

## What it is
A Red-Black Tree is a [binary tree](glossary:binary-tree) used to search sorted [keys](glossary:key). Every node has a color. The root is black, a red node cannot have a red child, and every path to a missing child contains the same number of black nodes. This count is called black height; missing children count as black too.

## How it works
To search, compare your key with the current node and choose its left or right child. Insertion adds a red leaf. If its parent is red, a fix-up either recolors a red parent and uncle, or uses a [rotation](glossary:rotation) with a black uncle. An inner bend needs a rotation before the final outer rotation.

Deletion removes one occurrence. With two children, its [in-order successor](glossary:in-order-successor) takes its place. Removing a black node can leave one branch with too few black nodes. The fix-up examines the sibling and its children, then recolors, rotates or carries that missing black upward. An absent sibling or child is black.

## Real-life analogy
Imagine sorting people into branching queues with red or black tickets. Red tickets cannot stand together, and every route to an exit must pass the same number of black tickets. Changing tickets and moving short sections of the queue keeps routes from becoming long chains.

## When to use it
Use it for a sorted collection that changes often. Its balancing rules keep searches short even when you insert keys in increasing order.

## When to avoid it
Use a hash table when you need only equality lookups. Use a B-tree to explore several keys in one node, or a simple BST when your main goal is learning basic search paths.

## In PyDSA
Choose finite numbers or strings. Duplicate keys are stored as separate nodes; insertion initially follows the right branch on a tie, but rotations can place equal keys on either side. Delete removes one occurrence. You can insert, delete, trace searches and four traversals, or inspect height, leaves and black height. Nodes show R or B as well as colors, so the diagram works with colors off. Examples and random trees are available, along with practice and an insertion-path experiment.
