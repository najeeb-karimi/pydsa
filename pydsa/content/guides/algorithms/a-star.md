# A* on a Grid
> A* finds a shortest route through a grid of open cells and walls. Manhattan distance estimates how far the goal is and helps the search choose which cell to explore next.

## What it is
A* is a [shortest path](glossary:shortest-path) search that combines distance traveled with an estimate of distance remaining. This grid has four possible directions, each costing one move; diagonal moves are not allowed.

## How it works
1. Put the start in the open frontier with distance zero.
2. Give each open cell priority equal to its traveled distance plus Manhattan distance: the row difference plus the column difference to the goal.
3. Take the cell with the lowest priority and put it in the closed set. Ties prefer a smaller remaining estimate, then earlier arrival.
4. Improve its open neighbors when a shorter route reaches them. Remember their previous cell.
5. Stop when the goal is taken from the frontier and rebuild the path. If the frontier empties first, the goal is unreachable.

Manhattan distance never overestimates the remaining cost here: walls may force extra moves, but cannot reduce the row and column moves needed. It is also consistent across neighboring cells, so closed cells need not reopen. Setting the estimate to zero runs Dijkstra on exactly the same grid.

## Real-life analogy
Walk through a city of square blocks, using a map to favor streets that lead toward your destination. Barriers can force a detour, so you still keep alternative routes waiting.

## When to use it
- A game or maze needs a shortest route to one goal.
- You have a safe distance estimate that guides a search past irrelevant cells.

## When to avoid it
- Diagonal moves or different costs make this grid's Manhattan estimate unsuitable.
- You need distances to every cell rather than one goal.

## In PyDSA
- Open A* from Graph Algorithms or a graph's algorithms menu, or use `--topic a-star`.
- Use the example or choose up to ten rows and columns. Type . and # row by row, or place random walls, then choose open start and goal cells using zero-based coordinates.
- Each step draws open cells (o), closed cells (x), walls (#) and the current path (*). S and G mark endpoints; B marks a cell that is both.
- Compare path lengths and expanded-cell counts with Dijkstra. Savings depend on walls and tie choices; they are not guaranteed to be positive.
- Code views, quizzes, predictions and growth experiments complete the topic.
