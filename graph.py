"""Graph implementation: directed weighted graph using an adjacency matrix."""

import utility

# TODO: removing an edge doesn't report when there is no edge between the two vertices


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

    def add_edge(self, u, v, weight):
        """Add (or overwrite) a directed edge from u to v with the given weight."""
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.adj_matrix[u][v] = weight
            print(f"\n✅ Edge addition successful. Edge added from vertex {u} to {v} with weight {weight}.")
        else:
            print(f"\n🚫 Edge addition unsuccessful. Invalid vertices: {u}, {v}.\nValid vertices are in the range 0 to {self.num_vertices - 1}.")

    def remove_edge(self, u, v):
        """Remove the directed edge from u to v by setting its weight to 0."""
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.adj_matrix[u][v] = 0
            print(f"\n✅ Edge removal successful. Edge removed from vertex {u} to {v}.")
        else:
            print(f"\n🚫 Edge removal unsuccessful. Invalid vertices: {u}, {v}.\nValid vertices are in the range 0 to {self.num_vertices - 1}.")

    def add_vertex(self):
        """Add a new vertex with no edges; it gets the next free number."""
        self.num_vertices += 1
        # Add a new column to every existing row
        for row in self.adj_matrix:
            row.append(0)
        # Add a new row at the bottom of the matrix
        self.adj_matrix.append([0] * self.num_vertices)
        print(f"\n✅ Vertex addition successful. Vertex {self.num_vertices - 1} added.")

    def remove_vertex(self, v):
        """Remove a vertex and all of its edges; higher-numbered vertices shift down by one."""
        if 0 <= v < self.num_vertices:
            # Remove the vertex's row
            self.adj_matrix.pop(v)
            # Remove the vertex's column
            for row in self.adj_matrix:
                row.pop(v)
            self.num_vertices -= 1
            print(f"\n✅ Vertex removal successful. Vertex {v} removed.")
        else:
            print(f"\n🚫 Vertex removal unsuccessful. Invalid vertex: {v}.\nValid vertices are in the range 0 to {self.num_vertices - 1}.")

    def dfs_util(self, v, visited):
        """Visit v, print it, then recursively visit its unvisited neighbors."""
        visited[v] = True
        print(v, end=' ')

        for i in range(self.num_vertices):
            if self.adj_matrix[v][i] != 0 and not visited[i]:
                self.dfs_util(i, visited)

    def dfs(self, start_vertex):
        """Print a depth-first traversal starting from start_vertex."""
        if 0 <= start_vertex < self.num_vertices:
            visited = [False] * self.num_vertices
            self.dfs_util(start_vertex, visited)
            print("\nℹ️ DFS Traversal")  # Ends the traversal line and labels it
        else:
            print(f"\n🚫 DFS traversal unsuccessful. Invalid vertex: {start_vertex}.\nValid vertices are in the range 0 to {self.num_vertices - 1}.")

    def bfs(self, start_vertex):
        """Print a breadth-first traversal starting from start_vertex."""
        if 0 <= start_vertex < self.num_vertices:
            visited = [False] * self.num_vertices
            # A plain list is used as the queue
            queue = []
            queue.append(start_vertex)
            visited[start_vertex] = True

            while queue:
                v = queue.pop(0)
                print(v, end=' ')

                # Enqueue every unvisited neighbor of v and mark it as visited
                for i in range(self.num_vertices):
                    if self.adj_matrix[v][i] != 0 and not visited[i]:
                        queue.append(i)
                        visited[i] = True
            print("\nℹ️ BFS Traversal")  # Ends the traversal line and labels it
        else:
            print(f"\n🚫 DFS traversal unsuccessful. Invalid vertex: {start_vertex}.\nValid vertices are in the range 0 to {self.num_vertices - 1}.")

    def search_edge(self, u, v):
        """Print whether there is an edge from u to v, and its weight if there is."""
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            result = self.adj_matrix[u][v] != 0
            if result is True:
                weight = self.adj_matrix[u][v]
                print(f"\n✅ Edge searching successful. Edge with weight {weight} found from vertex {u} to {v}.")
            else:
                print(f"\n❌ Edge searching successful. No edge found from vertex {u} to {v}.")
        else:
            print(f"\n🚫 Edge searching unsuccesful. Invalid vertices: {u}, {v}.\nValid vertices are in the range 0 to {self.num_vertices - 1}.")

    def display(self):
        """Print the adjacency matrix, one row per vertex."""
        for row in self.adj_matrix:
            print("🔹", self.adj_matrix.index(row), row)


def adj_matrix_main():
    """Create an adjacency matrix graph and run its operation menu."""
    print("\nℹ️ This program implements a Directed Weighted Graph through the Adjacency Matrix representation. If an unweighted graph is desired, the weights can be simply set to 1.")

    # Vertex count validation loop
    while True:
        num_vertices = utility.input_verify("int", "total number of vertices you want in the Adjacency Matrix")
        if num_vertices != None:
            adj_matrix = MatrixDirectedWeightedGraph(num_vertices)
            print(f"\n👇🏻 Here's your Adjacency Matrix with {num_vertices} vertices:")
            adj_matrix.display()
            print(f"\n⚠️ Keep in mind that the vertices are identified with integers in the range zero to number of vertices minus 1, which means 0 to {num_vertices - 1} as of now.")
            break
        else:
            print("\n🚫 The number of vertices can only be an INT.")
            continue

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the Adjacency Matrix Graph?
★0) Definition
★1) Adding a Vertex
★2) Removing a Vertex
★3) Adding an Edge
★4) Removing an Edge
★5) Searching an Edge
★6) Traversals
★7) Displaying
★8) New Graph
★9) New Data Structure
★10) Exiting the Program

>>> """)
        match opr:

            # Definition
            case "0":
                graph_intro("def")

            # Adding a vertex
            case "1":
                adj_matrix.add_vertex()
                adj_matrix.display()

            # Removing a vertex
            case "2":
                u = get_u(msg="vertex that you want to remove")
                adj_matrix.remove_vertex(u)
                adj_matrix.display()

            # Adding an edge
            case "3":
                # Collect the three inputs an edge needs: source, destination and weight
                u = get_u()
                v = get_v()
                weight = get_weight()
                adj_matrix.add_edge(u, v, weight)
                adj_matrix.display()

            # Removing an edge
            case "4":
                # Only the two vertices are needed here
                u = get_u()
                v = get_v()
                adj_matrix.remove_edge(u, v)
                adj_matrix.display()

            # Searching an edge
            case "5":
                u = get_u()
                v = get_v()
                adj_matrix.search_edge(u, v)

            # Traversals
            case "6":

                # Traversal type selection loop
                while True:
                    traversal_type = input("""\n🗂️ Which traversal do you want?
●1) BFS (Breadth-First Search)
●2) DFS (Depth-First Search)
>>> """)
                    match traversal_type:
                        # BFS
                        case "1":
                            start_vertex = get_u(msg="starting vertex for the BFS")
                            print("\n👉🏻 ", end="")
                            adj_matrix.bfs(start_vertex)
                            break

                        # DFS
                        case "2":
                            start_vertex = get_u(msg="starting vertex for the DFS")
                            print("\n👉🏻 ", end="")
                            adj_matrix.dfs(start_vertex)
                            break

                        # Invalid
                        case _:
                            print("\n❌ Invalid code number!")
                            continue

            # Displaying
            case "7":
                print("\n👇🏻 Here's your Adjacency Matrix:")
                adj_matrix.display()

            # New graph
            case "8":
                utility.clear()
                graph_intro("full")
                graph_main()
                break

            # New data structure
            case "9":
                utility.clear()
                utility.main_intro()
                break

            # Exit the program
            case "10":
                exit()

            # Invalid
            case _:
                print("\n🚫 Invalid operation code!")


# ---------------------------------------------------------------------------
# Graph main and intro functions
# ---------------------------------------------------------------------------

def graph_main():
    """Show the graph intro and open the adjacency matrix graph menu."""
    graph_intro("full")
    adj_matrix_main()


def graph_intro(condition):
    """Print the ASCII art and definition ("full") or only the definition ("def")."""
    graph_ascii = """\n
  .-_'''-.   .-------.       ____    .-------. .---.  .---.  
 '_( )_   \  |  _ _   \    .'  __ `. \  _(`)_ \|   |  |_ _|  
|(_ o _)|  ' | ( ' )  |   /   '  \  \| (_ o._)||   |  ( ' )  
. (_,_)/___| |(_ o _) /   |___|  /  ||  (_,_) /|   '-(_{;}_) 
|  |  .-----.| (_,_).' __    _.-`   ||   '-.-' |      (_,_)  
'  \  '-   .'|  |\ \  |  |.'   _    ||   |     | _ _--.   |  
 \  `-'`   | |  | \ `'   /|  _( )_  ||   |     |( ' ) |   |  
  \        / |  |  \    / \ (_ o _) //   )     (_{;}_)|   |  
   `'-...-'  ''-'   `'-'   '.(_,_).' `---'     '(_,_) '---'\n"""

    graph_def = """\n🎯 A graph is a non-linear data structure consisting of vertices (nodes) and edges that connect pairs of vertices. Graphs are used to model relationships between entities, making them essential in various fields such as computer science, biology, social networks, and transportation. Graphs can be directed or undirected, weighted or unweighted, and can contain cycles or be acyclic. The versatility of graphs allows them to represent complex structures and relationships, enabling efficient problem-solving and analysis. Graphs can be represented using either an Adjacency Matrix or an Adjacency List.

🌟 An adjacency matrix is a 2D array used to represent a graph, where the rows and columns correspond to vertices. The element at row (i) and column (j) indicates the presence and weight of an edge between vertices (i) and (j). For an undirected graph, the matrix is symmetric, while for a directed graph, it is not. The adjacency matrix allows for quick edge lookups with a time complexity of O(1), but it requires O(V^2) space, making it more suitable for dense graphs where the number of edges is close to the maximum possible.

🌟 An adjacency list represents a graph using an array of lists. Each element in the array corresponds to a vertex, and the list at each index contains the vertices adjacent to that vertex. This representation is more space-efficient for sparse graphs, as it only stores existing edges, resulting in a space complexity of O(V + E). Adjacency lists allow for efficient traversal of the graph, making them ideal for algorithms like Depth-First Search (DFS) and Breadth-First Search (BFS). However, edge lookups can be slower compared to an adjacency matrix, with a time complexity proportional to the degree of the vertex."""

    if condition == "full":
        print(graph_ascii)
        print(graph_def)
    elif condition == "def":
        print(graph_def)


# ---------------------------------------------------------------------------
# Input helpers for vertices and weights
# ---------------------------------------------------------------------------

def get_u(msg="first vertex"):
    """Ask for the first vertex until an int is entered; msg customizes the prompt."""
    while True:
        u = utility.input_verify("int", msg)
        if u is None:
            print(f"\n🚫 Vertices are identified by integers in accordance with the matrix.")
            continue
        else:
            return u


def get_v():
    """Ask for the second vertex until an int is entered."""
    while True:
        v = utility.input_verify("int", "second vertex")
        if v is None:
            print(f"\n🚫 Vertices are identified by integers in accordance with the matrix.")
            continue
        else:
            return v


def get_weight():
    """Ask for an edge weight until an int is entered."""
    while True:
        weight = utility.input_verify("int", "weight")
        if weight is None:
            print(f"\n🚫 Weight can only be an INT.")
            continue
        else:
            return weight


# Run the graph module on its own
if __name__ == "__main__":
    graph_main()
