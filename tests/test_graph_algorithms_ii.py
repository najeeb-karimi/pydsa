"""Shortest paths checked against Dijkstra, exhaustive small cycles and independent grid BFS."""

import itertools
import random
from collections import deque
from math import inf

import pytest

from pydsa.algorithms import graph_algorithms as algorithms
from pydsa.algorithms.grid_search import Grid, a_star, manhattan
from pydsa.core.errors import NegativeCycleError, NegativeWeightError, NotFoundError
from pydsa.core.graph import ListGraph, MatrixGraph


def make_graph(n, edges, representation=ListGraph, directed=True):
    graph = MatrixGraph(n, directed) if representation is MatrixGraph else ListGraph(directed)
    if representation is ListGraph:
        for vertex in range(n):
            graph.add_vertex(vertex)
    for edge in edges:
        graph.add_edge(*edge)
    return graph


def random_graph(rng, representation, directed, negative=False):
    n = rng.randint(1, 5)
    weights = [-4, -2, -1, 1, 2, 3, 5] if negative else [1, 2, 3, 5]
    edges = [(u, v, rng.choice(weights)) for u in range(n) for v in range(n)
             if (directed or u <= v) and rng.random() < .25]
    return make_graph(n, edges, representation, directed)


def reachable(graph, source):
    reached, waiting = {source}, [source]
    while waiting:
        for v, _ in graph.edges(waiting.pop()):
            if v not in reached:
                reached.add(v)
                waiting.append(v)
    return reached


def negative_cycles(graph):
    """Enumerate simple directed cycles, including self-loops and two-way undirected edges."""
    vertices = graph.vertices()
    weights = {(u, v): weight for u in vertices for v, weight in graph.edges(u)}
    cycles = []
    for length in range(1, len(vertices) + 1):
        for middle in itertools.permutations(vertices, length):
            cycle = (*middle, middle[0])
            pairs = list(zip(cycle, cycle[1:]))
            if all(pair in weights for pair in pairs) and sum(weights[pair] for pair in pairs) < 0:
                cycles.append(cycle)
    return cycles


def path_cost(graph, path):
    return sum(dict(graph.edges(u))[v] for u, v in zip(path, path[1:]))


@pytest.mark.parametrize("representation", [ListGraph, MatrixGraph])
@pytest.mark.parametrize("directed", [True, False])
def test_bellman_ford_matches_dijkstra(representation, directed):
    rng = random.Random(11)
    for _ in range(100):
        graph = random_graph(rng, representation, directed)
        for source in graph.vertices():
            paths = algorithms.bellman_ford(graph, source)
            assert paths.distances == algorithms.dijkstra(graph, source).distances
            for target in graph.vertices():
                route = algorithms.shortest_path(paths, target)
                if route is None:
                    assert paths.distances[target] == inf
                else:
                    assert route[0] == source and route[-1] == target
                    assert path_cost(graph, route) == paths.distances[target]


@pytest.mark.parametrize("representation", [ListGraph, MatrixGraph])
@pytest.mark.parametrize("directed", [True, False])
def test_negative_cycles_match_exhaustive_search(representation, directed):
    rng = random.Random(73)
    for _ in range(120):
        graph = random_graph(rng, representation, directed, negative=True)
        cycles = negative_cycles(graph)
        for source in graph.vertices():
            has_cycle = any(cycle[0] in reachable(graph, source) for cycle in cycles)
            if has_cycle:
                with pytest.raises(NegativeCycleError) as caught:
                    algorithms.bellman_ford(graph, source)
                cycle = caught.value.cycle
                assert cycle[0] == cycle[-1]
                assert len(set(cycle[:-1])) == len(cycle) - 1
                assert path_cost(graph, cycle) < 0
                assert cycle[0] in reachable(graph, source)
            else:
                paths = algorithms.bellman_ford(graph, source)
                assert paths.distances[source] == 0
        if cycles:
            with pytest.raises(NegativeCycleError) as caught:
                algorithms.floyd_warshall(graph)
            problem = caught.value
            assert problem.negative_vertices
            assert all(problem.distances[v][v] < 0 for v in problem.negative_vertices)
        else:
            all_pairs = algorithms.floyd_warshall(graph)
            for source in graph.vertices():
                expected = algorithms.bellman_ford(graph, source)
                assert all_pairs.distances[source] == expected.distances
                for target in graph.vertices():
                    route = algorithms.all_pairs_path(all_pairs, source, target)
                    if route is None:
                        assert expected.distances[target] == inf
                    else:
                        assert route[0] == source and route[-1] == target
                        assert path_cost(graph, route) == expected.distances[target]


def test_adapter_only_zero_weights_and_noncontiguous_vertices():
    class Adapter:
        def vertices(self):
            return [40, 10, 90, 70]

        def edges(self, vertex):
            return {40: [(10, 0), (90, 5)], 10: [(90, -3)], 90: [], 70: []}[vertex]

    graph = Adapter()
    single = algorithms.bellman_ford(graph, 40)
    pairs = algorithms.floyd_warshall(graph)
    assert single.distances == {40: 0, 10: 0, 90: -3, 70: inf}
    assert algorithms.shortest_path(single, 90) == [40, 10, 90]
    assert algorithms.all_pairs_path(pairs, 40, 90) == [40, 10, 90]
    assert algorithms.all_pairs_path(pairs, 40, 70) is None
    assert algorithms.all_pairs_path(pairs, 40, 40) == [40]
    with pytest.raises(NotFoundError):
        algorithms.bellman_ford(graph, 0)
    assert algorithms.floyd_warshall(make_graph(0, [])).distances == {}


def test_disconnected_cycles_and_negative_self_loops():
    graph = make_graph(4, [(0, 1, -1), (2, 3, -4), (3, 2, 1)])
    with pytest.raises(NegativeWeightError, match="Try Bellman-Ford"):
        algorithms.dijkstra(graph, 0)
    assert algorithms.bellman_ford(graph, 0).distances == {0: 0, 1: -1, 2: inf, 3: inf}
    with pytest.raises(NegativeCycleError):
        algorithms.floyd_warshall(graph)
    graph = make_graph(1, [(0, 0, -1)])
    with pytest.raises(NegativeCycleError) as caught:
        algorithms.bellman_ford(graph, 0)
    assert caught.value.cycle == [0, 0]


def test_pass_snapshots_and_highlights_match_restricted_paths():
    graph = make_graph(4, [(0, 1, 3), (1, 2, -2), (2, 3, 1), (0, 3, 8)])
    events = []
    result = algorithms.floyd_warshall(graph, events)
    prior = {u: {v: 0 if u == v else dict(graph.edges(u)).get(v, inf) for v in graph.vertices()}
             for u in graph.vertices()}
    weights = {(u, v): weight for u in graph.vertices() for v, weight in graph.edges(u)}
    for k, event in enumerate(events):
        assert event.data["vertex"] == k
        for u in graph.vertices():
            for v in graph.vertices():
                candidates = [0] if u == v else []
                allowed = [x for x in range(k + 1) if x not in (u, v)]
                for length in range(len(allowed) + 1):
                    for middle in itertools.permutations(allowed, length):
                        pairs = list(zip((u, *middle, v), (u, *middle, v)[1:]))
                        if all(pair in weights for pair in pairs):
                            candidates.append(sum(weights[pair] for pair in pairs))
                assert event.snapshot[u][v] == min(candidates, default=inf)
                assert ((u, v) in event.marks) == (event.snapshot[u][v] < prior[u][v])
        prior = event.snapshot
    result.distances[0][3] = 1000
    assert events[-1].snapshot[0][3] == 2
    trace = []
    single = algorithms.bellman_ford(graph, 0, trace)
    assert [e.kind for e in trace] == ["bellman_pass", "bellman_pass"]
    assert trace[-1].data["improvements"] == 0
    single.distances[3] = 1000
    assert trace[0].snapshot[3] == 2


def bfs(board, start, goal):
    waiting, seen = deque([(start, 0)]), {start}
    while waiting:
        (row, column), distance = waiting.popleft()
        if (row, column) == goal:
            return distance
        for cell in ((row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)):
            if (0 <= cell[0] < board.rows and 0 <= cell[1] < board.columns
                    and cell not in board.walls and cell not in seen):
                seen.add(cell)
                waiting.append((cell, distance + 1))
    return None


@pytest.mark.parametrize("heuristic", [manhattan, None], ids=["A-star", "Dijkstra"])
def test_grid_paths_match_bfs(heuristic):
    rng = random.Random(501)
    for _ in range(400):
        rows, columns = rng.randint(1, 10), rng.randint(1, 10)
        cells = [(r, c) for r in range(rows) for c in range(columns)]
        start, goal = rng.choice(cells), rng.choice(cells)
        walls = {cell for cell in cells if cell not in (start, goal) and rng.random() < .35}
        board, trace = Grid(rows, columns, walls), []
        paths = a_star(board, start, goal, trace, heuristic=heuristic)
        reference = bfs(board, start, goal)
        assert (None if paths.path is None else len(paths.path) - 1) == reference
        assert len(paths.expanded) == len(set(paths.expanded))
        assert a_star(board, start, goal, heuristic=heuristic) == paths
        if paths.path is not None:
            assert paths.path[0] == start and paths.path[-1] == goal
            assert all(cell not in walls for cell in paths.path)
            assert all(manhattan(u, v) == 1 for u, v in zip(paths.path, paths.path[1:]))
        for event in trace:
            opened, closed, path = event.snapshot
            assert not opened & closed and not (opened | closed) & walls
            assert all(manhattan(u, v) == 1 for u, v in zip(path, path[1:]))
            if path:
                assert path[0] == start and path[-1] in closed


def test_manhattan_saves_expansions_on_an_open_grid():
    board = Grid(10, 10)
    informed = a_star(board, (0, 0), (9, 9))
    uninformed = a_star(board, (0, 0), (9, 9), heuristic=None)
    assert len(informed.path) == len(uninformed.path) == 19
    assert len(informed.expanded) == 19 and len(uninformed.expanded) == 100
    assert a_star(board, (0, 0), (0, 0)).path == [(0, 0)]


@pytest.mark.parametrize("rows, columns, walls", [(0, 1, ()), (1, -1, ()), (True, 2, ()),
                                                 (2.0, 2, ()), (2, 2, {(2, 0)}), (2, 2, {(False, 0)})])
def test_invalid_grids(rows, columns, walls):
    with pytest.raises(ValueError):
        Grid(rows, columns, walls)


@pytest.mark.parametrize("start, goal", [((-1, 0), (0, 0)), ((0, 0), (2, 0)), ((0, 1), (0, 0)),
                                       ((0, 0), (0, 1)), ((False, 0), (0, 0)), ([0, 0], (1, 1))])
def test_invalid_endpoints(start, goal):
    with pytest.raises(ValueError):
        a_star(Grid(2, 2, {(0, 1)}), start, goal)
