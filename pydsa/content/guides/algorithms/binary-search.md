# Binary Search
> Binary Search looks at the middle of a sorted list and throws away the half that can't contain the target. Every check halves what's left, so even a huge list needs only a few checks.

## What it is
Binary Search is a search for sorted data. Because the values are in order, one comparison with the middle value tells you which half the target must be in, and the other half can be ignored completely.

## How it works
1. Keep track of a range, from a low position to a high position, that could hold the target. At first, it's the whole list.
2. Check the value in the middle of the range.
3. If it equals the target, you've found it.
4. If it's smaller than the target, the target can only be on its right, so the range now starts after the middle.
5. If it's larger, the target can only be on its left, so the range now ends before the middle.
6. Repeat from step 2 until you find the target or the range is empty.

For example, searching `[1, 3, 5, 7, 9, 11, 13]` for 11 first checks 7 in the middle, then 11 in the middle of the right half, and stops.

Doubling the length of the list only adds one more check, which is why Binary Search stays fast on huge lists. The number of checks grows with the [logarithm](glossary:logarithm) of the length.

## Real-life analogy
Guessing a number between 1 and 100 while someone tells you "higher" or "lower" after each guess. Guessing 50 first rules out half the numbers at once, and you never need more than 7 guesses.

## When to use it
- The data is already sorted, like a dictionary, a sorted log file or a list you keep in order.
- You search many times, so sorting once and then using Binary Search pays off.

## When to avoid it
- The data isn't sorted, and you'll only search once; a Linear Search is cheaper than sorting first.
- You can't jump to the middle quickly, as in a linked list.

## In PyDSA
- Binary Search runs on a sorted copy of your list and reports the index where the target first appears in your original list.
- The positions it checked are numbered under the sorted copy, so you can watch the range shrink.
- Sorting the copy takes time too, which is why the array's complexity table includes the sort in Binary Search's cost.
