"""Graph screen: adjacency matrix and adjacency list representations."""

from pydsa.content import texts
from pydsa.core.errors import DuplicateError, NotFoundError, OutOfBoundsError
from pydsa.core.graph import ListDirectedWeightedGraph, MatrixDirectedWeightedGraph
from pydsa.ui import render
from pydsa.ui.console import ask_int, value_prompt
from pydsa.ui.menu import Menu, operation_menu


def run():
    """Show the graph intro, let the user pick a representation and run its menu."""
    render.intro(texts.GRAPH_ASCII, texts.GRAPH_DEFINITION)
    return Menu(
        "\n🧪 Which type of graph representation do you want?",
        [[("Adjacency Matrix", matrix_menu), ("Adjacency List", list_menu)]],
        invalid="\n🚫 Invalid representation type code!",
    ).select()


# ---------------------------------------------------------------------------
# Input helpers for vertices and weights
# ---------------------------------------------------------------------------

def ask_vertex(msg="first vertex"):
    """Ask for a vertex until an int is entered; msg customizes the prompt."""
    return ask_int(value_prompt(msg, "INT"), "\n🚫 Vertices are identified by integers.")


def ask_edge():
    """Ask for the two vertices of an edge."""
    return ask_vertex(), ask_vertex("second vertex")


def ask_weight():
    """Ask for an edge weight until an int is entered."""
    return ask_int(value_prompt("weight", "INT"), "\n🚫 Weight can only be an INT.")


def traversals(run_traversal):
    """Let the user pick BFS or DFS; run_traversal(name) asks for the start vertex and prints the result."""
    Menu(
        "\n🗂️ Which traversal do you want?",
        [[("BFS (Breadth-First Search)", lambda: run_traversal("BFS")),
          ("DFS (Depth-First Search)", lambda: run_traversal("DFS"))]],
        bullet="●",
    ).select()


# ---------------------------------------------------------------------------
# Adjacency Matrix
# ---------------------------------------------------------------------------

def matrix_menu():
    """Create an adjacency matrix graph and run its operation menu."""
    print(texts.MATRIX_GRAPH_INFO)
    graph = Menu(
        "\n🛠️ Do you want to create an Adjacency Matrix graph yourself or use the preloaded example?",
        [[("Create an Adjacency Matrix Graph", create_matrix), ("Use the example", example_matrix)]],
        bullet="●",
    ).select()

    def show():
        render.indexed_rows(graph.adj_matrix)

    def invalid_range():
        return f"\nValid vertices are in the range 0 to {graph.num_vertices - 1}."

    def add_vertex():
        vertex = graph.add_vertex()
        print(f"\n✅ Vertex addition successful. Vertex {vertex} added.")
        show()

    def remove_vertex():
        vertex = ask_vertex("vertex that you want to remove")
        try:
            graph.remove_vertex(vertex)
            print(f"\n✅ Vertex removal successful. Vertex {vertex} removed.")
        except OutOfBoundsError:
            print(f"\n🚫 Vertex removal unsuccessful. Invalid vertex: {vertex}.{invalid_range()}")
        show()

    def add_edge():
        u, v = ask_edge()
        weight = ask_weight()
        try:
            graph.add_edge(u, v, weight)
            print(f"\n✅ Edge addition successful. Edge added from vertex {u} to {v} with weight {weight}.")
        except OutOfBoundsError:
            print(f"\n🚫 Edge addition unsuccessful. Invalid vertices: {u}, {v}.{invalid_range()}")
        show()

    def remove_edge():
        u, v = ask_edge()
        try:
            if graph.remove_edge(u, v):
                print(f"\n✅ Edge removal successful. Edge removed from vertex {u} to {v}.")
            else:
                print(f"\n❌ Edge removal unsuccessful. No edge found from vertex {u} to {v}.")
        except OutOfBoundsError:
            print(f"\n🚫 Edge removal unsuccessful. Invalid vertices: {u}, {v}.{invalid_range()}")
        show()

    def search_edge():
        u, v = ask_edge()
        try:
            weight = graph.search_edge(u, v)
        except OutOfBoundsError:
            print(f"\n🚫 Edge searching unsuccessful. Invalid vertices: {u}, {v}.{invalid_range()}")
            return
        if weight is not None:
            print(f"\n✅ Edge searching successful. Edge with weight {weight} found from vertex {u} to {v}.")
        else:
            print(f"\n❌ Edge searching successful. No edge found from vertex {u} to {v}.")

    def run_traversal(name):
        start = ask_vertex(f"starting vertex for the {name}")
        print("\n👉🏻 ", end="")
        try:
            order = graph.bfs(start) if name == "BFS" else graph.dfs(start)
        except OutOfBoundsError:
            print(f"\n🚫 {name} traversal unsuccessful. Invalid vertex: {start}.{invalid_range()}")
            return
        render.vertex_order(order, name)

    def display():
        print("\n👇🏻 Here's your Adjacency Matrix:")
        show()

    return operation_menu("Adjacency Matrix Graph", texts.GRAPH_DEFINITION, [
        ("Adding a Vertex", add_vertex),
        ("Removing a Vertex", remove_vertex),
        ("Adding an Edge", add_edge),
        ("Removing an Edge", remove_edge),
        ("Searching an Edge", search_edge),
        ("Traversals", lambda: traversals(run_traversal)),
        ("Displaying", display),
    ], new_label="New Graph", new_intro=False).run()


def matrix_created(graph, heading):
    """Print a new matrix graph under heading, with a reminder of how vertices are numbered."""
    print(heading)
    render.indexed_rows(graph.adj_matrix)
    print(f"\n⚠️ Keep in mind that the vertices are identified with integers in the range zero to number of vertices minus 1, which means 0 to {graph.num_vertices - 1} as of now.")


def create_matrix():
    """Ask for the number of vertices and return a graph with no edges."""
    num_vertices = ask_int(value_prompt("total number of vertices you want in the Adjacency Matrix", "INT"),
                           "\n🚫 The number of vertices must be an INT of at least 1.", min_value=1)
    graph = MatrixDirectedWeightedGraph(num_vertices)
    matrix_created(graph, f"\n👇🏻 Here's your Adjacency Matrix with {num_vertices} vertices:")
    return graph


def example_matrix():
    """Return the preloaded example matrix graph."""
    graph = MatrixDirectedWeightedGraph(4)
    # Vertices are identified by their index, so filling the matrix is the same as adding the edges one by one
    graph.adj_matrix = [[10, 0, 30, 19], [17, 22, 37, 0], [0, 672, 8, 45], [0, 0, 0, 0]]
    matrix_created(graph, "\n👇🏻 Here's an example Adjacency Matrix with 4 vertices:")
    return graph


# ---------------------------------------------------------------------------
# Adjacency List
# ---------------------------------------------------------------------------

def list_menu():
    """Create an adjacency list graph and run its operation menu."""
    print(texts.LIST_GRAPH_INFO)
    graph = Menu(
        "\n🛠️ Do you want to create an Adjacency List graph yourself or use the preloaded example?",
        [[("Create an Adjacency List Graph", create_list), ("Use the example", example_list)]],
        bullet="●",
    ).select()

    def show():
        render.adjacency_list(graph.adj_list)

    def add_vertex():
        vertex = ask_vertex("vertex that you want to add")
        try:
            graph.add_vertex(vertex)
            print(f"\n✅ Vertex addition successful. Vertex {vertex} added.")
        except DuplicateError:
            print(f"\n🚫 Vertex addition unsuccessful. Vertex {vertex} already exists.")
        show()

    def remove_vertex():
        vertex = ask_vertex("vertex that you want to remove")
        try:
            graph.remove_vertex(vertex)
            print(f"\n✅ Vertex removal successful. Vertex {vertex} removed.")
        except NotFoundError:
            print(f"\n🚫 Vertex removal unsuccessful. Vertex {vertex} does not exist.")
        show()

    def add_edge():
        u, v = ask_edge()
        weight = ask_weight()
        try:
            graph.add_edge(u, v, weight)
            print(f"\n✅ Edge addition successful. Edge added from {u} to {v} with weight {weight}.")
        except NotFoundError:
            print(f"\n🚫 Edge addition unsuccessful. One or both vertices {u}, {v} do not exist.")
        show()

    def remove_edge():
        u, v = ask_edge()
        try:
            if graph.remove_edge(u, v):
                print(f"\n✅ Edge removal successful. Edge removed from {u} to {v}.")
            else:
                print(f"\n❌ Edge removal unsuccessful. No edge found from {u} to {v}.")
        except NotFoundError:
            print(f"\n🚫 Edge removal unsuccessful. One or both vertices {u}, {v} do not exist.")
        show()

    def search_edge():
        u, v = ask_edge()
        try:
            weight = graph.search_edge(u, v)
        except NotFoundError:
            print(f"\n🚫 Edge searching unsuccessful. Vertex {u} does not exist.")
            return
        if weight is not None:
            print(f"\n✅ Edge searching successful. Edge found from {u} to {v} with weight {weight}.")
        else:
            print(f"\n❌ Edge searching successful. No edge found from {u} to {v}.")

    def run_traversal(name):
        start = ask_vertex(f"starting vertex for the {name}")
        print("\n👉🏻 ", end="")
        try:
            order = graph.bfs(start) if name == "BFS" else graph.dfs(start)
        except NotFoundError:
            print(f"\n🚫 {name} traversal unsuccessful. Vertex {start} does not exist.")
            return
        render.vertex_order(order, name)

    def display():
        print("\n👇🏻 Here's your Adjacency List:")
        show()

    return operation_menu("Adjacency List Graph", texts.GRAPH_DEFINITION, [
        ("Adding a Vertex", add_vertex),
        ("Removing a Vertex", remove_vertex),
        ("Adding an Edge", add_edge),
        ("Removing an Edge", remove_edge),
        ("Searching an Edge", search_edge),
        ("Traversals", lambda: traversals(run_traversal)),
        ("Displaying", display),
    ], new_label="New Graph", new_intro=False).run()


def create_list():
    """Return an empty adjacency list graph."""
    graph = ListDirectedWeightedGraph()
    print("\n✅ Adjacency List successfully initialized.")
    # The graph starts empty, so vertices have to be added before anything else
    print("\n⚠️ Make sure to add vertices through operation #1 before going for other operations.")
    return graph


def example_list():
    """Return the preloaded example adjacency list graph."""
    graph = ListDirectedWeightedGraph()
    print("\n✅ Adjacency List successfully initialized.")
    graph.adj_list = {0: [(0, 10), (2, 30), (3, 19)], 1: [(0, 17), (1, 22), (2, 37)], 2: [(1, 672), (2, 8), (3, 45)], 3: []}
    print("\n👇🏻 Here's an example Adjacency List Graph:")
    render.adjacency_list(graph.adj_list)
    return graph
