# Shell Sort
> Shell Sort is Insertion Sort with a head start: it first sorts values that are far apart, then closer ones, and finishes with a normal Insertion Sort. Moving values long distances early leaves little work for the end.

## What it is
Shell Sort is a [comparison sort](glossary:comparison-sort) named after its inventor, Donald Shell. Insertion Sort is slow when a value has to travel a long way, because it only moves one position at a time. Shell Sort fixes that by first sorting values that are a gap apart, so values can cross the list in big jumps.

## How it works
1. Choose a gap. PyDSA starts with half the length of the list.
2. Do a gapped insertion sort: for every position from the gap onward, take its value and shift it back, one gap at a time, past the larger values in front of it. Afterward, every value is in order with the value one gap before it.
3. Halve the gap and repeat.
4. The last round uses a gap of 1, which is a plain Insertion Sort. By then, the list is nearly sorted, so this round is quick.

For example, a list of 8 values uses the gaps 4, 2 and 1. The first round sorts the pairs at positions 0 and 4, 1 and 5, 2 and 6, and 3 and 7.

How fast Shell Sort is depends on its gaps. Halving is the simplest choice, but some other sequences of gaps are faster.

## Real-life analogy
Tidying a messy bookshelf. First you move each book roughly into the right section of the shelf, then into the right part of its section, and only at the end do you swap neighbors to get the exact order.

## When to use it
- Medium-sized lists, where it's much faster than Insertion Sort and still simple.
- Small devices without room for recursion or extra memory, since it sorts [in place](glossary:in-place) with plain loops.

## When to avoid it
- You need a [stable](glossary:stable-sort) sort; the long jumps can reorder equal values.
- Large lists, where Merge Sort, Quick Sort or Heap Sort are faster and more predictable.

## In PyDSA
- The gaps start at half the length of the list and halve after every round, so 8 values use the gaps 4, 2 and 1.
- Every gap is one step, so you can watch the list get closer to sorted after each round.
