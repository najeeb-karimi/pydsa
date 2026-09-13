"""Searching screen: every searching algorithm on a list you type.

The array screen searches with the same algorithm list and runner.
"""

from pydsa.algorithms import searching
from pydsa.content import complexity, texts
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_list, ask_value, error, not_found, plural, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt
from pydsa.ui.screens.sorting_algorithms import Algorithm

SEARCHES = [
    Algorithm("Linear Search", searching.linear_search, texts.LINEAR_SEARCH_INFO),
    Algorithm("Binary Search", searching.binary_search, texts.BINARY_SEARCH_INFO),
    Algorithm("Jump Search", searching.jump_search, texts.JUMP_SEARCH_INFO),
    Algorithm("Interpolation Search", searching.interpolation_search, texts.INTERPOLATION_SEARCH_INFO,
              "Interpolation Search only works on numbers, because it does math on the values."),
    Algorithm("Exponential Search", searching.exponential_search, texts.EXPONENTIAL_SEARCH_INFO),
]

EXAMPLE = [10, 1987, 672, 8, 2004, 42, 7, 300]


def show_definition():
    render.definition(texts.SEARCHING_DEFINITION, complexity.SEARCHING)


def run():
    """Get a list to search and run the searching menu."""
    render.intro(texts.SEARCHING_ASCII, texts.SEARCHING_DEFINITION, complexity.SEARCHING)
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
    ], definition=show_definition, new_label="New List").run()


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
    render.explanation(f"How {search.name} Works", search.info)
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
