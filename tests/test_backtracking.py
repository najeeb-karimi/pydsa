"""Legal Hanoi moves, itertools permutations and exhaustive queen models."""

from itertools import permutations
import math

import pytest

from pydsa.algorithms import backtracking as core


@pytest.mark.parametrize("n", range(11))
def test_every_hanoi_move_is_legal_and_snapshot_matches(n):
    trace, stats = [], core.RecursionStats()
    moves = core.hanoi(n, trace, stats=stats)
    assert len(moves) == 2 ** n - 1 == stats.moves
    assert len(trace) == len(moves)
    assert stats.calls == 2 ** (n + 1) - 1
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    for i, ((disk, source, target), event) in enumerate(zip(moves, trace), 1):
        assert source != target and pegs[source][-1] == disk
        assert not pegs[target] or pegs[target][-1] > disk
        pegs[target].append(pegs[source].pop())
        assert event.snapshot == tuple(tuple(pegs[peg]) for peg in "ABC")
        assert event.data == {"disk": disk, "source": source, "target": target, "move": i}
    assert pegs == {"A": [], "B": [], "C": list(range(n, 0, -1))}
    assert core.hanoi(n) == moves


@pytest.mark.parametrize("items", [[], [1], [1, 2, 3], ["a", "b"], [1, 1, 2], list(range(6))])
def test_permutations_match_itertools_and_tree_structure(items):
    trace, stats, before = [], core.RecursionStats(), items[:]
    answers = core.permutations(items, trace, stats=stats)
    assert answers == list(permutations(items)) == core.permutations(items)
    assert items == before
    calls = [event for event in trace if event.kind == "rec_call"]
    assert stats.calls == len(calls) == sum(math.factorial(len(items)) // math.factorial(len(items) - k) for k in range(len(items) + 1))
    assert stats.choices == stats.calls - 1
    prefixes = {}
    for event in calls:
        prefix, identifier, parent = event.snapshot, event.data["identifier"], event.data["parent"]
        if parent is not None:
            assert prefix[:-1] == prefixes[parent]
        else:
            assert prefix == ()
        prefixes[identifier] = prefix
    assert [event.snapshot for event in trace if event.kind == "rec_permutation"] == answers


def valid(board):
    return len(set(board)) == len(board) and all(abs(a - b) != j - i for i, a in enumerate(board) for j, b in enumerate(board) if i < j)


@pytest.mark.parametrize("n,count", list(enumerate([1, 1, 0, 0, 2, 10, 4, 40, 92])))
def test_queens_counts_and_constraints(n, count):
    stats = core.RecursionStats()
    answers = core.n_queens(n, stats=stats)
    assert len(answers) == count == len(set(answers))
    assert all(len(board) == n and valid(board) for board in answers)
    if n <= 6:
        assert answers == [board for board in permutations(range(n)) if valid(board)]
    assert stats.choices == n * (stats.calls - len(answers))


def test_queens_trace_includes_every_placement_undo_and_solution():
    trace, stats = [], core.RecursionStats()
    answers = core.n_queens(5, trace, stats=stats)
    board, found, placed, removed = (), [], 0, 0
    frozen_first = None
    for event in trace:
        n, snapshot = event.snapshot
        row, column = event.data["row"], event.data["column"]
        assert n == 5 and valid(snapshot)
        if event.kind == "rec_place":
            assert row == len(board) and snapshot == (*board, column)
            board, placed = snapshot, placed + 1
            if frozen_first is None:
                frozen_first = event.snapshot
        elif event.kind == "rec_remove":
            assert board[-1] == column and snapshot == board[:-1]
            board, removed = snapshot, removed + 1
        elif event.kind == "rec_solution":
            assert snapshot == board and len(board) == 5
            found.append(board)
        else:
            assert event.kind == "rec_reject" and snapshot == board
            assert not valid((*board, column))
    assert board == () and placed == removed == stats.calls - 1
    assert found == answers
    assert frozen_first == (5, (0,))


@pytest.mark.parametrize("bad", [-1, True, 1.5, "3", None])
def test_invalid_sizes(bad):
    for function in (core.hanoi, core.n_queens):
        with pytest.raises(ValueError):
            function(bad)
