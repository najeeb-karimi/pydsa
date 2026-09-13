"""Every topic PyDSA teaches: the ID used by --topic, its title, its category and how to open it."""

from typing import Callable, NamedTuple

from pydsa.ui.screens import (
    array, deque, disjoint_set, graph, graph_algorithms, hash_set, hash_table, heap, linked_list, queue,
    searching_algorithms, sorting_algorithms, stack, tree, trie,
)

CATEGORIES = {
    "linear": "Linear data structures",
    "non-linear": "Non-linear data structures",
    "algorithms": "Algorithms",
}


class Topic(NamedTuple):
    """A topic and how to open it."""

    id: str
    title: str
    category: str
    open: Callable[[], object]  # Shows the topic and returns a Nav when the user leaves it
    parent: str | None = None  # The ID of the topic whose menu leads here; None for topics on a category menu


def _slug(name):
    return name.lower().replace(" ", "-")


TOPICS = (
    Topic("array", "Array", "linear", array.run),
    Topic("stack", "Stack", "linear", stack.run),
    Topic("queue", "Queue", "linear", queue.run),
    Topic("deque", "Deque", "linear", deque.run),
    Topic("linked-list", "Linked List", "linear", linked_list.run),
    *(Topic(_slug(kind.name), kind.name.title(), "linear", lambda kind=kind: linked_list.run_kind(kind), "linked-list")
      for kind in (linked_list.SINGLY, linked_list.DOUBLY, linked_list.SINGLY_CIRCULAR, linked_list.DOUBLY_CIRCULAR)),

    Topic("tree", "Tree", "non-linear", tree.run),
    Topic("bst", "Binary Search Tree (BST)", "non-linear", lambda: tree.run_kind(tree.BST), "tree"),
    Topic("avl-tree", "AVL Tree", "non-linear", lambda: tree.run_kind(tree.AVL), "tree"),
    Topic("heap", "Heap & Priority Queue", "non-linear", heap.run),
    Topic("min-heap", "Min Heap", "non-linear", lambda: heap.run_kind(heap.MIN), "heap"),
    Topic("max-heap", "Max Heap", "non-linear", lambda: heap.run_kind(heap.MAX), "heap"),
    Topic("priority-queue", "Priority Queue", "non-linear", heap.run_queue, "heap"),
    Topic("trie", "Trie", "non-linear", trie.run),
    Topic("graph", "Graph", "non-linear", graph.run),
    Topic("adjacency-matrix-graph", "Adjacency Matrix Graph", "non-linear", graph.run_matrix, "graph"),
    Topic("adjacency-list-graph", "Adjacency List Graph", "non-linear", graph.run_list, "graph"),
    Topic("hash-table", "Hash Table", "non-linear", hash_table.run),
    Topic("chaining-hash-table", "Separate Chaining Hash Table", "non-linear",
          lambda: hash_table.run_kind(hash_table.CHAINING), "hash-table"),
    Topic("linear-probing-hash-table", "Linear Probing Hash Table", "non-linear",
          lambda: hash_table.run_kind(hash_table.PROBING), "hash-table"),
    Topic("hash-set", "Hash Set", "non-linear", hash_set.run, "hash-table"),
    Topic("disjoint-set", "Disjoint Set", "non-linear", disjoint_set.run),

    # Each algorithm opens the screen that runs it
    Topic("sorting", "Sorting", "algorithms", sorting_algorithms.run),
    *(Topic(_slug(sort.name), sort.name, "algorithms", sorting_algorithms.run, "sorting") for sort in sorting_algorithms.SORTS),
    Topic("searching", "Searching", "algorithms", searching_algorithms.run),
    *(Topic(_slug(search.name), search.name, "algorithms", searching_algorithms.run, "searching")
      for search in searching_algorithms.SEARCHES),
    Topic("graph-algorithms", "Graph Algorithms", "algorithms", graph_algorithms.run),
    *(Topic(topic_id, title, "algorithms", graph_algorithms.run, "graph-algorithms") for topic_id, title in (
        ("dijkstra", "Dijkstra's Shortest Paths"),
        ("topological-sort", "Topological Sort"),
        ("cycle-detection", "Cycle Detection"),
        ("prim", "Minimum Spanning Tree (Prim)"),
        ("kruskal", "Minimum Spanning Tree (Kruskal)"),
    )),
)


def find(topic_id):
    """Return the topic with the given ID (in any letter case), or None."""
    return next((topic for topic in TOPICS if topic.id == topic_id.lower()), None)


def listed(category):
    """Return the topics shown on a category's menu."""
    return [topic for topic in TOPICS if topic.category == category and topic.parent is None]
