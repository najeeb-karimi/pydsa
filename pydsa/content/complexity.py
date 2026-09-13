"""Time and space complexity of the operations PyDSA implements, shown with each definition."""

from typing import NamedTuple


class ComplexityTable(NamedTuple):
    """A titled table of complexities with an optional explanatory note."""

    title: str
    columns: tuple
    rows: tuple
    note: str | None = None


ARRAY = ComplexityTable(
    "Array operations",
    ("Operation", "Time", "Extra space"),
    (
        ("Insert at an index", "O(1)", "O(1)"),
        ("Delete at an index", "O(1)", "O(1)"),
        ("Get by index", "O(1)", "O(1)"),
        ("Linear search", "O(n)", "O(1)"),
        ("Binary search", "O(n log n)", "O(n)"),
    ),
    "n is the number of elements. Binary search itself takes O(log n), but PyDSA first sorts a copy of the array so the original order is kept.",
)

SORTING = ComplexityTable(
    "Sorting algorithms",
    ("Algorithm", "Best", "Average", "Worst", "Extra space"),
    (
        ("Bubble sort", "O(n)", "O(n²)", "O(n²)", "O(1)"),
        ("Selection sort", "O(n²)", "O(n²)", "O(n²)", "O(1)"),
        ("Insertion sort", "O(n)", "O(n²)", "O(n²)", "O(1)"),
        ("Quick sort", "O(n log n)", "O(n log n)", "O(n²)", "O(log n)"),
        ("Heap sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(1)"),
        ("Shell sort", "O(n log n)", "Depends on the gaps", "O(n²)", "O(1)"),
    ),
    "Quick sort's extra space is for its recursive calls and can grow to O(n) in the worst case.",
)

STACK = ComplexityTable(
    "Stack operations",
    ("Operation", "Time", "Extra space"),
    (
        ("Push", "O(1)", "O(1)"),
        ("Pop", "O(1)", "O(1)"),
        ("Peek", "O(1)", "O(1)"),
        ("Check if empty or full", "O(1)", "O(1)"),
        ("Size", "O(1)", "O(1)"),
    ),
)

QUEUE = ComplexityTable(
    "Queue operations",
    ("Operation", "Time", "Extra space"),
    (
        ("Enqueue", "O(1)", "O(1)"),
        ("Dequeue", "O(1)", "O(1)"),
        ("Peek front or rear", "O(1)", "O(1)"),
        ("Check if empty or full", "O(1)", "O(1)"),
        ("Size", "O(1)", "O(1)"),
    ),
    "The circular array lets both ends wrap around, so no items are ever shifted.",
)

DEQUE = ComplexityTable(
    "Deque operations",
    ("Operation", "Time", "Extra space"),
    (
        ("Push front or back", "O(1)", "O(1)"),
        ("Pop front or back", "O(1)", "O(1)"),
        ("Peek front or back", "O(1)", "O(1)"),
        ("Check if empty or full", "O(1)", "O(1)"),
        ("Size", "O(1)", "O(1)"),
    ),
    "Both ends wrap around the circular array, so no items are ever shifted.",
)

LINKED_LIST = ComplexityTable(
    "Linked list operations",
    ("Operation", "Singly", "Doubly", "Singly circular", "Doubly circular"),
    (
        ("Insert at beginning", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("Insert at position", "O(n)", "O(n)", "O(n)", "O(n)"),
        ("Insert at end", "O(n)", "O(n)", "O(1)", "O(1)"),
        ("Delete from beginning", "O(1)", "O(1)", "O(1)", "O(1)"),
        ("Delete from position", "O(n)", "O(n)", "O(n)", "O(n)"),
        ("Delete from end", "O(n)", "O(n)", "O(n)", "O(1)"),
        ("Search or display", "O(n)", "O(n)", "O(n)", "O(n)"),
        ("Walk k nodes around the loop", "—", "—", "O(k)", "O(k)"),
    ),
    "n is the number of nodes, and apart from the walk, every operation uses O(1) extra space. The singly and doubly linked lists only keep a reference to the head, so reaching the end takes O(n). The singly circular list also keeps a reference to the tail, and the doubly circular list reaches its tail through the head's prev link, so their ends are faster. Deleting from the end of the singly circular list still takes O(n), because the node before the tail can only be found by walking from the head.",
)

TREE = ComplexityTable(
    "Tree operations",
    ("Operation", "BST (average)", "BST (worst)", "AVL tree"),
    (
        ("Insert", "O(log n)", "O(n)", "O(log n)"),
        ("Delete", "O(log n)", "O(n)", "O(log n)"),
        ("Search", "O(log n)", "O(n)", "O(log n)"),
        ("Smallest or largest key", "O(log n)", "O(n)", "O(log n)"),
        ("Inorder, preorder or postorder", "O(n)", "O(n)", "O(n)"),
        ("Level order", "O(n)", "O(n)", "O(n)"),
        ("Height", "O(n)", "O(n)", "O(1)"),
        ("Node or leaf count", "O(n)", "O(n)", "O(n)"),
    ),
    "A BST reaches its worst case when keys arrive in sorted order and the tree turns into a chain. An AVL tree rotates to stay balanced, so its height is always O(log n), and every node already stores its own height. Traversals use O(h) extra space for their recursion, where h is the height, and level order uses O(n) for its queue.",
)

HEAP = ComplexityTable(
    "Heap operations",
    ("Operation", "Time", "Extra space"),
    (
        ("Insert (sift up)", "O(log n)", "O(1)"),
        ("Extract the root (sift down)", "O(log n)", "O(1)"),
        ("Peek at the root", "O(1)", "O(1)"),
        ("Build from a list (heapify)", "O(n)", "O(1)"),
        ("The other extreme (largest in a min heap)", "O(n)", "O(1)"),
        ("Level order", "O(n)", "O(n)"),
        ("Height, node or leaf count", "O(1)", "O(1)"),
    ),
    "n is the number of keys. A heap is a complete binary tree, so it's always log n levels tall, and its shape follows from its size alone. Heapify is O(n) rather than O(n log n) because most nodes sit near the bottom and only sift down a few levels.",
)

PRIORITY_QUEUE = ComplexityTable(
    "Priority queue operations",
    ("Operation", "Time", "Extra space"),
    (
        ("Enqueue", "O(log n)", "O(1)"),
        ("Dequeue", "O(log n)", "O(1)"),
        ("Peek", "O(1)", "O(1)"),
        ("Change priority", "O(n)", "O(1)"),
        ("Size", "O(1)", "O(1)"),
    ),
    "Changing a priority takes O(n) because the item has to be found first; moving it to its new place only takes O(log n).",
)

TRIE = ComplexityTable(
    "Trie operations",
    ("Operation", "Time", "Extra space"),
    (
        ("Insert a word", "O(L)", "O(L)"),
        ("Search a word", "O(L)", "O(1)"),
        ("Delete a word", "O(L)", "O(L)"),
        ("Check a prefix", "O(P)", "O(1)"),
        ("Autocomplete", "O(P + K)", "O(K)"),
        ("Word count", "O(1)", "O(1)"),
    ),
    "L is the length of the word, P the length of the prefix and K the number of nodes below the prefix. None of them depend on how many words the trie holds. The trie itself takes space proportional to the total number of characters, minus the prefixes its words share.",
)

GRAPH = ComplexityTable(
    "Graph operations",
    ("Operation", "Adjacency matrix", "Adjacency list"),
    (
        ("Add vertex", "O(V)", "O(1)"),
        ("Remove vertex", "O(V²)", "O(V + E)"),
        ("Add or remove an edge", "O(1)", "O(deg)"),
        ("Search an edge", "O(1)", "O(deg)"),
        ("BFS or DFS", "O(V²)", "O(V + E)"),
        ("Space", "O(V²)", "O(V + E)"),
    ),
    "V is the number of vertices, E the number of edges and deg the number of edges leaving the source vertex.",
)

HASH_TABLE = ComplexityTable(
    "Hash table operations",
    ("Operation", "Separate chaining", "Linear probing"),
    (
        ("Insert", "O(1) average, O(n) worst", "O(1) average, O(n) worst"),
        ("Search", "O(1) average, O(n) worst", "O(1) average, O(n) worst"),
        ("Delete", "O(1) average, O(n) worst", "O(1) average, O(n²) worst"),
        ("Space", "O(m + n)", "O(m)"),
    ),
    "n is the number of keys and m the number of buckets or slots. The averages assume the keys spread out evenly. Deleting from the probing table also rehashes the rest of the cluster, which is where its O(n²) worst case comes from.",
)

HASH_SET = ComplexityTable(
    "Hash set operations",
    ("Operation", "Average", "Worst"),
    (
        ("Add", "O(1)", "O(n)"),
        ("Remove", "O(1)", "O(n)"),
        ("Check membership", "O(1)", "O(n)"),
        ("Union", "O(n + m)", "O((n + m)²)"),
        ("Intersection", "O(n)", "O(n · m)"),
        ("Difference", "O(n)", "O(n · m)"),
        ("Subset check", "O(n)", "O(n · m)"),
    ),
    "n and m are the sizes of the two sets. Every item costs one lookup in the underlying hash table, which is O(1) on average and only slows down when many items share a bucket.",
)

DISJOINT_SET = ComplexityTable(
    "Disjoint set operations",
    ("Operation", "Time", "Extra space"),
    (
        ("Find", "O(α(n)) amortized", "O(1)"),
        ("Union", "O(α(n)) amortized", "O(1)"),
        ("Check if connected", "O(α(n)) amortized", "O(1)"),
        ("List sets", "O(n log n)", "O(n)"),
    ),
    "α(n) is the inverse Ackermann function, which stays below 5 for any number of elements you could ever store. Listing the sets follows every element up to its root without compressing paths, and union by rank keeps every tree at most log n tall. Without union by rank and path compression, a single find could take O(n).",
)
