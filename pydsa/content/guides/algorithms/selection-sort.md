# Selection Sort
> Selection Sort finds the smallest value in the unsorted part of the list and swaps it to the front of that part. It repeats until the whole list is sorted, one position at a time.

## What it is
Selection Sort is a [comparison sort](glossary:comparison-sort) that divides the list into two parts: a sorted part at the front, which starts out empty, and an unsorted part with everything else. Every pass selects the smallest value of the unsorted part and moves it to the end of the sorted part.

## How it works
1. Look through the whole unsorted part and remember where its smallest value is.
2. Swap that value with the first value of the unsorted part. The sorted part is now one value longer.
3. Repeat from step 1 on the rest of the list, until only one value is left.

For example, on `[3, 1, 2]`, the first pass finds 1 and swaps it with 3, giving `[1, 3, 2]`. The second pass finds 2 and swaps it with 3, giving `[1, 2, 3]`.

Selection Sort makes the same comparisons however the list starts out, because it has to look through the entire unsorted part to be sure it found the smallest value.

## Real-life analogy
Picking players for a team, where the captain always chooses the best player who's still waiting. Every pick means looking over everyone who's left.

## When to use it
- Learning about sorting, since the idea is easy to picture.
- Writing to memory is expensive, since it makes at most one swap per pass.

## When to avoid it
- Almost always in practice. It does the same large amount of comparing even on a sorted list.
- You need a [stable](glossary:stable-sort) sort. Its long-distance swaps can change the order of equal values.

## In PyDSA
- Every pass is one step, including passes where the smallest value was already in place and is swapped with itself.
- For descending order, each pass selects the largest value instead.
- Run `Compare All Algorithms` on a sorted list and on a reversed one: Selection Sort's comparisons stay exactly the same.
