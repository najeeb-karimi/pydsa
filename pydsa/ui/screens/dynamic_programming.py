"""Choose a bounded DP example, watch its states and reconstruct its answer."""

import random

from pydsa.algorithms import dynamic_programming as dp
from pydsa.content import texts
from pydsa.ui import render, stepper
from pydsa.ui.console import ask, ask_int, error, info, result
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu, topic_option
from pydsa.ui.screens.sorting_algorithms import Algorithm

KINDS = (
    Algorithm("Fibonacci", dp.fibonacci_table, "fibonacci"),
    Algorithm("0/1 Knapsack", dp.knapsack, "knapsack"),
    Algorithm("Longest Common Subsequence", dp.longest_common_subsequence, "longest-common-subsequence"),
    Algorithm("Coin Change", dp.minimum_coins, "coin-change"),
)


def run():
    render.intro(texts.DYNAMIC_PROGRAMMING_ASCII, "dynamic-programming")
    return Menu("Which dynamic programming problem?", [
        [topic_option(kind.guide, kind.name, lambda kind=kind: open_kind(kind)) for kind in KINDS],
        [("Read the Guide", lambda: render.guide("dynamic-programming")), back_option()],
    ]).run()


def open_kind(kind):
    while True:
        outcome = run_kind(kind)
        if outcome is not Nav.NEW:
            return None if outcome is Nav.BACK else outcome


def run_kind(kind):
    render.intro(getattr(texts, kind.guide.replace("-", "_").upper() + "_ASCII"), kind.guide)
    data = Menu("How do you want to choose the inputs?", [
        [("Type inputs", lambda: create(kind)), ("Use the example", lambda: example(kind)),
         ("Generate random inputs", lambda: random_example(kind))], [back_option()],
    ]).open()
    if data is Nav.BACK:
        return Nav.BACK
    display(kind, data)
    return operation_menu(kind.name, kind.guide, operations(kind, data), new_label="New Inputs").run()


def read_integers(name, maximum, minimum=0, largest=30):
    """Allow an empty input, but reject decimals, missing entries and oversized lists."""
    while True:
        text = ask(f"Enter {name}, comma separated (up to {maximum}; Enter means empty):")
        try:
            values = [] if not text.strip() else [int(part.strip()) for part in text.split(",")]
            if len(values) <= maximum and all(minimum <= value <= largest for value in values):
                return values
        except ValueError:
            pass
        error(f"Use at most {maximum} whole numbers between {minimum} and {largest}.")


def read_sequence(name):
    while True:
        text = ask(f"Enter the {name} sequence (up to 12 characters; Enter means empty):")
        if len(text) <= 12:
            return text
        error("Use at most 12 characters.")


def create(kind):
    if kind.guide == "fibonacci":
        return (ask_int("Fibonacci index n (0–16)?", "n", min_value=0, max_value=16),)
    if kind.guide == "knapsack":
        weights = read_integers("weights", 8, 1)
        while True:
            values = read_integers("values", 8)
            if len(weights) == len(values):
                break
            error("Weights and values must have the same length.")
        capacity = ask_int("Capacity (0–30)?", "capacity", min_value=0, max_value=30)
        return weights, values, capacity
    if kind.guide == "longest-common-subsequence":
        return read_sequence("first"), read_sequence("second")
    return (read_integers("coin denominations", 6, 1),
            ask_int("Target amount (0–30)?", "target", min_value=0, max_value=30))


def example(kind):
    info("Loaded the example inputs.")
    return {"fibonacci": (5,), "knapsack": ([2, 3, 4, 5], [3, 4, 5, 8], 7),
            "longest-common-subsequence": ("ABCBDAB", "BDCABA"), "coin-change": ([1, 3, 4], 6)}[kind.guide]


def random_example(kind):
    info("Generated small random inputs; Type inputs lets you choose their sizes.")
    if kind.guide == "fibonacci":
        return (random.randint(2, 8),)
    if kind.guide == "knapsack":
        n = random.randint(2, 5)
        return [random.randint(1, 6) for _ in range(n)], [random.randint(1, 9) for _ in range(n)], random.randint(4, 12)
    if kind.guide == "longest-common-subsequence":
        return tuple("".join(random.choice("ABCD") for _ in range(random.randint(3, 7))) for _ in range(2))
    return sorted(random.sample(range(1, 7), 3)), random.randint(4, 12)


def display(kind, data):
    if kind.guide == "fibonacci":
        info(f"Index n: {data[0]}. Base values: F(0) = 0 and F(1) = 1.")
    elif kind.guide == "knapsack":
        render.dp_items(*data)
    elif kind.guide == "longest-common-subsequence":
        info(f"First sequence: {data[0]!r}; second sequence: {data[1]!r}.")
    else:
        info(f"Coins: {sorted(set(data[0]))}; target: {data[1]}. Coins can be reused; duplicate denominations merge.")


def operations(kind, data):
    if kind.guide == "fibonacci":
        actions = [(name, lambda function=function: solve(kind, data, function)) for name, function in (
            ("Plain Recursion", dp.fibonacci_recursive), ("Memoization", dp.fibonacci_memoized),
            ("Table", dp.fibonacci_table))]
        actions.append(("Compare Call Counts", lambda: compare(data[0])))
    elif kind.guide == "coin-change":
        actions = [("Fewest Coins", lambda: solve(kind, data, dp.minimum_coins)),
                   ("Count Ways", lambda: solve(kind, data, dp.coin_change_ways))]
    else:
        actions = [("Solve", lambda: solve(kind, data, kind.function))]
    return [*actions, ("Display", lambda: display(kind, data))]


def solve(kind, data, function):
    render.explanation(kind.guide)
    trace, stats = [], dp.DPStats()
    answer = function(*data, trace=trace, stats=stats)

    def all_states(events):
        for number, event in enumerate(events, 1):
            render.dp_step(number, event)

    stepper.play(trace, render.dp_step, summary=all_states)
    if len(trace) > stepper.MANY_STEPS:
        last = next((event for event in reversed(trace) if event.snapshot), None)
        if last:
            render.dp_step(len(trace), last)
    if kind.guide == "fibonacci":
        result(f"F({data[0]}) = {answer}; calls: {stats.calls}; states computed: {stats.cells}.")
        if function is not dp.fibonacci_table:
            if data[0] <= 6:
                render.recursion_tree(trace, "Fibonacci call tree", "dp_call")
            else:
                info("The full call tree is drawn for n up to 6. Larger runs keep the narrated calls.")
    elif kind.guide == "knapsack":
        result(f"Best value: {answer.value}; chosen item indexes: {list(answer.items)}.")
    elif kind.guide == "longest-common-subsequence":
        result(f"Common subsequence: {answer.sequence!r}; length: {len(answer.sequence)}.")
    elif function is dp.minimum_coins:
        if answer.count is None:
            result("The target cannot be made with these coins.")
        else:
            result(f"Fewest coins: {answer.count}; chosen coins: {list(answer.coins)}.")
    else:
        result(f"Number of ways: {answer} (unordered combinations).")


def compare(n):
    rows = []
    for name, function in (("Plain recursion", dp.fibonacci_recursive), ("Memoization", dp.fibonacci_memoized), ("Table", dp.fibonacci_table)):
        stats = dp.DPStats()
        value = function(n, stats=stats)
        rows.append((name, value, stats.calls, stats.cells))
    render.fibonacci_comparison(rows)
    info("Calls count function entries, including memo cache hits. The table method has one call; states count computed entries. Integer arithmetic and rendering take additional work.")
