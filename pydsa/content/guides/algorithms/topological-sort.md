# Topological Sort
> A topological sort lines up the vertices of a directed graph so every edge points from an earlier vertex to a later one. It's how you order tasks when some tasks have to happen before others.

## What it is
A topological sort takes a [directed graph](glossary:directed-graph), where an edge from `u` to `v` means "`u` must come before `v`", and produces an order that respects every edge. A graph can have many valid orders. If the graph has a [cycle](glossary:cycle), there's no valid order at all, because every task on the cycle would have to come before itself.

## How it works
PyDSA uses Kahn's algorithm:
1. Count the edges pointing into every vertex. That count is the vertex's [in-degree](glossary:in-degree).
2. Put every vertex with an in-degree of 0 into a queue. Nothing has to come before those vertices, so they're ready.
3. Take a vertex from the queue and add it to the order.
4. Remove its outgoing edges by lowering the in-degree of each of its neighbors by 1. Any neighbor that drops to 0 is now ready, so it joins the queue.
5. Repeat from step 3 until the queue is empty.

If every vertex made it into the order, the order is valid. If some vertices are left over, their in-degree never reached 0, because they're on a cycle or come after one, and the graph has no topological order.

## Real-life analogy
Getting dressed. Socks come before shoes, and a shirt before a jacket, but it doesn't matter whether you put on your shirt or your socks first. Any order that respects every "before" rule works.

## When to use it
- Planning which courses to take when some courses are prerequisites of others.
- Build tools and package managers, which have to build or install dependencies first.
- Spreadsheets, which recalculate cells in an order where every cell's inputs are ready.
- Checking whether a set of dependencies contains a circular one.

## When to avoid it
- The graph is undirected, since "before" needs a direction.
- The dependencies contain a cycle you can't break; no valid order exists.

## In PyDSA
- Topological sort is only offered for directed graphs.
- Vertices with an in-degree of 0 are taken in the order the graph lists its vertices, so the result is one valid order among possibly many.
- When the graph has a cycle, PyDSA lists the vertices that are on a cycle or come after one.
