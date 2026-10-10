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

BANKS.update({
    "lru-cache": (
        ("Which key is evicted from a full LRU cache?", "The least recently used key", ("The smallest key", "The most recently used key", "A random key"), "The list's tail is the entry used least recently."),
        ("What happens after a successful Get?", "The key becomes most recent", ("The key is deleted", "The capacity doubles", "Every other value changes"), "A hit moves its known node to the head."),
        ("Does replacing an existing key evict another key?", "No, it reuses the same entry", ("Yes, always", "Only the head is evicted", "The whole cache is cleared"), "Replacement does not increase the number of entries."),
        ("What does the cache's chaining table map keys to?", "Doubly linked nodes", ("Sorted indexes", "Bloom bits", "Graph edges"), "The known node can be moved without searching the recency list."),
        ("What does a missing Get do to recency?", "Leaves it unchanged", ("Evicts the tail", "Reverses the list", "Inserts a placeholder"), "Only a successful Get or a Put marks a key recent."),
    ),
    "skip-list": (
        ("Which lane contains every skip-list key?", "Level 1", ("Only the highest lane", "Level 0 in PyDSA", "No lane"), "Higher lanes are subsets of the sorted base lane."),
        ("What makes a node join another lane in PyDSA?", "Heads on a seeded fair coin", ("A rotation", "A hash collision", "Always being the largest key"), "Promotion repeats until tails or the level cap."),
        ("How does a skip-list search move?", "Right, then down", ("Only left", "Only upward", "In random directions"), "It takes useful express links before descending to a finer lane."),
        ("What fraction of nodes is expected to reach level 3?", "About one quarter", ("Every node", "About one half", "About three quarters"), "Reaching level 3 needs two heads in a row."),
        ("What does Delete remove when duplicate keys exist?", "One occurrence", ("All occurrences", "Every upper lane", "Only the head sentinel"), "Each inserted key has its own node and deletion unlinks one matching node."),
    ),
    "bloom-filter": (
        ("What does a Bloom filter's positive answer mean?", "The item might be present", ("The item is certainly present", "The item is certainly absent", "The filter stores its value"), "Other items can set all the same bits, producing a false positive."),
        ("What proves that an item is absent?", "At least one checked bit is zero", ("Every checked bit is one", "The array has any zero bit", "The string is long"), "An added item always has all its selected bits set."),
        ("Can adding items cause a false negative?", "No, adding never clears bits", ("Yes, on every collision", "Only after repeated adds", "Only for empty strings"), "Once added, an item's positions remain set."),
        ("Why does PyDSA use salted SHA-256 rather than Python's string hash?", "To keep positions stable between runs", ("To prove membership", "To eliminate collisions", "To sort the bits"), "Fixed numbered salts and UTF-8 encoding produce deterministic positions."),
        ("Why is ordinary deletion unsupported?", "Clearing shared bits could hide another item", ("Strings cannot be hashed", "Bits cannot change", "Hashes always give distinct positions"), "A bit may belong to several added items, so clearing it risks a false negative."),
    ),
    "segment-tree": (
        ("What does a segment-tree node describe?", "An array range and its aggregate", ("A sorted key and its color", "A hash bucket", "A graph edge"), "Each node summarizes a contiguous array range."),
        ("Which node can answer a whole-array query immediately?", "The root", ("Only the last leaf", "Every leaf must be visited", "An outside node"), "The root stores the aggregate for the whole array."),
        ("What should a query do with a partly overlapping node?", "Query both children", ("Use its whole answer", "Ignore it entirely", "Replace its value"), "Only the covered parts of its children may contribute."),
        ("After replacing one value, which nodes must be recomputed?", "Its leaf and ancestors", ("Every node in the tree", "Only unrelated leaves", "No nodes"), "Only those ranges contain the changed array position."),
        ("Which range operations can you choose in PyDSA?", "Sum, minimum or maximum", ("Only sorting", "Only a prefix count", "Word completion"), "The chosen operation is used consistently when building, updating and querying."),
    ),
    "fenwick-tree": (
        ("What determines the length of internal block i?", "Its lowest set bit, i & -i", ("The array's largest value", "Its number of children", "The hash of i"), "The lowest set bit gives the number of values summed by that block."),
        ("What jump does a prefix query make?", "Subtract the lowest set bit", ("Add the lowest set bit", "Always add one", "Double the sum"), "Removing that bit moves to the next non-overlapping block before the current one."),
        ("How does a Fenwick tree find a range sum?", "Subtract two prefix sums", ("Subtract two prefix minima", "Sort the array first", "Read only one endpoint"), "Sum through the end, then subtract the prefix before the start."),
        ("Which indexes does PyDSA use for its internal Fenwick blocks?", "One-based indexes", ("Zero-based indexes", "Negative indexes only", "Sorted keys"), "Public array positions start at 0, while the block table starts at 1."),
        ("What is added to affected blocks during a point replacement?", "The new value minus the old value", ("The entire new value every time", "The index", "The block's length"), "Adding the difference replaces the contribution without counting the old value twice."),
    ),
    "red-black-tree": (
        ("What color must a nonempty Red-Black tree's root have?", "Black", ("Red", "Either color", "No color"), "Fix-up finishes by making the root black."),
        ("Which child is forbidden under a red node?", "A red child", ("A black child", "An absent child", "A smaller key"), "Two consecutive red nodes break a balancing rule."),
        ("How are absent leaves treated when counting black height?", "As black", ("As red", "As stored keys", "As rotations"), "Every missing child contributes one black leaf to its path."),
        ("What can repair a Red-Black tree after an update?", "Recoloring and rotations", ("Sorting every key again", "Hashing the root", "Discarding duplicate keys"), "These local changes restore the color rules while keeping search order."),
        ("What does deleting a duplicate key remove in PyDSA?", "One occurrence", ("All occurrences", "The whole tree", "Only red occurrences"), "Each insertion adds one node and each successful deletion removes one node."),
    ),
    "b-tree": (
        ("With minimum degree t, how many keys can one B-tree node hold at most?", "2t − 1", ("t − 1", "t", "2t + 1"), "A full node has 2t minus one keys and can have 2t children."),
        ("What must be equal for all B-tree leaves?", "Their depth", ("Their keys", "Their colors", "Their number of siblings"), "Splits and deletion repairs preserve the common leaf level."),
        ("What happens before insertion enters a full child?", "The child splits and its middle key moves up", ("The tree loses its root", "Every key is rehashed", "The child is ignored"), "Splitting leaves space in the child chosen next."),
        ("What can give a minimum-size child enough keys before deletion descends?", "Borrowing from a sibling or merging", ("Painting it red", "Increasing every key", "Removing every child"), "A separator moves through the parent, or two siblings join around it."),
        ("How many children does an internal node with k keys have?", "k + 1", ("k", "Always two", "2k + 1"), "The keys separate one more child range than there are keys."),
    ),
})


BANKS.update({
    "bellman-ford": (
        ("Which weights can Bellman-Ford accept?", "Negative and non-negative weights", ("Only positive weights", "Only zero weights", "No edge weights"), "Repeated relaxation handles negative edges unless a reachable negative cycle prevents a minimum."),
        ("How many ordinary passes can Bellman-Ford need?", "At most V minus one", ("Exactly one", "V squared", "One per possible path"), "A simple path visits at most V vertices and uses at most V minus one edges."),
        ("What does a pass with no improvements allow?", "Stopping early", ("Reversing all edges", "Deleting the source", "Declaring every vertex unreachable"), "No further pass can improve a distance when a complete pass changed nothing."),
        ("What does an improvement in the extra pass mean?", "A negative cycle is reachable from the source", ("Every edge is negative", "A positive cycle exists", "The source is missing"), "Without a reachable negative cycle, V minus one passes cover the shortest simple paths."),
        ("Does a disconnected negative cycle affect this source?", "No, unless the source can reach it", ("Always", "Only if it has three vertices", "Only in a matrix graph"), "Relaxation cannot enter a region whose distance stays infinity."),
    ),
    "floyd-warshall": (
        ("What does Floyd-Warshall calculate?", "Shortest distances between every pair", ("Only one source distance", "A spanning tree", "A topological ordering"), "A row and column identify each source and target pair."),
        ("What does the outer vertex k represent?", "An allowed intermediate stop", ("The edge count", "The largest distance", "A wall"), "Each pass considers routes through the next intermediate vertex."),
        ("Which two distances form a candidate through k?", "Distance from u to k plus k to v", ("u to v minus k to v", "Only the direct edge", "The diagonal alone"), "The candidate connects the route into k with the route out of k."),
        ("Which matrix entry reveals a negative cycle?", "A negative diagonal entry", ("Any infinity entry", "Any positive entry", "A zero diagonal"), "A negative route from a vertex back to itself can be repeated indefinitely."),
        ("What information reconstructs a path in PyDSA?", "The next hop toward each target", ("Only the vertex count", "A sorted edge list", "Only diagonal entries"), "Follow next hops until the chosen target is reached."),
    ),
    "a-star": (
        ("What is A*'s priority?", "Distance traveled plus estimated distance remaining", ("Distance traveled only", "Wall count only", "Arrival time only"), "Priority combines the known route cost with a safe estimate of what remains."),
        ("What is Manhattan distance on this grid?", "Absolute row difference plus absolute column difference", ("Only row difference", "Number of walls", "Diagonal distance rounded down"), "Four-direction moves must cover both coordinate differences."),
        ("Which heuristic turns A* into Dijkstra?", "Zero everywhere", ("Twice the actual distance", "The wall count", "A negative estimate"), "With no estimate, priority equals distance traveled."),
        ("What does an empty frontier before reaching the goal mean?", "The goal is unreachable", ("The path has zero moves", "Every wall should be removed", "The grid is sorted"), "No discovered route has an unexplored next cell."),
        ("Does A* always expand strictly fewer cells than Dijkstra?", "No, walls and ties affect the saving", ("Yes, on every grid", "Only if start equals goal", "It never expands cells"), "A good estimate can save work, but strict savings are not guaranteed."),
    ),
})

BANKS.update({
    "string-algorithms": (
        ("What does an exact string search return in PyDSA?", "Every matching start position", ("Only the last match", "Only the text length", "A sorted text"), "All occurrences are reported by zero-based starting index."),
        ("Where does aa occur in aaaa?", "At indexes 0, 1 and 2", ("Only index 0", "At indexes 1 and 3", "Nowhere"), "Occurrences can overlap, so a match does not skip the next starting position."),
        ("Where does an empty pattern match?", "At every boundary, including the end", ("Nowhere", "Only before the first character", "Only in empty text"), "An empty sequence fits between any two characters and at either end."),
        ("What if the pattern is longer than the text?", "There are no matches", ("The text is repeated", "The pattern is shortened", "The first index always matches"), "No alignment has room for the whole pattern."),
        ("What does the comparison table include for KMP?", "Search and prefix-table character comparisons", ("Only the text length", "Only hash updates", "Only successful matches"), "Preprocessing is real work and is shown separately before the total."),
    ),
    "naive-string-search": (
        ("How far does naive search shift after each alignment?", "One character", ("The pattern length", "Half the text", "A random distance"), "One-character shifts preserve overlapping matches."),
        ("When can an alignment stop checking characters?", "At its first mismatch", ("Only at the end of the text", "After sorting", "Only after a hash hit"), "A single unequal character already rules out that alignment."),
        ("What extra preprocessing does naive search require?", "None", ("A prefix table", "A rolling hash", "A sorted pattern"), "It compares the original characters directly."),
        ("Which input can make naive search repeat much work?", "Long shared prefixes followed by a mismatch", ("An empty pattern only", "A longer pattern with no alignment", "Always-distinct first characters"), "It checks those prefixes again at many starts."),
        ("How many starts can fit a length-3 pattern in length-5 text?", "Three", ("Two", "Five", "Eight"), "The possible starts are 0, 1 and 2."),
    ),
    "kmp": (
        ("What does a KMP prefix entry store?", "Longest proper prefix that is also a suffix", ("A hash of the text", "The next character code", "The number of full matches"), "The entry measures a reusable border of the pattern prefix ending there."),
        ("What is the prefix table for abab?", "[0, 0, 1, 2]", ("[1, 2, 3, 4]", "[0, 0, 0, 0]", "[0, 1, 2, 3]"), "The final ab is also the opening ab; a whole prefix cannot count as its own proper prefix."),
        ("After a mismatch with j matched characters, what does KMP use?", "The entry at j minus one", ("A random starting index", "The largest text character", "The hash modulus"), "That earlier border gives a shorter prefix already known to match."),
        ("Does KMP move its text cursor backward?", "No", ("After every mismatch", "After every match", "Only for spaces"), "The pattern moves while the text cursor stays in place or advances."),
        ("Why reuse the final prefix entry after a full match?", "To find overlapping matches", ("To remove duplicates from the text", "To sort results", "To avoid counting preprocessing"), "A suffix of one match can be the prefix of the next."),
    ),
    "rabin-karp": (
        ("Does an equal window hash prove a character match?", "No, it needs verification", ("Always", "Only with modulus 2", "Only for overlapping windows"), "Different strings can have equal hashes."),
        ("What is a spurious hit?", "Equal hashes but unequal characters", ("A real overlapping match", "An empty pattern", "A prefix-table entry"), "Verification catches a collision before it becomes a reported match."),
        ("What makes hash collisions easier to demonstrate?", "A small modulus", ("Removing verification", "Sorting the text", "An empty text only"), "Fewer possible hashes make different windows share values more often."),
        ("What does a rolling update remove first?", "The outgoing character's weighted contribution", ("The whole pattern", "The last match index", "Every text character"), "It reuses the previous hash instead of hashing the whole next window again."),
        ("Do zero character comparisons mean the algorithm did no work?", "No, hashing still took work", ("Yes", "Only if KMP was also run", "Only for Unicode"), "Hash construction and rolling arithmetic are excluded from the character-comparison table."),
    ),
})

BANKS.update({
    'dynamic-programming': (
        ('What makes dynamic programming useful?', 'Repeated subproblems',
         ('Only sorted keys', 'Only tree rotations', 'No dependencies'),
         'Saved answers avoid solving repeated states again.'),
        ('What does memoization save?', 'Previously computed answers',
         ('Only input indexes', 'Only branch names', 'Only random seeds'),
         'A later call can reuse the answer for the same state.'),
        ('What order must a table follow?', 'Dependencies before their users',
         ('Always reverse alphabetic order', 'Always random order', 'Only largest states first'),
         'Each recurrence needs earlier answers to be available.'),
        ('Why trace backward through a table?', 'To rebuild the selected choices',
         ('To sort every row', 'To remove all base cases', 'To add more capacity'),
         'A score alone does not identify the chosen items or characters.'),
        ('Does every recursive problem benefit from memoization?', 'No, states must repeat to save work',
         ('Yes, always', 'Only if it has strings', 'Only if it has no base case'),
         'Caching disjoint subproblems can add overhead without avoiding calculations.'),
    ),
    'fibonacci': (
        ('What is F(0)?', '0', ('1', '2', 'Undefined'), 'PyDSA uses zero and one as the first two base values.'),
        ('How is F(n) computed for n at least 2?', 'F(n - 1) + F(n - 2)',
         ('F(n - 1) times n', 'n squared', 'F(n - 1) - F(n - 2)'),
         'Each later Fibonacci value adds the two preceding values.'),
        ('Why is plain recursion slow?', 'It repeats the same subproblems',
         ('It sorts the input', 'It never reaches a base case', 'It uses no function calls'),
         'Many branches ask for the same smaller Fibonacci numbers.'),
        ('Does a memo cache hit count as a call?', 'Yes', ('No', 'Only for n = 0', 'Only if the cache is empty'),
         'The function is entered even when it immediately returns a saved answer.'),
        ('How many function calls does the table method count?', 'One',
         ('Exactly n squared', 'Exactly two per entry', 'Zero'),
         'Loop iterations are counted separately as computed states.'),
    ),
    'knapsack': (
        ('What does 0/1 mean?', 'Take an item once or leave it out',
         ('Only one item may exist', 'Every weight must be one', 'Items can be split'),
         'Each input item is a separate whole-item choice.'),
        ('Why use the previous row when taking an item?', 'To prevent reusing that item',
         ('To sort the weights', 'To count coins', 'To increase capacity'),
         'The previous row only allows earlier items.'),
        ('What does a column represent?', 'Available capacity',
         ('A character index', 'A peg name', 'A queen diagonal'),
         'Each column solves the selection problem under that weight limit.'),
        ('What does traceback do on an equal-value tie?', 'Skip the current item',
         ('Take every item', 'Split the item', 'Restart the table'),
         'PyDSA prefers the previous row when either choice gives the same value.'),
        ('What value does an empty item list give?', 'Zero', ('The capacity', 'Negative one', 'An error'),
         'No selected items means no total value.'),
    ),
    'longest-common-subsequence': (
        ('Must subsequence characters be adjacent?', 'No, only their order must stay the same',
         ('Yes, always', 'Only when they repeat', 'They must be sorted'), 'Gaps are permitted in a subsequence.'),
        ('Which arrow is used when characters match?', 'Diagonal', ('Up only', 'Left only', 'Down'),
         'A match extends the best answer for the preceding two prefixes.'),
        ('Which way does PyDSA move on a mismatch tie?', 'Up', ('Down', 'Always diagonal', 'Randomly'),
         'A consistent tie rule rebuilds one valid longest answer.'),
        ('Why reverse collected traceback characters?', 'They were collected from the end',
         ('To alphabetize them', 'To remove gaps', 'To change the length'),
         'Traceback visits the last selected character first.'),
        ('What LCS length does an empty string give?', 'Zero', ('One', "The other string's length", 'Undefined'),
         'An empty sequence cannot supply a character.'),
    ),
    'coin-change': (
        ('Can a denomination be used more than once?', 'Yes, supplies are unlimited',
         ('No, only once', 'Only denomination one', 'Only the largest'),
         'This coin-change model permits unlimited reuse.'),
        ('How many ways make amount zero?', 'One empty combination', ('Zero', 'Two', 'One per denomination'),
         'Choosing no coins is one valid way to pay zero.'),
        ('Are 1 + 3 and 3 + 1 different ways?', 'No, order is ignored',
         ('Yes, always', 'Only for target four', 'Only with duplicate denominations'),
         'The ways table counts combinations, not ordered sequences.'),
        ('Why can largest-coin-first fail for [1, 3, 4] and target 6?', '3 + 3 uses fewer coins than 4 + 1 + 1',
         ('Four cannot be used', 'One is forbidden', 'Six has no solution'),
         'The dynamic program compares every possible last denomination.'),
        ('What happens to duplicate denominations?', 'They merge into one denomination',
         ('They double every answer', 'They become negative', 'They make the target invalid'),
         'Equal coin values do not represent different kinds of coins.'),
    ),
    'recursion-backtracking': (
        ('What ends a recursive branch?', 'A base case', ('A color change', 'A hash collision', 'A larger input'),
         'The base case returns without making smaller recursive calls.'),
        ('What must a recursive call make progress toward?', 'Its base case',
         ('An infinite loop', 'A bigger board', 'More unused input forever'),
         'Progress ensures the branch eventually finishes.'),
        ('What follows exploring a backtracking choice?', 'Undo that choice',
         ('Keep all its marks forever', 'Delete every answer', 'Shuffle unrelated data'),
         'Sibling branches need the state from before the choice.'),
        ('What is pruning?', 'Rejecting branches that cannot succeed',
         ('Deleting valid answers', 'Sorting all choices', 'Removing the base case'),
         'Constraints can rule out a branch before exploring it.'),
        ('Why cap demonstration sizes?', 'Branching can grow very quickly',
         ('Recursion only accepts odd inputs', 'Every board has one solution', 'Function calls cannot be counted'),
         'Readable playback and bounded work need small examples.'),
    ),
    'tower-of-hanoi': (
        ('Which disk can be moved from a peg?', 'Only the top disk',
         ('Only the bottom disk', 'Any disk', 'Only the largest disk'),
         'Disks below another disk cannot be picked up directly.'),
        ('Can a larger disk sit above a smaller disk?', 'No', ('Yes', 'Only on peg B', 'Only on the last move'),
         'The disk order must remain valid after every move.'),
        ('How many moves do three disks need?', '7', ('3', '6', '9'), 'The recurrence gives two cubed minus one.'),
        ('What happens before moving the largest disk?', 'Move the smaller tower to the spare peg',
         ('Move every disk together', 'Delete a disk', 'Swap peg names only'),
         "The largest disk must become the source peg's top disk."),
        ('How many moves do zero disks need?', '0', ('1', '2', 'An infinite number'),
         'An empty tower is the recursive base case.'),
    ),
    'permutations': (
        ('How many arrangements do three distinct items have?', '6', ('3', '9', '8'),
         'There are three choices, then two, then one.'),
        ('When is a prefix a complete permutation?', 'When every input position is used',
         ('After the first choice', 'When it is sorted', 'Only when values repeat'),
         'A complete arrangement has all positions exactly once.'),
        ('What follows returning from a branch?', 'Remove its choice and mark it unused',
         ('Leave it used forever', 'Sort every answer', 'Discard sibling branches'),
         'Undo restores the state needed to try the next position.'),
        ('Can equal input values produce duplicate outputs?', 'Yes, their positions are distinct',
         ('No, outputs are always unique', 'Only with empty input', 'Only when sorted'),
         'PyDSA follows the positional behavior of itertools.permutations.'),
        ('How many permutations does empty input have?', 'One empty permutation', ('Zero', 'Two', 'An error'),
         'There is one way to arrange zero positions.'),
    ),
    'n-queens': (
        ('Which shared lines make queens attack?', 'Rows, columns and diagonals',
         ('Only rows', 'Only columns', 'Only adjacent squares'), 'A queen attacks along all three kinds of lines.'),
        ('Why place queens row by row?', 'To ensure at most one queen in each row',
         ('To avoid every diagonal automatically', 'To sort queens', 'To force one solution'),
         'Column and diagonal sets then handle the remaining constraints.'),
        ('What must be cleared during backtracking?', 'The queen and its column and diagonal marks',
         ('Only the solution count', 'All earlier rows', 'The board size'),
         'Leaving stale marks would wrongly reject later choices.'),
        ('How many solutions does a four-by-four board have?', '2', ('1', '4', '0'),
         'Both arrangements are counted, including their symmetry.'),
        ('Which positive board sizes have no solutions?', '2 and 3', ('1 and 4', '4 and 5', '7 and 8'),
         'The small boards cannot keep every queen off shared lines.'),
    ),
})

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
