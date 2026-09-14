# Which Data Structure Should I Use?
> Start from what you need to do with your data, then pick the structure that makes that operation easy. Every suggestion names its topic ID, so you can also open it with pydsa --topic followed by the ID.

## Keep items in the order they arrive
- Undo history, or going back the way you came: a Stack (`stack`), because the newest item is always the first one out.
- Tasks handled in the order they arrive: a Queue (`queue`), because the oldest item is always the first one out.
- Adding and removing at both ends, like a history with a size limit: a Deque (`deque`).
- Players taking turns, or a playlist that repeats: a Singly Circular Linked List (`singly-circular-linked-list`), because the last item leads back to the first.

## Reach items by position
- Reading and writing values by their position when the size stays the same: an Array (`array`).
- Inserting and removing in the middle of a sequence you walk through anyway: a Doubly Linked List (`doubly-linked-list`), because unlinking a node doesn't move any other node.

## Look items up quickly
- Finding a value by its key, like a word's definition in a dictionary: a Hash Table (`hash-table`).
- Checking whether you've already seen an item, or removing duplicates: a Hash Set (`hash-set`).
- Finding every word that starts with a few letters, as autocomplete does: a Trie (`trie`).

## Keep items sorted
- A sorted collection you keep adding to and removing from, with quick searches: an AVL Tree (`avl-tree`), because it stays balanced whatever order the keys arrive in.
- Sorting a list once, then searching it many times: Merge Sort (`merge-sort`) or Quick Sort (`quick-sort`), followed by Binary Search (`binary-search`).

## Get the most important item next
- Always taking the smallest or the largest item: a Min Heap (`min-heap`) or a Max Heap (`max-heap`).
- Serving items by priority, with ties served in arrival order: a Priority Queue (`priority-queue`).

## Model connections
- Places and routes, friendships or any other network: a graph stored as an Adjacency List (`adjacency-list-graph`) when most vertices have few neighbors, or as an Adjacency Matrix (`adjacency-matrix-graph`) when most pairs of vertices are connected.
- The shortest route between places: Dijkstra's Algorithm (`dijkstra`).
- Tasks that depend on other tasks: a Topological Sort (`topological-sort`).
- Connecting everything as cheaply as possible: Prim's Algorithm (`prim`) or Kruskal's Algorithm (`kruskal`).
- Tracking which items end up in the same group as connections are added: a Disjoint Set (`disjoint-set`).

## Still not sure?
Ask yourself which operation will happen most often: adding items, removing them, reaching them by position, finding them by key, or getting the smallest one. The structure that makes that operation quick is usually the right choice, and every topic's complexity table shows you how quick each of its operations is.
