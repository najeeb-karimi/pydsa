"""Graph algorithms that work on both graph representations through vertices() and edges(v).

Every algorithm takes an optional trace list and records what it did at each step, as TraceEvents whose
snapshot is the state to draw: the distances, the counts of edges still pointing at each vertex, the path
the search is on or the edges chosen so far.
"""

from collections import deque
from math import inf
from typing import NamedTuple

from pydsa.algorithms.trace import record
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.errors import CycleError, NegativeWeightError
from pydsa.core.heap import MinHeap


def edge_list(graph):
    """Return every edge as (u, v, weight); an undirected edge is listed once, from the vertex that comes first."""
    position = {v: index for index, v in enumerate(graph.vertices())}
    return [
        (u, v, weight)
        for u in graph.vertices()
        for v, weight in graph.edges(u)
        if graph.directed or position[u] <= position[v]
    ]


def _require_undirected(graph, name):
    if graph.directed:
        raise ValueError(f"{name} needs an undirected graph.")


# ---------------------------------------------------------------------------
# Shortest paths
# ---------------------------------------------------------------------------

class ShortestPaths(NamedTuple):
    """The result of Dijkstra's algorithm from one source vertex."""

    source: int
    distances: dict  # Vertex -> length of the shortest path, or inf if it can't be reached
    previous: dict  # Vertex -> the vertex before it on its shortest path (None for the source and unreachable ones)
    order: list  # The vertices in the order their distances became final


def dijkstra(graph, source, trace=None):
    """Return the shortest paths from source to every vertex, using a min heap of (distance, vertex) pairs.

    Raises NegativeWeightError if any edge has a negative weight, since Dijkstra's algorithm can't handle one.
    """
    graph._check_vertices(source)
    for u, v, weight in edge_list(graph):
        if weight < 0:
            raise NegativeWeightError(u, v, weight)

    distances = {v: inf for v in graph.vertices()}
    previous = {v: None for v in graph.vertices()}
    distances[source] = 0
    order, heap = [], MinHeap()
    heap.insert((0, source))
    while not heap.is_empty():
        (distance, u), _ = heap.extract()
        if distance > distances[u]:
            record(trace, "stale", dict(distances), {u: "checked"}, vertex=u, distance=distance)
            continue  # An outdated entry: u was already reached by a shorter path
        order.append(u)
        record(trace, "settle", dict(distances), {u: "settled"}, vertex=u, distance=distance)
        for v, weight in graph.edges(u):
            if distance + weight < distances[v]:
                distances[v] = distance + weight
                previous[v] = u
                heap.insert((distances[v], v))
                record(trace, "relax", dict(distances), {v: "moved"},
                       vertex=v, distance=distances[v], through=u)
    return ShortestPaths(source, distances, previous, order)


def shortest_path(paths, target):
    """Return the vertices on the shortest path from the source to target, or None if target can't be reached."""
    if paths.distances[target] == inf:
        return None
    path = [target]
    while path[-1] != paths.source:
        path.append(paths.previous[path[-1]])
    return path[::-1]


# ---------------------------------------------------------------------------
# Topological sort and cycles
# ---------------------------------------------------------------------------

def topological_sort(graph, trace=None):
    """Return the vertices so every edge goes from an earlier vertex to a later one (Kahn's algorithm).

    Raises CycleError if the graph has a cycle, since then no such order exists.
    """
    if not graph.directed:
        raise ValueError("A topological sort needs a directed graph.")
    in_degree = {v: 0 for v in graph.vertices()}
    for _, v, _ in edge_list(graph):
        in_degree[v] += 1

    # Start with the vertices no edge points to, and remove each one's edges as it's placed
    queue = deque(v for v in graph.vertices() if in_degree[v] == 0)
    order = []
    if queue:
        record(trace, "no_incoming", dict(in_degree), {v: "waiting" for v in queue}, vertices=list(queue))
    while queue:
        u = queue.popleft()
        order.append(u)
        record(trace, "place", dict(in_degree), {u: "visited"}, vertex=u)
        for v, _ in graph.edges(u):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                record(trace, "ready", dict(in_degree), {v: "waiting"}, vertex=v)

    if len(order) < len(in_degree):
        remaining = [v for v in graph.vertices() if in_degree[v] > 0]
        record(trace, "cycle_left", dict(in_degree), {v: "checked" for v in remaining}, vertices=remaining)
        raise CycleError(order, remaining)
    return order


def find_cycle(graph, trace=None):
    """Return a cycle as a list of vertices that starts and ends with the same vertex, or None if there's none.

    A directed graph is searched with DFS coloring, and an undirected graph with a disjoint set.
    """
    return _directed_cycle(graph, trace) if graph.directed else _undirected_cycle(graph, trace)


def _directed_cycle(graph, trace=None):
    """DFS that marks vertices as unvisited, on the current path or finished; an edge back into the path closes a cycle."""
    on_path, finished, path = set(), set(), []

    def visit(u):
        on_path.add(u)
        path.append(u)
        record(trace, "enter", list(path), {u: "on_path"}, vertex=u)
        for v, _ in graph.edges(u):
            if v in on_path:
                record(trace, "cycle_edge", list(path), {v: "on_path", u: "checked"}, u=u, v=v)
                return path[path.index(v):] + [v]
            if v not in finished:
                cycle = visit(v)
                if cycle:
                    return cycle
        on_path.remove(u)
        path.pop()
        finished.add(u)
        record(trace, "leave", list(path), {u: "done"}, vertex=u)
        return None

    for vertex in graph.vertices():
        if vertex not in finished:
            cycle = visit(vertex)
            if cycle:
                return cycle
    return None


def _undirected_cycle(graph, trace=None):
    """Add the edges one by one; an edge between two vertices that are already connected closes a cycle."""
    vertices = graph.vertices()
    position = {v: index for index, v in enumerate(vertices)}
    union_find = DisjointSet(len(vertices))
    forest = {v: [] for v in vertices}  # The edges added so far, which never contain a cycle
    added = []
    for u, v, _ in edge_list(graph):
        if union_find.connected(position[u], position[v]):
            record(trace, "cycle_link", list(added), {u: "checked", v: "checked"}, u=u, v=v)
            return _forest_path(forest, v, u) + [v]
        union_find.union(position[u], position[v])
        forest[u].append(v)
        forest[v].append(u)
        added.append((u, v))
        record(trace, "join", list(added), {u: "visited", v: "visited"}, u=u, v=v)
    return None


def _forest_path(forest, start, goal):
    """Return the only path from start to goal in a forest, found with BFS."""
    previous, queue = {start: None}, deque([start])
    while queue:
        u = queue.popleft()
        for v in forest[u]:
            if v not in previous:
                previous[v] = u
                queue.append(v)
    path = [goal]
    while path[-1] != start:
        path.append(previous[path[-1]])
    return path[::-1]


# ---------------------------------------------------------------------------
# Minimum spanning trees
# ---------------------------------------------------------------------------

class SpanningForest(NamedTuple):
    """A minimum spanning tree, or a forest of them when the graph isn't connected."""

    edges: list  # (u, v, weight) in the order the algorithm chose them
    total: int | float
    trees: int  # 1 when the graph is connected
    skipped: list  # Edges the algorithm looked at and left out, because they would have closed a cycle


def prim(graph, trace=None):
    """Grow a tree from the first vertex, always adding the lightest edge that reaches a new vertex (using a min heap).

    When the tree can't grow any further, a new tree starts from the next vertex that isn't in one yet.
    """
    _require_undirected(graph, "Prim's algorithm")
    visited, chosen, skipped, trees = set(), [], [], 0
    for start in graph.vertices():
        if start in visited:
            continue
        trees += 1
        visited.add(start)
        record(trace, "start_tree", list(chosen), {start: "visited"}, vertex=start)
        heap = MinHeap()
        for v, weight in graph.edges(start):
            if v not in visited:
                heap.insert((weight, start, v))
        while not heap.is_empty():
            (weight, u, v), _ = heap.extract()
            if v in visited:
                skipped.append((u, v, weight))
                record(trace, "skip", list(chosen), {u: "checked", v: "checked"}, u=u, v=v, weight=weight)
                continue
            visited.add(v)
            chosen.append((u, v, weight))
            record(trace, "accept", list(chosen), {v: "visited"}, u=u, v=v, weight=weight)
            for neighbor, neighbor_weight in graph.edges(v):
                if neighbor not in visited:
                    heap.insert((neighbor_weight, v, neighbor))
    return SpanningForest(chosen, sum(weight for _, _, weight in chosen), trees, skipped)


def kruskal(graph, trace=None):
    """Go through the edges from lightest to heaviest, adding each one that doesn't close a cycle (using a disjoint set)."""
    _require_undirected(graph, "Kruskal's algorithm")
    vertices = graph.vertices()
    position = {v: index for index, v in enumerate(vertices)}
    union_find = DisjointSet(len(vertices))
    chosen, skipped = [], []
    for u, v, weight in sorted(edge_list(graph), key=lambda edge: (edge[2], position[edge[0]], position[edge[1]])):
        if union_find.union(position[u], position[v]):
            chosen.append((u, v, weight))
            record(trace, "accept", list(chosen), {u: "visited", v: "visited"}, u=u, v=v, weight=weight)
        else:
            skipped.append((u, v, weight))
            record(trace, "skip", list(chosen), {u: "checked", v: "checked"}, u=u, v=v, weight=weight)
    return SpanningForest(chosen, sum(weight for _, _, weight in chosen), len(vertices) - len(chosen), skipped)
