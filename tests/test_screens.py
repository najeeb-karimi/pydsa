"""Screen flows: scripted console sessions that walk through every menu and exit cleanly."""

import pytest

from pydsa import app


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
    assert "⏳ Version 3.1" in out
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


def test_linked_lists(play):
    out = play(
        "1", "4", "1", "1",  # Linear > Linked List > Singly > Start empty
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


def test_trees(play):
    out = play(
        "2", "1", "1", "1", "0", "1", "1",  # Non-linear > Tree > BST > Create > back > Create > Numbers
        "6",  # Display the empty tree
        "2", "1", "50", "2", "1", "30", "2", "2", "70.5",
        "4", "1", "30", "4", "1", "99",
        "3", "1", "99", "3", "1", "50",
        "5", "2", "5", "0",  # Preorder traversal, then back
        "7", "2", "2", "5", "1",  # New Tree: the AVL example, inorder
        "8", "0",
    )
    assert "Created an empty BST for numbers." in out
    assert "The tree is empty." in out
    assert "Inserted 50." in out
    assert "Found 30 in the tree." in out
    assert "99 isn't in the tree." in out
    assert "99 isn't in the tree, so nothing was deleted." in out
    assert "Deleted 50." in out
    assert "Preorder traversal: 70.5, 30" in out
    assert "Inorder traversal: 10, 20, 30, 50, 60, 70, 80" in out


def test_graphs(play):
    out = play(
        "2", "2", "1", "1", "x", "0", "3",  # Non-linear > Graph > Matrix > Create with 3 vertices
        "4", "0", "1", "0", "5",  # Add an edge: weight 0 is rejected, then 5
        "4", "0", "1", "7",  # Update it
        "4", "0", "9", "2",  # Missing vertex
        "6", "0", "1", "6", "1", "0",
        "5", "1", "0", "5", "0", "1",
        "2", "3", "1", "3", "7",  # Add a vertex, remove vertex 1, then a missing one
        "7", "1", "0", "7", "2", "5",
        "8",
        "9", "2", "1", "8",  # New Graph: an empty adjacency list
        "2", "0", "2", "1", "2", "1",  # Add vertices 0 and 1, then 1 again
        "4", "0", "1", "4", "4", "0", "5", "3",
        "7", "2", "0",
        "3", "0",
        "10", "0",
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
    assert "The graph has no vertices yet." in out
    assert "Vertex 1 already exists." in out
    assert "Vertex 5 doesn't exist. Existing vertices: 0, 1." in out
    assert "DFS from vertex 0: 0 → 1" in out
    assert "Removed vertex 0 and all of its edges." in out


def test_hash_tables(play):
    out = play(
        "2", "3", "2", "1", "3",  # Non-linear > Hash Table > Linear Probing > Create with 3 slots
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
