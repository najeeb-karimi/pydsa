# Glossary
> Short explanations of the words PyDSA's guides use, from A to Z. The guides show these words in bold.

## Adjacent
Two vertices are adjacent when an edge connects them directly, which also makes them neighbors. In a directed graph, `v` is adjacent to `u` when there's an edge from `u` to `v`.

## Algorithm
A precise, step-by-step recipe for solving a problem, such as sorting a list or finding the shortest route. The same problem can often be solved by several algorithms that differ in speed and memory use.

## Amortized time
The average cost of an operation over a long run of operations, even when a few of them are expensive. For example, a disjoint set's path compression makes some finds slower so that later finds become almost instant.

## Balance factor
The height of a node's left subtree minus the height of its right subtree. An AVL tree keeps every balance factor at -1, 0 or 1, and rotates nodes when one goes outside that range.

## Best, average and worst case
The cost of an algorithm often depends on its input, not just on the input's size. The best case is the luckiest input, like searching for a value that's first in the list, the worst case is the unluckiest input, and the average case is what to expect from typical inputs.

## Big O notation
A way to describe how the work or memory of an algorithm grows as its input grows, ignoring constant factors and small details. O(1) means the cost stays the same however big the input gets, O(log n) that it grows very slowly, O(n) that it grows in step with the input, and O(n²) that doubling the input makes it about four times as big.

## Binary tree
A tree where every node has at most two children, called its left child and its right child.

## Breadth-first search (BFS)
A way to explore a graph or tree that visits all the neighbors of the starting vertex first, then all of their neighbors, and so on, spreading outward in rings. It uses a queue to remember which vertices to visit next.

## Bucket
One position of a hash table's array, where the keys that hash to that position are stored. In a linear probing table, the positions are usually called slots.

## Call stack
The stack a program uses to keep track of the functions that are running. Calling a function pushes a frame with its local variables, and returning from the function pops that frame.

## Capacity
The largest number of items a data structure with a fixed size can hold. In PyDSA, you choose the capacity of a stack, queue or deque when you create it.

## Circular array
An array whose ends are treated as joined, so moving past the last slot wraps around to slot 0. Queues and deques use one so their items never have to shift.

## Cluster
A run of taken slots next to each other in a linear probing hash table. A key that lands anywhere in a cluster has to probe to its end, so long clusters slow the table down.

## Collision
When two different keys hash to the same position in a hash table. Every hash table needs a way to handle collisions, such as separate chaining or linear probing.

## Comparison sort
A sorting algorithm that decides the order only by comparing two values at a time, like Bubble Sort, Quick Sort and Merge Sort. No comparison sort can beat O(n log n) comparisons in the worst case.

## Complete binary tree
A binary tree where every level is full except possibly the last one, which is filled from left to right. Its shape depends only on its number of nodes, which lets a heap store it in a plain array.

## Connected graph
An undirected graph with a path between every pair of vertices. A graph that isn't connected falls apart into separate pieces, called connected components.

## Contiguous memory
Memory where values are stored in one unbroken block, one right after another. Arrays use contiguous memory, which lets the computer find any index with a single calculation.

## Cycle
A path in a graph that starts and ends at the same vertex. Trees never contain cycles, and a directed graph with a cycle has no topological order.

## Data structure
A way of organizing data in a computer so that certain operations are easy and quick, like an array, a stack or a hash table. Each data structure is quick at some operations and slow at others.

## Degree
The number of edges connected to a vertex. In a directed graph, the edges leaving a vertex give its out-degree, and the edges arriving give its in-degree.

## Dense and sparse graphs
A dense graph has edges between most pairs of its vertices, while a sparse graph has far fewer edges than that, like a road map. Dense graphs suit an adjacency matrix, and sparse graphs an adjacency list.

## Depth-first search (DFS)
A way to explore a graph or tree that follows one path as deep as it can go, then backs up to the last choice and tries the next path. It uses a stack, or recursion, to remember where to back up to.

## Directed graph
A graph where every edge has a direction, going from one vertex to another, like a one-way street. An edge from `u` to `v` doesn't let you travel from `v` back to `u`.

## Divide and conquer
A strategy that splits a problem into smaller pieces of the same kind, solves each piece, and combines their answers. Merge Sort and Quick Sort both divide and conquer.

## Dynamic array
An array that grows by itself: when it runs out of room, it moves its values into a bigger block of memory. Python's `list` is a dynamic array.

## Edge
A connection between two vertices in a graph, or between a parent and a child in a tree. An edge can have a direction and a weight.

## FIFO (First In, First Out)
The rule that the item added first is the first one removed, like in a line of people. Queues follow the FIFO rule.

## Greedy algorithm
An algorithm that builds its answer step by step, always making the choice that looks best right now and never taking it back. Dijkstra's, Prim's and Kruskal's algorithms are greedy, and for their problems, the greedy choices add up to the best answer.

## Hash function
A function that turns a key into a number, which a hash table wraps around to its size to get the key's position. The same key always gives the same number, and a good hash function spreads different keys out evenly.

## Head and tail
The first and last nodes of a linked list. Many operations start at the head, and a list that also keeps a reference to its tail can reach its end right away.

## Heap property
The rule every heap follows: in a min heap, each parent is smaller than or equal to its children, and in a max heap, each parent is larger than or equal to its children. It guarantees that the smallest or largest key is at the root.

## Heapify
Turning a whole list into a heap at once by sifting down every parent, starting with the last parent and working back to the root. It's quicker than inserting the values one at a time.

## Height
The number of levels in a tree, counting the root as level 1, so an empty tree has a height of 0. Some books count the edges on the longest path from the root instead, which gives one less.

## In-degree
The number of edges pointing into a vertex of a directed graph. A topological sort starts with the vertices whose in-degree is 0.

## In-order successor
The node that comes right after a node when a binary search tree is read in sorted order. When the node has a right subtree, its successor holds the smallest key in that subtree.

## In-place
An algorithm works in place when it rearranges the data inside the list it was given, using only a small, fixed amount of extra memory. Quick Sort and Heap Sort work in place, but Merge Sort needs extra room.

## Index
The number of a position in an array or a list. In Python and in PyDSA, indexes start at 0, so the last index of a list with 5 values is 4.

## Inverse Ackermann function
An extremely slow-growing function, written α(n), that appears in the cost of disjoint set operations. It stays below 5 for any number of elements that could fit in a computer, so in practice it acts like a constant.

## Key
The value used to find, order or compare an item, like the number in a tree node or the word in a dictionary. In a hash table, each key is paired with a value.

## Leaf
A node in a tree that has no children.

## Level
All the nodes of a tree that are the same number of steps away from the root. The root is on the first level, its children are on the second, and so on.

## LIFO (Last In, First Out)
The rule that the item added last is the first one removed, like in a stack of plates. Stacks follow the LIFO rule.

## Link (pointer)
A reference stored in a node that tells you where another node is, such as the next node of a linked list. Following links is how you move through linked lists, trees and graphs.

## Logarithm
Roughly, the number of times you can halve a number before reaching 1. The logarithm of 1,000 is about 10, and of 1,000,000 about 20, which is why algorithms whose work grows with the logarithm of the input, like Binary Search, stay quick on huge inputs.

## Node
One element of a linked list, tree or trie, holding an item and links to other nodes.

## Overflow and underflow
Overflow is trying to add an item to a data structure that's already full, like pushing onto a full stack. Underflow is trying to remove an item from one that's empty.

## Parent and child
In a tree, a node's children are the nodes directly below it, and its parent is the node directly above it. Every node except the root has exactly one parent.

## Path
A sequence of vertices where each one is connected to the next by an edge. The length of a path is its number of edges, or the sum of their weights in a weighted graph.

## Path compression
A trick used by a disjoint set: after a find, every element visited along the way is linked straight to the root. Later finds on those elements take a single step.

## Pivot
The value Quick Sort chooses to split a list around, with smaller values going before it and larger values after it. A pivot close to the middle value makes Quick Sort fastest.

## Prefix
The beginning part of a string. "ca" and "car" are both prefixes of "card", and a trie stores words so that words with the same prefix share their nodes.

## Priority
A number that says how important an item is, which decides when a priority queue serves it. In PyDSA, a smaller number means a higher priority.

## Probing
Checking slot after slot in an open addressing hash table to find a free slot or a key. Linear probing checks the very next slot each time, wrapping around at the end of the table.

## Recursion
When a function solves a problem by calling itself on smaller versions of the same problem, until it reaches a case small enough to answer directly. Tree traversals, Merge Sort and Quick Sort are often written with recursion.

## Rehashing
Inserting keys into a hash table again, so each one lands where its hash function now leads. PyDSA's linear probing table rehashes the rest of a cluster after a delete, so no search stops at the gap too early.

## Relaxation
In shortest path algorithms, checking whether going through a vertex gives a neighbor a shorter distance than it has so far, and updating the neighbor's distance if it does.

## Representative
The member of a disjoint set's set that stands for the whole set, which is the root of the set's tree. Two elements are in the same set when they have the same representative.

## Root
The top node of a tree, and the only node without a parent. In a disjoint set, the root of each set's tree is the set's representative.

## Rotation
A small rearrangement of a binary search tree that lifts a child above its parent while keeping every key in the right order. AVL trees use rotations to stay balanced.

## Shortest path
The path between two vertices with the smallest total weight, or with the fewest edges in a graph without weights. Two vertices can have more than one shortest path of the same length.

## Sifting
Moving a key up or down a heap to restore the heap property. Sifting up swaps a key with its parent while it belongs above its parent, and sifting down swaps a key with a child while that child belongs above it.

## Space complexity
How the extra memory an algorithm needs grows as its input grows, usually written in Big O notation.

## Spanning tree
A set of edges that connects every vertex of an undirected graph without forming a cycle. A minimum spanning tree is the spanning tree whose weights add up to the least.

## Stable sort
A sorting algorithm is stable when equal values keep the order they had before sorting. Stability matters when you sort by one thing and then by another, like sorting people by name and then by age.

## Subtree
A node of a tree together with all the nodes below it. The left subtree of a node starts at its left child, and the right subtree at its right child.

## Time complexity
How the work an algorithm does grows as its input grows, usually written in Big O notation. It's measured in steps, such as comparisons, rather than in seconds, so it doesn't depend on how fast the computer is.

## Traversal
Visiting every node of a tree or graph once, in a set order. Trees have inorder, preorder, postorder and level order traversals, and graphs have breadth-first and depth-first search.

## Undirected graph
A graph where every edge goes both ways, like a two-way street. An edge between `u` and `v` lets you travel from either one to the other.

## Union by rank
A rule used by a disjoint set: when two sets merge, the root of the shorter tree goes under the root of the taller one. It keeps the trees short, so finds stay quick.

## Vertex (plural: vertices)
A point in a graph, also called a node. Vertices are connected to each other by edges.

## Weight
A number attached to an edge of a graph, such as a distance, a time or a cost. The length of a path in a weighted graph is the sum of its edges' weights.
