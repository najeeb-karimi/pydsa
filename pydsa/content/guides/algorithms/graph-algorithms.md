# Graph Algorithms
> Graph algorithms answer questions about connections: the cheapest route between two places, an order for tasks that depend on each other, whether connections loop back on themselves, and the cheapest way to connect everything. They power maps, build tools, course planners and network design.

## What it is
Graph algorithms are [algorithms](glossary:algorithm) that work on the [vertices](glossary:vertex) and [edges](glossary:edge) of a graph. PyDSA has four kinds:
- Dijkstra's algorithm finds the [shortest path](glossary:shortest-path) from one vertex to every other vertex.
- A topological sort lines up the vertices of a [directed graph](glossary:directed-graph) so every edge points forward.
- Cycle detection finds a [cycle](glossary:cycle), a path that leads back to where it started.
- Prim's algorithm and Kruskal's algorithm find a minimum [spanning tree](glossary:spanning-tree): the cheapest set of edges that connects every vertex.

## How it works
Most graph algorithms explore the graph step by step and keep track of what they've learned so far:
- Dijkstra's algorithm and Prim's algorithm are [greedy algorithms](glossary:greedy-algorithm) that use a min heap to always handle the closest vertex or the lightest edge next.
- A topological sort counts the edges pointing into every vertex, its [in-degree](glossary:in-degree), and places a vertex once nothing points to it anymore.
- Cycle detection runs a [depth-first search](glossary:depth-first-search) on a directed graph, and uses a disjoint set on an undirected graph.
- Kruskal's algorithm goes through the edges from lightest to heaviest and uses a disjoint set to skip the edges that would close a cycle.

Some algorithms only make sense for one kind of graph. A topological sort needs directed edges, minimum spanning trees need undirected edges, and Dijkstra's algorithm needs weights that aren't negative.

## Real-life analogy
A delivery company planning its week. It needs the quickest route to every address, an order for loading the trucks when some packages have to go in before others, a check that no set of instructions sends a driver around in circles, and the cheapest set of roads that reaches every town.

## When to use it
- Navigation and routing, with Dijkstra's algorithm.
- Scheduling tasks, build steps or courses with prerequisites, with a topological sort.
- Spotting circular dependencies or deadlocks, with cycle detection.
- Designing networks of cables, pipes or roads that connect everything cheaply, with Prim's or Kruskal's algorithm.

## When to avoid it
- The question isn't about connections; a simpler data structure or algorithm will do.
- The graph has negative weights and you need shortest paths. Dijkstra's algorithm can give wrong answers, and an algorithm such as Bellman-Ford is needed instead.

## In PyDSA
- This screen runs the algorithms on the directed example graph, the undirected example graph or a random graph.
- To run them on a graph you build yourself, open Graph under the non-linear data structures and choose `Graph Algorithms` in its menu.
- Only the algorithms that fit the graph's direction are offered: topological sort for directed graphs, and minimum spanning trees for undirected graphs.
