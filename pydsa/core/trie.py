"""Trie (prefix tree) of strings.

insert(), search() and delete() take an optional trace list and record the path they walked through the
nodes, as TraceEvents whose snapshot is the prefix spelled so far.
"""

from pydsa.algorithms.trace import record
from pydsa.core.errors import DuplicateError, InvalidTypeError, NotFoundError


class TrieNode:
    """Node of a trie: one child per next character, and a mark if the path to it spells a word."""

    def __init__(self):
        self.children = {}  # Character -> child node
        self.is_word = False


class Trie:
    """Case-sensitive trie that stores unique, non-empty words."""

    def __init__(self, words=()):
        self.root = TrieNode()
        self.word_count = 0
        for word in words:
            self.insert(word)

    @staticmethod
    def _check(text, what="word"):
        if not isinstance(text, str):
            raise InvalidTypeError(f"A {what} must be a str.")

    def __len__(self):
        return self.word_count

    def _find(self, prefix, trace=None):
        """Return the node where the path spelling prefix ends, or None if there's no such path."""
        self._check(prefix, "prefix")
        node = self.root
        for position, char in enumerate(prefix, start=1):
            spelled = prefix[:position]
            node = node.children.get(char)
            if node is None:
                record(trace, "no_link", spelled, {spelled: "missing"}, char=char, prefix=spelled)
                return None
            record(trace, "follow", spelled, {spelled: "checked"}, char=char, prefix=spelled)
        return node

    def insert(self, word, trace=None):
        """Insert word and return how many new nodes it needed."""
        self._check(word)
        if not word:
            raise ValueError("A word needs at least one character.")
        node, added = self.root, 0
        for position, char in enumerate(word, start=1):
            spelled = word[:position]
            if char not in node.children:
                node.children[char] = TrieNode()
                added += 1
                record(trace, "new_node", spelled, {spelled: "new"}, char=char, prefix=spelled)
            else:
                record(trace, "follow", spelled, {spelled: "checked"}, char=char, prefix=spelled)
            node = node.children[char]
        if node.is_word:
            raise DuplicateError(f"{word!r} is already in the trie.")
        node.is_word = True
        self.word_count += 1
        record(trace, "mark_word", word, {word: "new"}, word=word)
        return added

    def search(self, word, trace=None):
        """Return True if word was inserted (a prefix of another word doesn't count)."""
        node = self._find(word, trace)
        found = node is not None and node is not self.root and node.is_word
        if node is not None:
            record(trace, "is_word" if found else "not_word", word, {word: "checked"}, word=word)
        return found

    def __contains__(self, word):
        return self.search(word)

    def starts_with(self, prefix):
        """Return True if at least one word starts with prefix."""
        node = self._find(prefix)
        return node is not None and (node.is_word or bool(node.children))

    def autocomplete(self, prefix=""):
        """Return every word that starts with prefix, in alphabetical order."""
        node = self._find(prefix)
        words = []
        if node is not None:
            self._collect(node, prefix, words)
        return words

    def words(self):
        """Return every word in alphabetical order."""
        return self.autocomplete()

    def _collect(self, node, spelled, words):
        """Add the words below node to words, depth first with the children in character order."""
        if node.is_word:
            words.append(spelled)
        for char in sorted(node.children):
            self._collect(node.children[char], spelled + char, words)

    def delete(self, word, trace=None):
        """Delete word, prune the nodes that no longer lead to any word and return how many were pruned."""
        self._check(word)
        path = [self.root]
        for char in word:
            child = path[-1].children.get(char)
            if child is None:
                break
            path.append(child)
        if len(path) != len(word) + 1 or not word or not path[-1].is_word:
            raise NotFoundError(f"{word!r} isn't in the trie.")

        path[-1].is_word = False
        self.word_count -= 1
        record(trace, "unmark", word, {word: "checked"}, word=word)
        pruned = 0
        # Walk back toward the root, removing nodes that end no word and have no children left
        for depth in range(len(word), 0, -1):
            node = path[depth]
            if node.is_word or node.children:
                record(trace, "keep_node", word[:depth], {word[:depth]: "checked"}, prefix=word[:depth])
                break
            del path[depth - 1].children[word[depth - 1]]
            pruned += 1
            record(trace, "prune", word[:depth - 1], {word[:depth]: "removed"}, prefix=word[:depth])
        return pruned

    def node_count(self):
        """Return the number of nodes, not counting the root."""
        count, stack = 0, [self.root]
        while stack:
            node = stack.pop()
            count += len(node.children)
            stack.extend(node.children.values())
        return count
