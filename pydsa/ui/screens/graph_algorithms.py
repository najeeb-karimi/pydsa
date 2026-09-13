"""Graph algorithms screen: runs the graph algorithms on an example graph.

The graph screen runs the same algorithms on a graph you build yourself.
"""

from pydsa.content import complexity, texts
from pydsa.core.graph import ListGraph
from pydsa.ui import render
from pydsa.ui.console import info
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.screens import graph as graph_screen


def show_definition():
    render.definition(texts.GRAPH_ALGORITHMS_DEFINITION, complexity.GRAPH_ALGORITHMS)


def run():
    """Pick an example graph and run the graph algorithms menu."""
    render.intro(texts.GRAPH_ALGORITHMS_ASCII, texts.GRAPH_ALGORITHMS_DEFINITION, complexity.GRAPH_ALGORITHMS)
    info(texts.GRAPH_ALGORITHMS_INFO)
    graph = Menu("🛠️ Which example graph do you want to use?", [
        [("The directed example graph (Dijkstra, Topological Sort, Cycle Detection)", lambda: example(True)),
         ("The undirected example graph (Dijkstra, Cycle Detection, Prim, Kruskal)", lambda: example(False)),
         ("A random graph", lambda: graph_screen.fill_random(graph_screen.new_list_graph))],
        [back_option()],
    ]).open()
    if graph is Nav.BACK:
        return Nav.BACK

    return operation_menu(f"{graph_screen.describe(graph)} graph", [
        *graph_screen.algorithm_options(graph),
        ("Display", lambda: graph_screen.show(graph)),
    ], definition=show_definition, new_label="New Graph").run()


def example(directed):
    graph = ListGraph(directed)
    graph_screen.load_example(graph)
    return graph
