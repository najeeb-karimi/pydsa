"""Graph screen: adjacency matrix and adjacency list representations."""

from pydsa.content import complexity, texts
from pydsa.core.errors import DuplicateError, NotFoundError, OutOfBoundsError
from pydsa.core.graph import ListDirectedWeightedGraph, MatrixDirectedWeightedGraph
from pydsa.ui import render
from pydsa.ui.console import ask_int, error, info, not_found, plural, result, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu

# The matrix graph raises OutOfBoundsError for a missing vertex, the list graph NotFoundError
MISSING_VERTEX = (OutOfBoundsError, NotFoundError)


def show_definition():
    render.definition(texts.GRAPH_DEFINITION, complexity.GRAPH)


def run():
    """Show the graph intro, let the user pick a representation and run its menu."""
    render.intro(texts.GRAPH_ASCII, texts.GRAPH_DEFINITION, complexity.GRAPH)
    return Menu("🧪 Which graph representation do you want?", [
        [("Adjacency Matrix", matrix_menu), ("Adjacency List", list_menu)],
        [back_option()],
    ]).open()


# ---------------------------------------------------------------------------
# Shared by both representations
# ---------------------------------------------------------------------------

def ask_vertex(question):
    return ask_int(question, "vertex")


def ask_edge():
    """Ask for the source and destination vertices of an edge."""
    return ask_vertex("🔢 Which vertex does the edge start from?"), ask_vertex("🔢 Which vertex does the edge go to?")


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
    if isinstance(graph, MatrixDirectedWeightedGraph):
        hint = f"Valid vertices are 0 to {graph.num_vertices - 1}." if graph.num_vertices else ""
    else:
        hint = f"Existing vertices: {', '.join(str(v) for v in graph.adj_list)}." if graph.adj_list else ""
    error(f"Vertex {vertex} doesn't exist. {hint or 'The graph has no vertices yet.'}")


def graph_menu(name, graph, show, add_vertex, remove_vertex):
    """Run the operation menu shared by both representations."""
    return operation_menu(name, [
        ("Add Vertex", add_vertex),
        ("Remove Vertex", remove_vertex),
        ("Add Edge", lambda: add_edge(graph, show)),
        ("Remove Edge", lambda: remove_edge(graph, show)),
        ("Search Edge", lambda: search_edge(graph)),
        ("Traversals", lambda: traversals(graph)),
        ("Display", show),
    ], definition=show_definition, new_label="New Graph").run()


def add_edge(graph, show):
    u, v = ask_edge()
    weight = ask_weight()
    try:
        replaced = graph.search_edge(u, v) is not None
        graph.add_edge(u, v, weight)
    except MISSING_VERTEX:
        missing_vertex(graph, u, v)
        return
    if replaced:
        success(f"Updated the edge from {u} to {v} to weight {weight}.")
    else:
        success(f"Added an edge from {u} to {v} with weight {weight}.")
    show()


def remove_edge(graph, show):
    u, v = ask_edge()
    try:
        removed = graph.remove_edge(u, v)
    except MISSING_VERTEX:
        missing_vertex(graph, u, v)
        return
    if not removed:
        not_found(f"There's no edge from {u} to {v}, so nothing was removed.")
        return
    success(f"Removed the edge from {u} to {v}.")
    show()


def search_edge(graph):
    u, v = ask_edge()
    try:
        weight = graph.search_edge(u, v)
    except MISSING_VERTEX:
        missing_vertex(graph, u, v)
        return
    if weight is None:
        not_found(f"There's no edge from {u} to {v}.")
    else:
        success(f"Found an edge from {u} to {v} with weight {weight}.")


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
# Adjacency Matrix
# ---------------------------------------------------------------------------

def matrix_menu():
    """Create an adjacency matrix graph and run its operation menu."""
    info(texts.MATRIX_GRAPH_INFO)
    graph = Menu("🛠️ Do you want to create an adjacency matrix graph yourself or use the preloaded example?", [
        [("Create a graph", create_matrix), ("Use the example", example_matrix)],
        [back_option()],
    ]).open()
    if graph is Nav.BACK:
        return Nav.BACK

    def show():
        render.adjacency_matrix(graph.adj_matrix)

    def add_vertex():
        vertex = graph.add_vertex()
        success(f"Added vertex {vertex}.")
        show()

    def remove_vertex():
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
        show()

    return graph_menu("adjacency matrix graph", graph, show, add_vertex, remove_vertex)


def create_matrix():
    """Ask for the number of vertices and return a graph with no edges."""
    count = ask_int("🔢 How many vertices should the graph have?", "number of vertices", min_value=1)
    graph = MatrixDirectedWeightedGraph(count)
    success(f"Created a graph with {plural(count, 'vertex', 'vertices')} and no edges. The vertices are numbered 0 to {count - 1}.")
    render.adjacency_matrix(graph.adj_matrix)
    return graph


def example_matrix():
    """Return the preloaded example matrix graph."""
    graph = MatrixDirectedWeightedGraph(4)
    # Vertices are identified by their index, so filling the matrix is the same as adding the edges one by one
    graph.adj_matrix = [[10, 0, 30, 19], [17, 22, 37, 0], [0, 672, 8, 45], [0, 0, 0, 0]]
    success("Loaded the example graph. Its vertices are numbered 0 to 3.")
    render.adjacency_matrix(graph.adj_matrix)
    return graph


# ---------------------------------------------------------------------------
# Adjacency List
# ---------------------------------------------------------------------------

def list_menu():
    """Create an adjacency list graph and run its operation menu."""
    info(texts.LIST_GRAPH_INFO)
    graph = Menu("🛠️ Do you want to create an adjacency list graph yourself or use the preloaded example?", [
        [("Create a graph", create_list), ("Use the example", example_list)],
        [back_option()],
    ]).open()
    if graph is Nav.BACK:
        return Nav.BACK

    def show():
        render.adjacency_list(graph.adj_list)

    def add_vertex():
        vertex = ask_vertex("🔢 Which vertex do you want to add?")
        try:
            graph.add_vertex(vertex)
        except DuplicateError:
            error(f"Vertex {vertex} already exists.")
            return
        success(f"Added vertex {vertex}.")
        show()

    def remove_vertex():
        vertex = ask_vertex("🔢 Which vertex do you want to remove?")
        try:
            graph.remove_vertex(vertex)
        except NotFoundError:
            missing_vertex(graph, vertex)
            return
        success(f"Removed vertex {vertex} and all of its edges.")
        show()

    return graph_menu("adjacency list graph", graph, show, add_vertex, remove_vertex)


def create_list():
    """Return an empty adjacency list graph."""
    success("Created an empty graph. Start by adding some vertices with Add Vertex.")
    return ListDirectedWeightedGraph()


def example_list():
    """Return the preloaded example adjacency list graph."""
    graph = ListDirectedWeightedGraph()
    graph.adj_list = {0: [(0, 10), (2, 30), (3, 19)], 1: [(0, 17), (1, 22), (2, 37)], 2: [(1, 672), (2, 8), (3, 45)], 3: []}
    success("Loaded the example graph.")
    render.adjacency_list(graph.adj_list)
    return graph
