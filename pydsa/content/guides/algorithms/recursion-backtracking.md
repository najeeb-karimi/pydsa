# Recursion & Backtracking

> Break a task into smaller calls, or try a choice and undo it to explore alternatives. Trees and boards make the branches visible.

## What it is
[Recursion](glossary:recursion) solves a task through smaller calls. Backtracking explores alternatives by making and undoing choices.

## How it works
Start with a base case that ends recursion. Make progress toward it on each call. For backtracking, reject invalid choices early, explore a valid branch, then restore the previous state before trying its sibling.

## Real-life analogy
Explore a maze with a trail of breadcrumbs, walking back to a junction whenever a branch is exhausted.

## When to use it
Use it for naturally nested tasks, exhaustive generation and constraint puzzles with useful pruning.

## When to avoid it
Avoid unrestricted deep calls or huge search spaces when an iterative or specialized solution is available.

## In PyDSA
Choose Tower of Hanoi, Permutations or N-Queens. Every problem supports typed inputs, an example, random data, code and practice. Sizes are capped; runs over 200 events offer a short summary unless you choose interactive playback.
