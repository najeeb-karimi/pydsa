"""Screen flows: scripted console sessions that walk through the menus and exit cleanly."""

import pytest

from pydsa import app
from pydsa.ui import render


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
        monkeypatch.setattr("os.system", lambda command: 0)
        app.run()
        assert list(remaining) == [], "The app exited before using every scripted answer"
        return capsys.readouterr().out

    return run_session


def test_exit_from_the_categories_and_go_back(play):
    out = play("7", "1", "0", "2", "9", "0", "1", "2", "2", "10")
    assert "⏳ Version 3.0" in out
    assert out.count("❌ Invalid code number!") == 2
    assert "Which Non-linear Data Structure" in out


def test_array_sort_and_search(play):
    out = play("1", "1", "2", "4", "1", "1", "5", "2", "672", "11")
    assert "🪜 Sorting Steps:\n🔹 [10, 672, 1987, 8, 2004]" in out
    assert "♻️ Sorted array:\n👉 [8, 10, 672, 1987, 2004]" in out
    assert "✅ Element found at index: 2." in out


def test_new_array_restarts_and_new_data_structure_goes_home(play):
    out = play("1", "1", "2", "9", "2", "10", "1", "2", "2", "10")
    assert out.count("Here's an example int array") == 2
    assert out.count("💻 Welcome to PyDSA") == 3
    assert "Here's an example stack with size 5" in out


def test_stack_push_pop(play):
    out = play("1", "2", "1", "1", "1", "5", "1", "1", "hi", "2", "3", "9", "1", "2", "1", "1", "10")
    assert "🚫 Stack is full; item not pushed." in out
    assert "👋 Item removed: 5" in out
    assert "🚫 Stack is empty." in out


def test_queue_strikes_out_dequeued_items(play):
    out = play("1", "3", "1", "2", "1", "ab", "2", "8", "7", "11")
    assert f"👉 [{render.strike('ab')!r}, None]" in out
    assert len(render.strike("ab")) == 4
    assert "👉 Queue size: 0/2" in out


def test_doubly_linked_list(play):
    out = play("1", "4", "2", "1", "2", "1", "3", "2", "x", "8", "12")
    assert "✅ Insertion successful.\n👉 1" in out
    assert "🚫 Invalid data type; item not inserted." in out


def test_avl_tree_with_strings(play):
    out = play("2", "1", "2", "1", "2", "1", "m", "1", "c", "1", "a", "4", "2", "7")
    assert "👉🏻 ['c', 'a', 'm']\nℹ️ Preorder Traversal" in out


def test_graph_traversal_errors(play):
    out = play("2", "2", "2", "2", "6", "1", "9", "6", "2", "1", "10")
    assert "🚫 BFS traversal unsuccessful. Vertex 9 does not exist." in out
    assert "👉🏻 1 0 2 3 \nℹ️ DFS Traversal" in out


def test_probing_hash_table_delete_reports_rehashing(play):
    out = play("2", "3", "2", "1", "3",
               "1", "2", "1", "1", "a", "1", "2", "4", "1", "b",
               "2", "2", "1", "7")
    assert "✅ Deletion successful. Deleted key (1) from index 1.\n♻️ Rehashed 1 key(s) from the same cluster." in out
