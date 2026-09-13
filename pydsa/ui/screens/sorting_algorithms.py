"""Sorting screen: every sorting algorithm on a list you type, plus a comparison of all of them.

The array screen sorts with the same algorithm list and runner.
"""

from typing import Callable, NamedTuple

from pydsa.algorithms import sorting
from pydsa.content import complexity, texts
from pydsa.ui import render
from pydsa.ui.console import ask_list, ask_order, error, info, plural, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu


class Algorithm(NamedTuple):
    """A sorting or searching algorithm, its explanation and what to say when it can't handle the data."""

    name: str
    function: Callable
    info: str
    limit: str = ""


SORTS = [
    Algorithm("Bubble Sort", sorting.bubble_sort, texts.BUBBLE_SORT_INFO),
    Algorithm("Selection Sort", sorting.selection_sort, texts.SELECTION_SORT_INFO),
    Algorithm("Insertion Sort", sorting.insertion_sort, texts.INSERTION_SORT_INFO),
    Algorithm("Quick Sort", sorting.quick_sort, texts.QUICK_SORT_INFO),
    Algorithm("Heap Sort", sorting.heap_sort, texts.HEAP_SORT_INFO),
    Algorithm("Shell Sort", sorting.shell_sort, texts.SHELL_SORT_INFO),
    Algorithm("Merge Sort", sorting.merge_sort, texts.MERGE_SORT_INFO),
    Algorithm("Counting Sort", sorting.counting_sort, texts.COUNTING_SORT_INFO,
              f"Counting Sort only sorts whole numbers (int) less than {sorting.COUNTING_RANGE_LIMIT:,} apart."),
    Algorithm("Radix Sort", sorting.radix_sort, texts.RADIX_SORT_INFO,
              "Radix Sort only sorts whole numbers (int) that aren't negative."),
]

EXAMPLE = [170, 45, 75, 90, 802, 24, 2, 66]


def show_definition():
    render.definition(texts.SORTING_DEFINITION, complexity.SORTING)


def run():
    """Get a list to sort and run the sorting menu."""
    render.intro(texts.SORTING_ASCII, texts.SORTING_DEFINITION, complexity.SORTING)
    items = Menu("🛠️ Do you want to type a list yourself or use the preloaded example?", [
        [("Type a list of numbers", lambda: create("num")),
         ("Type a list of words", lambda: create("str")),
         ("Use the example", example)],
        [back_option()],
    ]).open()
    if items is Nav.BACK:
        return Nav.BACK

    return operation_menu("list", [
        *[(sort.name, lambda sort=sort: sort_copy(items, sort)) for sort in SORTS],
        ("Compare All Algorithms", lambda: compare(items)),
        ("Display", lambda: render.array(items)),
    ], definition=show_definition, new_label="New List", home_label="Main Menu").run()


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


def run_sort(items, sort, noun):
    """Explain sort, then sort items in place with it, showing every step; return False if it can't sort items.

    noun names the data in messages, as in "the array".
    """
    render.explanation(f"How {sort.name} Works", sort.info)
    if not sorting.accepts(sort.function, items):
        error(sort.limit)
        return False
    order = ask_order()
    stats = sorting.SortStats()
    steps = render.sorting_steps(items, sort.function(items, order, stats))
    order_name = "ascending" if order == "asc" else "descending"
    success(f"Sorted {noun} in {order_name} order in {plural(steps, 'step')}, "
            f"with {plural(stats.comparisons, 'comparison')} and {plural(stats.writes, 'write')}.")
    return True


def sort_copy(items, sort):
    """Sort a copy of items, so every algorithm can be tried on the same list."""
    copy = list(items)
    if run_sort(copy, sort, "a copy of the list"):
        render.array(copy)
        info("The list itself is unchanged, so you can try another algorithm on it.")


def compare(items):
    """Run every algorithm on its own copy of items and show how much work each one did."""
    render.explanation("How the Comparison Works", texts.SORT_COMPARISON_INFO)
    order = ask_order()
    results = []
    for sort in SORTS:
        if not sorting.accepts(sort.function, items):
            results.append((sort.name, None, 0))
            continue
        stats = sorting.SortStats()
        steps = sum(1 for _ in sort.function(list(items), order, stats))
        results.append((sort.name, stats, steps))
    render.sort_comparison(results)
