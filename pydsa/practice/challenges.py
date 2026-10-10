"""Predict a real operation on fresh, visible data; answers come from the core implementation."""

import ast
import random
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable

from pydsa.algorithms import graph_algorithms, searching, sorting
from pydsa.core.array import Array
from pydsa.core.b_tree import BTree
from pydsa.core.deque import Deque
from pydsa.core.disjoint_set import DisjointSet
from pydsa.core.graph import ListGraph, MatrixGraph
from pydsa.core.hash_set import HashSet
from pydsa.core.hash_table import ChainingHashTable, LinearProbingHashTable
from pydsa.core.heap import MaxHeap, MinHeap
from pydsa.core.linked_list import DoublyCircularLinkedList, DoublyLinkedList, SinglyCircularLinkedList, SinglyLinkedList
from pydsa.core.priority_queue import PriorityQueue
from pydsa.core.queue import Queue
from pydsa.core.red_black_tree import RedBlackTree
from pydsa.core.segment_tree import SegmentTree
from pydsa.core.fenwick_tree import FenwickTree
from pydsa.core.stack import Stack
from pydsa.core.tree import AVLTree, BinarySearchTree
from pydsa.core.trie import Trie
from pydsa.ui import render


@dataclass(frozen=True)
class Challenge:
    topic: str
    prompt: str
    state: dict
    answer: object
    explanation: str
    draw: Callable[[], None]
    solve: Callable[[], object]

    def check(self, text):
        """Accept numbers, true/false, and lists with brackets or comma-separated values."""
        text = text.strip()
        try:
            value = ast.literal_eval(text)
        except (ValueError, SyntaxError):
            value = text
        if isinstance(self.answer, bool):
            return text.casefold() in (("true", "yes") if self.answer else ("false", "no"))
        if isinstance(self.answer, list):
            if isinstance(value, tuple):
                value = list(value)
            elif not isinstance(value, list):
                try:
                    value = [ast.literal_eval(part.strip()) for part in text.split(",")]
                except (ValueError, SyntaxError):
                    return False
        if type(value) is bool and type(self.answer) is not bool:
            return False
        return _same_answer(value, self.answer)


def _same_answer(value, answer):
    """Compare predictions without treating a boolean as a number, including inside lists."""
    if type(value) is bool or type(answer) is bool:
        return type(value) is type(answer) and value == answer
    if isinstance(answer, list):
        return (isinstance(value, list) and len(value) == len(answer)
                and all(_same_answer(item, expected) for item, expected in zip(value, answer)))
    return value == answer


def _challenge(topic, prompt, state, structure, operation, draw, explanation, clone=None):
    def solve():
        return operation(clone() if clone else deepcopy(structure))
    return Challenge(topic, prompt, state, solve(), explanation, lambda: draw(structure), solve)


LINKED = {
    "linked-list": SinglyLinkedList,
    "singly-linked-list": SinglyLinkedList,
    "doubly-linked-list": DoublyLinkedList,
    "singly-circular-linked-list": SinglyCircularLinkedList,
    "doubly-circular-linked-list": DoublyCircularLinkedList,
}
SORTS = {name.replace("_", "-"): getattr(sorting, name) for name in (
    "bubble_sort", "selection_sort", "insertion_sort", "quick_sort", "heap_sort", "shell_sort", "merge_sort",
    "counting_sort", "radix_sort",
)}
SEARCHES = {name.replace("_", "-"): getattr(searching, name) for name in (
    "linear_search", "binary_search", "jump_search", "interpolation_search", "exponential_search",
)}
GRAPH_TOPICS = {"graph", "adjacency-list-graph", "adjacency-matrix-graph", "graph-algorithms",
                "dijkstra", "topological-sort", "cycle-detection", "prim", "kruskal"}
SUPPORTED = frozenset({"segment-tree", "fenwick-tree", "array", "stack", "queue", "deque", "tree", "bst", "avl-tree", "red-black-tree", "b-tree", "heap", "min-heap",
                       "max-heap", "priority-queue", "trie", "hash-table", "chaining-hash-table",
                       "linear-probing-hash-table", "hash-set", "disjoint-set", "sorting", "searching"}
                      | set(LINKED) | set(SORTS) | set(SEARCHES) | GRAPH_TOPICS)


def make(topic, rng=None):
    rng = rng or random.Random()
    values = rng.sample(range(1, 30), 5)
    state = {"values": values}
    if topic in ("segment-tree", "fenwick-tree"):
        left = rng.randrange(len(values))
        right = rng.randrange(left, len(values))
        position, replacement = rng.randrange(len(values)), rng.randrange(-10, 30)
        operation = rng.choice(("sum", "min", "max")) if topic == "segment-tree" else "sum"
        tree = SegmentTree(values, operation) if topic == "segment-tree" else FenwickTree(values)
        state.update(left=left, right=right, index=position, replacement=replacement, operation=operation)

        def replace_and_query(tree):
            tree.update(position, replacement)
            return tree.query(left, right) if topic == "segment-tree" else tree.range_sum(left, right)

        return _challenge(topic,
                          f"After replacing index {position} with {replacement}, what is the {operation} of "
                          f"the inclusive range [{left}, {right}]?", state, tree, replace_and_query,
                          render.segment_tree if topic == "segment-tree" else render.fenwick_tree,
                          "Replace the value first, then use every position from the range start through its end.")
    if topic == "array":
        array = Array(5, int, 0)
        for i, value in enumerate(values):
            array.insert(i, value)
        index = rng.randrange(5)
        state["index"] = index
        return _challenge(topic, f"What does Get at index {index} return?", state, array, lambda a: a.get(index),
                          lambda a: render.array(a.items), "An array index selects that slot directly.")
    if topic == "stack":
        stack = Stack(7)
        for value in values:
            stack.push(value)
        return _challenge(topic, "What does the next Pop return?", state, stack, lambda s: s.pop(), render.stack,
                          "A stack removes the most recently pushed item.")
    if topic == "queue":
        queue = Queue(7)
        for value in values:
            queue.enqueue(value)
        return _challenge(topic, "What does the next Dequeue return?", state, queue, lambda q: q.dequeue(),
                          lambda q: render.circular_slots(q, {"front": q.front, "rear": q.rear}),
                          "The oldest waiting item leaves first.")
    if topic == "deque":
        deque = Deque(7)
        for value in values:
            deque.push_back(value)
        front = rng.choice((True, False))
        state["front"] = front
        return _challenge(topic, f"What does Pop {'Front' if front else 'Back'} return?", state, deque,
                          lambda d: d.pop_front() if front else d.pop_back(),
                          lambda d: render.circular_slots(d, {"front": d.front, "back": d.back}),
                          "A deque can remove the item at either end.")
    if topic in LINKED:
        linked = LINKED[topic]()
        for value in values:
            linked.insert_at_end(value)
        return _challenge(topic, "What does deleting from the beginning return?", state, linked,
                          lambda linked: linked.delete_from_beginning(),
                          lambda linked: render.linked_list(list(linked), doubly="doubly" in topic,
                                                           circular="circular" in topic),
                          "The head is the first node, even when the links form a circle.")
    if topic in ("red-black-tree", "b-tree"):
        degree = rng.choice((2, 3))
        tree = BTree(degree) if topic == "b-tree" else RedBlackTree()
        for value in values:
            tree.insert(value)
        target = rng.randrange(1, 30)
        state.update(target=target, degree=degree)

        def insert_and_walk(tree):
            tree.insert(target)
            return tree.inorder()

        return _challenge(topic, f"After inserting {target}, what sequence does inorder traversal return?",
                          state, tree, insert_and_walk, render.b_tree if topic == "b-tree" else render.red_black_tree,
                          "Inorder reads keys in sorted order, including every duplicate after insertion.")
    if topic in ("tree", "bst", "avl-tree"):
        tree = AVLTree("num") if topic == "avl-tree" else BinarySearchTree("num")
        for value in values:
            tree.insert(value)
        level = rng.choice((True, False))
        state["level"] = level
        return _challenge(topic, f"What sequence does {'level-order' if level else 'inorder'} traversal return?",
                          state, tree, lambda t: t.level_order() if level else t.inorder(), render.binary_tree,
                          "Level order visits breadth first; inorder visits left, node, right.")
    if topic in ("heap", "min-heap", "max-heap"):
        heap = MaxHeap("num") if topic == "max-heap" else MinHeap("num")
        heap.heapify(values)
        return _challenge(topic, "What does the next Extract return?", state, heap, lambda h: h.extract()[0],
                          render.heap, f"The {'largest' if topic == 'max-heap' else 'smallest'} value is at the root.")
    if topic == "priority-queue":
        entries = [(f"job-{i + 1}", rng.randint(1, 3)) for i in range(5)]
        state["entries"] = entries
        def new_queue():
            queue = PriorityQueue()
            for item, priority in entries:
                queue.enqueue(item, priority)
            return queue
        return _challenge(topic, "Which job does the next Dequeue return?", state, new_queue(), lambda q: q.dequeue()[0],
                          render.priority_queue, "The smallest priority number wins; ties follow arrival order.", new_queue)
    if topic == "trie":
        words = rng.sample(["car", "card", "cart", "cat", "dog", "door", "dot"], 5)
        prefix = rng.choice(("ca", "do"))
        state.update(words=words, prefix=prefix)
        return _challenge(topic, f"What list does autocomplete for {prefix!r} return?", state, Trie(words),
                          lambda t: t.autocomplete(prefix), render.trie,
                          "Autocomplete collects stored words below the prefix in character order.")
    if topic in ("hash-table", "chaining-hash-table", "linear-probing-hash-table"):
        probing = topic == "linear-probing-hash-table"
        table = LinearProbingHashTable(7) if probing else ChainingHashTable(7)
        keys = [rng.randrange(7)]
        keys += [keys[0] + 7, keys[0] + 14]
        for key in keys:
            table.insert(key, str(key))
        target = keys[0] + 21
        state.update(keys=keys, target=target, size=7)
        return _challenge(topic, f"In which {'slot' if probing else 'bucket'} will inserting key {target} land? "
                          "For these small integer keys, the home index is key % 7.", state, table,
                          lambda t: t.insert(target, str(target))[0],
                          render.probing_table if probing else render.chaining_table,
                          "Probing advances past occupied slots; chaining keeps all colliding pairs in their home bucket.")
    if topic == "hash-set":
        a, b = HashSet(8, values[:3]), HashSet(8, values[2:])
        state.update(a=values[:3], b=values[2:])
        return _challenge(topic, "Which sorted list of items is in the intersection of A and B?", state, (a, b),
                          lambda pair: sorted(pair[0].intersection(pair[1])),
                          lambda pair: render.hash_sets({"A": pair[0], "B": pair[1]}),
                          "Intersection keeps only items present in both sets.")
    if topic == "disjoint-set":
        union_find = DisjointSet(7)
        pairs = [(rng.randrange(7), rng.randrange(7)) for _ in range(5)]
        for a, b in pairs:
            union_find.union(a, b)
        element = rng.randrange(7)
        state.update(pairs=pairs, element=element, parents=list(union_find.parent))
        return _challenge(topic, f"Which root does Find({element}) return?", state, union_find,
                          lambda u: u.find(element), render.disjoint_set,
                          "Follow the parent links until an element is its own parent.")
    if topic == "sorting" or topic in SORTS:
        def sort(items):
            if topic == "sorting":
                # Bubble's first pass has exactly n - 1 adjacent comparisons; its first n - 1 swaps are not a pass.
                for i in range(len(items) - 1):
                    pair = items[i:i + 2]
                    for _ in sorting.bubble_sort(pair):
                        pass
                    items[i:i + 2] = pair
            else:
                for _ in SORTS[topic](items):
                    pass
            return items
        prompt = "What is the array after one ascending bubble pass?" if topic == "sorting" else "What is the fully sorted array in ascending order?"
        return _challenge(topic, prompt, state, values, sort, render.array,
                          "A bubble pass compares each neighboring pair once; a complete sort puts all values in order.")
    if topic == "searching" or topic in SEARCHES:
        target = rng.choice(values)
        state["target"] = target
        search = SEARCHES.get(topic, searching.linear_search)
        return _challenge(topic, f"Which original index does searching for {target} return?", state, values,
                          lambda items: search(items, target), render.array,
                          "PyDSA reports the first matching index in the original list, even when searching a sorted copy.")
    if topic in GRAPH_TOPICS:
        return _graph(topic, rng)
    raise KeyError(f"No prediction challenge for {topic!r}")


def _graph(topic, rng):
    directed = topic not in ("prim", "kruskal")
    graph = MatrixGraph(5, directed) if topic == "adjacency-matrix-graph" else ListGraph(directed)
    if isinstance(graph, ListGraph):
        for v in range(5):
            graph.add_vertex(v)
    edges = [(i, i + 1, rng.randint(1, 9)) for i in range(4)]
    edges += [(0, 2, rng.randint(1, 9)), (1, 4, rng.randint(1, 9))]
    if topic == "cycle-detection" and rng.choice((True, False)):
        edges.append((4, 0, 1))
    for u, v, weight in edges:
        graph.add_edge(u, v, weight)
    state = {"edges": edges, "directed": directed}
    if topic == "topological-sort":
        prompt, operation = "What topological sequence does Kahn's algorithm return?", graph_algorithms.topological_sort
        explanation = "Place vertices only after all their incoming dependencies have been removed."
    elif topic == "cycle-detection":
        prompt = "Does this directed graph contain a cycle? Type true or false."
        operation = lambda g: graph_algorithms.find_cycle(g) is not None
        explanation = "A directed cycle returns to a vertex along the directions of its edges."
    elif topic in ("prim", "kruskal"):
        prompt = "What is the total weight of the minimum spanning tree?"
        algorithm = graph_algorithms.prim if topic == "prim" else graph_algorithms.kruskal
        operation = lambda g: algorithm(g).total
        explanation = "The spanning tree connects every vertex without cycles at minimum total weight."
    else:
        prompt, operation = "What is the shortest distance from 0 to 4?", lambda g: graph_algorithms.dijkstra(g, 0).distances[4]
        explanation = "Compare the total weights of possible routes; the fewest edges need not give the shortest distance."
    draw = (lambda g: render.adjacency_matrix(g.adj_matrix, g.directed)) if isinstance(graph, MatrixGraph) else (
        lambda g: render.adjacency_list(g.adj_list, g.directed))
    return _challenge(topic, prompt, state, graph, operation, draw, explanation)
