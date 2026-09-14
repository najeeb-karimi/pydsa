# Graph
> A graph is a set of points, called vertices, connected by lines, called edges. It can model any kind of connection, like roads between cities or friendships between people.

## What it is
A graph is a [data structure](glossary:data-structure) made of [vertices](glossary:vertex) and [edges](glossary:edge). Each edge connects two vertices, and two vertices joined by an edge are [adjacent](glossary:adjacent). Unlike a tree, a graph has no root, and it can contain [cycles](glossary:cycle).

Graphs differ in two main ways:
- In a [directed graph](glossary:directed-graph), each edge goes one way, like a one-way street. In an [undirected graph](glossary:undirected-graph), each edge goes both ways.
- In a weighted graph, each edge has a [weight](glossary:weight), such as a distance or a cost.

## How it works
A graph is usually stored in one of two ways:
- An adjacency matrix is a grid with a row and a column for every vertex. The cell in row `u` and column `v` holds the weight of the edge from `u` to `v`, or 0 when there isn't one. Checking for an edge is instant, but the grid needs a cell for every pair of vertices.
- An adjacency list gives every vertex a list of the edges that leave it. It only stores the edges that exist, but checking for one edge means looking through a vertex's list.

To visit the vertices, you start from one vertex and follow edges:
- [Breadth-first search](glossary:breadth-first-search) visits all the neighbors first, then their neighbors, spreading outward in rings.
- [Depth-first search](glossary:depth-first-search) follows one [path](glossary:path) as far as it goes, then backs up and tries the next one.

## Real-life analogy
A subway map. The stations are vertices, the tracks between them are edges, and the travel time between two neighboring stations is the weight of their edge.

## When to use it
- Maps and navigation, to find routes between places.
- Social networks, where people are vertices and friendships are edges.
- Dependencies, like tasks that must happen before others, or courses and their prerequisites.
- Networks of computers, pipes or power lines.

## When to avoid it
- Your data is a simple sequence or a strict hierarchy; a list or a tree describes it more simply.
- You only need to look items up by key; a hash table is simpler.

## In PyDSA
- After the graph opens, you choose an adjacency matrix or an adjacency list. You can also open one directly with its topic ID.
- Both graphs are weighted, and you choose whether their edges are directed or undirected. For an unweighted graph, give every edge a weight of 1.
- `Traversals` runs BFS or DFS from a vertex you choose. `Graph Algorithms` runs shortest paths, topological sort, cycle detection and minimum spanning trees on your graph.
