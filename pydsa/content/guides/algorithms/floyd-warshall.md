# Floyd-Warshall
> Floyd-Warshall finds shortest distances between every pair of vertices. Its matrix improves as each vertex becomes an allowed intermediate stop, and a negative diagonal reveals a negative cycle.

## What it is
Floyd-Warshall stores all-pairs [shortest paths](glossary:shortest-path) in a distance matrix. It accepts negative edges, but shortest routes through a negative cycle have no finite minimum.

## How it works
1. Start with direct edge weights, zero for staying at a vertex, and infinity where no route is known. A negative self-loop overrides the zero diagonal.
2. Choose the next intermediate vertex k.
3. For every pair u and v, compare the current distance with the route from u through k to v. Replace it if that route is shorter.
4. Save the first hop of the improved route so a path can later be reconstructed.
5. Repeat for every k. If any diagonal is negative, report a negative cycle instead of rebuilding paths.

Without negative cycles, the matrix after k describes paths using only the intermediates considered so far. To reconstruct a route, repeatedly take the saved next hop toward its target. Infinity still means unreachable.

## Real-life analogy
Fill a travel planner with fares between every pair of towns. Allow one transfer town at a time and replace fares whenever a connection through it is cheaper.

## When to use it
- You will ask many shortest-path questions on the same small or dense graph.
- You want a table of distances between every pair, including negative edges.

## When to avoid it
- A large sparse graph makes storing and checking all pairs expensive.
- You need routes from only one source; use Bellman-Ford or Dijkstra instead.

## In PyDSA
- Run it on an example, a random graph or your own graph in either representation.
- Each intermediate vertex produces a matrix with improved cells highlighted and marked with * when colors are off. Narrow terminals show a table of pairs instead.
- Choose a source and target to rebuild a route. Negative diagonal vertices are reported before route prompts.
- Guides, code views, quizzes, predictions and an experiment counting pair checks are available.
