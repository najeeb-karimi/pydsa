# Min Heap
> A min heap keeps the smallest key at its root, and every parent is smaller than or equal to its children. Looking at the smallest key is instant, and removing it only takes a short trip down the tree.

## What it is
A min heap is a [complete binary tree](glossary:complete-binary-tree) stored in an array, where every parent's [key](glossary:key) is smaller than or equal to the keys of its children. That's the [heap property](glossary:heap-property) of a min heap. It says nothing about the order of siblings, so the second-smallest key is one of the root's children, but not necessarily the left one.

## How it works
- `Insert` appends the key as the last leaf, then [sifts it up](glossary:sifting): while the key is smaller than its parent, the two swap.
- `Extract Min` removes the root and moves the last leaf into its place, then sifts that key down: while it's larger than one of its children, it swaps with the smaller child.
- `Peek Min` reads the root without changing anything.
- `Build from a List` uses [heapify](glossary:heapify). It treats the list as a tree and sifts down every parent, starting from the last parent and working back to the root. Most nodes sit near the bottom and barely move, which makes this quicker than inserting the keys one at a time.

The largest key in a min heap is always a [leaf](glossary:leaf), but it could be any of them, so finding it means checking every leaf.

## Real-life analogy
A to-do list where you always do the task with the nearest deadline first. You don't need the whole list sorted, only to know which deadline comes next.

## When to use it
- You always want the smallest item next, like the nearest deadline or the shortest distance found so far.
- Dijkstra's algorithm and Prim's algorithm, which repeatedly take the closest vertex or the lightest edge.
- Merging many sorted lists into one, by always taking the smallest of their front items.

## When to avoid it
- You need the largest item instead; use a max heap.
- You need to find or remove keys other than the smallest one.

## In PyDSA
- You choose whether the heap holds numbers or strings, and duplicate keys are allowed.
- Every operation that moves keys shows each step as a tree and as the array, with the keys that moved highlighted.
- `Tree Stats` shows the height and the number of nodes and leaves, which all follow from the heap's size alone.
