"""Sorting screen: every sorting algorithm on a list you type, plus a comparison of all of them.

The array screen sorts with the same algorithm list and runner.
"""

from typing import Callable, NamedTuple

from pydsa.algorithms import sorting
from pydsa.content import texts
from pydsa.ui import random_data, render, stepper
from pydsa.ui.console import ask_list, ask_order, error, info, plural, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu


class Algorithm(NamedTuple):
    """A sorting or searching algorithm, its guide and what to say when it can't handle the data."""

    name: str
    function: Callable
    guide: str  # The ID of its guide and topic
    limit: str = ""


SORTS = [
    Algorithm("Bubble Sort", sorting.bubble_sort, "bubble-sort"),
    Algorithm("Selection Sort", sorting.selection_sort, "selection-sort"),
    Algorithm("Insertion Sort", sorting.insertion_sort, "insertion-sort"),
    Algorithm("Quick Sort", sorting.quick_sort, "quick-sort"),
    Algorithm("Heap Sort", sorting.heap_sort, "heap-sort"),
    Algorithm("Shell Sort", sorting.shell_sort, "shell-sort"),
    Algorithm("Merge Sort", sorting.merge_sort, "merge-sort"),
    Algorithm("Counting Sort", sorting.counting_sort, "counting-sort",
              f"Counting Sort only sorts whole numbers (int) less than {sorting.COUNTING_RANGE_LIMIT:,} apart."),
    Algorithm("Radix Sort", sorting.radix_sort, "radix-sort",
              "Radix Sort only sorts whole numbers (int) that aren't negative."),
]

EXAMPLE = [170, 45, 75, 90, 802, 24, 2, 66]


def run():
    """Get a list to sort and run the sorting menu."""
    render.intro(texts.SORTING_ASCII, "sorting")
    items = Menu("🛠️ Do you want to type a list yourself or use the preloaded example?", [
        [("Type a list of numbers", lambda: create("num")),
         ("Type a list of words", lambda: create("str")),
         ("Use the example", example),
         ("Fill with random values", random_data.create_number_list)],
        [back_option()],
    ]).open()
    if items is Nav.BACK:
        return Nav.BACK

    return operation_menu("list", "sorting", operations(items), guides=[sort.guide for sort in SORTS],
                          new_label="New List").run()


def operations(items):
    """Return the sorting operations on items as (label, action) pairs."""
    return [
        *[(sort.name, lambda sort=sort: sort_copy(items, sort)) for sort in SORTS],
        ("Compare All Algorithms", lambda: compare(items)),
        ("Display", lambda: render.array(items)),
    ]


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
    render.explanation(sort.guide)
    if not sorting.accepts(sort.function, items):
        error(sort.limit)
        return False
    order = ask_order()
    stats = sorting.SortStats()
    before = list(items)  # The steps are played after the sorting is done, so the first list is kept here
    steps = stepper.play(sort.function(items, order, stats), render.list_step,
                         lambda events: render.sorting_steps(before, events))
    order_name = "ascending" if order == "asc" else "descending"
    success(f"Sorted {noun} in {order_name} order in {plural(len(steps), 'step')}, "
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
