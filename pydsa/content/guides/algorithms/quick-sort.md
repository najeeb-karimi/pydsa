# Quick Sort
> Quick Sort picks a pivot value, moves everything smaller to its left and everything larger to its right, then sorts both sides the same way. On most lists, it's one of the fastest sorting algorithms there is.

## What it is
Quick Sort is a [divide and conquer](glossary:divide-and-conquer) [comparison sort](glossary:comparison-sort). Its key step is the partition: it chooses a [pivot](glossary:pivot) and rearranges the list so the pivot lands in its final sorted position, with smaller values before it and larger values after it. Then it sorts the two sides using [recursion](glossary:recursion).

## How it works
1. Choose a pivot. PyDSA uses the last value of the part being sorted.
2. Partition: go through the other values, and move each one that belongs before the pivot to the front of the part. Then swap the pivot into the spot right after them.
3. The pivot is now in its final place. Quick Sort the values on its left, then the values on its right.
4. A part with one value or none is already sorted, so the recursion stops there.

For example, sorting `[3, 1, 4, 2]` with the pivot 2 moves 1 to the front and places 2 right after it: `[1, 2, 4, 3]`. The left side, `[1]`, is done, and sorting the right side, `[4, 3]`, with the pivot 3 gives `[1, 2, 3, 4]`.

Quick Sort is fast when the pivots split the list into parts of similar size. When the pivot is always the smallest or largest value, as with the last value of an already sorted list, each partition only sets aside that one value, and Quick Sort becomes slow.

## Real-life analogy
Sorting a pile of exams by grade. You take one exam, put the lower grades on its left and the higher grades on its right, and then do the same with each smaller pile.

## When to use it
- General-purpose sorting of large lists in memory, where it's usually faster than the other comparison sorts.
- You want to sort [in place](glossary:in-place), without a second copy of the list.

## When to avoid it
- You need a [stable](glossary:stable-sort) sort; partitioning can reorder equal values.
- The list may already be sorted or reversed, and you use a simple pivot rule like PyDSA's; that's the slow case. Real libraries choose their pivots more carefully.
- You need a guarantee that it's never slow; Merge Sort and Heap Sort always stay fast.

## In PyDSA
- The pivot is always the last value of the part being partitioned, which is known as the Lomuto partition scheme.
- Every partition is one step, and each step shows the pivot in its final place.
- Run Quick Sort on a sorted list in `Compare All Algorithms` to see how many more comparisons it needs.
