"""Searching screen: every searching algorithm on a list you type.

The array screen searches with the same algorithm list and runner.
"""

from pydsa.algorithms import searching
from pydsa.content import texts
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_list, ask_value, error, not_found, plural, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt
from pydsa.ui.screens.sorting_algorithms import Algorithm

SEARCHES = [
    Algorithm("Linear Search", searching.linear_search, "linear-search"),
    Algorithm("Binary Search", searching.binary_search, "binary-search"),
    Algorithm("Jump Search", searching.jump_search, "jump-search"),
    Algorithm("Interpolation Search", searching.interpolation_search, "interpolation-search",
              "Interpolation Search only works on numbers, because it does math on the values."),
    Algorithm("Exponential Search", searching.exponential_search, "exponential-search"),
]

EXAMPLE = [10, 1987, 672, 8, 2004, 42, 7, 300]


def run():
    """Get a list to search and run the searching menu."""
    render.intro(texts.SEARCHING_ASCII, "searching")
    items = Menu("🛠️ Do you want to type a list yourself or use the preloaded example?", [
        [("Type a list of numbers", lambda: create("num")),
         ("Type a list of words", lambda: create("str")),
         ("Use the example", example),
         ("Fill with random values", random_data.create_number_list)],
        [back_option()],
    ]).open()
    if items is Nav.BACK:
        return Nav.BACK

    kind = "str" if isinstance(items[0], str) else "num"
    return operation_menu("list", [
        *[(search.name, lambda search=search: run_search(items, search, kind, "the list")) for search in SEARCHES],
        ("Display", lambda: render.array(items)),
    ], guides=["searching", *(search.guide for search in SEARCHES)], new_label="New List").run()


def create(kind):
    """Ask for a list of numbers or words (kind "num" or "str") and return it."""
    what = "numbers" if kind == "num" else "words"
    items = ask_list(f"✍️ Enter the {what}, separated by commas:", kind, what)
    success(f"Created a list of {plural(len(items), what[:-1])}.")
    render.array(items)
    return items


def example():
    success("Loaded the example list.")
    render.array(EXAMPLE)
    return list(EXAMPLE)


def run_search(items, search, kind, noun):
    """Explain search, ask for a target of the given kind and search items for it, showing the positions checked.

    noun names the data in messages, as in "the array".
    """
    render.explanation(search.guide)
    if not searching.accepts(search.function, items):
        error(search.limit)
        return
    target = ask_value(kind, "target")
    probes = []
    index = search.function(items, target, probes)
    checked = plural(len(probes), "position")
    if search.function is searching.linear_search:
        render.search_probes(items, probes, f"Checked {checked}, numbered in order under the values.")
    else:
        render.search_probes(sorted(items), probes, f"Searched this sorted copy and checked {checked}, numbered in order under the values.")
    if index == -1:
        not_found(f"{fmt(target)} isn't in {noun}.")
    else:
        success(f"Found {fmt(target)} at index {index}.")
