"""Graph algorithms, checked against brute force and reference algorithms on small random graphs."""

import itertools
import random
from math import inf

import pytest

from pydsa.algorithms import graph_algorithms
from pydsa.core.errors import CycleError, NegativeWeightError
from pydsa.core.graph import ListGraph, MatrixGraph

REPRESENTATIONS = pytest.mark.parametrize("representation", [MatrixGraph, ListGraph], ids=lambda cls: cls.__name__)
POSITIVE = range(1, 10)
ANY_WEIGHT = [weight for weight in range(-5, 10) if weight]  # 0 would mean "no edge" in a matrix


def random_graph(rng, representation, directed, max_vertices=6, weights=POSITIVE):
    n = rng.randint(1, max_vertices)
    if representation is MatrixGraph:
        graph = MatrixGraph(n, directed)
    else:
        graph = ListGraph(directed)
        for vertex in rng.sample(range(20), n):  # List graphs can use any vertex numbers
            graph.add_vertex(vertex)
    vertices = graph.vertices()
    for _ in range(rng.randint(0, 2 * n)):
        graph.add_edge(rng.choice(vertices), rng.choice(vertices), rng.choice(weights))
    return graph


def bellman_ford(graph, source):
    distances = {vertex: inf for vertex in graph.vertices()}
    distances[source] = 0
    edges = [(u, v, weight) for u in graph.vertices() for v, weight in graph.edges(u)]
    for _ in range(len(distances)):
        for u, v, weight in edges:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
    return distances


def roots(graph, edges):
    """Return a find function for the components that edges join, built naively."""
    parent = {vertex: vertex for vertex in graph.vertices()}

    def find(vertex):
        while parent[vertex] != vertex:
            vertex = parent[vertex]
        return vertex

    for u, v, _ in edges:
        parent[find(u)] = find(v)
    return find


def component_count(graph):
    find = roots(graph, graph_algorithms.edge_list(graph))
    return len({find(vertex) for vertex in graph.vertices()})


def is_forest(graph, edges):
    return component_count_after(graph, edges) == len(graph.vertices()) - len(edges)


def component_count_after(graph, edges):
    find = roots(graph, edges)
    return len({find(vertex) for vertex in graph.vertices()})


@REPRESENTATIONS
@pytest.mark.parametrize("directed", [True, False], ids=["directed", "undirected"])
def test_dijkstra_matches_bellman_ford(representation, directed):
    rng = random.Random(21)
    for _ in range(300):
        graph = random_graph(rng, representation, directed)
        source = rng.choice(graph.vertices())
        paths = graph_algorithms.dijkstra(graph, source)
        assert paths.distances == bellman_ford(graph, source)
        assert sorted(paths.order) == sorted(v for v, distance in paths.distances.items() if distance < inf)
        for target in graph.vertices():
            path = graph_algorithms.shortest_path(paths, target)
            if paths.distances[target] == inf:
                assert path is None
            else:
                assert path[0] == source and path[-1] == target
                assert sum(graph.search_edge(u, v) for u, v in zip(path, path[1:])) == paths.distances[target]


def test_dijkstra_rejects_negative_weights():
    graph = ListGraph()
    for vertex in range(3):
        graph.add_vertex(vertex)
    graph.add_edge(0, 1, 2)
    graph.add_edge(1, 2, -1)
    with pytest.raises(NegativeWeightError) as problem:
        graph_algorithms.dijkstra(graph, 0)
    assert problem.value.edge == (1, 2, -1)


@REPRESENTATIONS
def test_topological_sort_and_directed_cycles(representation):
    rng = random.Random(22)
    for _ in range(300):
        graph = random_graph(rng, representation, True, max_vertices=5)
        vertices, edges = graph.vertices(), graph_algorithms.edge_list(graph)
        acyclic = any(all(order.index(u) < order.index(v) for u, v, _ in edges) for order in itertools.permutations(vertices))

        cycle = graph_algorithms.find_cycle(graph)
        assert (cycle is None) == acyclic
        if cycle:
            assert cycle[0] == cycle[-1] and len(set(cycle[:-1])) == len(cycle) - 1
            assert all(graph.search_edge(u, v) is not None for u, v in zip(cycle, cycle[1:]))

        if acyclic:
            order = graph_algorithms.topological_sort(graph)
            assert sorted(order) == sorted(vertices)
            assert all(order.index(u) < order.index(v) for u, v, _ in edges)
        else:
            with pytest.raises(CycleError) as problem:
                graph_algorithms.topological_sort(graph)
            assert sorted(problem.value.order + problem.value.remaining) == sorted(vertices)


@REPRESENTATIONS
def test_undirected_cycles(representation):
    rng = random.Random(23)
    for _ in range(300):
        graph = random_graph(rng, representation, False)
        edges = graph_algorithms.edge_list(graph)
        # A graph without cycles is a forest, which has exactly one edge fewer than vertices per component
        has_cycle = len(edges) > len(graph.vertices()) - component_count(graph)

        cycle = graph_algorithms.find_cycle(graph)
        assert (cycle is not None) == has_cycle
        if cycle:
            steps = list(zip(cycle, cycle[1:]))
            assert cycle[0] == cycle[-1] and len(set(cycle[:-1])) == len(cycle) - 1
            assert len({frozenset(step) for step in steps}) == len(steps)  # A real cycle never reuses an edge
            assert all(graph.search_edge(u, v) is not None for u, v in steps)


@REPRESENTATIONS
def test_spanning_forests_match_brute_force(representation):
    rng = random.Random(24)
    for _ in range(200):
        graph = random_graph(rng, representation, False, max_vertices=5, weights=ANY_WEIGHT)
        edges, trees = graph_algorithms.edge_list(graph), component_count(graph)
        size = len(graph.vertices()) - trees
        best = min(
            sum(weight for _, _, weight in subset)
            for subset in itertools.combinations(edges, size)
            if is_forest(graph, subset)
        )
        for algorithm in (graph_algorithms.prim, graph_algorithms.kruskal):
            forest = algorithm(graph)
            assert forest.total == best
            assert forest.trees == trees
            assert len(forest.edges) == size and is_forest(graph, forest.edges)
            assert all(graph.search_edge(u, v) == weight for u, v, weight in forest.edges)


def test_algorithms_check_the_direction():
    with pytest.raises(ValueError):
        graph_algorithms.topological_sort(ListGraph(directed=False))
    with pytest.raises(ValueError):
        graph_algorithms.prim(ListGraph())
    with pytest.raises(ValueError):
        graph_algorithms.kruskal(MatrixGraph(2))
