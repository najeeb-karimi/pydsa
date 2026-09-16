"""Graph screen: adjacency matrix and adjacency list representations, and the graph algorithms that run on them."""

from pydsa.algorithms import graph_algorithms
from pydsa.content import texts
from pydsa.core.errors import CycleError, DuplicateError, NegativeWeightError, NotFoundError, OutOfBoundsError
from pydsa.core.graph import ListGraph, MatrixGraph
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_int, error, info, not_found, plural, result, success
from pydsa.ui.menu import Menu, Nav, back_option, noted, operation_menu

# The matrix graph raises OutOfBoundsError for a missing vertex, the list graph NotFoundError
MISSING_VERTEX = (OutOfBoundsError, NotFoundError)

# Both example graphs have the vertices 0 to 4. The directed one has no cycles, so it can be sorted topologically.
EXAMPLE_VERTICES = 5
EXAMPLE_EDGES = {
    True: [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)],
    False: [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3), (2, 4, 9)],
}


def run():
    """Show the graph intro, let the user pick a representation and run its menu."""
    render.intro(texts.GRAPH_ASCII, "graph")
    return Menu("🧪 Which graph representation do you want?", [
        [("Adjacency Matrix", matrix_menu), ("Adjacency List", list_menu)],
        [back_option()],
    ]).open()


def run_matrix():
    """Show the graph intro and run the adjacency matrix menu, skipping the choice of representation."""
    render.intro(texts.GRAPH_ASCII, "graph")
    return matrix_menu()


def run_list():
    """Show the graph intro and run the adjacency list menu, skipping the choice of representation."""
    render.intro(texts.GRAPH_ASCII, "graph")
    return list_menu()


# ---------------------------------------------------------------------------
# Shared by both representations
# ---------------------------------------------------------------------------

def describe(graph):
    return "directed" if graph.directed else "undirected"


def with_article(graph):
    return "a directed" if graph.directed else "an undirected"


def show(graph):
    if isinstance(graph, MatrixGraph):
        render.adjacency_matrix(graph.adj_matrix, graph.directed)
    else:
        render.adjacency_list(graph.adj_list, graph.directed)


def ask_direction():
    """Ask whether the edges have a direction; return True for directed, False for undirected, or Nav.BACK."""
    return Menu("🧭 Should the edges have a direction?", [
        [("Directed (each edge goes one way)", lambda: True),
         ("Undirected (each edge goes both ways)", lambda: False)],
        [back_option()],
    ]).open()


def ask_vertex(question):
    return ask_int(question, "vertex")


def ask_edge(graph):
    """Ask for the two vertices of an edge."""
    if graph.directed:
        return ask_vertex("🔢 Which vertex does the edge start from?"), ask_vertex("🔢 Which vertex does the edge go to?")
    return ask_vertex("🔢 What's the first vertex of the edge?"), ask_vertex("🔢 What's the second vertex of the edge?")


def edge_name(graph, u, v):
    """Describe an edge, as in "from 0 to 1" or "between 0 and 1"."""
    return f"from {u} to {v}" if graph.directed else f"between {u} and {v}"


def ask_weight():
    """Ask for an edge weight until a whole number other than 0 is typed."""
    while True:
        weight = ask_int("⚖️ What's the weight of the edge?", "weight")
        if weight != 0:
            return weight
        error("The weight can't be 0, because 0 means \"no edge\" in an adjacency matrix. Use 1 for an unweighted edge.")


def missing_vertex(graph, *vertices):
    """Report the first of vertices that isn't in the graph, with a hint about the valid ones."""
    vertex = next(v for v in vertices if not graph.has_vertex(v))
    if isinstance(graph, MatrixGraph):
        hint = f"Valid vertices are 0 to {graph.num_vertices - 1}." if graph.num_vertices else ""
    else:
        hint = f"Existing vertices: {', '.join(str(v) for v in graph.adj_list)}." if graph.adj_list else ""
    error(f"Vertex {vertex} doesn't exist. {hint or 'The graph has no vertices yet.'}")


def load_example(graph):
    """Fill an empty graph with the example edges for its direction."""
    if isinstance(graph, ListGraph):
        for vertex in range(EXAMPLE_VERTICES):
            graph.add_vertex(vertex)
    for u, v, weight in EXAMPLE_EDGES[graph.directed]:
        graph.add_edge(u, v, weight)
    success(f"Loaded the example {describe(graph)} graph. Its vertices are numbered 0 to {EXAMPLE_VERTICES - 1}.")
    show(graph)


def graph_menu(graph):
    """Run the operation menu shared by both representations."""
    representation = "matrix" if isinstance(graph, MatrixGraph) else "list"
    return operation_menu(f"{describe(graph)} adjacency {representation} graph", f"adjacency-{representation}-graph",
                          operations(graph), guides=["graph", "graph-algorithms"], new_label="New Graph").run()


def operations(graph):
    """Return the operations of an adjacency matrix or adjacency list graph as (label, action) pairs."""
    matrix = isinstance(graph, MatrixGraph)
    return [
        ("Add Vertex", lambda: (add_matrix_vertex if matrix else add_list_vertex)(graph)),
        ("Remove Vertex", lambda: (remove_matrix_vertex if matrix else remove_list_vertex)(graph)),
        ("Add Edge", lambda: add_edge(graph)),
        ("Remove Edge", lambda: remove_edge(graph)),
        ("Search Edge", lambda: search_edge(graph)),
        ("Traversals", lambda: traversals(graph)),
        ("Graph Algorithms", lambda: pick_algorithm(graph)),
        ("Display", lambda: show(graph)),
    ]


def add_edge(graph):
    u, v = ask_edge(graph)
    weight = ask_weight()
    try:
        replaced = graph.search_edge(u, v) is not None
        graph.add_edge(u, v, weight)
    except MISSING_VERTEX:
        missing_vertex(graph, u, v)
        return
    if replaced:
        success(f"Updated the edge {edge_name(graph, u, v)} to weight {weight}.")
    else:
        success(f"Added an edge {edge_name(graph, u, v)} with weight {weight}.")
    show(graph)


def remove_edge(graph):
    u, v = ask_edge(graph)
    try:
        removed = graph.remove_edge(u, v)
    except MISSING_VERTEX:
        missing_vertex(graph, u, v)
        return
    if not removed:
        not_found(f"There's no edge {edge_name(graph, u, v)}, so nothing was removed.")
        return
    success(f"Removed the edge {edge_name(graph, u, v)}.")
    show(graph)


def search_edge(graph):
    u, v = ask_edge(graph)
    try:
        weight = graph.search_edge(u, v)
    except MISSING_VERTEX:
        missing_vertex(graph, u, v)
        return
    if weight is None:
        not_found(f"There's no edge {edge_name(graph, u, v)}.")
    else:
        success(f"Found an edge {edge_name(graph, u, v)} with weight {weight}.")


def traversals(graph):
    """Let the user pick BFS or DFS and show the order the vertices are visited in."""
    Menu("🗂️ Which traversal do you want?", [
        [("BFS (Breadth-First Search)", lambda: traverse(graph, "BFS")),
         ("DFS (Depth-First Search)", lambda: traverse(graph, "DFS"))],
        [back_option()],
    ]).select()


def traverse(graph, name):
    start = ask_vertex(f"🔢 Which vertex should the {name} start from?")
    try:
        order = graph.bfs(start) if name == "BFS" else graph.dfs(start)
    except MISSING_VERTEX:
        missing_vertex(graph, start)
        return
    result(f"{name} from vertex {start}: {' → '.join(str(vertex) for vertex in order)}")


# ---------------------------------------------------------------------------
# Graph algorithms
# ---------------------------------------------------------------------------

def algorithm_options(graph):
    """Return the (label, action) pairs of the algorithms that fit the graph's direction."""
    options = [("Dijkstra's Shortest Paths", lambda: shortest_paths(graph))]
    if graph.directed:
        options.append(("Topological Sort", lambda: topological_sort(graph)))
    options.append(("Cycle Detection", lambda: cycle_detection(graph)))
    if not graph.directed:
        options += [
            ("Minimum Spanning Tree (Prim)", lambda: spanning_tree(graph, "Prim")),
            ("Minimum Spanning Tree (Kruskal)", lambda: spanning_tree(graph, "Kruskal")),
        ]
    return options


def pick_algorithm(graph):
    """Let the user pick one of the graph algorithms that fit the graph and run it."""
    if graph.directed:
        info("Minimum spanning trees need an undirected graph, so they aren't offered for this one.")
    else:
        info("A topological sort needs a directed graph, so it isn't offered for this one.")
    Menu("🧮 Which graph algorithm do you want to run?", [noted("graph-algorithms", algorithm_options(graph)),
                                                        [back_option()]]).select()


def shortest_paths(graph):
    render.explanation("dijkstra")
    source = ask_vertex("🔢 Which vertex should the paths start from?")
    try:
        paths = graph_algorithms.dijkstra(graph, source)
    except MISSING_VERTEX:
        missing_vertex(graph, source)
        return
    except NegativeWeightError as problem:
        u, v, weight = problem.edge
        error(f"Dijkstra's algorithm can't handle negative weights, but the edge {edge_name(graph, u, v)} weighs {weight}.")
        return
    routes = {vertex: graph_algorithms.shortest_path(paths, vertex) for vertex in graph.vertices()}
    reachable = sum(route is not None for route in routes.values()) - 1
    success(f"Found the shortest paths from vertex {source} to {plural(reachable, 'other vertex', 'other vertices')}.")
    render.shortest_paths(paths, routes)


def topological_sort(graph):
    render.explanation("topological-sort")
    try:
        order = graph_algorithms.topological_sort(graph)
    except CycleError as problem:
        error("The graph has a cycle, so it has no topological order.")
        info(f"These vertices are on a cycle or come after one: {', '.join(str(v) for v in problem.remaining)}.")
        return
    if not order:
        info("The graph has no vertices yet.")
        return
    result(f"Topological order: {' → '.join(str(vertex) for vertex in order)}")


def cycle_detection(graph):
    render.explanation("cycle-detection")
    cycle = graph_algorithms.find_cycle(graph)
    if cycle is None:
        result("The graph has no cycles.")
    else:
        link = " → " if graph.directed else " — "
        result(f"Found a cycle: {link.join(str(vertex) for vertex in cycle)}")


def spanning_tree(graph, name):
    """Build a minimum spanning tree (or forest) with Prim's or Kruskal's algorithm (name)."""
    render.explanation(name.lower())
    if not graph.vertices():
        info("The graph has no vertices yet.")
        return
    forest = (graph_algorithms.prim if name == "Prim" else graph_algorithms.kruskal)(graph)
    if forest.trees == 1:
        success(f"Found a minimum spanning tree with {plural(len(forest.edges), 'edge')} and a total weight of {forest.total}.")
    else:
        success(f"Found a minimum spanning forest of {forest.trees} trees with a total weight of {forest.total}.")
        info("The graph isn't connected, so each connected part gets a tree of its own.")
    render.spanning_forest(forest)


# ---------------------------------------------------------------------------
# Adjacency Matrix
# ---------------------------------------------------------------------------

def matrix_menu():
    """Show the summary of the adjacency matrix graph, then create one and run its operation menu."""
    render.summary("adjacency-matrix-graph")
    graph = Menu("🛠️ Do you want to create an adjacency matrix graph yourself or use the preloaded example?", [
        [("Create a graph", create_matrix), ("Use the example", example_matrix),
         ("Fill with random values", lambda: fill_random(MatrixGraph))],
        [back_option()],
    ]).open()
    if graph is Nav.BACK:
        return Nav.BACK

    return graph_menu(graph)


def add_matrix_vertex(graph):
    vertex = graph.add_vertex()
    success(f"Added vertex {vertex}.")
    show(graph)


def remove_matrix_vertex(graph):
    vertex = ask_vertex("🔢 Which vertex do you want to remove?")
    last = graph.num_vertices - 1
    try:
        graph.remove_vertex(vertex)
    except OutOfBoundsError:
        missing_vertex(graph, vertex)
        return
    message = f"Removed vertex {vertex} and all of its edges."
    if vertex < last:
        message += " The vertices after it moved down by one number."
    success(message)
    show(graph)


def create_matrix():
    """Ask for the direction and the number of vertices, and return a graph with no edges."""
    directed = ask_direction()
    if directed is Nav.BACK:
        return Nav.BACK
    count = ask_int("🔢 How many vertices should the graph have?", "number of vertices", min_value=1)
    graph = MatrixGraph(count, directed)
    success(f"Created {with_article(graph)} graph with {plural(count, 'vertex', 'vertices')}, numbered 0 to {count - 1}.")
    show(graph)
    return graph


def example_matrix():
    """Ask for the direction and return the matching example graph."""
    directed = ask_direction()
    if directed is Nav.BACK:
        return Nav.BACK
    graph = MatrixGraph(EXAMPLE_VERTICES, directed)
    load_example(graph)
    return graph


# ---------------------------------------------------------------------------
# Adjacency List
# ---------------------------------------------------------------------------

def list_menu():
    """Show the summary of the adjacency list graph, then create one and run its operation menu."""
    render.summary("adjacency-list-graph")
    graph = Menu("🛠️ Do you want to create an adjacency list graph yourself or use the preloaded example?", [
        [("Create a graph", create_list), ("Use the example", example_list),
         ("Fill with random values", lambda: fill_random(new_list_graph))],
        [back_option()],
    ]).open()
    if graph is Nav.BACK:
        return Nav.BACK

    return graph_menu(graph)


def add_list_vertex(graph):
    vertex = ask_vertex("🔢 Which vertex do you want to add?")
    try:
        graph.add_vertex(vertex)
    except DuplicateError:
        error(f"Vertex {vertex} already exists.")
        return
    success(f"Added vertex {vertex}.")
    show(graph)


def remove_list_vertex(graph):
    vertex = ask_vertex("🔢 Which vertex do you want to remove?")
    try:
        graph.remove_vertex(vertex)
    except NotFoundError:
        missing_vertex(graph, vertex)
        return
    success(f"Removed vertex {vertex} and all of its edges.")
    show(graph)


def create_list():
    """Ask for the direction and return an empty adjacency list graph."""
    directed = ask_direction()
    if directed is Nav.BACK:
        return Nav.BACK
    success(f"Created an empty {'directed' if directed else 'undirected'} graph. Add some vertices with Add Vertex.")
    return ListGraph(directed)


def example_list():
    """Ask for the direction and return the matching example graph."""
    directed = ask_direction()
    if directed is Nav.BACK:
        return Nav.BACK
    graph = ListGraph(directed)
    load_example(graph)
    return graph


# ---------------------------------------------------------------------------
# Random graphs
# ---------------------------------------------------------------------------

def new_list_graph(vertex_count, directed):
    """Return an adjacency list graph with the vertices 0 to vertex_count - 1 and no edges."""
    graph = ListGraph(directed)
    for vertex in range(vertex_count):
        graph.add_vertex(vertex)
    return graph


def fill_random(make_graph):
    """Ask for the direction, vertices and edges, and return a random graph made with make_graph(count, directed)."""
    directed = ask_direction()
    if directed is Nav.BACK:
        return Nav.BACK
    count = ask_int("🔢 How many vertices should the graph have?", "number of vertices",
                    min_value=1, max_value=random_data.MAX_VERTICES)
    connected = False
    if count > 1:
        connected = Menu("🔗 Should every vertex be reachable from vertex 0?", [
            [("Yes, connect them all", lambda: True), ("No, place the edges anywhere", lambda: False)],
            [back_option()],
        ]).select()
        if connected is Nav.BACK:
            return Nav.BACK
    fewest, most = random_data.edge_limits(count, directed, connected)
    edge_count = 0
    if most:
        edge_count = ask_int(f"🎲 How many random edges do you want? Choose {fewest} to {most}.", "number of edges",
                             min_value=fewest, max_value=most)

    graph = make_graph(count, directed)
    for u, v, weight in random_data.edges(graph.vertices(), edge_count, directed, connected):
        graph.add_edge(u, v, weight)
    success(f"Created {with_article(graph)} graph with {plural(count, 'vertex', 'vertices')} "
            f"and {plural(edge_count, 'random edge')}.")
    show(graph)
    return graph
