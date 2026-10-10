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
from pydsa.core.errors import CycleError, NegativeCycleError, NegativeWeightError, NotFoundError
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
    """Shortest paths from one source; order is used only by Dijkstra."""

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
            if trace is not None:
                record(trace, "stale", dict(distances), {u: "checked"}, vertex=u, distance=distance)
            continue  # An outdated entry: u was already reached by a shorter path
        order.append(u)
        if trace is not None:
            record(trace, "settle", dict(distances), {u: "settled"}, vertex=u, distance=distance)
        for v, weight in graph.edges(u):
            if distance + weight < distances[v]:
                distances[v] = distance + weight
                previous[v] = u
                heap.insert((distances[v], v))
                if trace is not None:
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


def bellman_ford(graph, source, trace=None):
    """Relax every directed arc for at most V-1 passes, then check for a reachable negative cycle.

    Only vertices() and edges(v) are required. Undirected edges must expose both directions.
    NegativeCycleError carries a closed cycle in edge order; unreachable cycles are ignored.
    """
    vertices = list(graph.vertices())
    if source not in vertices:
        raise NotFoundError(source)
    edges = [(u, v, weight) for u in vertices for v, weight in graph.edges(u)]
    distances = dict.fromkeys(vertices, inf)
    previous = dict.fromkeys(vertices)
    distances[source] = 0
    for number in range(1, len(vertices)):
        changed = {}
        for u, v, weight in edges:
            if distances[u] != inf and distances[u] + weight < distances[v]:
                distances[v], previous[v] = distances[u] + weight, u
                changed[v] = "moved"
        if trace is not None:
            record(trace, "bellman_pass", dict(distances), changed,
                   number=number, improvements=len(changed), checks=len(edges))
        if not changed:
            break
    # A full extra pass both detects the cycle and gives a predecessor inside it.
    last = None
    for u, v, weight in edges:
        if distances[u] != inf and distances[u] + weight < distances[v]:
            distances[v], previous[v], last = distances[u] + weight, u, v
    if last is not None:
        for _ in vertices:
            last = previous[last]
        cycle, cursor = [last], previous[last]
        while cursor != last:
            cycle.append(cursor)
            cursor = previous[cursor]
        cycle.append(last)
        cycle.reverse()
        if trace is not None:
            record(trace, "bellman_cycle", dict(distances), {v: "moved" for v in cycle}, cycle=cycle)
        raise NegativeCycleError(cycle, distances=distances)
    return ShortestPaths(source, distances, previous, [])


class AllPairsPaths(NamedTuple):
    """All-pairs distances and the next vertex to take on each finite route."""

    distances: dict
    next_hop: dict


def floyd_warshall(graph, trace=None):
    """Consider each vertex as an intermediate stop; reject negative diagonals after the last pass."""
    vertices = list(graph.vertices())
    distances = {u: {v: 0 if u == v else inf for v in vertices} for u in vertices}
    next_hop = {u: dict.fromkeys(vertices) for u in vertices}
    for u in vertices:
        next_hop[u][u] = u
        for v, weight in graph.edges(u):
            if weight < distances[u][v]:
                distances[u][v], next_hop[u][v] = weight, v
    for k in vertices:
        changed = {}
        for u in vertices:
            for v in vertices:
                candidate = distances[u][k] + distances[k][v]
                if candidate < distances[u][v]:
                    distances[u][v], next_hop[u][v] = candidate, next_hop[u][k]
                    changed[u, v] = "moved"
        if trace is not None:
            record(trace, "floyd_pass", {u: dict(row) for u, row in distances.items()}, changed,
                   vertex=k, improvements=len(changed), checks=len(vertices) ** 2)
    negative = [v for v in vertices if distances[v][v] < 0]
    if negative:
        if trace is not None:
            record(trace, "floyd_cycle", {u: dict(row) for u, row in distances.items()},
                   {(v, v): "moved" for v in negative}, vertices=negative)
        raise NegativeCycleError(distances=distances, negative_vertices=negative)
    return AllPairsPaths(distances, next_hop)


def all_pairs_path(paths, source, target):
    """Reconstruct one route, or return None when the target is unreachable."""
    if paths.distances[source][target] == inf:
        return None
    route = [source]
    while route[-1] != target:
        route.append(paths.next_hop[route[-1]][target])
    return route


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
        if trace is not None:
            record(trace, "no_incoming", dict(in_degree), {v: "waiting" for v in queue}, vertices=list(queue))
    while queue:
        u = queue.popleft()
        order.append(u)
        if trace is not None:
            record(trace, "place", dict(in_degree), {u: "visited"}, vertex=u)
        for v, _ in graph.edges(u):
            in_degree[v] -= 1
            if trace is not None:
                record(trace, "edge_removed", dict(in_degree), {v: "moved"}, u=u, v=v, degree=in_degree[v])
            if in_degree[v] == 0:
                queue.append(v)
                if trace is not None:
                    record(trace, "ready", dict(in_degree), {v: "waiting"}, vertex=v)

    if len(order) < len(in_degree):
        remaining = [v for v in graph.vertices() if in_degree[v] > 0]
        if trace is not None:
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
        if trace is not None:
            record(trace, "enter", list(path), {u: "on_path"}, vertex=u)
        for v, _ in graph.edges(u):
            if v in on_path:
                if trace is not None:
                    record(trace, "cycle_edge", list(path), {v: "on_path", u: "checked"}, u=u, v=v)
                return path[path.index(v):] + [v]
            if v not in finished:
                cycle = visit(v)
                if cycle:
                    return cycle
        on_path.remove(u)
        path.pop()
        finished.add(u)
        if trace is not None:
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
            if trace is not None:
                record(trace, "cycle_link", list(added), {u: "checked", v: "checked"}, u=u, v=v)
            return _forest_path(forest, v, u) + [v]
        union_find.union(position[u], position[v])
        forest[u].append(v)
        forest[v].append(u)
        added.append((u, v))
        if trace is not None:
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
        if trace is not None:
            record(trace, "start_tree", list(chosen), {start: "visited"}, vertex=start)
        heap = MinHeap()
        for v, weight in graph.edges(start):
            if v not in visited:
                heap.insert((weight, start, v))
        while not heap.is_empty():
            (weight, u, v), _ = heap.extract()
            if v in visited:
                skipped.append((u, v, weight))
                if trace is not None:
                    record(trace, "skip", list(chosen), {u: "checked", v: "checked"}, u=u, v=v, weight=weight)
                continue
            visited.add(v)
            chosen.append((u, v, weight))
            if trace is not None:
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
            if trace is not None:
                record(trace, "accept", list(chosen), {u: "visited", v: "visited"}, u=u, v=v, weight=weight)
        else:
            skipped.append((u, v, weight))
            if trace is not None:
                record(trace, "skip", list(chosen), {u: "checked", v: "checked"}, u=u, v=v, weight=weight)
    return SpanningForest(chosen, sum(weight for _, _, weight in chosen), len(vertices) - len(chosen), skipped)
