# Merge Sort
> Merge Sort splits the list in half, sorts each half, and merges the two sorted halves back together. It's always fast and keeps equal values in their original order.

## What it is
Merge Sort is a [divide and conquer](glossary:divide-and-conquer) [comparison sort](glossary:comparison-sort). A list with one value is already sorted, and two sorted lists are easy to combine, so Merge Sort breaks the list down until the pieces are tiny and then builds the sorted list back up.

## How it works
1. If the part of the list has fewer than two values, it's already sorted.
2. Otherwise, split it into a left half and a right half, and Merge Sort each half using [recursion](glossary:recursion).
3. Merge the two sorted halves: compare their front values, take the one that comes first, and repeat until one half runs out. Then copy over what's left of the other half.
4. Write the merged values back into the list.

For example, `[3, 1, 4, 2]` splits into `[3, 1]` and `[4, 2]`. Those become `[1, 3]` and `[2, 4]`, and merging them takes 1, 2, 3 and 4 in turn.

A list can only be halved a few times before every piece holds a single value, and each level of merging touches every value once. That's why Merge Sort is fast on every list, sorted or not.

## Real-life analogy
Two teachers each sort half of a stack of exams by name. Then they combine their piles by repeatedly taking whichever of the two top exams comes first.

## When to use it
- You need a [stable](glossary:stable-sort) sort that's always fast, like when you sort a table by one column and then by another.
- Sorting linked lists, where merging only relinks nodes.
- Data too big to fit in memory, which is sorted in chunks that are merged afterward.

## When to avoid it
- Memory is tight. Merging needs room for a temporary copy of the values being merged.
- The lists are tiny, where Insertion Sort's simplicity wins.

## In PyDSA
- Every merge is one step, starting with the smallest pieces and ending with the merge that joins the two halves of the whole list.
- When two front values are equal, the one from the left half is taken first, which is what keeps Merge Sort stable.
