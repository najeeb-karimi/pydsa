# Bellman-Ford
> Bellman-Ford finds shortest routes from one vertex even when some edges have negative weights. It also detects a reachable negative cycle, where repeating a loop keeps making a route cheaper.

## What it is
Bellman-Ford is a [shortest path](glossary:shortest-path) algorithm that revisits distances rather than treating a vertex as final on its first visit. Unreachable vertices keep a distance of infinity.

## How it works
1. Give the source distance zero and all other vertices infinity.
2. Make a pass over every directed edge. If reaching its destination through its source is cheaper, replace the distance and predecessor. This is [relaxation](glossary:relaxation).
3. Repeat at most one fewer times than the number of vertices. Stop early when a pass makes no changes.
4. Check one more pass. An improvement now means a negative cycle is reachable from the source.
5. Follow predecessors far enough to enter that cycle, then walk around it and reverse the order to show its directed edges. Without a negative cycle, follow predecessors back to reconstruct routes.

Each pass uses improvements immediately, so edge order can change how quickly it finishes. An unreachable negative cycle does not affect this source. In an undirected graph, a negative edge can be taken forward and backward repeatedly and therefore forms a negative cycle.

## Real-life analogy
Compare travel offers where a rebate can make one leg cheaper than zero. Recheck every connection as new deals improve the total. A loop that pays you on every trip means there is no cheapest finite itinerary.

## When to use it
- Edges include negative costs or credits.
- You need to know whether a negative cycle is reachable from a chosen source.

## When to avoid it
- All costs are non-negative and Dijkstra can do less work.
- You need distances between every pair in a small dense graph; consider Floyd-Warshall.

## In PyDSA
- Choose an example with negative weights, a random graph, or a graph you build yourself.
- Every relaxation pass shows a table with improved distances marked. A reachable negative cycle is displayed as a closed route.
- Read the guide, inspect pseudocode and source, answer quizzes and predictions, or count edge checks in the growth experiment.
