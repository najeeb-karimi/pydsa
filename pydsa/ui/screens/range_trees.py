"""Range-query trees built from numeric arrays, with visible ranges and binary jumps."""

from typing import Callable, NamedTuple

from pydsa.content import notes, texts
from pydsa.core.errors import InvalidTypeError
from pydsa.core.fenwick_tree import FenwickTree
from pydsa.core.segment_tree import SegmentTree, numbers
from pydsa.ui import random_data, render, stepper
from pydsa.ui.console import ask_int, ask_list, ask_value, error, result, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu


class TreeKind(NamedTuple):
    guide: str
    name: str
    draw: Callable
    draw_step: Callable


SEGMENT = TreeKind("segment-tree", "segment tree", render.segment_tree, render.segment_step)
FENWICK = TreeKind("fenwick-tree", "Fenwick tree", render.fenwick_tree, render.fenwick_step)
EXAMPLE = (2, 1, 5, 3, 4, 7, 6, 8)


def run_segment():
    return run(SEGMENT)


def run_fenwick():
    return run(FENWICK)


def run(kind):
    render.intro(texts.SEGMENT_TREE_ASCII if kind is SEGMENT else texts.FENWICK_TREE_ASCII, kind.guide)
    tree = Menu(f"🛠️ How do you want to create the {kind.name}?", [
        [("Type an array of numbers", lambda: create(kind)),
         ("Use the example", lambda: create(kind, "example")),
         ("Fill with random values", lambda: create(kind, "random"))],
        [back_option()],
    ]).open()
    if tree is Nav.BACK:
        return Nav.BACK
    return operation_menu(kind.name, kind.guide, operations(tree, kind), new_label=f"New {kind.name}").run()


def ask_numbers():
    while True:
        values = ask_list("✍️ Enter numbers separated by commas (at most 50):", "num", "numbers")
        try:
            numbers(values)
        except InvalidTypeError as problem:
            error(str(problem))
            continue
        if len(values) > random_data.MAX_ITEMS:
            error("Use at most 50 numbers so the steps stay readable.")
            continue
        return values


def create(kind, mode="typed"):
    operation = "sum"
    if kind is SEGMENT:
        operation = Menu("🤔 What should each range store?", [
            [("Sum", lambda: "sum"), ("Minimum", lambda: "min"), ("Maximum", lambda: "max")],
            [back_option()],
        ]).select()
        if operation is Nav.BACK:
            return Nav.BACK
    values = list(EXAMPLE) if mode == "example" else (
        random_data.ints(random_data.ask_count("numbers"), low=-20, high=50) if mode == "random" else ask_numbers())
    tree = SegmentTree(operation=operation) if kind is SEGMENT else FenwickTree()
    render.operation_note(notes.find(kind.guide, "Build from Array"))
    build(tree, kind, values)
    return tree


def operations(tree, kind):
    queries = [("Range Query", lambda: range_query(tree, kind))] if kind is SEGMENT else [
        ("Prefix Sum", lambda: prefix(tree)), ("Range Sum", lambda: range_query(tree, kind))]
    return [
        ("Build from Array", lambda: build(tree, kind, ask_numbers())),
        *queries,
        ("Point Update", lambda: update(tree, kind)),
        ("Display", lambda: kind.draw(tree)),
    ]


def build(tree, kind, values):
    trace = []
    tree.build(values, trace)
    stepper.play(trace, kind.draw_step)
    success(f"Built the {kind.name} from {len(tree)} numbers.")
    kind.draw(tree)


def range_query(tree, kind):
    left = ask_int("↔️ Range start (zero-based, inclusive):", "range start", min_value=0, max_value=len(tree) - 1)
    right = ask_int("↔️ Range end (inclusive):", "range end", min_value=left, max_value=len(tree) - 1)
    trace = []
    value = tree.query(left, right, trace) if kind is SEGMENT else tree.range_sum(left, right, trace)
    stepper.play(trace, kind.draw_step)
    operation = tree.operation if kind is SEGMENT else "sum"
    result(f"Range [{left}, {right}] {operation}: {render.fmt(value)}.")


def prefix(tree):
    end = ask_int("↔️ Prefix end (inclusive; -1 is empty):", "prefix end", min_value=-1, max_value=len(tree) - 1)
    trace = []
    value = tree.prefix_sum(end, trace)
    stepper.play(trace, render.fenwick_step)
    result(f"Prefix [0, {end}] sum: {render.fmt(value)}.")


def update(tree, kind):
    position = ask_int("📍 Which array index should change?", "index", min_value=0, max_value=len(tree) - 1)
    while True:
        value = ask_value("num", "replacement value")
        trace = []
        try:
            tree.update(position, value, trace)
        except InvalidTypeError as problem:
            error(str(problem))
            continue
        break
    stepper.play(trace, kind.draw_step)
    success(f"Replaced index {position} with {render.fmt(value)}.")
    kind.draw(tree)
