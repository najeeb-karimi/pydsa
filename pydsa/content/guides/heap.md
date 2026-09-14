# Heap and Priority Queue
> A heap is a tree that always keeps the smallest key, or the largest one, at its root, where you can grab it right away. A priority queue uses a heap to always serve the most important item next.

## What it is
A heap is a [complete binary tree](glossary:complete-binary-tree) that follows the [heap property](glossary:heap-property):
- In a min heap, every parent's [key](glossary:key) is smaller than or equal to its children's keys, so the smallest key is at the [root](glossary:root).
- In a max heap, every parent's key is larger than or equal to its children's keys, so the largest key is at the root.

A heap is only partly sorted. The root always holds the extreme key, but siblings and cousins can be in any order.

A priority queue is a queue where each item has a [priority](glossary:priority), and the item with the highest priority leaves first, however long the others have waited. A heap is the classic way to build one.

## How it works
Because a heap is a complete tree, it fits in a plain array without any links. The root is at index 0, and the children of the node at index `i` are at `2i + 1` and `2i + 2`. Reading the array from left to right is the same as reading the tree level by level.

- Inserting adds the key as the last leaf, then [sifts it up](glossary:sifting): as long as it belongs above its parent, the two swap places.
- Extracting the root moves the last leaf into the root's place, then sifts it down: as long as a child belongs above it, it swaps places with the child that belongs highest.
- [Heapify](glossary:heapify) builds a heap from a whole list at once by sifting down every parent, from the last parent back up to the root.

A complete tree is never taller than it needs to be, and a sift only travels along one path between the top and the bottom.

## Real-life analogy
A hospital emergency room. Patients aren't seen in the order they arrive: the most urgent case always goes next, and a newly arrived patient in serious condition moves ahead of everyone less urgent.

## When to use it
- You repeatedly need the smallest or largest item, but not the rest in order.
- Scheduling by importance, like the tasks of an operating system or the events of a simulation.
- Graph algorithms such as Dijkstra's shortest paths and Prim's minimum spanning tree.
- Finding the 10 largest items of a huge list without sorting all of it.

## When to avoid it
- You need to search for any key; a heap has to check its keys one by one.
- You need every item in sorted order all the time; a balanced tree keeps them sorted.

## In PyDSA
- After the heap opens, you choose a min heap, a max heap or the priority queue. You can also open one directly with `min-heap`, `max-heap` or `priority-queue`.
- Inserting, extracting and building a heap from a list show every swap, both as a tree and as the array.
- The priority queue is built on the min heap, so a smaller number means a higher priority.
