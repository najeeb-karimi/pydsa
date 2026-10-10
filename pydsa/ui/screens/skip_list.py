"""Skip-list levels, seeded coin flips and right/down search paths."""

from pydsa.content import texts
from pydsa.core.errors import InvalidTypeError, NotFoundError
from pydsa.core.skip_list import SkipList
from pydsa.ui import random_data, render, stepper
from pydsa.ui.console import ask_int, ask_value, error, not_found, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu


def run():
    render.intro(texts.SKIP_LIST_ASCII, "skip-list")
    linked = Menu("🛠️ How do you want to create the skip list?", [
        [("Create an empty skip list", create), ("Use the example", example),
         ("Fill with random values", lambda: create(True))], [back_option()],
    ]).open()
    if linked is Nav.BACK:
        return Nav.BACK
    return operation_menu("skip list", "skip-list", operations(linked), new_label="New Skip List").run()


def create(random=False):
    kind = Menu("🤔 Which type of keys do you want?", [
        [("Numbers", lambda: "num"), ("Strings", lambda: "str")], [back_option()],
    ]).select()
    if kind is Nav.BACK:
        return Nav.BACK
    seed = ask_int("🎲 Seed for the level coin flips?", "seed")
    linked = SkipList(kind, seed)
    if random:
        trace = []
        for key in random_data.values(kind, random_data.ask_count("keys")):
            linked.insert(key, trace)
        stepper.play(trace, render.skip_step)
    success(f"Created the skip list with seed {seed}.")
    render.skip_list(linked)
    return linked


def example():
    linked = SkipList(seed=7)
    for key in (10, 20, 30, 40, 50, 60):
        linked.insert(key)
    success("Loaded the example skip list with seed 7.")
    render.skip_list(linked)
    return linked


def operations(linked):
    return [("Insert", lambda: operate(linked, "insert")), ("Delete", lambda: operate(linked, "delete")),
            ("Search", lambda: operate(linked, "search")), ("Display", lambda: render.skip_list(linked))]


def operate(linked, operation):
    key, trace = ask_value(linked.data_type, "key"), []
    try:
        node = getattr(linked, operation)(key, trace)
    except (InvalidTypeError, NotFoundError) as problem:
        stepper.play(trace, render.skip_step)
        error(str(problem))
        return
    stepper.play(trace, render.skip_step)
    if operation == "search":
        if node is None:
            not_found(f"Key {render.fmt(key)} is not in the skip list.")
        else:
            success(f"Found {render.fmt(key)} in the skip list.")
    else:
        success(f"{'Inserted' if operation == 'insert' else 'Deleted one occurrence of'} {render.fmt(key)}.")
    render.skip_list(linked)
