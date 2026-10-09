"""Explained multiple-choice questions. Related topics share foundations and add their own question."""

from pydsa.practice.quiz import Question

# Each row is (prompt, correct choice, three distractors, explanation). The player shuffles the choices.
BANKS = {
    "array": (
        ("Which operation reads one array position directly?", "Get by index", ("Traverse every item", "Pop the root", "Follow a link"), "An index names the slot to read directly."),
        ("What happens when you delete an item in PyDSA's array?", "The slot returns to its default value", ("The array shrinks", "Every later item moves left", "The whole array is cleared"), "This array has fixed slots; deleting resets one slot."),
        ("Which index names the first slot?", "0", ("1", "-1", "The capacity"), "PyDSA numbers array positions starting at zero."),
        ("Can a fixed-size array grow when it is full?", "No, its size stays fixed", ("Yes, it doubles", "Only after sorting", "Only for strings"), "You choose its size when creating it."),
        ("What must match when inserting an array value?", "The array's data type", ("The index's spelling", "The previous value", "The largest value"), "PyDSA checks values against the array's chosen data type."),
    ),
    "stack": (
        ("Which item leaves a stack first?", "The most recently pushed item", ("The oldest item", "The smallest item", "A random item"), "A stack follows last in, first out."),
        ("What does peek do?", "Reads the top without removing it", ("Removes the top", "Clears the stack", "Reads the bottom"), "Peek leaves the stack unchanged."),
        ("Push 4, then 9. What does pop return?", "9", ("4", "Both values", "Nothing"), "The last pushed value sits on top."),
        ("What happens if you push onto a full PyDSA stack?", "The push is refused", ("The bottom disappears", "The capacity doubles", "The top is overwritten"), "The stack's fixed capacity prevents overflow."),
        ("Which task fits a stack?", "Undoing the most recent action", ("Serving people in arrival order", "Looking up words by prefix", "Finding the cheapest route"), "Undo usually reverses the last action first."),
    ),
    "queue": (
        ("Which item leaves a queue first?", "The oldest waiting item", ("The newest item", "The largest item", "The item at the highest slot"), "A queue follows first in, first out."),
        ("Where does enqueue add an item?", "At the rear", ("At the front", "At the smallest value", "At any chosen index"), "Items join behind those already waiting."),
        ("Enqueue 4, then 9. What does dequeue return?", "4", ("9", "Both values", "The rear index"), "The first arrival leaves first."),
        ("Why does a circular queue wrap around?", "To reuse empty slots at the beginning", ("To reverse arrivals", "To sort items", "To increase capacity"), "Its indexes wrap while its logical arrival order stays the same."),
        ("What does peek at the front change?", "Nothing", ("It removes the front", "It advances the rear", "It clears the queue"), "Peek reads the next item without dequeuing it."),
    ),
    "deque": (
        ("Where can a deque add and remove items?", "At both ends", ("Only at the front", "Only at the back", "Only in the middle"), "A deque is a double-ended queue."),
        ("Push 4 at the back, then 9 at the front. What is at the front?", "9", ("4", "Nothing", "Both values"), "Pushing at the front puts the new value before the existing one."),
        ("How can a deque behave like a stack?", "Push and pop at the same end", ("Sort after every push", "Always pop from the opposite end", "Read only the middle"), "Using one end gives last in, first out behavior."),
        ("How can a deque behave like a queue?", "Push at the back and pop at the front", ("Push and pop at the back", "Push and pop at the front", "Never remove items"), "Opposite ends preserve arrival order."),
        ("What does peek_back do?", "Reads the back without removing it", ("Removes the back", "Moves the front", "Reverses the deque"), "Both peek operations leave the deque unchanged."),
    ),
    "linked-list": (
        ("How are linked list items connected?", "Through links between nodes", ("Through array indexes only", "Through hash codes", "Through priorities"), "Each node stores a value and links to other nodes."),
        ("What does the head identify?", "The first node", ("The last node", "The largest value", "The number of nodes"), "The head is where forward traversal begins."),
        ("How do you reach a later position?", "Follow links from earlier nodes", ("Jump directly by arithmetic", "Read a hash bucket", "Rotate the head"), "A linked list walks through links rather than indexing a contiguous array."),
        ("What changes when a new node is inserted at the beginning?", "The head points to the new node", ("Every value is copied", "The list is sorted", "All links are removed"), "The new node becomes the head and links to the previous head."),
        ("What does searching a linked list compare?", "Node values one at a time", ("Only the head's address", "Only node counts", "Hash codes in a table"), "The search follows links and checks each node's value."),
    ),
    "tree": (
        ("What is the root of a tree?", "The top node", ("Every leaf", "The smallest key always", "The last inserted node always"), "Every other node descends from the root."),
        ("Which traversal reads a search tree's keys in sorted order?", "Inorder", ("Preorder", "Postorder", "Level order"), "Inorder visits the left subtree, the node, then the right subtree."),
        ("What is a leaf?", "A node with no children", ("The root of every tree", "A node with two children", "A node's parent"), "Leaves end a branch."),
        ("What does level-order traversal use to visit nodes?", "A queue", ("A hash function", "A sorted set", "A word prefix"), "A queue visits each level before moving to the next."),
        ("Which key can replace a deleted node with two children?", "Its inorder successor", ("Any leaf", "The largest key anywhere", "The number of children"), "The smallest key in the right subtree preserves search order."),
    ),
    "heap": (
        ("What does the heap rule relate?", "A parent and its children", ("Every pair of neighbors in the array", "Only the leaves", "Only the first and last insertion"), "A heap keeps each parent above its children according to its min or max rule."),
        ("What shape does a binary heap keep?", "A complete binary tree", ("A single chain", "Any graph", "A tree with only left children"), "Its levels fill from left to right, except that the last level may be incomplete."),
        ("After adding a heap leaf, how can it move into place?", "Sift up", ("Binary search", "Path compression", "Rehash"), "It swaps with its parent while it belongs above that parent."),
        ("What moves to the root after extraction?", "The last leaf", ("A random node", "The oldest inserted value", "A new default value"), "The last leaf fills the root's gap and then sifts down."),
        ("Is a heap's array always fully sorted?", "No, only the heap rule is guaranteed", ("Yes, always ascending", "Yes, always descending", "Only when it has duplicates"), "The heap rule does not order siblings or unrelated branches."),
    ),
    "priority-queue": (
        ("Which priority number is served first in PyDSA?", "The smallest", ("The largest", "The newest", "The average"), "PyDSA implements its priority queue with a min heap."),
        ("What breaks a tie between equal priorities?", "Arrival order", ("Alphabetical item order", "A random choice", "The item with more letters"), "Equal-priority entries are served first in, first out."),
        ("Does peek remove the next entry?", "No", ("Yes", "Only on a tie", "Only for numbers"), "Peek reports the next item and its priority without removing them."),
        ("What can change which entry is served next?", "Changing an entry's priority", ("Reading its size", "Displaying it", "Checking whether it is empty"), "A priority change can sift an entry to a new heap position."),
        ("Which task fits a priority queue?", "Serving urgent jobs before ordinary jobs", ("Reading text by prefix", "Keeping unique values only", "Walking a circular list"), "Priority queues choose by importance before arrival order."),
    ),
    "trie": (
        ("What do words with a shared prefix share in a trie?", "Their first character nodes", ("Their last node always", "One hash slot", "Their lengths"), "Common initial letters follow the same path."),
        ("What distinguishes a whole word from just a prefix?", "A word-end mark", ("The root's value", "The number of siblings", "Its hash"), "A path may exist without its final node being marked as a stored word."),
        ("Store 'car' and 'card'. Is 'ca' a stored word?", "No, it is only a prefix", ("Yes, every prefix is a word", "Only after searching", "Only after deleting 'car'"), "Only explicitly inserted words have word-end marks."),
        ("Which operation finds words beginning with 'ca'?", "Autocomplete", ("Extract", "Union", "Rotate"), "Autocomplete finds the prefix node and collects words below it."),
        ("When can a deleted word's node be pruned?", "When no remaining word needs it", ("Whenever it has a parent", "Whenever it has children", "Only when it is the root"), "Shared paths must stay for other words."),
    ),
    "graph": (
        ("What does a directed edge mean?", "You can follow it in its stated direction", ("You can always follow it both ways", "Its weight is negative", "It joins a vertex to itself only"), "The reverse edge is a separate connection in a directed graph."),
        ("Which traversal explores level by level?", "BFS", ("DFS", "Inorder", "Heap extraction"), "Breadth-first search uses a queue to explore the nearest unseen vertices first."),
        ("Which traversal follows one branch before backing out?", "DFS", ("BFS", "Radix sort", "Linear probing"), "Depth-first search explores a path and then backtracks."),
        ("What can an edge's weight represent?", "A travel cost or distance", ("The number of vertices always", "The vertex's array index always", "Only the insertion order"), "Weighted edges attach a cost to each connection."),
        ("Why track visited vertices during traversal?", "To avoid revisiting them through cycles", ("To sort their names", "To change edge weights", "To remove all edges"), "A visited record keeps a traversal from looping forever."),
    ),
    "hash-table": (
        ("What does a hash table store?", "Key-value pairs", ("Only ordered numbers", "Only tree nodes", "Only distances"), "A key identifies the value to look up."),
        ("What is a hash collision?", "Different keys have the same home index", ("A key has no value", "Two tables have different sizes", "A lookup succeeds"), "The collision strategy decides how both pairs can be stored."),
        ("What does inserting an existing key do in PyDSA?", "Updates its value", ("Creates an identical second key", "Always raises an error", "Clears its bucket"), "Each key identifies one stored value."),
        ("What does separate chaining use for collisions?", "A list of pairs in the bucket", ("A tree rotation", "The next free slot only", "Path compression"), "Several pairs can share a bucket."),
        ("What does linear probing try after an occupied slot?", "The next slot, wrapping around", ("Only the first slot", "A random bucket", "The previous key's value"), "Probing continues until it finds the key or a free slot."),
    ),
    "hash-set": (
        ("What does a set keep?", "Unique items", ("Every duplicate", "Only sorted items", "Key-value pairs with priorities"), "Adding the same item twice does not add another copy."),
        ("What does union include?", "Items in either set", ("Only shared items", "Only items in the first set", "No items"), "Union combines both sets without duplicates."),
        ("What does intersection include?", "Items in both sets", ("Items in only one set", "Every item in either set", "Only the smallest item"), "Intersection keeps the shared members."),
        ("What does A minus B include?", "Items in A that are not in B", ("Items in B that are not in A", "Every shared item", "The number of items in B"), "Set difference depends on which set comes first."),
        ("When is A a subset of B?", "Every item in A is also in B", ("Only their sizes match", "They have no shared items", "B has fewer items"), "Subset checks membership, not just size."),
    ),
    "disjoint-set": (
        ("What does find return?", "The representative root of an element's group", ("The smallest element always", "Its array capacity", "Every graph edge"), "Elements in the same group lead to the same root."),
        ("What does union do?", "Joins two groups", ("Sorts all members", "Deletes a root", "Splits a group"), "Union connects the roots if the groups are different."),
        ("What does path compression change?", "Parent links point straight at the root", ("The group's members", "The number of elements", "The order of unions"), "It shortens later finds without changing group membership."),
        ("Why use union by rank?", "To avoid unnecessarily tall parent trees", ("To sort member values", "To change element IDs", "To force the smallest root"), "The shorter tree hangs under the taller one."),
        ("What happens when already connected elements are united?", "Their group stays the same", ("A new group appears", "Both are removed", "Their group splits"), "Their roots already match, so there is nothing to join."),
    ),
    "sorting": (
        ("What is ascending order?", "Smallest to largest", ("Largest to smallest", "Insertion order", "Random order"), "Ascending sorting places smaller values before larger ones."),
        ("What does a stable sort preserve?", "The relative order of equal values", ("Every original index", "The original unsorted list", "The largest value's position"), "Equal-key records stay in their earlier relative order."),
        ("What does a comparison count measure?", "How often two values are compared", ("Elapsed milliseconds only", "The list's capacity", "The number of algorithms"), "A work count measures operations independently of machine speed."),
        ("How many writes does one swap count as in PyDSA?", "Two", ("Zero", "One", "Three"), "Each of the two list slots receives a value."),
        ("Why compare sorts on copies of the same list?", "So every sort starts with the same input", ("So no sort uses memory", "So every sort makes the same number of comparisons", "So all results stay unsorted"), "Otherwise an earlier sort could make the later sort's input easier."),
    ),
    "searching": (
        ("What does a successful PyDSA search return?", "An index in the original list", ("Only a sorted-copy index", "The number of matches", "The target's hash"), "Even searches using a sorted copy map the answer back to the original list."),
        ("What result means the target is missing?", "-1", ("0", "1", "The list's last index"), "Valid indexes start at zero; -1 signals that nothing matched."),
        ("Which search works without sorting first?", "Linear search", ("Binary search", "Jump search", "Interpolation search"), "Linear search checks each item in its existing order."),
        ("What does a probe count measure?", "Positions checked during the search", ("Only elapsed time", "The target's value", "Memory addresses"), "Probes show how much of the list the search examined."),
        ("What happens to the original list when PyDSA binary-searches it?", "Its order stays unchanged", ("It is sorted in place", "It is cleared", "Its first item is removed"), "PyDSA searches a sorted copy."),
    ),
    "graph-algorithms": (
        ("Which algorithm finds shortest paths with nonnegative weights?", "Dijkstra", ("Kruskal", "Topological sort", "Counting sort"), "Dijkstra settles the nearest vertex and improves neighboring distances."),
        ("Which graph can have a topological order?", "A directed graph without cycles", ("Any graph with a cycle", "Only an undirected graph", "Only a complete graph"), "A dependency cycle cannot be placed in a valid earlier-to-later order."),
        ("What does a minimum spanning tree minimize?", "Total weight while connecting all vertices", ("Each source-to-target distance", "The number of vertex names", "Only the largest edge"), "It connects the graph as cheaply as possible without cycles."),
        ("What does a spanning algorithm return for a disconnected graph?", "A spanning forest", ("A single connected tree anyway", "A directed cycle", "A sorted array"), "Each connected component gets its own tree."),
        ("Why skip an edge that would close a cycle in a spanning tree?", "Its endpoints are already connected", ("Its weight must be negative", "It has no vertices", "Its names are equal in length"), "The extra connection is unnecessary and would break the tree rule."),
    ),
}

# Variant-specific questions replace one foundation question, keeping each bank at five questions.
VARIANTS = {
    "singly-linked-list": ("linked-list", "How can you move through a singly linked list?", "Forward through next links", ("Backward through previous links", "Only by array index", "Only by hash lookup"), "Each node has a next link, without a previous link."),
    "doubly-linked-list": ("linked-list", "What extra link does a doubly linked node have?", "A previous link", ("A hash bucket", "A priority", "A tree root"), "Previous links allow traversal backward as well as forward."),
    "singly-circular-linked-list": ("linked-list", "Where does the last node's next link lead?", "Back to the head", ("To None", "To the smallest value", "To an array slot"), "The next links form a loop; traversal must know when to stop."),
    "doubly-circular-linked-list": ("linked-list", "Where does the head's previous link lead?", "To the last node", ("To None", "To the second node", "To a hash slot"), "The links wrap in both directions."),
    "bst": ("tree", "Where does a duplicate BST key go in PyDSA?", "Into the right subtree", ("Into the left subtree", "It is always rejected", "It replaces the root"), "BST insertion takes the right branch when the key is not smaller."),
    "avl-tree": ("tree", "What balance does an AVL tree maintain?", "Child subtree heights differ by at most one", ("All leaves have identical depths", "Every key is unique", "The root is always the smallest key"), "Rotations restore this balance after updates."),
    "min-heap": ("heap", "Which value sits at a min heap's root?", "The smallest", ("The largest", "The oldest", "The most recent"), "Every parent is no larger than its children."),
    "max-heap": ("heap", "Which value sits at a max heap's root?", "The largest", ("The smallest", "The oldest", "The most recent"), "Every parent is no smaller than its children."),
    "adjacency-matrix-graph": ("graph", "What does a zero matrix cell mean in PyDSA?", "No edge", ("An edge of zero cost", "A visited vertex", "A deleted graph"), "This matrix implementation reserves zero for absent edges."),
    "adjacency-list-graph": ("graph", "What does each adjacency list entry hold?", "A neighbor and its weight", ("Only a matrix row number", "A tree parent", "A word prefix"), "Each vertex lists its outgoing weighted edges."),
    "chaining-hash-table": ("hash-table", "Can a chaining bucket hold more than one pair?", "Yes, colliding keys share its list", ("No, only one pair fits", "Only when keys are equal", "Only after deletion"), "Separate chaining stores multiple distinct pairs in one bucket."),
    "linear-probing-hash-table": ("hash-table", "Why rehash a cluster after deleting a probing key?", "So a gap does not hide later keys", ("To alphabetize values", "To increase every hash", "To remove all collisions forever"), "A lookup stops at an empty slot, so later colliding keys must be placed where they remain reachable."),
}

ALGORITHM_DETAILS = {
    "bubble-sort": ("sorting", "What does a bubble pass compare?", "Adjacent values", ("Only the first and last", "Only every third value", "Hash codes"), "Out-of-order neighbors swap; a value moves toward its final end."),
    "selection-sort": ("sorting", "What does selection sort choose next?", "The next smallest or largest remaining value", ("A random pivot", "An empty slot", "A word prefix"), "It scans the unsorted part and places the next value in order."),
    "insertion-sort": ("sorting", "Where does insertion sort put the next value?", "Into its place in the sorted prefix", ("Into a hash bucket", "At the root of a trie", "Into a random position"), "Earlier values shift to make room."),
    "quick-sort": ("sorting", "What does quicksort partition around?", "A pivot", ("A graph root", "A word prefix", "A set union"), "Partitioning separates values that belong before and after the pivot."),
    "heap-sort": ("sorting", "What helps heap sort select its next value?", "The heap root", ("The oldest insertion", "A word prefix", "A random vertex"), "The heap rule puts the next extreme value at the root."),
    "shell-sort": ("sorting", "How does Shell sort compare positions at first?", "Using a gap larger than one", ("Using only equal keys", "Using a hash table", "Using no comparisons"), "Its gaps shrink until a final adjacent insertion pass."),
    "merge-sort": ("sorting", "What does merge sort combine?", "Two sorted halves", ("Two hash codes", "Only the largest values", "Only duplicate keys"), "It repeatedly takes the next front value from the appropriate half."),
    "counting-sort": ("sorting", "Which inputs fit counting sort in PyDSA?", "Integers within a limited range", ("Any words", "Any decimals", "Any range of integers without a limit"), "It allocates a counter for each value between the smallest and largest."),
    "radix-sort": ("sorting", "Which values can PyDSA radix sort handle?", "Nonnegative integers", ("Any negative integers", "Any words", "Any decimals"), "It groups numbers by successive decimal digits."),
    "linear-search": ("searching", "How does linear search move?", "One position at a time", ("By halving a range", "By tree rotations", "By hash collisions"), "It compares each value until it finds a match or reaches the end."),
    "binary-search": ("searching", "How does binary search narrow its range?", "By checking the middle", ("By checking every value", "By counting digits", "By scanning graph edges"), "The middle comparison rules out one half."),
    "jump-search": ("searching", "What follows a jump that passes the target?", "A linear scan of the candidate block", ("A tree rotation", "A set union", "A full reverse sort"), "The target, if present, is between the previous and current block boundaries."),
    "interpolation-search": ("searching", "What helps interpolation search estimate a position?", "The target and boundary values", ("Only the list length", "A random choice", "The number of letters in a word"), "It uses numeric distances between values, so it requires numbers."),
    "exponential-search": ("searching", "How does exponential search expand its bound?", "It doubles the bound", ("It always adds one", "It decreases the bound", "It uses hash codes"), "After finding a bound it binary-searches the remaining range."),
    "dijkstra": ("graph-algorithms", "Which weights does Dijkstra reject?", "Negative weights", ("Positive weights", "All equal weights", "Large weights"), "A negative edge can improve a vertex after its distance was treated as final."),
    "topological-sort": ("graph-algorithms", "Which vertex can Kahn's algorithm place next?", "One with no remaining incoming edges", ("One with the largest weight", "One on a cycle", "Only vertex zero"), "It has no unresolved dependencies."),
    "cycle-detection": ("graph-algorithms", "Which directed DFS edge reveals a cycle?", "An edge back into the current path", ("Every edge to a finished vertex", "Every outgoing edge", "Only the lightest edge"), "A return to a vertex still on the path closes a directed loop."),
    "prim": ("graph-algorithms", "Which edge does Prim choose?", "The cheapest edge from its tree to an unseen vertex", ("The heaviest edge", "Any edge between visited vertices", "Only an edge from vertex zero"), "Prim grows a tree across its boundary."),
    "kruskal": ("graph-algorithms", "In what order does Kruskal consider edges?", "By increasing weight", ("By decreasing weight", "Only by arrival order", "Only by vertex name"), "It accepts the next cheapest edge that joins different components."),
}


def _questions():
    for topic, rows in BANKS.items():
        for number, (prompt, correct, others, explanation) in enumerate(rows, 1):
            yield Question(f"{topic}-{number}", topic, prompt, (correct, *others), 0, explanation)
    for topic, (parent, prompt, correct, others, explanation) in {**VARIANTS, **ALGORITHM_DETAILS}.items():
        rows = (*BANKS[parent][:4], (prompt, correct, others, explanation))
        for number, (prompt, correct, others, explanation) in enumerate(rows, 1):
            yield Question(f"{topic}-{number}", topic, prompt, (correct, *others), 0, explanation)


QUESTIONS = tuple(_questions())


def for_topic(topic):
    return tuple(question for question in QUESTIONS if question.topic == topic)
