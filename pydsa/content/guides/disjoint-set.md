# Disjoint Set
> A disjoint set, also called Union-Find, keeps track of which elements are grouped together, in groups that never overlap. It can merge two groups and tell you whether two elements share a group, both almost instantly.

## What it is
A disjoint set splits elements into sets that share no elements, so each element belongs to exactly one set. Each set has a [representative](glossary:representative), one of its members that acts as the name of the set. It supports two main operations:
- `Find` returns the representative of an element's set.
- `Union` merges the sets of two elements into one.

Two elements are connected when `Find` gives the same representative for both of them.

## How it works
Each set is stored as a tree inside a parent array. Every element points to its parent, and the [root](glossary:root) of each tree points to itself and is the set's representative.
- `Find` follows the parent links up from an element until it reaches the root.
- `Union` finds both roots and makes one of them the parent of the other.

Left alone, those trees could grow into long chains that make `Find` slow. Two tricks keep them flat:
- [Union by rank](glossary:union-by-rank) attaches the root of the shorter tree under the root of the taller one. Every root has a rank, which is an upper limit on the height of its tree.
- [Path compression](glossary:path-compression) makes every element visited during a `Find` point straight at the root, so the next `Find` on any of them takes a single step.

Together, they make both operations so quick that, in practice, they take about the same time however many elements there are. Their cost grows with the [inverse Ackermann function](glossary:inverse-ackermann-function), which stays below 5 for any number of elements you could ever store.

## Real-life analogy
Friend groups at a new school. At first, everyone is on their own. When two people become friends, their groups merge into one. To tell whether two students are in the same group, you ask each of them who their group's leader is and compare the answers.

## When to use it
- Kruskal's minimum spanning tree algorithm, to check whether an edge would close a cycle.
- Detecting cycles in an undirected graph.
- Tracking which computers in a network can reach each other as cables are added.
- Grouping the neighboring pixels of the same color into regions of an image.

## When to avoid it
- You need to split groups apart again; a disjoint set can only merge them.
- You often need to list the members of a group, since the structure only stores parent links.

## In PyDSA
- The elements are numbered from 0, so the parent and rank arrays are plain lists.
- The display shows the parent and rank arrays, followed by every set with its root and members.
- `Find` tells you when path compression relinked elements, and shows the arrays again so you can see what changed.
- `List Sets` follows every element to its root without compressing any paths, so it never changes the structure.
