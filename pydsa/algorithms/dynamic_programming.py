"""Dynamic programming with optional immutable snapshots and actual work counters.

Tables retain all states for teaching and reconstruction. Costs assume unit-cost
integer arithmetic; Fibonacci values and coin counts can require large integers.
"""

from dataclasses import dataclass
from typing import NamedTuple

from pydsa.algorithms.trace import record


@dataclass
class DPStats:
    calls: int = 0
    cells: int = 0


class KnapsackResult(NamedTuple):
    value: int
    items: tuple[int, ...]  # Original zero-based item indexes.
    table: tuple[tuple[int, ...], ...]


class LCSResult(NamedTuple):
    sequence: str
    table: tuple[tuple[int, ...], ...]
    directions: tuple[tuple[str, ...], ...]


class CoinResult(NamedTuple):
    count: int | None  # None means the target cannot be made.
    coins: tuple[int, ...]


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer of at least {minimum}.")


def _freeze(table):
    return tuple(tuple(row) for row in table)


def _table_event(trace, kind, table, rows, columns, marks=None, arrows=None, **data):
    if trace is not None:
        snapshot = {"table": _freeze(table), "rows": tuple(rows), "columns": tuple(columns)}
        if arrows is not None:
            snapshot["arrows"] = _freeze(arrows)
        record(trace, kind, snapshot, marks, **data)


def fibonacci_recursive(n, trace=None, *, stats=None):
    """Compute F(0)=0, F(1)=1 by plain recursion, counting every function entry."""
    return _fibonacci(n, False, trace, stats)


def fibonacci_memoized(n, trace=None, *, stats=None):
    """Compute each Fibonacci state once, counting cache-hit calls as calls too."""
    return _fibonacci(n, True, trace, stats)


def _fibonacci(n, memoized, trace, stats):
    _integer(n, "n")
    stats = stats if stats is not None else DPStats()
    cache = {}
    next_id = 0

    def visit(k, parent=None):
        nonlocal next_id
        identifier = next_id
        next_id += 1
        stats.calls += 1
        record(trace, "dp_call", identifier=identifier, parent=parent, label=f"F({k})", n=k)
        if memoized and k in cache:
            record(trace, "dp_cache", n=k, value=cache[k])
            return cache[k]
        value = k if k < 2 else visit(k - 1, identifier) + visit(k - 2, identifier)
        stats.cells += 1  # States actually computed, rather than reused.
        if memoized:
            cache[k] = value
        record(trace, "dp_return", n=k, value=value)
        return value

    return visit(n)


def fibonacci_table(n, trace=None, *, stats=None):
    """Fill an explicit table from the two base states; this is one function call."""
    _integer(n, "n")
    stats = stats if stats is not None else DPStats()
    stats.calls += 1
    table = [[None] * (n + 1)]
    for i in range(n + 1):
        table[0][i] = i if i < 2 else table[0][i - 1] + table[0][i - 2]
        stats.cells += 1
        _table_event(trace, "dp_cell", table, ["F"], range(n + 1), {(0, i): "filled"},
                     row=0, column=i, value=table[0][i], reason="Use the base value" if i < 2 else "Add the preceding two entries")
    return table[0][n]


def knapsack(weights, values, capacity, trace=None, *, stats=None):
    """Choose each positive-weight item at most once; ties prefer leaving it out."""
    weights, values = tuple(weights), tuple(values)
    _integer(capacity, "Capacity")
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same length.")
    for weight in weights:
        _integer(weight, "Weight", 1)
    for value in values:
        _integer(value, "Value")
    stats = stats if stats is not None else DPStats()
    stats.calls += 1
    table = [[0] * (capacity + 1)] + [[0] + [None] * capacity for _ in weights]
    rows, columns = range(len(table)), range(capacity + 1)
    _table_event(trace, "dp_start", table, rows, columns, algorithm="Knapsack", base="zero items or zero capacity give value zero")
    for i, (weight, value) in enumerate(zip(weights, values), 1):
        for c in range(1, capacity + 1):
            skip = table[i - 1][c]
            take = value + table[i - 1][c - weight] if weight <= c else -1
            table[i][c] = max(skip, take)
            stats.cells += 1
            _table_event(trace, "dp_cell", table, rows, columns, {(i, c): "filled"},
                         row=i, column=c, value=table[i][c],
                         reason=f"Compare leaving item {i - 1} out ({skip}) with taking it ({take if take >= 0 else 'does not fit'})")
    chosen, c = [], capacity
    for i in range(len(weights), 0, -1):
        take = table[i][c] != table[i - 1][c]
        if take:
            chosen.append(i - 1)
        _table_event(trace, "dp_take", table, rows, columns, {(i, c): "checked"},
                     item=i - 1, decision="Take" if take else "Skip", capacity=c)
        if take:
            c -= weights[i - 1]
    return KnapsackResult(table[-1][-1], tuple(reversed(chosen)), _freeze(table))


def longest_common_subsequence(first, second, trace=None, *, stats=None):
    """Find one LCS of two strings; on an equal-length tie, traceback moves up."""
    if not isinstance(first, str) or not isinstance(second, str):
        raise TypeError("Both sequences must be strings.")
    stats = stats if stats is not None else DPStats()
    stats.calls += 1
    table = [[0] * (len(second) + 1)] + [[0] + [None] * len(second) for _ in first]
    arrows = [[""] * len(table[0]) for _ in table]
    rows, columns = ("empty", *first), ("empty", *second)
    _table_event(trace, "dp_start", table, rows, columns, arrows=arrows,
                 algorithm="LCS", base="an empty prefix has common length zero")
    for i, a in enumerate(first, 1):
        for j, b in enumerate(second, 1):
            if a == b:
                table[i][j], arrows[i][j] = table[i - 1][j - 1] + 1, "↖"
                reason = "Matching characters extend the diagonal subsequence"
            elif table[i - 1][j] >= table[i][j - 1]:
                table[i][j], arrows[i][j] = table[i - 1][j], "↑"
                reason = "Keep the upper entry (also the tie rule)"
            else:
                table[i][j], arrows[i][j] = table[i][j - 1], "←"
                reason = "Keep the left entry"
            stats.cells += 1
            _table_event(trace, "dp_cell", table, rows, columns, {(i, j): "filled"}, arrows,
                         row=i, column=j, value=table[i][j], reason=reason)
    i, j, letters = len(first), len(second), []
    while i and j:
        direction = arrows[i][j]
        if direction == "↖":
            letters.append(first[i - 1])
        _table_event(trace, "dp_lcs_rebuild", table, rows, columns, {(i, j): "checked"}, arrows,
                     row=i, column=j, direction=direction, sequence="".join(reversed(letters)))
        if direction == "↖":
            i, j = i - 1, j - 1
        elif direction == "↑":
            i -= 1
        else:
            j -= 1
    return LCSResult("".join(reversed(letters)), _freeze(table), _freeze(arrows))


def _denominations(coins, target):
    _integer(target, "Target")
    coins = tuple(coins)
    for coin in coins:
        _integer(coin, "Coin", 1)
    return tuple(sorted(set(coins)))


def minimum_coins(coins, target, trace=None, *, stats=None):
    """Unlimited coins; return None for an impossible target, and rebuild one optimum."""
    coins = _denominations(coins, target)
    stats = stats if stats is not None else DPStats()
    stats.calls += 1
    table, previous = [[0] + [None] * target], [None] * (target + 1)
    _table_event(trace, "dp_start", table, ["fewest"], range(target + 1),
                 algorithm="Fewest coins", base="amount zero needs zero coins; other amounts start unreachable")
    for amount in range(1, target + 1):
        best = None
        for coin in coins:
            stats.cells += 1  # Every denomination tested, including coins too large.
            if coin <= amount and table[0][amount - coin] is not None:
                candidate = table[0][amount - coin] + 1
                if best is None or candidate < best:
                    best, previous[amount] = candidate, coin
        table[0][amount] = best
        _table_event(trace, "dp_cell", table, ["fewest"], range(target + 1), {(0, amount): "filled"},
                     row=0, column=amount, value=best, reason="Try every last coin using an already solved smaller amount")
    chosen, amount = [], target
    while amount and previous[amount] is not None:
        coin = previous[amount]
        chosen.append(coin)
        _table_event(trace, "dp_coin_rebuild", table, ["fewest"], range(target + 1), {(0, amount): "checked"},
                     amount=amount, coin=coin, remaining=amount - coin)
        amount -= coin
    return CoinResult(table[0][target], tuple(chosen))


def coin_change_ways(coins, target, trace=None, *, stats=None):
    """Count unordered combinations with unlimited coins; duplicate denominations merge."""
    coins = _denominations(coins, target)
    stats = stats if stats is not None else DPStats()
    stats.calls += 1
    table = [[1] + [0] * target] + [[1] + [None] * target for _ in coins]
    rows, columns = ("none", *coins), range(target + 1)
    _table_event(trace, "dp_start", table, rows, columns,
                 algorithm="Coin ways", base="there is one empty combination for zero, and no positive amount without coins")
    for i, coin in enumerate(coins, 1):
        for amount in range(1, target + 1):
            table[i][amount] = table[i - 1][amount]
            if coin <= amount:
                table[i][amount] += table[i][amount - coin]
            stats.cells += 1
            _table_event(trace, "dp_cell", table, rows, columns, {(i, amount): "filled"},
                         row=i, column=amount, value=table[i][amount],
                         reason=f"Ways without {coin}, plus ways using it from this same row")
    return table[-1][-1]
