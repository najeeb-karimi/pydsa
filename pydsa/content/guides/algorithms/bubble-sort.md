# Bubble Sort
> Bubble Sort walks through the list again and again, swapping every pair of neighbors that are in the wrong order. After each pass, the largest remaining value has bubbled up to its place at the end.

## What it is
Bubble Sort is a simple [comparison sort](glossary:comparison-sort) that only ever compares and swaps values sitting right next to each other. It's named after the way large values rise toward the end of the list, like bubbles rising in water.

## How it works
1. Start at the beginning of the list and compare the first two values.
2. If they're in the wrong order, swap them.
3. Move one position to the right and compare the next pair. Keep going until the end of the list, where the largest value has now arrived.
4. Repeat the pass, stopping one position earlier each time, since the end of the list is already sorted.
5. If a whole pass makes no swaps, the list is sorted, and you can stop early.

For example, on `[3, 2, 1]`, the first pass swaps 3 and 2, then 3 and 1, giving `[2, 1, 3]`. The second pass swaps 2 and 1, giving `[1, 2, 3]`.

## Real-life analogy
Lining up children by height when only neighbors may swap places. The tallest child keeps swapping forward until reaching the end of the line, then the second tallest does the same, and so on.

## When to use it
- Learning how sorting works, since every step is easy to follow.
- Very small lists, or lists that are almost sorted already, where the early stop kicks in after a pass or two.

## When to avoid it
- Any list of real size. Every pass looks at nearly the whole list, so doubling the length makes it about four times as slow. Insertion Sort does less work, and Merge Sort and Quick Sort are much faster.

## In PyDSA
- Every swap is a step, so a list in reverse order shows many steps.
- The sort stops as soon as a pass makes no swaps, so an already sorted list finishes after one pass without any steps.
- Bubble Sort is [stable](glossary:stable-sort): it only swaps neighbors that are strictly out of order, so equal values never pass each other.
