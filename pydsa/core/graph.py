"""Directed weighted graphs stored as an adjacency matrix and as an adjacency list."""

from collections import deque

from pydsa.core.errors import DuplicateError, NotFoundError, OutOfBoundsError


# ---------------------------------------------------------------------------
# Adjacency Matrix Directed Weighted Graph
# ---------------------------------------------------------------------------

class MatrixDirectedWeightedGraph:
    """Directed weighted graph stored as an adjacency matrix, with vertices numbered from 0."""

    def __init__(self, num_vertices):
        """Initialize the graph with a given number of vertices and no edges."""
        self.num_vertices = num_vertices
        # A weight of 0 means there is no edge
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def has_vertex(self, v):
        """Return True if v is a vertex of the graph."""
        return 0 <= v < self.num_vertices

    def _check_vertices(self, *vertices):
        """Raise OutOfBoundsError if any of the vertices isn't in the graph."""
        if not all(self.has_vertex(v) for v in vertices):
            raise OutOfBoundsError(f"Valid vertices are in the range 0 to {self.num_vertices - 1}.")

    def add_edge(self, u, v, weight):
        """Add (or overwrite) a directed edge from u to v with the given weight."""
        self._check_vertices(u, v)
        self.adj_matrix[u][v] = weight

    def remove_edge(self, u, v):
        """Remove the directed edge from u to v; return False if there was no such edge."""
        self._check_vertices(u, v)
        if self.adj_matrix[u][v] == 0:
            return False
        self.adj_matrix[u][v] = 0
        return True

    def search_edge(self, u, v):
        """Return the weight of the edge from u to v, or None if there is no such edge."""
        self._check_vertices(u, v)
        return self.adj_matrix[u][v] or None

    def add_vertex(self):
        """Add a new vertex with no edges and return its number (the next free one)."""
        self.num_vertices += 1
        # Add a new column to every existing row
        for row in self.adj_matrix:
            row.append(0)
        # Add a new row at the bottom of the matrix
        self.adj_matrix.append([0] * self.num_vertices)
        return self.num_vertices - 1

    def remove_vertex(self, v):
        """Remove a vertex and all of its edges; higher-numbered vertices shift down by one."""
        self._check_vertices(v)
        # Remove the vertex's row
        self.adj_matrix.pop(v)
        # Remove the vertex's column
        for row in self.adj_matrix:
            row.pop(v)
        self.num_vertices -= 1

    def neighbors(self, v):
        """Return the vertices v has an edge to, in increasing order."""
        return [i for i in range(self.num_vertices) if self.adj_matrix[v][i] != 0]

    def dfs(self, start_vertex):
        """Return the vertices in depth-first order starting from start_vertex."""
        self._check_vertices(start_vertex)
        order = []
        visited = [False] * self.num_vertices

        def visit(v):
            """Visit v, then recursively visit its unvisited neighbors."""
            visited[v] = True
            order.append(v)
            for i in self.neighbors(v):
                if not visited[i]:
                    visit(i)

        visit(start_vertex)
        return order

    def bfs(self, start_vertex):
        """Return the vertices in breadth-first order starting from start_vertex."""
        self._check_vertices(start_vertex)
        order = []
        visited = [False] * self.num_vertices
        queue = deque([start_vertex])
        visited[start_vertex] = True

        while queue:
            v = queue.popleft()
            order.append(v)
            # Enqueue every unvisited neighbor of v and mark it as visited
            for i in self.neighbors(v):
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
        return order


# ---------------------------------------------------------------------------
# Adjacency List Directed Weighted Graph
# ---------------------------------------------------------------------------

class ListDirectedWeightedGraph:
    """Directed weighted graph stored as an adjacency list."""

    def __init__(self):
        """Initialize an empty graph.

        adj_list maps each vertex to a list of (neighbor, weight) tuples, one per outgoing edge.
        """
        self.adj_list = {}

    def has_vertex(self, v):
        """Return True if v is a vertex of the graph."""
        return v in self.adj_list

    def _check_vertices(self, *vertices):
        """Raise NotFoundError if any of the vertices isn't in the graph."""
        missing = [v for v in vertices if v not in self.adj_list]
        if missing:
            raise NotFoundError(f"Vertex {missing[0]} does not exist.")

    def add_vertex(self, vertex):
        """Add a vertex with no edges."""
        if vertex in self.adj_list:
            raise DuplicateError(f"Vertex {vertex} already exists.")
        self.adj_list[vertex] = []

    def remove_vertex(self, vertex):
        """Remove a vertex along with every edge to and from it."""
        self._check_vertices(vertex)
        # Remove every edge that points to this vertex
        for u in self.adj_list:
            self.adj_list[u] = [edge for edge in self.adj_list[u] if edge[0] != vertex]
        # Remove the vertex itself, along with its outgoing edges
        del self.adj_list[vertex]

    def add_edge(self, u, v, weight):
        """Add a directed edge from u to v with the given weight, replacing any existing u -> v edge."""
        self._check_vertices(u, v)
        self.adj_list[u] = [edge for edge in self.adj_list[u] if edge[0] != v]
        self.adj_list[u].append((v, weight))

    def remove_edge(self, u, v):
        """Remove the directed edge from u to v; return False if there was no such edge."""
        self._check_vertices(u, v)
        if not any(edge[0] == v for edge in self.adj_list[u]):
            return False
        self.adj_list[u] = [edge for edge in self.adj_list[u] if edge[0] != v]
        return True

    def search_edge(self, u, v):
        """Return the weight of the edge from u to v, or None if there is no such edge."""
        self._check_vertices(u)
        for neighbor, weight in self.adj_list[u]:
            if neighbor == v:
                return weight
        return None

    def neighbors(self, v):
        """Return the vertices v has an edge to, in the order the edges were added."""
        return [neighbor for neighbor, _ in self.adj_list[v]]

    def dfs(self, start_vertex):
        """Return the vertices in depth-first order starting from start_vertex."""
        self._check_vertices(start_vertex)
        order = []
        visited = set()

        def visit(v):
            """Visit v, then recursively visit its unvisited neighbors."""
            visited.add(v)
            order.append(v)
            for neighbor in self.neighbors(v):
                if neighbor not in visited:
                    visit(neighbor)

        visit(start_vertex)
        return order

    def bfs(self, start_vertex):
        """Return the vertices in breadth-first order starting from start_vertex."""
        self._check_vertices(start_vertex)
        order = []
        visited = {start_vertex}
        queue = deque([start_vertex])

        while queue:
            v = queue.popleft()
            order.append(v)
            for neighbor in self.neighbors(v):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        return order
