# Dijkstra's Algorithm
> Dijkstra's algorithm finds the shortest path from one vertex to every other vertex in a graph whose edge weights aren't negative. It always settles the closest vertex it hasn't finished yet, and every distance it settles is final.

## What it is
Dijkstra's algorithm, named after Edsger Dijkstra, is a [greedy algorithm](glossary:greedy-algorithm) that finds [shortest paths](glossary:shortest-path). The length of a path is the sum of its edges' [weights](glossary:weight), such as kilometers or minutes. Starting from a source [vertex](glossary:vertex), it works out the shortest distance to every vertex, along with the path that achieves it.

## How it works
1. Give the source a distance of 0 and every other vertex a distance of infinity, which means "not reached yet".
2. Put the source into a min heap, which always hands back the vertex with the smallest distance.
3. Take the closest vertex out of the heap. Its distance is now final. If the heap hands back a vertex that was already reached by a shorter path, skip it.
4. Check each of its edges: if going through this vertex gives a neighbor a smaller distance than it has so far, update the neighbor's distance, remember this vertex as the neighbor's previous vertex, and put the neighbor into the heap. That check is called [relaxation](glossary:relaxation).
5. Repeat from step 3 until the heap is empty.

To rebuild the shortest path to any vertex, follow its previous vertices back to the source. Vertices whose distance is still infinity can't be reached.

The greedy choice is safe because no weight is negative: once the closest unfinished vertex is taken, no path through the vertices still waiting could reach it for less. A negative weight breaks that promise, since a longer detour could suddenly become cheaper.

## Real-life analogy
Water flowing through a network of pipes from a single tap. It reaches the nearest junctions first and spreads outward, and the moment it first arrives at a junction shows the quickest way to get there.

## When to use it
- Route planning in maps and navigation apps.
- Finding the cheapest or quickest path through a network, like data traveling between routers.
- Any problem you can draw as moving between states, with a cost that isn't negative for each move.

## When to avoid it
- Some weights are negative; use the Bellman-Ford algorithm.
- Every edge has the same weight; a [breadth-first search](glossary:breadth-first-search) finds the shortest paths more simply.
- You only need the path to one faraway target on a huge map. Variants such as A* search, which head toward the target, are faster.

## In PyDSA
- You choose the source vertex. PyDSA refuses to run on a graph with a negative weight and tells you which edge has it.
- The result is a table of every vertex with its distance and path, marking the vertices that can't be reached.
- The note under the table lists the order in which the distances became final, which is the order the heap handed out the vertices.
- The heap is PyDSA's own min heap. A vertex reached again by a shorter path is simply added again, and its outdated entry is skipped later.
