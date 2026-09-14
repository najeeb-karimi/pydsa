# Searching
> Searching finds where a target value is in a collection, or tells you that it isn't there. Some searches work on any list, while others need sorted data and, in exchange, get to skip most of it.

## What it is
A searching [algorithm](glossary:algorithm) looks for a target value and returns its position, its [index](glossary:index), or reports that the target is missing. The simplest search checks every value. Smarter searches use the order of sorted data to rule out whole parts of the list at once.

## How it works
PyDSA has five searches, each with its own strategy:
- Linear Search checks the values one by one, from the start. It works on any list.
- Binary Search checks the middle of a sorted list and throws away the half that can't hold the target.
- Jump Search jumps ahead in blocks of a fixed size, then checks inside the one block that could hold the target.
- Interpolation Search guesses where the target should be from its value, like opening a dictionary near the end for a word that starts with W.
- Exponential Search checks positions 1, 2, 4, 8 and so on to find a range, then runs Binary Search inside it.

The searches for sorted data all rely on the same idea: if the value you're looking at is smaller than the target, the target can only come after it.

## Real-life analogy
Finding a name in a phone book. You could read every name from the first page, or you could use the alphabetical order to jump close to the right page and narrow it down from there.

## When to use it
- Linear Search when the data is small, unsorted or searched only once.
- A search for sorted data when the data is sorted already, or when you'll search it so often that sorting it once pays off.

## When to avoid it
- You look things up by key all the time and don't need any order; a hash table finds keys without searching.

## In PyDSA
- Every search except Linear Search runs on a sorted copy of your list, so your list keeps its order. It reports the index where the target first appears in your original list.
- After every search, PyDSA shows the positions the algorithm checked, numbered in order, so you can see how much of the list each search skipped.
- Interpolation Search only works on numbers, because it does arithmetic on the values.
