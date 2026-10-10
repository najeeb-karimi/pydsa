"""Recursive puzzles with independent results, optional traces and counted work."""

from dataclasses import dataclass

from pydsa.algorithms.trace import record


@dataclass
class RecursionStats:
    calls: int = 0
    choices: int = 0
    moves: int = 0


def _size(n):
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer.")


def hanoi(n, trace=None, *, stats=None):
    """Return (disk, source, destination) moves from A to C, with B as spare."""
    _size(n)
    stats = stats if stats is not None else RecursionStats()
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    moves = []

    def move(size, source, target, spare):
        stats.calls += 1
        if not size:
            return
        move(size - 1, source, spare, target)
        disk = pegs[source].pop()
        pegs[target].append(disk)
        moves.append((disk, source, target))
        stats.moves += 1
        if trace is not None:
            record(trace, "rec_move", tuple(tuple(pegs[peg]) for peg in "ABC"),
                   disk=disk, source=source, target=target, move=len(moves))
        move(size - 1, spare, target, source)

    move(n, "A", "C", "B")
    return moves


def permutations(items, trace=None, *, stats=None):
    """Generate in input-position order, matching itertools even for equal values.

    Equal values at distinct positions can produce duplicate permutations. The
    empty input has one permutation: the empty tuple.
    """
    items = tuple(items)
    stats = stats if stats is not None else RecursionStats()
    answers, path, used = [], [], [False] * len(items)
    next_id = 0

    def visit(parent=None):
        nonlocal next_id
        identifier = next_id
        next_id += 1
        stats.calls += 1
        if trace is not None:
            record(trace, "rec_call", tuple(path), identifier=identifier, parent=parent, label=repr(tuple(path)), depth=len(path))
        if len(path) == len(items):
            answers.append(tuple(path))
            record(trace, "rec_permutation", tuple(path) if trace is not None else None, count=len(answers))
        else:
            for i, item in enumerate(items):
                if not used[i]:
                    stats.choices += 1
                    used[i] = True
                    path.append(item)
                    visit(identifier)
                    path.pop()
                    used[i] = False
        record(trace, "rec_return", tuple(path) if trace is not None else None, depth=len(path))

    visit()
    return answers


def n_queens(n, trace=None, *, stats=None):
    """Return column-per-row solutions, pruning occupied columns and diagonals.

    No symmetry reduction: every solution is counted. The empty board has one
    empty solution. UI limits are intentionally separate from this pure core.
    """
    _size(n)
    stats = stats if stats is not None else RecursionStats()
    answers, board, columns, descending, ascending = [], [], set(), set(), set()

    def emit(kind, row, column, **data):
        if trace is not None:
            record(trace, kind, (n, tuple(board)), {(row, column): "checked"}, row=row, column=column, **data)

    def visit(row):
        stats.calls += 1
        if row == n:
            answers.append(tuple(board))
            emit("rec_solution", row, -1, count=len(answers))
            return
        for column in range(n):
            stats.choices += 1
            if column in columns or row - column in descending or row + column in ascending:
                emit("rec_reject", row, column)
                continue
            columns.add(column)
            descending.add(row - column)
            ascending.add(row + column)
            board.append(column)
            emit("rec_place", row, column)
            visit(row + 1)
            board.pop()
            columns.remove(column)
            descending.remove(row - column)
            ascending.remove(row + column)
            emit("rec_remove", row, column)

    visit(0)
    return answers
