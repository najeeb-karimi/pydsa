"""Hash table implementation using separate chaining (open hashing) for collision resolution."""

import utility


# ---------------------------------------------------------------------------
# Hash table with Separate Chaining (Open Hashing)
# ---------------------------------------------------------------------------

class ChainingHashTable:
    """Hash table where each bucket is a list, so colliding keys are chained in the same bucket."""

    def __init__(self, size):
        """Initialize the hash table with the given number of empty buckets."""
        self.size = size
        self.table = [[] for _ in range(size)]
        print(f"\n✅ Initialized hash table with {size} buckets.")
        print("ℹ️ Since Chaining uses another data structure for collision resolution, the hash table remains dynamic, so you need not worry about storage space!\n")

    def hash_function(self, key):
        """Return the bucket index for a key: its hash code modulo the table size."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert a key-value pair, or update the value if the key already exists; return a status message."""
        index = self.hash_function(key)
        # Update the value if the key is already in the bucket
        for kv in self.table[index]:
            if kv[0] == key:
                kv[1] = value
                return f"\n✅ Insertion successful. Updated key ({key}) with value ({value}) at index {index}."
        # Otherwise, append a new key-value pair to the bucket
        self.table[index].append([key, value])
        return f"\n✅ Insertion successful. Inserted key ({key}) with value ({value}) at index {index}."

    def lookup(self, key):
        """Look up a key and return a message with its index and value, or a not-found message."""
        index = self.hash_function(key)
        for kv in self.table[index]:
            if kv[0] == key:
                return f"\n✅ Searching successful. Key ({key}) found at index {index} with value ({kv[1]})."
        return f"\n❌ Searching successful. Key ({key}) not found."

    def delete(self, key):
        """Delete a key-value pair and return a status message."""
        index = self.hash_function(key)
        for i, kv in enumerate(self.table[index]):
            if kv[0] == key:
                del self.table[index][i]
                return f"\n✅ Deletion successful. Deleted key ({key}) from index {index}."
        return f"\n🚫 Deletion unsuccessful. Key ({key}) not found, nothing to delete."

    def display(self):
        """Print the hash table, one bucket per line."""
        for bucket in self.table:
            print("🔹", self.table.index(bucket), bucket)


def chaining_main():
    """Create a separate chaining hash table and run its operation menu."""

    # Table size validation loop; the size is the only input needed to create the table
    while True:
        size = utility.input_verify("int", "the total number of buckets you want; in other words, the size of the hash table")
        if size is not None:
            chaining_ht = ChainingHashTable(size)
            chaining_ht.display()
            break
        else:
            print("\n🚫 Invalid data type. Hash table size must be an INT.")
            continue

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the Chaining Hash Table?
★0) Definition
★1) Insertion
★2) Deletion
★3) Searching
★4) Displaying
★5) New Hash Table
★6) New Data Structure
★7) Exiting the Program

>>> """)
        match opr:

            # Definition
            case "0":
                hash_table_intro("def")

            # Insertion
            case "1":
                key = get_key()
                value = get_value()
                result = chaining_ht.insert(key, value)
                print(result)

            # Deletion
            case "2":
                key = get_key(text="key that you want to delete")
                result = chaining_ht.delete(key)
                print(result)

            # Searching
            case "3":
                key = get_key(text="key that you want to  search for")
                result = chaining_ht.lookup(key)
                print(result)

            # Displaying
            case "4":
                print("\n👇🏻 Here's a display of your Hash Table:")
                chaining_ht.display()

            # New hash table
            case "5":
                utility.clear()
                hash_table_intro("full")
                hash_table_main()
                break

            # New data structure
            case "6":
                utility.clear()
                utility.main_intro()
                break

            # Exit the program
            case "7":
                exit()

            # Invalid
            case _:
                print("\n🚫 Invalid operation code!")


# ---------------------------------------------------------------------------
# Hash table main and intro functions
# ---------------------------------------------------------------------------

def hash_table_main():
    """Show the hash table intro and open the separate chaining hash table menu."""
    hash_table_intro("full")
    chaining_main()


def hash_table_intro(condition):
    """Print the ASCII art and definition ("full") or only the definition ("def")."""
    hash_table_ascii = """\n
.---.  .---.    ____       .-'''-. .---.  .---.         ,---------.    ____     _______     .---.       .-''-.   
|   |  |_ _|  .'  __ `.   / _     \|   |  |_ _|         \          \ .'  __ `. \  ____  \   | ,_|     .'_ _   \  
|   |  ( ' ) /   '  \  \ (`' )/`--'|   |  ( ' )          `--.  ,---'/   '  \  \| |    \ | ,-./  )    / ( ` )   ' 
|   '-(_{;}_)|___|  /  |(_ o _).   |   '-(_{;}_)            |   \   |___|  /  || |____/ / \  '_ '`) . (_ o _)  | 
|      (_,_)    _.-`   | (_,_). '. |      (_,_)             :_ _:      _.-`   ||   _ _ '.  > (_)  ) |  (_,_)___| 
| _ _--.   | .'   _    |.---.  \  :| _ _--.   |             (_I_)   .'   _    ||  ( ' )  \(  .  .-' '  \   .---. 
|( ' ) |   | |  _( )_  |\    `-'  ||( ' ) |   |            (_(=)_)  |  _( )_  || (_{;}_) | `-'`-'|___\  `-'    / 
(_{;}_)|   | \ (_ o _) / \       / (_{;}_)|   |             (_I_)   \ (_ o _) /|  (_,_)  /  |        \\       /  
'(_,_) '---'  '.(_,_).'   `-...-'  '(_,_) '---'             '---'    '.(_,_).' /_______.'   `--------` `'-..-'\n"""

    hash_table_def = """\n🎯 A graph is a non-linear data structure consisting of vertices (nodes) and edges that connect pairs of vertices. Graphs are used to model relationships between entities, making them essential in various fields such as computer science, biology, social networks, and transportation. Graphs can be directed or undirected, weighted or unweighted, and can contain cycles or be acyclic. The versatility of graphs allows them to represent complex structures and relationships, enabling efficient problem-solving and analysis. Graphs can be represented using either an Adjacency Matrix or an Adjacency List.

🌟 An adjacency matrix is a 2D array used to represent a graph, where the rows and columns correspond to vertices. The element at row (i) and column (j) indicates the presence and weight of an edge between vertices (i) and (j). For an undirected graph, the matrix is symmetric, while for a directed graph, it is not. The adjacency matrix allows for quick edge lookups with a time complexity of O(1), but it requires O(V^2) space, making it more suitable for dense graphs where the number of edges is close to the maximum possible.

🌟 An adjacency list represents a graph using an array of lists. Each element in the array corresponds to a vertex, and the list at each index contains the vertices adjacent to that vertex. This representation is more space-efficient for sparse graphs, as it only stores existing edges, resulting in a space complexity of O(V + E). Adjacency lists allow for efficient traversal of the graph, making them ideal for algorithms like Depth-First Search (DFS) and Breadth-First Search (BFS). However, edge lookups can be slower compared to an adjacency matrix, with a time complexity proportional to the degree of the vertex."""

    if condition == "full":
        print(hash_table_ascii)
        print(hash_table_def)
    elif condition == "def":
        print(hash_table_def)


# ---------------------------------------------------------------------------
# Input helpers for keys and values
# ---------------------------------------------------------------------------

def get_key(text="key"):
    """Ask for a key of any type until a valid one is entered; text customizes the prompt."""
    print("\n🔑 Specify the Key:")
    while True:
        key = utility.input_verify(msg=text)
        if key is None:
            print(f"\n🚫 Invalid data type for the key.")
            continue
        else:
            return key


def get_value(text="value"):
    """Ask for a value of any type until a valid one is entered; text customizes the prompt."""
    print("\n🚪 Specify the Value:")
    while True:
        value = utility.input_verify(msg=text)
        if value is None:
            print(f"\n🚫 Invalid data type for the value.")
            continue
        else:
            return value


# Run the hash table module on its own
if __name__ == "__main__":
    hash_table_main()
