"""DP answers against exhaustive subsets, subsequences and coin counts."""

from copy import deepcopy
from itertools import product
import random

import pytest

from pydsa.algorithms import dynamic_programming as dp


def fib_model(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@pytest.mark.parametrize("n", range(19))
def test_fibonacci_answers_and_actual_call_counts(n):
    for function in (dp.fibonacci_recursive, dp.fibonacci_memoized, dp.fibonacci_table):
        stats, trace = dp.DPStats(), []
        value = function(n, trace, stats=stats)
        assert value == fib_model(n) == function(n)
        if function is dp.fibonacci_recursive:
            assert stats.calls == 2 * fib_model(n + 1) - 1
            assert stats.cells == stats.calls
        elif function is dp.fibonacci_memoized:
            assert stats.calls == (1 if n < 2 else 2 * n - 1)
            assert stats.cells == (1 if n < 2 else n + 1)
            assert sum(e.kind == "dp_cache" for e in trace) == stats.calls - stats.cells
        else:
            assert stats.calls == 1 and stats.cells == n + 1
            assert trace[-1].snapshot["table"][0] == tuple(fib_model(i) for i in range(n + 1))
        if function is not dp.fibonacci_table:
            calls = [event for event in trace if event.kind == "dp_call"]
            assert len(calls) == stats.calls
            parents = {event.data["identifier"]: event.data["n"] for event in calls}
            assert calls[0].data["parent"] is None
            for event in calls[1:]:
                assert parents[event.data["parent"]] - event.data["n"] in (1, 2)


def best_subset(weights, values, capacity):
    return max(sum(value for bit, value in zip(bits, values) if bit)
               for bits in product((False, True), repeat=len(weights))
               if sum(weight for bit, weight in zip(bits, weights) if bit) <= capacity)


def test_knapsack_random_subsets_and_reconstruction():
    rng = random.Random(18)
    for _ in range(180):
        size = rng.randrange(7)
        weights, values = [rng.randint(1, 8) for _ in range(size)], [rng.randrange(12) for _ in range(size)]
        capacity = rng.randrange(15)
        before, trace, stats = (weights[:], values[:]), [], dp.DPStats()
        answer = dp.knapsack(weights, values, capacity, trace, stats=stats)
        assert answer.value == best_subset(weights, values, capacity)
        assert len(set(answer.items)) == len(answer.items)
        assert sum(weights[i] for i in answer.items) <= capacity
        assert sum(values[i] for i in answer.items) == answer.value
        assert stats.cells == size * capacity
        assert (weights, values) == before
        assert answer == dp.knapsack(weights, values, capacity)
        taken = [e.data["item"] for e in trace if e.kind == "dp_take" and e.data["decision"] == "Take"]
        assert tuple(reversed(taken)) == answer.items
        assert len([e for e in trace if e.kind == "dp_cell"]) == size * capacity


def subsequences(text):
    return {"".join(c for c, bit in zip(text, bits) if bit) for bits in product((False, True), repeat=len(text))}


def test_lcs_matches_exhaustive_subsequences_including_unicode():
    rng = random.Random(29)
    for _ in range(130):
        first = "".join(rng.choice("ABé🦄") for _ in range(rng.randrange(7)))
        second = "".join(rng.choice("ABé🦄") for _ in range(rng.randrange(7)))
        common = subsequences(first) & subsequences(second)
        trace, stats = [], dp.DPStats()
        answer = dp.longest_common_subsequence(first, second, trace, stats=stats)
        assert answer.sequence in common and len(answer.sequence) == max(map(len, common))
        assert answer == dp.longest_common_subsequence(first, second)
        assert answer.table[-1][-1] == len(answer.sequence)
        assert stats.cells == len(first) * len(second)
        for event in trace:
            if event.kind == "dp_cell":
                i, j = event.data["row"], event.data["column"]
                if first[i - 1] == second[j - 1]:
                    assert answer.directions[i][j] == "↖"
        rebuilt = [e.data["sequence"] for e in trace if e.kind == "dp_lcs_rebuild"]
        if rebuilt:
            assert rebuilt[-1] == answer.sequence
    assert dp.longest_common_subsequence("ab", "ba").sequence == "a"  # Up on a tie.


def coin_model(coins, target):
    coins = sorted(set(coins))
    lengths = [sum(counts) for counts in product(*(range(target // coin + 1) for coin in coins))
               if sum(count * coin for count, coin in zip(counts, coins)) == target]
    return (min(lengths) if lengths else None), len(lengths)


@pytest.mark.parametrize("coins", [[], [1], [2, 4], [1, 3, 4], [3, 5], [2, 2, 3]])
@pytest.mark.parametrize("target", range(13))
def test_both_coin_problems_against_brute_force(coins, target):
    expected_min, expected_ways = coin_model(coins, target)
    trace, stats = [], dp.DPStats()
    answer = dp.minimum_coins(coins, target, trace, stats=stats)
    assert answer.count == expected_min
    assert all(c in coins for c in answer.coins)
    if expected_min is None:
        assert answer.coins == ()
    else:
        assert len(answer.coins) == expected_min and sum(answer.coins) == target
    assert stats.cells == len(set(coins)) * target
    rebuilt = [e for e in trace if e.kind == "dp_coin_rebuild"]
    assert tuple(e.data["coin"] for e in rebuilt) == answer.coins
    ways_trace, ways_stats = [], dp.DPStats()
    assert dp.coin_change_ways(coins, target, ways_trace, stats=ways_stats) == expected_ways
    assert ways_stats.cells == len(set(coins)) * target
    assert ways_trace[-1].snapshot["table"][-1][-1] == expected_ways
    assert dp.minimum_coins(coins, target) == answer
    assert dp.coin_change_ways(coins, target) == expected_ways


@pytest.mark.parametrize("function,args", [(dp.fibonacci_table, (7,)), (dp.knapsack, ([2, 3], [3, 4], 6)),
                                          (dp.longest_common_subsequence, ("ABA", "BAA")),
                                          (dp.minimum_coins, ([1, 3], 5)), (dp.coin_change_ways, ([1, 3], 5))])
def test_table_snapshots_preserve_previous_steps(function, args):
    trace = []
    function(*args, trace=trace)
    saved = [deepcopy(event.snapshot) for event in trace]
    function(*args, trace=trace)
    assert [event.snapshot for event in trace[:len(saved)]] == saved
    assert trace[0].snapshot != trace[-1].snapshot
    # Each cell update changes exactly the marked cell; other already solved cells stay put.
    for previous, current in zip(trace[:len(saved)], trace[1:len(saved)]):
        if current.kind == "dp_cell":
            for i, row in enumerate(previous.snapshot["table"]):
                for j, value in enumerate(row):
                    if (i, j) not in current.marks:
                        assert current.snapshot["table"][i][j] == value


@pytest.mark.parametrize("bad", [-1, 1.5, True, "2", None])
def test_invalid_indexes_capacities_and_targets(bad):
    for function in (dp.fibonacci_recursive, dp.fibonacci_memoized, dp.fibonacci_table):
        with pytest.raises(ValueError):
            function(bad)
    with pytest.raises(ValueError):
        dp.knapsack([1], [1], bad)
    for function in (dp.minimum_coins, dp.coin_change_ways):
        with pytest.raises(ValueError):
            function([1], bad)


@pytest.mark.parametrize("weights,values", [([0], [1]), ([-1], [1]), ([1.5], [1]), ([True], [1]),
                                         ([1], [-1]), ([1], [False]), ([1], [])])
def test_invalid_knapsack_items(weights, values):
    with pytest.raises(ValueError):
        dp.knapsack(weights, values, 3)


@pytest.mark.parametrize("coins", [[0], [-1], [1.5], [True]])
def test_invalid_denominations(coins):
    for function in (dp.minimum_coins, dp.coin_change_ways):
        with pytest.raises(ValueError):
            function(coins, 4)


def test_lcs_requires_strings():
    with pytest.raises(TypeError):
        dp.longest_common_subsequence([], "abc")
