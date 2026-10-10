# N-Queens

> Place one queen per row with no shared column or diagonal. Watch valid choices and backtracks, and count every solution.

## What it is
N-Queens asks for all nonattacking placements of n chess queens on an n by n board.

## How it works
Search one row at a time. Sets remember occupied columns and both diagonal directions. Reject an attacked square; otherwise place a queen and recurse. After the branch, remove the queen and its marks before trying another column. A full board is a solution; rotated and reflected solutions are counted separately.

## Real-life analogy
Schedule appointments while keeping several shared resources free, canceling a tentative booking when later bookings cannot fit.

## When to use it
Use it to learn constraint pruning and why restoring state is essential during backtracking.

## When to avoid it
Avoid exhaustive enumeration for large boards; specialized solvers and symmetry handling can reduce the search.

## In PyDSA
Type a board size from 0 to 8, load n = 4 or generate a small random size. Solve records every placement and removal, plus rejected squares. Watch each board interactively or use the bounded summary, then see the count and first solution. Sizes 2 and 3 have no solutions; size 0 has one empty solution.
