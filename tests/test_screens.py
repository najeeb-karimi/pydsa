"""Screen flows: scripted console sessions that walk through every menu and exit cleanly."""

import pytest

from pydsa import __version__, app


@pytest.fixture
def play(monkeypatch, capsys):
    """Run the whole app with scripted answers and return everything it printed."""

    def run_session(*answers):
        remaining = iter(answers)

        def scripted_input(prompt=""):
            print(prompt, end="")
            try:
                return next(remaining)
            except StopIteration:
                raise AssertionError("The app asked for more input than the script provides") from None

        monkeypatch.setattr("builtins.input", scripted_input)
        app.run()
        assert list(remaining) == [], "The app exited before using every scripted answer"
        return capsys.readouterr().out

    return run_session


def test_home_navigation(play):
    out = play("7", "1", "0", "2", "9", "0", "0")
    assert f"⏳ Version {__version__}" in out
    assert out.count("🚫 Invalid choice.") == 2
    assert "🧭 Which non-linear data structure" in out
    assert "Goodbye!" in out


def test_array(play):
    out = play(
        "1", "1", "1", "0", "2",  # Linear > Array > Create > back to the choices > Use the example
        "1",  # Definition
        "2", "1", "abc", "42", "9",  # Insert one item: an invalid int, then an index out of bounds
        "2", "1", "7", "0",
        "2", "2", "5", "4", "3", "2", "1",  # Fill the whole array
        "3", "1",  # Delete
        "4", "0",  # Get by index
        "5", "1", "1",  # Bubble sort, ascending
        "6", "2", "3",  # Binary search
        "6", "1", "99",  # Linear search
        "7", "8", "9",  # Size, data type, display
        "5", "0",  # Sort menu, then back
        "10", "1", "2", "x", "0", "2",  # New Array: a str array after two invalid sizes
        "2", "1", "hi", "1",
        "11", "0",  # New Data Structure, then exit
    )
    assert "⏱️ Array operations" in out
    assert "'abc' isn't a valid int." in out
    assert "Index 9 is out of bounds. Valid indexes are 0 to 4." in out
    assert "Inserted 7 at index 0." in out
    assert "Deleted 4 from index 1, which now holds 0 again." in out
    assert "Index 0 holds 5." in out
    assert "How Bubble Sort Works" in out
    assert "Sorted the array in ascending order in" in out
    assert "Found 3 at index 3." in out
    assert "99 isn't in the array." in out
    assert "The array has 5 elements." in out
    assert "The array holds int values." in out
    assert "The size must be a whole number." in out
    assert "The size must be at least 1." in out
    assert "Inserted 'hi' at index 1." in out


def test_stack(play):
    out = play(
        "1", "2", "1", "2",  # Linear > Stack > Create with room for 2 items
        "3", "4", "5",  # Pop, peek and check if empty on an empty stack
        "2", "12", "2",  # Push 12 as a str
        "2", "Messi",
        "2", "7", "1",  # Push 7 as an int: the stack is full
        "4", "6", "7", "8", "3",
        "9", "2",  # New Stack with the example
        "10", "0",
    )
    assert "The stack is empty, so there's nothing to pop." in out
    assert "The stack is empty, so there's nothing to peek at." in out
    assert "Is the stack empty? Yes." in out
    assert "Pushed '12' onto the stack." in out
    assert "The stack is full, so 7 wasn't pushed." in out
    assert "The top item is 'Messi'." in out
    assert "Is the stack full? Yes." in out
    assert "The stack holds 2 of 2 items." in out
    assert "Popped 'Messi' from the top." in out
    assert "Loaded the example stack." in out


def test_queue(play):
    out = play(
        "1", "3", "1", "2",  # Linear > Queue > Create with room for 2 items
        "2", "a", "2", "b", "2", "c",  # The third enqueue doesn't fit
        "3",
        "2", "d",  # Wraps around into slot 0
        "4", "5", "6", "7", "8", "9",
        "3", "3", "3",  # The last dequeue finds the queue empty
        "9", "0",
    )
    assert "The queue is full, so 'c' wasn't enqueued." in out
    assert "Dequeued 'a' from the front." in out
    assert "The front item is 'b'." in out
    assert "The rear item is 'd'." in out
    assert "Is the queue full? Yes." in out
    assert "The queue holds 2 of 2 items." in out
    assert "The queue is empty, so there's nothing to dequeue." in out
    assert "Struck-out items" in out


def test_deque(play):
    out = play(
        "1", "4", "1", "2",  # Linear > Deque > Create with room for 2 items
        "4", "6", "8",  # Pop front, peek front and check if empty on an empty deque
        "2", "a",  # Push 'a' onto the front
        "3", "7", "1",  # Push 7 onto the back as an int
        "3", "x",  # The deque is full
        "6", "7", "9", "10", "11",
        "5", "4",  # Pop back, then pop front
        "12", "2",  # New Deque with the example
        "13", "0",
    )
    assert "The deque is empty, so there's nothing to pop." in out
    assert "The deque is empty, so there's nothing to peek at." in out
    assert "Is the deque empty? Yes." in out
    assert "Pushed 'a' onto the front." in out
    assert "Pushed 7 onto the back." in out
    assert "The deque is full, so 'x' wasn't pushed." in out
    assert "The front item is 'a'." in out
    assert "The back item is 7." in out
    assert "Is the deque full? Yes." in out
    assert "The deque holds 2 of 2 items." in out
    assert "Popped 7 from the back." in out
    assert "Popped 'a' from the front." in out
    assert "Pushing 2.5 onto the front wrapped it around to the last slot." in out


def test_linked_lists(play):
    out = play(
        "1", "5", "1", "1",  # Linear > Linked List > Singly > Start empty
        "5", "9",  # Delete from and display an empty list
        "2", "2", "x", "10",  # Insert at beginning: an invalid int, then 10
        "4", "1", "b",  # Insert at end
        "3", "1", "3", "2.5",  # Insert at position 1
        "3", "9", "1", "z",  # Position out of bounds
        "8", "1", "b", "8", "2", "99",  # Search
        "6", "5", "6", "0", "7",  # Delete from position (out of bounds, then 0) and from the end
        "9",
        "10", "2", "2", "10",  # New Linked List: the doubly example, displayed backward
        "0",
    )
    assert "The list is empty, so there's nothing to delete." in out
    assert "The list is empty." in out
    assert "'x' isn't a valid int." in out
    assert "Inserted 10 at the beginning." in out
    assert "Inserted 'b' at the end." in out
    assert "Inserted 2.5 at position 1." in out
    assert "Position 9 is out of bounds. Valid positions are 0 to 3." in out
    assert "Found 'b' at position 2." in out
    assert "99 isn't in the list." in out
    assert "Position 5 is out of bounds. Valid positions are 0 to 2." in out
    assert "Deleted 10 from position 0." in out
    assert "Deleted 'b' from the end." in out
    assert "│ 2.5 │ → None" in out
    assert "│ 2.5 │ ⇄ │ 'Messi' │ ⇄ │ 10 │ → None" in out


def test_circular_linked_lists(play):
    out = play(
        "1", "5", "3", "1",  # Linear > Linked List > Singly Circular > Start empty
        "10",  # Walking an empty list
        "4", "1", "a", "4", "1", "b",  # Insert 'a' and 'b' at the end
        "2", "2", "1",  # Insert 1 at the beginning
        "3", "3", "1", "c",  # Insert 'c' at position 3, the end
        "7", "6", "1",  # Delete from the end, then from position 1
        "10", "5",  # Walk 5 nodes around a 2-node loop
        "9",
        "11", "4", "2",  # New Linked List: the doubly circular example
        "11", "2", "4",  # Walk 4 nodes backward
        "10",  # Display backward
        "13", "0",
    )
    assert "The list is empty, so there's nothing to walk around." in out
    assert "Inserted 'a' at the end." in out
    assert "Inserted 1 at the beginning." in out
    assert "Inserted 'c' at position 3." in out
    assert "Deleted 'c' from the end." in out
    assert "Deleted 'a' from position 1." in out
    assert "Visited 5 nodes starting from the head: 1 → 'b' → 1 → 'b' → 1" in out
    assert "the walk went around the loop more than once" in out
    assert "│ 1 │ → │ 'b' │ → back to the head" in out
    assert "Visited 4 nodes starting from the tail: 2.5 → 'Messi' → 10 → 2.5" in out
    assert "│ 2.5 │ ⇄ │ 'Messi' │ ⇄ │ 10 │ ⇄ back to the tail" in out


def test_trees(play):
    out = play(
        "2", "1", "1", "1", "0", "1", "1",  # Non-linear > Tree > BST > Create > back > Create > Numbers
        "7", "6",  # Display the empty tree and its stats
        "2", "1", "50", "2", "1", "30", "2", "2", "70.5",
        "4", "1", "30", "4", "1", "99",
        "3", "1", "99", "3", "1", "50",
        "5", "2", "5", "0",  # Preorder traversal, then back
        "6",  # Tree stats
        "8", "2", "2", "5", "4", "7",  # New Tree: the AVL example, level order, then display
        "9", "0",
    )
    assert "Created an empty BST for numbers." in out
    assert "The tree is empty." in out
    assert "Inserted 50." in out
    assert "Found 30 in the tree." in out
    assert "99 isn't in the tree." in out
    assert "99 isn't in the tree, so nothing was deleted." in out
    assert "Deleted 50." in out
    assert "Preorder traversal: 70.5, 30" in out
    assert "Height (levels)" in out
    assert "Level order traversal: 30, 10, 60, 20, 50, 70, 80" in out
    assert "30 (-1)" in out


def test_heaps(play):
    out = play(
        "2", "2", "1", "1", "1",  # Non-linear > Heap & Priority Queue > Min Heap > Create > Numbers
        "3", "4", "7", "8",  # Extract, peek, stats and display on an empty heap
        "2", "1", "30", "2", "1", "10", "2", "2", "5.5",  # Insert 30, 10 and 5.5
        "3",  # Extract the min
        "5", "4, x", "4,,1", "20, 10, 30, 5",  # Build from a list after an invalid and an empty key
        "4", "6", "7", "8",
        "9", "2", "2",  # New Heap: the max heap example
        "3", "4",
        "10", "0",
    )
    assert "The heap is empty, so there's nothing to extract." in out
    assert "The heap is empty, so there's nothing to peek at." in out
    assert "The heap is empty." in out
    assert "Inserted 30 with 0 swaps." in out
    assert "Inserted 10 with 1 swap." in out
    assert "Step 1: Moved 5.5 up, swapping it with its parent 10." in out
    assert "Extracted the smallest key, 5.5." in out
    assert "Step 0: Moved the last leaf, 10, to the root." in out
    assert "No swaps were needed" in out
    assert "'x' isn't a valid number." in out
    assert "Some of the keys are empty." in out
    assert "Built a min heap from 4 keys with 3 swaps." in out
    assert "The smallest key is 5." in out
    assert "Level order traversal: 5, 10, 30, 20" in out
    assert "Loaded the example max heap, built from 50, 30, 10, 20, 70, 60 and 80." in out
    assert "Extracted the largest key, 80." in out
    assert "The largest key is 70." in out


def test_priority_queue(play):
    out = play(
        "2", "2", "3", "1",  # Non-linear > Heap & Priority Queue > Priority Queue > Start empty
        "3", "4",  # Dequeue and peek on an empty queue
        "2", "1", "write", "2",  # Enqueue 'write' with priority 2
        "2", "1", "fix", "x", "1",  # Enqueue 'fix' after an invalid priority
        "2", "1", "test", "1",
        "5", "1", "nope", "0",  # Change the priority of a missing item
        "5", "1", "write", "0",  # 'write' jumps to the front
        "4", "6", "7",
        "3", "3", "3", "3",  # Dequeue all three items, then one more
        "8", "3", "2",  # New Heap: the example priority queue
        "9", "0",
    )
    assert "The priority queue is empty, so there's nothing to dequeue." in out
    assert "The priority queue is empty, so there's nothing to peek at." in out
    assert "Enqueued 'write' with priority 2." in out
    assert "The priority must be a whole number." in out
    assert "Step 1: Moved 1: 'fix' up, swapping it with its parent 2: 'write'." in out
    assert "'nope' isn't in the priority queue, so nothing changed." in out
    assert "Changed the priority of 'write' from 2 to 0." in out
    assert "The next item is 'write', with priority 0." in out
    assert "The priority queue holds 3 items." in out
    assert "Serving order" in out
    assert "Dequeued 'fix', which had priority 1." in out
    assert "That was the only item, so the priority queue is empty now." in out
    assert "'Deploy' has the same priority as 'Fix bug'" in out


def test_trie(play):
    out = play(
        "2", "3", "1",  # Non-linear > Trie > Start empty
        "3", "car", "8", "7",  # Delete from, display and count an empty trie
        "2", " ", "card",  # An empty word, then 'card'
        "2", "car", "2", "car",  # 'car' reuses the nodes of 'card', then it's a duplicate
        "2", "cat",
        "4", "ca", "4", "cat", "4", "dog",
        "5", "ca", "5", "x",
        "6", "car", "6", "", "6", "z",
        "3", "car", "3", "card",
        "7", "8",
        "9", "2",  # New Trie with the example
        "10", "0",
    )
    assert "'car' isn't in the trie, so nothing was deleted." in out
    assert "The trie is empty." in out
    assert "The trie holds 0 words in 0 nodes" in out
    assert "The word needs at least one character." in out
    assert "Inserted 'card' with 4 new nodes." in out
    assert "Inserted 'car' with 0 new nodes." in out
    assert "The first 3 characters reused nodes that other words already had." in out
    assert "'car' is already in the trie, so nothing changed." in out
    assert "'ca' isn't a word in the trie, although some words start with it." in out
    assert "Found 'cat' in the trie." in out
    assert "'dog' isn't in the trie." in out
    assert "Does any word start with 'ca'? Yes." in out
    assert "Does any word start with 'x'? No." in out
    assert "Words starting with 'car': 'car', 'card'" in out
    assert "Words starting with '': 'car', 'card', 'cat'" in out
    assert "No words start with 'z'." in out
    assert "Deleted 'car'. Other words still use all of its nodes" in out
    assert "Deleted 'card' and pruned 2 nodes that no longer led to a word." in out
    assert "The trie holds 1 word in 3 nodes" in out
    assert "✓ 'cat'" in out
    assert "Loaded the example trie with the words 'car', 'card', 'care', 'cat', 'do' and 'dog'." in out


def test_graphs(play):
    out = play(
        "2", "4", "1", "1", "1", "x", "0", "3",  # Non-linear > Graph > Matrix > Create > Directed with 3 vertices
        "4", "0", "1", "0", "5",  # Add an edge: weight 0 is rejected, then 5
        "4", "0", "1", "7",  # Update it
        "4", "0", "9", "2",  # Missing vertex
        "6", "0", "1", "6", "1", "0",
        "5", "1", "0", "5", "0", "1",
        "2", "3", "1", "3", "7",  # Add a vertex, remove vertex 1, then a missing one
        "7", "1", "0", "7", "2", "5",
        "8", "2",  # Graph Algorithms > Topological Sort
        "4", "0", "2", "-3", "8", "1", "0",  # Add a negative edge, then Dijkstra refuses to run
        "8", "3",  # Cycle Detection
        "9",
        "10", "2", "1", "2", "9",  # New Graph: an empty undirected adjacency list
        "2", "0", "2", "1", "2", "1",  # Add vertices 0 and 1, then 1 again
        "4", "0", "1", "4", "4", "0", "5", "3",
        "7", "2", "0",
        "8", "4",  # Graph Algorithms > Kruskal
        "3", "0",
        "11", "0",
    )
    assert "The number of vertices must be a whole number." in out
    assert "The weight can't be 0" in out
    assert "Added an edge from 0 to 1 with weight 5." in out
    assert "Updated the edge from 0 to 1 to weight 7." in out
    assert "Vertex 9 doesn't exist. Valid vertices are 0 to 2." in out
    assert "Found an edge from 0 to 1 with weight 7." in out
    assert "There's no edge from 1 to 0." in out
    assert "There's no edge from 1 to 0, so nothing was removed." in out
    assert "Removed the edge from 0 to 1." in out
    assert "Added vertex 3." in out
    assert "Removed vertex 1 and all of its edges. The vertices after it moved down by one number." in out
    assert "Vertex 7 doesn't exist. Valid vertices are 0 to 2." in out
    assert "BFS from vertex 0: 0" in out
    assert "Vertex 5 doesn't exist." in out
    assert "Topological order: 0 → 1 → 2" in out
    assert "Dijkstra's algorithm can't handle negative weights, but the edge from 0 to 2 weighs -3." in out
    assert "The graph has no cycles." in out
    assert "The graph has no vertices yet." in out
    assert "Vertex 1 already exists." in out
    assert "Added an edge between 0 and 1 with weight 4." in out
    assert "Vertex 5 doesn't exist. Existing vertices: 0, 1." in out
    assert "DFS from vertex 0: 0 → 1" in out
    assert "Found a minimum spanning tree with 1 edge and a total weight of 4." in out
    assert "Removed vertex 0 and all of its edges." in out


def test_hash_tables(play):
    out = play(
        "2", "5", "2", "1", "3",  # Non-linear > Hash Table > Linear Probing > Create with 3 slots
        "2", "2", "1", "1", "a",  # Keys 1, 4 and 7 all hash to slot 1
        "2", "2", "4", "1", "b",
        "2", "2", "7", "1", "c",
        "2", "2", "10", "1", "d",  # The table is full
        "2", "2", "4", "1", "B",  # Update
        "4", "2", "7", "4", "2", "5",
        "3", "2", "1", "3", "2", "5",
        "5",
        "6", "1", "2", "5",  # New Hash Table: the chaining example
        "7", "0",
    )
    assert "Inserted key 1 with value 'a' in slot 1." in out
    assert "Inserted key 4 with value 'b' in slot 2." in out
    assert "Inserted key 7 with value 'c' in slot 0." in out
    assert "The table is full, so key 10 wasn't inserted." in out
    assert "Updated key 4 with value 'B' in slot 2." in out
    assert "Found key 7 in slot 0 with value 'c'." in out
    assert "Key 5 isn't in the table." in out
    assert "Deleted key 1 from slot 1." in out
    assert "Rehashed 2 keys from the same cluster" in out
    assert "Key 5 isn't in the table, so nothing was deleted." in out
    assert "Separate Chaining Hash Table" in out


def test_hash_sets(play):
    out = play(
        "2", "5", "3", "1", "3",  # Non-linear > Hash Table > Hash Set > Create two sets with 3 buckets
        "2", "1", "2", "1", "2", "1", "2", "2", "2", "1", "1", "x",  # Add 1, 2 and 'x' to A
        "2", "2", "2", "2", "2", "2", "1", "x",  # Add 2 and 'x' to B
        "2", "1", "2", "1",  # A already has 1
        "3", "2", "2", "9", "3", "2", "2", "2",  # Remove 9 (missing) and 2 from B
        "4", "1", "x",
        "5", "6", "7", "1", "7", "2", "8",
        "9", "11", "0",
    )
    assert "Created two empty sets, A and B, with 3 buckets each." in out
    assert "Added 1 to set A." in out
    assert "1 is already in set A, so nothing changed." in out
    assert "9 isn't in set B, so nothing was removed." in out
    assert "Removed 2 from set B." in out
    assert "Is 'x' in set A? Yes. Is it in set B? Yes." in out
    assert "A ∪ B = {1, 2, 'x'}" in out
    assert "A ∩ B = {'x'}" in out
    assert "A − B = {1, 2}" in out
    assert "B − A = ∅ (the empty set)" in out
    assert "Is A a subset of B (A ⊆ B)? No." in out
    assert "Is B a subset of A (B ⊆ A)? Yes." in out
    assert "A = {1, 2, 'x'}" in out


def test_disjoint_sets(play):
    out = play(
        "2", "6", "1", "x", "5",  # Non-linear > Disjoint Set > Create with 5 elements after an invalid size
        "2", "0", "1", "2", "2", "3", "2", "1", "3",  # Union 0 and 1, 2 and 3, then 1 and 3
        "3", "3",  # Find 3, which compresses its path
        "2", "0", "3",  # Already in the same set
        "4", "1", "4",
        "2", "4", "9",  # Missing element
        "5", "6",
        "7", "2",  # New Disjoint Set with the example
        "8", "0",
    )
    assert "The number of elements must be a whole number." in out
    assert "Created a disjoint set of 5 elements, numbered 0 to 4, each in a set of its own." in out
    assert "Merged the sets of 0 and 1. Their root is now 0." in out
    assert "Merged the sets of 1 and 3. Their root is now 0." in out
    assert "The root of 3 is 0." in out
    assert "Path compression pointed 1 element straight at the root." in out
    assert "0 and 3 are already in the same set, so nothing changed." in out
    assert "Are 1 and 4 connected? No." in out
    assert "Element 9 doesn't exist. Valid elements are 0 to 4." in out
    assert "2 sets" in out and "{0, 1, 2, 3}" in out
    assert "Loaded the example" in out


def test_sorting_algorithms(play):
    out = play(
        "3", "1", "1", "5, x", "3, -1, 2.5",  # Algorithms > Sorting > Type numbers, after an invalid one
        "8", "1",  # Merge Sort, ascending
        "9",  # Counting Sort can't sort the float
        "11", "2",  # Compare all algorithms, descending
        "12",
        "13", "3",  # New List: the example
        "10", "1",  # Radix Sort
        "9", "2",  # Counting Sort, descending
        "14", "0",  # Main Menu, then exit
    )
    assert "'x' isn't a valid number." in out
    assert "Created a list of 3 numbers." in out
    assert "How Merge Sort Works" in out
    assert "Sorted a copy of the list in ascending order in 2 steps, with 3 comparisons and 5 writes." in out
    assert "The list itself is unchanged" in out
    assert "Counting Sort only sorts whole numbers (int) less than 10,000 apart." in out
    assert "Sorting algorithms compared" in out
    assert "Loaded the example list." in out
    assert "Sorted a copy of the list in ascending order in 3 steps, with 0 comparisons and 24 writes." in out
    assert "Sorted a copy of the list in descending order in 8 steps" in out


def test_searching_algorithms(play):
    out = play(
        "3", "2", "3",  # Algorithms > Searching > the example
        "4", "1", "300",  # Jump Search for the int 300
        "5", "2", "7",  # Interpolation Search for the float 7.0
        "6", "1", "5",  # Exponential Search for a missing value
        "2", "1", "2004",
        "8", "2", "pear, apple, fig",  # New List of words
        "5",  # Interpolation Search can't search words
        "3", "fig",
        "9", "0",
    )
    assert "Found 300 at index 7." in out
    assert "Searched this sorted copy and checked 4 positions" in out
    assert "Found 7.0 at index 6." in out
    assert "5 isn't in the list." in out
    assert "Found 2004 at index 4." in out
    assert "Checked 5 positions, numbered in order under the values." in out
    assert "Created a list of 3 words." in out
    assert "Interpolation Search only works on numbers" in out
    assert "Found 'fig' at index 2." in out


def test_graph_algorithms(play):
    out = play(
        "3", "3", "1",  # Algorithms > Graph Algorithms > the directed example
        "2", "0",  # Dijkstra from vertex 0
        "3", "4", "5",  # Topological sort, cycle detection, display
        "2", "9",  # A missing vertex
        "6", "2",  # New Graph: the undirected example
        "3", "4", "5",  # Cycle detection, Prim and Kruskal
        "8", "0",
    )
    assert "Found the shortest paths from vertex 0 to 4 other vertices." in out
    assert "0 → 2 → 1 → 3 → 4" in out
    assert "Topological order: 0 → 2 → 1 → 3 → 4" in out
    assert "The graph has no cycles." in out
    assert "Vertex 9 doesn't exist. Existing vertices: 0, 1, 2, 3, 4." in out
    assert "Loaded the example undirected graph." in out
    assert "Found a cycle: 2 — 0 — 1 — 2" in out
    assert out.count("Found a minimum spanning tree with 4 edges and a total weight of 11.") == 2
    assert "Left out, because they would close a cycle: 0 — 1 (4), 2 — 3 (8), 2 — 4 (9)." in out
