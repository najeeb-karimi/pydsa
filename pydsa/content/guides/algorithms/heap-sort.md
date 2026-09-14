# Heap Sort
> Heap Sort turns the list into a max heap, then repeatedly swaps the largest value, at the root, to the end of the list and repairs the heap. It's always fast and needs no extra memory.

## What it is
Heap Sort is a [comparison sort](glossary:comparison-sort) that uses a max heap stored inside the list itself. In a max heap, every parent is larger than its children, so the largest value always sits at index 0, the [root](glossary:root). Heap Sort keeps taking that largest value and placing it at the end.

## How it works
1. [Heapify](glossary:heapify) the list: treat it as a [complete binary tree](glossary:complete-binary-tree), where the children of index `i` are at `2i + 1` and `2i + 2`, and [sift down](glossary:sifting) every parent, from the last parent back to the root. The list is now a max heap.
2. Swap the root, which holds the largest value, with the last value of the heap. That value is now in its final place, so the heap shrinks by one.
3. The new root is probably too small, so sift it down: swap it with its larger child until both of its children are smaller.
4. Repeat steps 2 and 3 until the heap holds a single value.

Sifting down only follows one path from the root toward a leaf, and a complete tree is short, so every round stays quick however the list starts out.

## Real-life analogy
A sports league that always knows its top team. Every week, the top team retires to the hall of fame, and the remaining teams play a few matches to decide the new leader, instead of replaying the whole season.

## When to use it
- You need a sort that's always fast, without Quick Sort's slow case.
- Memory is tight, since it sorts [in place](glossary:in-place).

## When to avoid it
- You need a [stable](glossary:stable-sort) sort; swapping the root to the end reorders equal values.
- You want the fastest sort in practice. Heap Sort jumps around the list, which computers read more slowly than neighboring values, so Quick Sort and Merge Sort usually beat it.

## In PyDSA
- For ascending order, PyDSA builds a max heap, and for descending order, a min heap.
- Steps come from both phases: one after each parent is sifted down while building the heap, then one after each swap to the end and one after each repair.
