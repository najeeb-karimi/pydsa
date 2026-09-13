"""Adjacency matrix and adjacency list graphs, checked against simple models and reference traversals."""

import random
from collections import deque

import pytest

from pydsa.core.errors import DuplicateError, NotFoundError, OutOfBoundsError
from pydsa.core.graph import ListGraph, MatrixGraph


def reference_bfs(neighbors, start):
    order, seen, queue = [], {start}, deque([start])
    while queue:
        v = queue.popleft()
        order.append(v)
        for n in neighbors(v):
            if n not in seen:
                seen.add(n)
                queue.append(n)
    return order


def reference_dfs(neighbors, start, seen=None):
    seen = set() if seen is None else seen
    seen.add(start)
    order = [start]
    for n in neighbors(start):
        if n not in seen:
            order += reference_dfs(neighbors, n, seen)
    return order


def test_matrix_random_operations():
    rng = random.Random(9)
    for _ in range(300):
        n = rng.randint(0, 6)
        graph, model = MatrixGraph(n), [[0] * n for _ in range(n)]
        for _ in range(40):
            size = len(model)
            op = rng.choice(["add_edge", "add_edge", "remove_edge", "add_vertex", "remove_vertex", "search", "bfs", "dfs"])
            u, v = rng.randint(-1, size), rng.randint(-1, size)
            valid = 0 <= u < size and 0 <= v < size
            if op == "add_vertex":
                assert graph.add_vertex() == size
                for row in model:
                    row.append(0)
                model.append([0] * (size + 1))
            elif op == "remove_vertex":
                if 0 <= u < size:
                    graph.remove_vertex(u)
                    model.pop(u)
                    for row in model:
                        row.pop(u)
                else:
                    with pytest.raises(OutOfBoundsError):
                        graph.remove_vertex(u)
            elif op in ("bfs", "dfs"):
                if 0 <= u < size:
                    reference = reference_bfs if op == "bfs" else reference_dfs
                    assert getattr(graph, op)(u) == reference(lambda x: [i for i in range(len(model)) if model[x][i]], u)
                else:
                    with pytest.raises(OutOfBoundsError):
                        getattr(graph, op)(u)
            elif not valid:
                with pytest.raises(OutOfBoundsError):
                    {"add_edge": lambda: graph.add_edge(u, v, 1), "remove_edge": lambda: graph.remove_edge(u, v),
                     "search": lambda: graph.search_edge(u, v)}[op]()
            elif op == "add_edge":
                weight = rng.randint(1, 9)
                graph.add_edge(u, v, weight)
                model[u][v] = weight
            elif op == "remove_edge":
                assert graph.remove_edge(u, v) == bool(model[u][v])
                model[u][v] = 0
            else:
                assert graph.search_edge(u, v) == (model[u][v] or None)

            assert graph.adj_matrix == model
            assert graph.num_vertices == len(model)
            assert graph.vertices() == list(range(len(model)))


def test_list_random_operations():
    rng = random.Random(10)
    for _ in range(300):
        graph, model = ListGraph(), {}
        for _ in range(40):
            op = rng.choice(["add_vertex", "add_vertex", "add_edge", "add_edge", "remove_edge", "remove_vertex", "search", "bfs", "dfs"])
            u, v = rng.randint(0, 6), rng.randint(0, 6)
            if op == "add_vertex":
                if u in model:
                    with pytest.raises(DuplicateError):
                        graph.add_vertex(u)
                else:
                    graph.add_vertex(u)
                    model[u] = []
            elif op == "remove_vertex":
                if u in model:
                    graph.remove_vertex(u)
                    for k in model:
                        model[k] = [e for e in model[k] if e[0] != u]
                    del model[u]
                else:
                    with pytest.raises(NotFoundError):
                        graph.remove_vertex(u)
            elif op in ("add_edge", "remove_edge"):
                weight = rng.randint(1, 9)
                call = (lambda: graph.add_edge(u, v, weight)) if op == "add_edge" else (lambda: graph.remove_edge(u, v))
                if u in model and v in model:
                    had_edge = any(e[0] == v for e in model[u])
                    result = call()
                    model[u] = [e for e in model[u] if e[0] != v] + ([(v, weight)] if op == "add_edge" else [])
                    if op == "remove_edge":
                        assert result == had_edge
                else:
                    with pytest.raises(NotFoundError):
                        call()
            elif op == "search":
                if u in model:
                    assert graph.search_edge(u, v) == next((w for n, w in model[u] if n == v), None)
                else:
                    with pytest.raises(NotFoundError):
                        graph.search_edge(u, v)
            elif u in model:
                reference = reference_bfs if op == "bfs" else reference_dfs
                assert getattr(graph, op)(u) == reference(lambda x: [e[0] for e in model[x]], u)
            else:
                with pytest.raises(NotFoundError):
                    getattr(graph, op)(u)

            assert graph.adj_list == model
            assert graph.vertices() == list(model)
            assert all(graph.edges(vertex) == model[vertex] for vertex in model)


@pytest.mark.parametrize("graph_class", [MatrixGraph, ListGraph], ids=lambda cls: cls.__name__)
def test_undirected_edges_are_stored_both_ways(graph_class):
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(1, 6)
        if graph_class is MatrixGraph:
            graph = MatrixGraph(n, directed=False)
        else:
            graph = ListGraph(directed=False)
            for vertex in range(n):
                graph.add_vertex(vertex)
        model = {}  # {u, v} -> weight
        for _ in range(30):
            u, v = rng.randrange(n), rng.randrange(n)
            pair = frozenset((u, v))
            if rng.random() < 0.6:
                weight = rng.randint(1, 9)
                graph.add_edge(u, v, weight)
                model[pair] = weight
            else:
                assert graph.remove_edge(u, v) == (pair in model)
                model.pop(pair, None)
            for a in range(n):
                expected = sorted((b, model[frozenset((a, b))]) for b in range(n) if frozenset((a, b)) in model)
                assert sorted(graph.edges(a)) == expected


def test_matrix_example_traversals():
    graph = MatrixGraph(4)
    graph.adj_matrix = [[10, 0, 30, 19], [17, 22, 37, 0], [0, 672, 8, 45], [0, 0, 0, 0]]
    assert graph.bfs(0) == [0, 2, 3, 1]
    assert graph.dfs(0) == [0, 2, 1, 3]
