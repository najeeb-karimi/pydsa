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

LINKED_LIST = ComplexityTable(
    "Linked list operations",
    ("Operation", "Singly", "Doubly"),
    (
        ("Insert at beginning", "O(1)", "O(1)"),
        ("Insert at position", "O(n)", "O(n)"),
        ("Insert at end", "O(n)", "O(n)"),
        ("Delete from beginning", "O(1)", "O(1)"),
        ("Delete from position", "O(n)", "O(n)"),
        ("Delete from end", "O(n)", "O(n)"),
        ("Search", "O(n)", "O(n)"),
        ("Display", "O(n)", "O(n)"),
    ),
    "n is the number of nodes, and every operation uses O(1) extra space. PyDSA only keeps a reference to the head, so reaching the end takes O(n); with a tail reference, inserting at the end would take O(1).",
)

TREE = ComplexityTable(
    "Tree operations",
    ("Operation", "BST (average)", "BST (worst)", "AVL tree"),
    (
        ("Insert", "O(log n)", "O(n)", "O(log n)"),
        ("Delete", "O(log n)", "O(n)", "O(log n)"),
        ("Search", "O(log n)", "O(n)", "O(log n)"),
        ("Traversal", "O(n)", "O(n)", "O(n)"),
    ),
    "A BST reaches its worst case when keys arrive in sorted order and the tree turns into a chain. An AVL tree rotates to stay balanced, so its height is always O(log n).",
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
