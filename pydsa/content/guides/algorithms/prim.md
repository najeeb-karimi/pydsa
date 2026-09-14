# Prim's Algorithm
> Prim's algorithm builds a minimum spanning tree by growing a single tree one vertex at a time, always adding the lightest edge that reaches a new vertex. The result connects every vertex with the smallest possible total weight.

## What it is
A [spanning tree](glossary:spanning-tree) of an [undirected graph](glossary:undirected-graph) is a set of edges that connects every [vertex](glossary:vertex) without forming a [cycle](glossary:cycle). A minimum spanning tree is the one whose [weights](glossary:weight) add up to the least. Prim's algorithm is a [greedy algorithm](glossary:greedy-algorithm) that finds one by starting from a single vertex and growing outward.

## How it works
1. Start with a tree that holds one vertex, and put every edge leaving it into a min heap, ordered by weight.
2. Take the lightest edge out of the heap.
3. If it leads to a vertex that's already in the tree, it would close a cycle, so leave it out.
4. Otherwise, add the edge and its new vertex to the tree, and put the new vertex's edges to vertices outside the tree into the heap.
5. Repeat from step 2 until the heap is empty.

If the graph isn't [connected](glossary:connected-graph), the heap runs out before every vertex is in the tree. Starting a new tree from a vertex that isn't in one yet, and repeating, gives a minimum spanning forest: one tree for each connected part.

## Real-life analogy
Bringing electricity from a power station to a group of villages. You always lay the next cable along the cheapest stretch that reaches a village without power yet, until every village is connected.

## When to use it
- Designing networks that connect every point as cheaply as possible, like cables, pipes or roads.
- Dense graphs with many edges, especially ones stored as an adjacency matrix.
- A quick first step for harder problems, like planning a short route that visits many cities.

## When to avoid it
- The graph is directed; minimum spanning trees are defined for undirected graphs.
- The graph is sparse and its edges already come as a list; Kruskal's algorithm is simpler there.

## In PyDSA
- Prim's algorithm is only offered for undirected graphs.
- The tree grows from the first vertex of the graph. When the graph isn't connected, a new tree starts from the next vertex that isn't in one yet.
- The result lists the chosen edges in the order they were added and their total weight, followed by the edges that were left out because they would have closed a cycle.
