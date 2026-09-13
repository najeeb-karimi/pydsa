"""Trie, checked against a set of words."""

import random

import pytest

from pydsa.core.errors import DuplicateError, InvalidTypeError, NotFoundError
from pydsa.core.trie import Trie


def random_word(rng):
    return "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))


def prefixes(words):
    """Every non-empty prefix of the words, which is exactly the set of nodes a pruned trie needs."""
    return {word[:end] for word in words for end in range(1, len(word) + 1)}


def test_random_operations_match_a_set():
    rng = random.Random(19)
    for _ in range(300):
        trie, model = Trie(), set()
        for _ in range(30):
            op = rng.choices(["insert", "delete", "search"], weights=[4, 2, 2])[0]
            word = random_word(rng)
            if op == "insert":
                if word in model:
                    with pytest.raises(DuplicateError):
                        trie.insert(word)
                else:
                    assert trie.insert(word) == len(prefixes(model | {word}) - prefixes(model))
                    model.add(word)
            elif op == "delete":
                if word in model:
                    assert trie.delete(word) == len(prefixes(model) - prefixes(model - {word}))
                    model.remove(word)
                else:
                    with pytest.raises(NotFoundError):
                        trie.delete(word)
            else:
                assert (word in trie) == (word in model)

            assert len(trie) == len(model)
            assert trie.words() == sorted(model)
            assert trie.node_count() == len(prefixes(model))  # Deleting never leaves dead branches behind
            prefix = random_word(rng)[:rng.randint(0, 2)]
            assert trie.starts_with(prefix) == any(word.startswith(prefix) for word in model)
            assert trie.autocomplete(prefix) == sorted(word for word in model if word.startswith(prefix))


def test_prefixes_are_not_words():
    trie = Trie(["card"])
    assert "car" not in trie and trie.starts_with("car")
    with pytest.raises(NotFoundError):
        trie.delete("car")
    assert "" not in trie


def test_delete_prunes_only_unused_nodes():
    trie = Trie(["car", "card", "cat"])
    assert trie.delete("car") == 0  # 'card' still uses every node of 'car'
    assert trie.delete("card") == 2  # 'd' and 'r' go, but 'ca' is shared with 'cat'
    assert trie.node_count() == 3
    assert trie.delete("cat") == 3
    assert trie.node_count() == 0 and len(trie) == 0


def test_invalid_words():
    trie = Trie(["Cat"])
    assert "cat" not in trie  # Case-sensitive
    with pytest.raises(ValueError):
        trie.insert("")
    with pytest.raises(InvalidTypeError):
        trie.insert(5)
    with pytest.raises(InvalidTypeError):
        trie.search(5)
