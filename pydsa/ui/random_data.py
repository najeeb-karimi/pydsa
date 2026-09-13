"""Random data for the create flows: values, words, number lists, key-value pairs, unions and graph edges."""

import random

from pydsa.ui import render
from pydsa.ui.console import ask_int, plural, success
from pydsa.ui.menu import Menu, Nav, back_option

MAX_ITEMS = 50  # The most random values a create flow offers, so the displays stay readable
MAX_VERTICES = 10
MAX_WEIGHT = 20

WORDS = ("apple", "banana", "berry", "cherry", "date", "fig", "grape", "kiwi",
         "lemon", "lime", "mango", "melon", "olive", "peach", "pear", "plum")
# Words that share their beginnings, so a random trie has branches worth looking at
TRIE_WORDS = ("car", "card", "care", "cart", "cat", "do", "dog", "done",
              "dot", "sun", "sunny", "tea", "team", "tear", "ten", "tent")

ARRANGEMENTS = {
    "random": "In random order",
    "sorted": "Already sorted",
    "reversed": "Sorted backwards",
    "duplicates": "With lots of duplicates",
}


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def ints(count, low=1, high=99, rng=random):
    return [rng.randint(low, high) for _ in range(count)]


def words(count, rng=random):
    """Return count random words, all different while there are enough words to go around."""
    if count <= len(WORDS):
        return rng.sample(WORDS, count)
    return [rng.choice(WORDS) for _ in range(count)]


def values(kind, count, rng=random):
    """Return count random values: ints for "int" or "num", words for "str", and a mix of both for "any"."""
    if kind in ("int", "num"):
        return ints(count, rng=rng)
    if kind == "str":
        return words(count, rng)
    return [rng.randint(1, 99) if rng.random() < 0.5 else rng.choice(WORDS) for _ in range(count)]


def number_list(count, arrangement, rng=random):
    """Return count random ints arranged as one of ARRANGEMENTS."""
    if arrangement == "duplicates":
        pool = ints(max(2, count // 3), rng=rng)
        numbers = [rng.choice(pool) for _ in range(count)]
    else:
        numbers = ints(count, 1, 999, rng)
    if arrangement == "sorted":
        numbers.sort()
    elif arrangement == "reversed":
        numbers.sort(reverse=True)
    return numbers


def trie_words(count, rng=random):
    """Return count different words from TRIE_WORDS."""
    return rng.sample(TRIE_WORDS, count)


def key_value_pairs(count, rng=random):
    """Return count (int key, word value) pairs with different keys."""
    keys = rng.sample(range(1, max(100, 3 * count)), count)
    return [(key, rng.choice(WORDS)) for key in keys]


def priority_items(count, rng=random):
    """Return count (word, priority from 1 to 5) pairs."""
    return [(rng.choice(WORDS), rng.randint(1, 5)) for _ in range(count)]


def unions(size, count, rng=random):
    """Return count random pairs of elements from 0 to size - 1."""
    return [(rng.randrange(size), rng.randrange(size)) for _ in range(count)]


def edge_limits(vertex_count, directed, connected):
    """Return the fewest and the most edges a random graph with vertex_count vertices can have."""
    most = vertex_count * (vertex_count - 1) // (1 if directed else 2)
    fewest = vertex_count - 1 if connected and vertex_count > 1 else 0
    return fewest, most


def edges(vertices, count, directed, connected, rng=random):
    """Return count random (u, v, weight) edges between different vertices, never repeating a pair.

    When connected, the first edges form a tree that reaches every vertex from the first one, following the
    edge directions, so count must be at least len(vertices) - 1.
    """
    vertices = list(vertices)
    position = {vertex: index for index, vertex in enumerate(vertices)}

    def pair(u, v):
        # An undirected edge is always spelled (earlier vertex, later vertex), so each pair appears once
        return (u, v) if directed or position[u] < position[v] else (v, u)

    chosen = []
    if connected:
        reached = vertices[:1]
        for vertex in rng.sample(vertices[1:], len(vertices) - 1):
            chosen.append(pair(rng.choice(reached), vertex))
            reached.append(vertex)
    taken = set(chosen)
    others = [(u, v) for u in vertices for v in vertices if u != v and pair(u, v) == (u, v) and (u, v) not in taken]
    rng.shuffle(others)
    chosen += others[:max(0, count - len(chosen))]
    return [(u, v, rng.randint(1, MAX_WEIGHT)) for u, v in chosen]


# ---------------------------------------------------------------------------
# Prompts shared by the create flows
# ---------------------------------------------------------------------------

def ask_count(what, maximum=MAX_ITEMS):
    """Ask how many random items to create, as in "How many random keys do you want?"."""
    return ask_int(f"🎲 How many random {what} do you want?", "count", min_value=1, max_value=maximum)


def ask_capacity_and_count(noun):
    """Ask for the capacity of a fixed-size structure and how many random items it starts with; return both."""
    capacity = ask_int(f"↔️ How many items should the {noun} be able to hold?", "size", min_value=1, max_value=MAX_ITEMS)
    count = ask_int("🎲 How many random items should it start with?", "count", min_value=0, max_value=capacity)
    return capacity, count


def create_number_list():
    """Ask for a size and an arrangement, show a random list of numbers and return it (or Nav.BACK)."""
    count = ask_count("numbers")
    arrangement = Menu("🔀 How should the numbers be arranged?", [
        [(label, lambda arrangement=arrangement: arrangement) for arrangement, label in ARRANGEMENTS.items()],
        [back_option()],
    ]).select()
    if arrangement is Nav.BACK:
        return Nav.BACK
    items = number_list(count, arrangement)
    success(f"Created a list of {plural(count, 'random number')}, {ARRANGEMENTS[arrangement].lower()}.")
    render.array(items)
    return items
