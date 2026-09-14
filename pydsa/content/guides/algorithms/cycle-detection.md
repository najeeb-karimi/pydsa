# Cycle Detection
> Cycle detection finds a path in a graph that leads back to where it started. It uses a depth-first search on directed graphs and a disjoint set on undirected graphs.

## What it is
A [cycle](glossary:cycle) is a [path](glossary:path) that starts and ends at the same [vertex](glossary:vertex) without using any edge twice. Finding one matters because cycles break many things: tasks with a circular dependency can never all be finished, and a spanning tree must not contain any cycle. Directed and undirected graphs need different methods, since in an undirected graph, simply walking back along the edge you just came from isn't a cycle.

## How it works
### Directed graphs
A [depth-first search](glossary:depth-first-search) tracks three states for every vertex: not visited yet, on the current path, and finished.
1. When the search reaches a vertex, the vertex joins the current path.
2. The search follows each of the vertex's edges in turn. If an edge leads to a vertex that's still on the current path, the search has come back around, and the part of the path from that vertex onward is a cycle.
3. Once all of its edges have been explored, the vertex is finished and leaves the path. Edges into finished vertices are safe, because everything reachable from them was already explored.
4. The search starts again from every vertex that isn't finished yet, so no part of the graph is missed.

### Undirected graphs
A disjoint set starts with every vertex in a set of its own.
1. Go through the edges one by one.
2. If an edge's two vertices are already in the same set, there's already a path between them, so this edge closes a cycle.
3. Otherwise, merge their two sets and move on to the next edge.

## Real-life analogy
Exploring a maze of one-way corridors while unrolling a ball of string behind you. If a corridor ever brings you back to string you laid on your current route, you've found a loop.

## When to use it
- Detecting circular dependencies between tasks, software packages or spreadsheet cells.
- Finding deadlocks, where programs wait for each other in a circle.
- Checking whether an undirected network is a tree, which means it's connected and has no cycles.

## When to avoid it
- You need an order for the tasks anyway; a topological sort reports a cycle along the way.
- You need every cycle in the graph; these methods stop at the first one they find.

## In PyDSA
- The method is chosen for you, based on whether the graph is directed.
- A cycle is shown as a list of vertices that starts and ends with the same vertex. For an undirected graph, PyDSA follows the edges it added before the closing edge to show the way around the cycle.
- If the graph has no cycle, PyDSA says so.
