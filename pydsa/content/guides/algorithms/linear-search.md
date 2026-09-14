# Linear Search
> Linear Search checks the values one by one, from the first to the last, until it finds the target or runs out of values. It's the simplest search, and it works on any list, sorted or not.

## What it is
Linear Search, also called sequential search, is the most direct way to find a value: look at every item in turn. It doesn't need the data to be sorted or a way to jump to a position, so it also works on a linked list, where you can only follow the links from the head.

## How it works
1. Start at the first value.
2. If it equals the target, you've found it: return its position.
3. Otherwise, move on to the next value. On a linked list, that means following the next link.
4. If you reach the end without finding the target, it isn't there.

When the target is near the start, the search ends quickly. When it's near the end or missing, every value gets checked.

## Real-life analogy
Looking for a friend in a line of people by starting at the front and checking each face until you spot them.

## When to use it
- The list is small or unsorted, or you'll only search it once.
- The data can only be read in order, like a linked list or a file read from start to end.
- You need the first match in the original order.

## When to avoid it
- The list is large and you search it often. Sort it once and use Binary Search, or use a hash table.

## In PyDSA
- Linear Search runs on your list as it is, without sorting it, and returns the index of the first match.
- The positions it checked are numbered under the values, which shows that it always starts from index 0.
- The linked list's `Search` uses Linear Search too, following the links from the head.
