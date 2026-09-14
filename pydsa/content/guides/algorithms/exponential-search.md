# Exponential Search
> Exponential Search checks positions 1, 2, 4, 8 and so on until it passes the target, then runs Binary Search in the range it found. It's especially quick when the target is near the start of a long list.

## What it is
Exponential Search, also called doubling search, is a search for sorted data in two phases. First, it finds a range that must contain the target by doubling the position it checks. Then, it hands that range over to Binary Search.

## How it works
1. Check the first value. If it's the target, you're done.
2. Check position 1, then 2, then 4, 8, 16 and so on, doubling each time, until the value at the position is greater than or equal to the target, or the position is past the end of the list.
3. If the value at that position is the target, you're done.
4. Otherwise, the target can only be between the previous position and this one, because the previous value was smaller. Run Binary Search on just that range.

The range it finds is never more than twice as far out as the target's position, so the work depends on where the target is, not on the length of the whole list.

## Real-life analogy
Looking for a house number on a very long street when you don't know how long the street is. You check the 1st, 2nd, 4th, 8th and 16th houses, and once you've gone too far, you search only the last stretch you covered.

## When to use it
- Sorted lists where the target is usually near the start.
- Sorted data whose length you don't know, like a stream of values, since the search never needs the end.

## When to avoid it
- The target could be anywhere in a list you can measure; plain Binary Search is just as good and simpler.
- The data isn't sorted.

## In PyDSA
- Exponential Search runs on a sorted copy of your list and reports the index where the target first appears in your original list.
- The numbered positions show the doubling checks first, then the Binary Search inside the final range.
