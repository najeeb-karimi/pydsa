# Adjacency Matrix Graph
> An adjacency matrix stores a graph as a grid with one row and one column for every vertex. The cell where a row meets a column tells you whether those two vertices are connected, and by what weight.

## What it is
An adjacency matrix is a square grid of numbers that describes every [edge](glossary:edge) of a graph. A graph with 5 [vertices](glossary:vertex), numbered 0 to 4, has a matrix with 5 rows and 5 columns. The cell in row `u` and column `v` holds the [weight](glossary:weight) of the edge from `u` to `v`, and 0 means there's no edge.

In an [undirected graph](glossary:undirected-graph), every edge is stored both ways, so the matrix is a mirror image of itself along its diagonal.

## How it works
- Adding, removing or checking an edge reads or writes a single cell, which is instant.
- Listing a vertex's neighbors reads its whole row, one cell for every vertex in the graph, even if the vertex has only one neighbor.
- Adding a vertex adds a column to every row and a new row at the bottom.
- Removing a vertex removes its row and its column, so the vertices after it move down by one number.

The grid always has a cell for every pair of vertices, whether or not their edge exists. Doubling the number of vertices makes the grid four times as big.

## Real-life analogy
The distance chart in a road atlas: a table with the same cities along the top and down the side, where each cell tells you how far apart two cities are.

## When to use it
- The graph is [dense](glossary:dense-and-sparse-graphs), with edges between most pairs of vertices.
- You check whether two particular vertices are connected much more often than you list neighbors.
- The graph is small, and a grid is the easiest thing to read and check by eye.

## When to avoid it
- The graph is sparse, with far fewer edges than pairs of vertices, like a road network. Most of the matrix would be zeros.
- Vertices come and go often, since every change resizes the whole grid.

## In PyDSA
- The vertices are numbered from 0, and removing one renumbers the vertices after it.
- A weight can be any whole number except 0, because 0 means "no edge".
- The display shows the grid with the source vertex down the side and the destination vertex along the top.
