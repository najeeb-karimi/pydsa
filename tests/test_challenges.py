"""Prediction answers checked against simple independent models across random seeds."""

import itertools
import random

import pytest
from rich.cells import cell_len

from pydsa import topics
from pydsa.practice import challenges
from pydsa.ui.console import console


def shortest(edges):
    weights = {(u, v): weight for u, v, weight in edges}
    costs = []
    for length in range(4):
        for middle in itertools.permutations((1, 2, 3), length):
            path = (0, *middle, 4)
            pairs = list(zip(path, path[1:]))
            if all(pair in weights for pair in pairs):
                costs.append(sum(weights[pair] for pair in pairs))
    return min(costs)


def minimum_tree(edges):
    candidates = []
    for chosen in itertools.combinations(edges, 4):
        reached = {0}
        while True:
            more = {v for u, v, _ in chosen if u in reached} | {u for u, v, _ in chosen if v in reached}
            if more <= reached:
                break
            reached |= more
        if len(reached) == 5:
            candidates.append(sum(weight for _, _, weight in chosen))
    return min(candidates)


def expected(topic, state):
    values = state.get("values")
    if topic in ("segment-tree", "fenwick-tree"):
        values = list(values)
        values[state["index"]] = state["replacement"]
        return {"sum": sum, "min": min, "max": max}[state["operation"]](values[state["left"]:state["right"] + 1])
    if topic == "array":
        return values[state["index"]]
    if topic in ("red-black-tree", "b-tree"):
        return sorted([*values, state["target"]])
    if topic == "stack":
        return values[-1]
    if topic == "queue" or topic in challenges.LINKED:
        return values[0]
    if topic == "deque":
        return values[0 if state["front"] else -1]
    if topic in ("heap", "min-heap", "max-heap"):
        return max(values) if topic == "max-heap" else min(values)
    if topic == "priority-queue":
        return min(enumerate(state["entries"]), key=lambda pair: (pair[1][1], pair[0]))[1][0]
    if topic == "trie":
        return sorted(word for word in state["words"] if word.startswith(state["prefix"]))
    if topic in ("hash-table", "chaining-hash-table", "linear-probing-hash-table"):
        slot = state["target"] % state["size"]
        return (slot + len(state["keys"])) % state["size"] if topic == "linear-probing-hash-table" else slot
    if topic == "hash-set":
        return sorted(set(state["a"]) & set(state["b"]))
    if topic == "disjoint-set":
        root = state["element"]
        while state["parents"][root] != root:
            root = state["parents"][root]
        return root
    if topic == "sorting":
        output = list(values)
        for i in range(len(output) - 1):
            if output[i] > output[i + 1]:
                output[i], output[i + 1] = output[i + 1], output[i]
        return output
    if topic in challenges.SORTS:
        return sorted(values)
    if topic == "searching" or topic in challenges.SEARCHES:
        return values.index(state["target"])
    if topic == "topological-sort":
        return list(range(5))  # The chain forces a unique order.
    if topic == "cycle-detection":
        return any(u == 4 and v == 0 for u, v, _ in state["edges"])
    if topic in ("prim", "kruskal"):
        return minimum_tree(state["edges"])
    if topic in challenges.GRAPH_TOPICS:
        return shortest(state["edges"])
    if topic in ("tree", "bst", "avl-tree") and not state["level"]:
        return sorted(values)
    return None  # Level order is checked against a separately constructed core tree below.


def test_every_registered_topic_has_a_prediction():
    assert challenges.SUPPORTED == {topic.id for topic in topics.TOPICS}


@pytest.mark.parametrize("topic", [entry.id for entry in topics.TOPICS])
def test_prediction_matches_models_and_real_result(topic):
    for seed in range(30):
        challenge = challenges.make(topic, random.Random(seed))
        reference = expected(topic, challenge.state)
        if reference is None:
            tree = challenges.AVLTree("num") if topic == "avl-tree" else challenges.BinarySearchTree("num")
            for value in challenge.state["values"]:
                tree.insert(value)
            reference = tree.level_order()
        assert challenge.answer == reference
        assert challenge.solve() == challenge.answer == challenge.solve()  # Cloning keeps retries independent.
        assert challenge.check(repr(challenge.answer))
        assert not challenge.check("definitely not the answer")


@pytest.mark.parametrize("width", [45, 90])
def test_every_prediction_can_draw_with_no_color(width, capsys):
    console.width = width
    console.no_color = True
    for entry in topics.TOPICS:
        challenges.make(entry.id, random.Random(1)).draw()
        out = capsys.readouterr().out
        assert out and all(cell_len(line) <= width for line in out.splitlines()), entry.id


def test_answer_formats():
    challenge = challenges.make("sorting", random.Random(2))
    assert challenge.check(", ".join(map(str, challenge.answer)))
    assert not challenge.check("[True]")
    numeric = challenges.make("array", random.Random(1))
    assert not numeric.check("True")
    word = challenges.make("priority-queue", random.Random(1))
    assert word.check(word.answer) and word.check(repr(word.answer))
