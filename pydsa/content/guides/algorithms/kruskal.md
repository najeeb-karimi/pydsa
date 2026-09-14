# Kruskal's Algorithm
> Kruskal's algorithm builds a minimum spanning tree by going through the edges from lightest to heaviest and adding each one that doesn't close a cycle. A disjoint set tells it right away whether an edge would close one.

## What it is
Kruskal's algorithm is a [greedy algorithm](glossary:greedy-algorithm) that finds a minimum [spanning tree](glossary:spanning-tree) of an [undirected graph](glossary:undirected-graph): the set of edges that connects every [vertex](glossary:vertex) with the smallest total [weight](glossary:weight) and no [cycle](glossary:cycle). Instead of growing one tree like Prim's algorithm, it grows many small trees at once and lets them merge.

## How it works
1. Sort all the edges from lightest to heaviest.
2. Start a disjoint set with every vertex in a set of its own.
3. Take the next edge. If its two vertices are already in the same set, they're already connected, so this edge would close a cycle: leave it out.
4. Otherwise, add the edge to the tree and merge the sets of its two vertices.
5. Repeat from step 3 until every edge has been considered.

If the graph isn't [connected](glossary:connected-graph), Kruskal's algorithm naturally ends up with a minimum spanning forest, with one tree for each connected part.

## Real-life analogy
Building bridges between islands on a budget. You go through all the possible bridges from cheapest to most expensive and build each one, unless the two islands it would join can already reach each other over bridges you've built.

## When to use it
- Sparse graphs, or whenever the edges already come as a list.
- Clustering: stopping before the last few edges leaves groups of closely connected vertices.
- Network design, like connecting offices with the least cable.

## When to avoid it
- The graph is dense, with far more edges than vertices. Sorting all those edges makes Prim's algorithm the better choice.
- The graph is directed.

## In PyDSA
- Kruskal's algorithm is only offered for undirected graphs.
- Edges with the same weight are taken in the order of their vertices, so the same graph always gives the same result.
- The result lists the chosen edges in order and their total weight, followed by the edges that were left out because they would have closed a cycle.
