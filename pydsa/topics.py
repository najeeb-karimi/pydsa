"""Every topic PyDSA teaches: its ID (used by --topic and by its guide), its title, its category and how to open it."""

from typing import Callable, NamedTuple

from pydsa.ui.screens import (
    array, balanced_trees, deque, disjoint_set, graph, graph_algorithms, hash_set, hash_table, heap, linked_list, queue,
    searching_algorithms, sorting_algorithms, stack, tree, trie,
)

CATEGORIES = {
    "linear": "Linear structures",
    "trees": "Trees & heaps",
    "graphs": "Graphs & sets",
    "hashing": "Hashing & caches",
    "algorithms": "Algorithms",
}


class Topic(NamedTuple):
    """A topic and how to open it."""

    id: str
    title: str
    category: str
    open: Callable[[], object]  # Shows the topic and returns a Nav when the user leaves it
    parent: str | None = None  # The ID of the topic whose menu leads here; None for topics on a category menu


TOPICS = (
    Topic("array", "Array", "linear", array.run),
    Topic("stack", "Stack", "linear", stack.run),
    Topic("queue", "Queue", "linear", queue.run),
    Topic("deque", "Deque", "linear", deque.run),
    Topic("linked-list", "Linked List", "linear", linked_list.run),
    *(Topic(kind.guide, kind.name.title(), "linear", lambda kind=kind: linked_list.run_kind(kind), "linked-list")
      for kind in (linked_list.SINGLY, linked_list.DOUBLY, linked_list.SINGLY_CIRCULAR, linked_list.DOUBLY_CIRCULAR)),

    Topic("tree", "Tree", "trees", tree.run),
    Topic("bst", "Binary Search Tree (BST)", "trees", lambda: tree.run_kind(tree.BST), "tree"),
    Topic("avl-tree", "AVL Tree", "trees", lambda: tree.run_kind(tree.AVL), "tree"),
    Topic("red-black-tree", "Red-Black Tree", "trees", balanced_trees.run_red_black),
    Topic("b-tree", "B-Tree", "trees", balanced_trees.run_b_tree),
    Topic("heap", "Heap & Priority Queue", "trees", heap.run),
    Topic("min-heap", "Min Heap", "trees", lambda: heap.run_kind(heap.MIN), "heap"),
    Topic("max-heap", "Max Heap", "trees", lambda: heap.run_kind(heap.MAX), "heap"),
    Topic("priority-queue", "Priority Queue", "trees", heap.run_queue, "heap"),
    Topic("trie", "Trie", "trees", trie.run),
    Topic("graph", "Graph", "graphs", graph.run),
    Topic("adjacency-matrix-graph", "Adjacency Matrix Graph", "graphs", graph.run_matrix, "graph"),
    Topic("adjacency-list-graph", "Adjacency List Graph", "graphs", graph.run_list, "graph"),
    Topic("hash-table", "Hash Table", "hashing", hash_table.run),
    Topic("chaining-hash-table", "Separate Chaining Hash Table", "hashing",
          lambda: hash_table.run_kind(hash_table.CHAINING), "hash-table"),
    Topic("linear-probing-hash-table", "Linear Probing Hash Table", "hashing",
          lambda: hash_table.run_kind(hash_table.PROBING), "hash-table"),
    Topic("hash-set", "Hash Set", "hashing", hash_set.run),
    Topic("disjoint-set", "Disjoint Set", "graphs", disjoint_set.run),

    # Each algorithm opens the screen that runs it
    Topic("sorting", "Sorting", "algorithms", sorting_algorithms.run),
    *(Topic(sort.guide, sort.name, "algorithms", sorting_algorithms.run, "sorting") for sort in sorting_algorithms.SORTS),
    Topic("searching", "Searching", "algorithms", searching_algorithms.run),
    *(Topic(search.guide, search.name, "algorithms", searching_algorithms.run, "searching")
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
