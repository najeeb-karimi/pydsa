# Adjacency List Graph
> An adjacency list stores a graph by giving every vertex its own list of the edges that leave it. It only uses memory for the edges that really exist.

## What it is
An adjacency list maps each [vertex](glossary:vertex) to a list of its [edges](glossary:edge), where each entry holds a neighbor and the edge's [weight](glossary:weight). A vertex without edges simply has an empty list. In an [undirected graph](glossary:undirected-graph), each edge appears in the lists of both of its vertices.

## How it works
- Adding a vertex adds a new, empty list.
- Adding an edge appends an entry to the source vertex's list, after removing any old edge to the same neighbor.
- Checking or removing an edge looks through the source vertex's list, so it takes as long as that vertex has edges, which is called its [degree](glossary:degree).
- Listing a vertex's neighbors just reads its list, which is exactly as long as the number of neighbors.
- Removing a vertex deletes its list, along with every entry in the other lists that points to it.

The whole graph takes one list per vertex plus one entry per edge. That's why adjacency lists suit big graphs where most vertices only have a few neighbors.

## Real-life analogy
The contacts on everyone's phone. Each person only stores the people they actually know, instead of a huge table with a cell for every person on Earth.

## When to use it
- The graph is [sparse](glossary:dense-and-sparse-graphs), with few edges per vertex, which is true of most real networks.
- Your algorithms go through each vertex's neighbors, as BFS, DFS, Dijkstra's algorithm and Prim's algorithm all do.
- Vertices are added and removed often, or aren't numbered in a neat range.

## When to avoid it
- The graph is dense, and you constantly check whether two particular vertices are connected; an adjacency matrix answers that instantly.

## In PyDSA
- You choose the number of every vertex you add, and removing a vertex doesn't renumber the others.
- A new graph starts with no vertices, so add some with `Add Vertex` before you add edges, or start from the example or from random values.
- The display lists every vertex with its edges, each shown as a neighbor and a weight. An undirected edge appears under both of its vertices.
