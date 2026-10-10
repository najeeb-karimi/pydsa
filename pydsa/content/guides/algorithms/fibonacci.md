# Fibonacci

> Compute the same sequence with plain recursion, memoization or a table. Actual call counts show the effect of reusing answers.

## What it is
Fibonacci starts with zero and one; each later value is the sum of its two predecessors.

## How it works
Plain [recursion](glossary:recursion) calls both predecessors, repeating many states. Memoization stores each result, but still counts entries that hit the cache. The table method fills entries from zero through n in one function call. The comparison separates calls from computed states.

## Real-life analogy
Ask a family member for a number, who asks two others; a shared notebook prevents repeated requests from becoming repeated calculations.

## When to use it
Use it to learn base cases, overlapping subproblems and the difference between recursion and tabulation.

## When to avoid it
Avoid plain recursion for large indexes; repeated calls grow rapidly. A two-value iterative method saves space when the full table is unnecessary.

## In PyDSA
Type n from 0 to 16, use n = 5 or generate a small random index. Run the three methods and Compare Call Counts. Recursive call trees are drawn through n = 6; larger runs keep narrated calls. The table highlights each entry.
