# Insertion Sort
> Insertion Sort builds the sorted list one value at a time, taking the next value and sliding it back into its place among the values before it. It's quick on lists that are already nearly sorted.

## What it is
Insertion Sort is a [comparison sort](glossary:comparison-sort) that keeps the front of the list sorted. At the start, the sorted part holds only the first value. Each step takes the first value of the unsorted part and inserts it into the right position in the sorted part.

## How it works
1. Take the next unsorted value and hold on to it.
2. Compare it with the sorted values before it, starting with the closest one. Every value that's larger shifts one position to the right to make room.
3. When you reach a value that's smaller or equal, or the start of the list, put the held value into the gap.
4. Repeat until every value has been inserted.

For example, on `[3, 1, 2]`, inserting 1 shifts 3 to the right, giving `[1, 3, 2]`. Inserting 2 shifts 3 to the right and stops at 1, giving `[1, 2, 3]`.

On a list that's already sorted, every value is compared once and stays where it is, so one quick pass is all it takes.

## Real-life analogy
Sorting a hand of cards as they're dealt to you. You pick up each new card and slide it left past the higher cards until it sits in the right spot.

## When to use it
- Small lists, where its simplicity beats the extra machinery of faster algorithms. Many sorting libraries switch to Insertion Sort for short stretches of a list.
- Lists that are nearly sorted, or data that arrives one value at a time and has to stay sorted.
- You need a [stable](glossary:stable-sort) sort that works [in place](glossary:in-place).

## When to avoid it
- Large lists in random or reversed order, where values have to shift a long way. Doubling the length makes it about four times as slow.

## In PyDSA
- Every insertion is one step, so a list of 8 values always takes 7 steps.
- The writes count every shift as well as every placement, so a reversed list shows many more writes than a sorted one.
