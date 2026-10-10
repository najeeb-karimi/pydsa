"""Bounded recursive examples, every Hanoi move and every queen placement and undo."""

import random

from pydsa.algorithms import backtracking as core
from pydsa.content import texts
from pydsa.ui import render, stepper
from pydsa.ui.console import ask_int, info, result
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu, topic_option
from pydsa.ui.screens.dynamic_programming import read_integers
from pydsa.ui.screens.sorting_algorithms import Algorithm

KINDS = (
    Algorithm("Tower of Hanoi", core.hanoi, "tower-of-hanoi"),
    Algorithm("Permutations", core.permutations, "permutations"),
    Algorithm("N-Queens", core.n_queens, "n-queens"),
)


def run():
    render.intro(texts.RECURSION_BACKTRACKING_ASCII, "recursion-backtracking")
    return Menu("Which recursion or backtracking problem?", [
        [topic_option(kind.guide, kind.name, lambda kind=kind: open_kind(kind)) for kind in KINDS],
        [("Read the Guide", lambda: render.guide("recursion-backtracking")), back_option()],
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


def create(kind):
    if kind.guide == "permutations":
        return read_integers("items", 4, -30)
    maximum = 10 if kind.guide == "tower-of-hanoi" else 8
    return ask_int(f"Size n (0–{maximum})?", "n", min_value=0, max_value=maximum)


def example(kind):
    info("Loaded the example inputs.")
    return {"tower-of-hanoi": 3, "permutations": [1, 2, 3], "n-queens": 4}[kind.guide]


def random_example(kind):
    info("Generated small random inputs; Type inputs lets you choose their sizes.")
    if kind.guide == "permutations":
        return random.sample(range(1, 10), random.randint(2, 4))
    return random.randint(2, 5)


def display(kind, data):
    if kind.guide == "tower-of-hanoi":
        render.hanoi_pegs((tuple(range(data, 0, -1)), (), ()))
    elif kind.guide == "permutations":
        info(f"Items: {data}. Equal values at different positions may produce repeated permutations.")
    else:
        render.queens_board(data, ())


def operations(kind, data):
    return [("Solve", lambda: solve(kind, data)), ("Display", lambda: display(kind, data))]


def solve(kind, data):
    render.explanation(kind.guide)
    trace, stats = [], core.RecursionStats()
    answer = kind.function(data, trace, stats=stats)
    def all_states(events):
        for number, event in enumerate(events, 1):
            render.backtracking_step(number, event)

    stepper.play(trace, render.backtracking_step, summary=all_states)
    if kind.guide == "tower-of-hanoi":
        render.hanoi_pegs(((), (), tuple(range(data, 0, -1))))
        result(f"Total moves: {len(answer)} = 2^{data} - 1.")
        info("Move the smaller tower away, move the largest disk once, then move the smaller tower back: T(n) = 2T(n - 1) + 1, starting at T(0) = 0.")
    elif kind.guide == "permutations":
        result(f"Permutations: {len(answer)}; recursive calls: {stats.calls}.")
        render.recursion_tree(trace, "Permutation recursion tree", "rec_call")
        result(f"First permutation: {answer[0]!r}; last permutation: {answer[-1]!r}.")
    else:
        result(f"Solutions: {len(answer)}; candidate squares checked: {stats.choices}.")
        if answer:
            info("First solution (column indexes by row): " + repr(answer[0]) + ".")
            render.queens_board(data, answer[0])
        else:
            info("Every branch was exhausted; this board size has no solution.")
