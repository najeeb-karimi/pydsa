"""Hash set screen, opened from the hash table screen. It works with two sets, A and B."""

from pydsa.content import complexity, texts
from pydsa.core.errors import NotFoundError
from pydsa.core.hash_set import HashSet
from pydsa.ui import random_data, render
from pydsa.ui.console import ask_int, ask_value, info, not_found, plural, result, success, yes_no
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt, set_items


def show_definition():
    render.definition(texts.HASH_SET_DEFINITION, complexity.HASH_SET)


def run():
    """Create two sets and run the hash set operation menu."""
    render.intro(texts.HASH_SET_ASCII, texts.HASH_SET_DEFINITION, complexity.HASH_SET)
    sets = Menu("🛠️ Do you want to create two sets yourself or use the preloaded example?", [
        [("Create two empty sets", create), ("Use the example", example), ("Fill with random values", fill_random)],
        [back_option()],
    ]).open()
    if sets is Nav.BACK:
        return Nav.BACK

    return operation_menu("hash sets", [
        ("Add", lambda: add(sets)),
        ("Remove", lambda: remove(sets)),
        ("Check Membership", lambda: contains(sets)),
        ("Union", lambda: result(f"A ∪ B = {set_items(sets['A'].union(sets['B']))}")),
        ("Intersection", lambda: result(f"A ∩ B = {set_items(sets['A'].intersection(sets['B']))}")),
        ("Difference", lambda: difference(sets)),
        ("Subset Check", lambda: subsets(sets)),
        ("Display", lambda: render.hash_sets(sets)),
    ], definition=show_definition, new_label="New Hash Set").run()


def create():
    """Ask for the number of buckets and return two empty sets."""
    size = ask_int("🔢 How many buckets should each set have?", "number of buckets", min_value=1)
    sets = {"A": HashSet(size), "B": HashSet(size)}
    success(f"Created two empty sets, A and B, with {plural(size, 'bucket')} each.")
    render.hash_sets(sets)
    return sets


def example():
    """Return the preloaded example sets."""
    sets = {"A": HashSet(5, [1, 2, 3, "Messi"]), "B": HashSet(5, [3, 4, "Messi", 2.5])}
    success("Loaded the example sets.")
    render.hash_sets(sets)
    return sets


def fill_random():
    """Ask for the number of buckets and random numbers, and return two sets of numbers from 1 to 20."""
    size = ask_int("🔢 How many buckets should each set have?", "number of buckets", min_value=1, max_value=random_data.MAX_ITEMS)
    count = ask_int("🎲 How many random numbers should each set get?", "count", min_value=1, max_value=random_data.MAX_ITEMS)
    # Numbers from a small range, so the two sets overlap and repeats show that a set keeps each item once
    sets = {name: HashSet(size, random_data.ints(count, 1, 20)) for name in ("A", "B")}
    success(f"Created two sets, A and B, from {plural(count, 'random number')} each. Repeated numbers were only added once.")
    render.hash_sets(sets)
    return sets


def pick_set(question):
    """Ask which of the two sets to use; return "A", "B" or Nav.BACK."""
    return Menu(question, [[("Set A", lambda: "A"), ("Set B", lambda: "B")], [back_option()]]).select()


def add(sets):
    name = pick_set("🤔 Which set do you want to add to?")
    if name is Nav.BACK:
        return
    item = ask_value()
    if sets[name].add(item):
        success(f"Added {fmt(item)} to set {name}.")
        render.hash_sets({name: sets[name]})
    else:
        info(f"{fmt(item)} is already in set {name}, so nothing changed.")


def remove(sets):
    name = pick_set("🤔 Which set do you want to remove from?")
    if name is Nav.BACK:
        return
    item = ask_value()
    try:
        sets[name].remove(item)
    except NotFoundError:
        not_found(f"{fmt(item)} isn't in set {name}, so nothing was removed.")
        return
    success(f"Removed {fmt(item)} from set {name}.")
    render.hash_sets({name: sets[name]})


def contains(sets):
    item = ask_value()
    result(f"Is {fmt(item)} in set A? {yes_no(item in sets['A'])}. Is it in set B? {yes_no(item in sets['B'])}.")


def difference(sets):
    """Let the user pick A − B or B − A and show it."""
    a, b = sets["A"], sets["B"]
    Menu("➖ Which difference do you want?", [
        [("A − B (the items in A but not in B)", lambda: result(f"A − B = {set_items(a.difference(b))}")),
         ("B − A (the items in B but not in A)", lambda: result(f"B − A = {set_items(b.difference(a))}"))],
        [back_option()],
    ]).select()


def subsets(sets):
    a, b = sets["A"], sets["B"]
    result(f"Is A a subset of B (A ⊆ B)? {yes_no(a.is_subset(b))}.")
    result(f"Is B a subset of A (B ⊆ A)? {yes_no(b.is_subset(a))}.")
