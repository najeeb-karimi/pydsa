# Dynamic Programming

> Solve overlapping subproblems once and reuse their answers. Compare recursion with saved results and tables.

## What it is
Dynamic programming is a way to build a larger answer from smaller problems that repeat.

## How it works
Choose a state that describes a subproblem. Define base answers, then a recurrence connecting states. Memoization saves answers during [recursion](glossary:recursion); tabulation fills them in dependency order. A separate traceback rebuilds choices when needed.

## Real-life analogy
Keep a notebook of solved homework questions instead of redoing the same question every time it appears.

## When to use it
Use it when smaller problems overlap and their optimal answers can combine into a larger optimal answer.

## When to avoid it
Avoid it when states do not repeat or the table would be too large; a direct or greedy solution may fit better.

## In PyDSA
Choose Fibonacci, 0/1 Knapsack, Longest Common Subsequence or Coin Change, then type inputs, load an example or generate random data. Watch tables, reconstruction and work counts. Each child screen includes code and practice.
