# Trie
> A trie, pronounced "try", stores words letter by letter in a tree, so words that start the same way share the same path. Finding a word takes as many steps as the word has letters, however many words the trie holds.

## What it is
A trie, also called a prefix tree, is a tree for storing strings. Each edge stands for one character, so the path from the [root](glossary:root) to any [node](glossary:node) spells out a [prefix](glossary:prefix). Words that share a prefix share those nodes. A node is marked when its path spells a complete word, which is how the trie tells the word "car" apart from the start of "card".

## How it works
- Inserting a word follows its characters from the root, creating every node that doesn't exist yet, and marks the last node as the end of a word.
- Searching follows the characters the same way. The word is there only if the whole path exists and its last node is marked.
- A prefix check only needs the path to exist.
- Autocomplete follows the prefix's path, then collects every marked node below the point where it ends.
- Deleting a word removes its mark, then walks back toward the root, removing the nodes that no longer lead to any word. Nodes that other words still use stay where they are.

None of these depend on how many words the trie holds, only on how long the word or prefix is.

## Real-life analogy
A dictionary with thumb tabs. You open the section for "c", then find "ca", then "car", narrowing it down letter by letter, and every word that starts with "car" is right there together.

## When to use it
- Autocomplete and search suggestions while someone is typing.
- Spell checkers and word games that test whether a word or a prefix exists.
- Routing tables that match addresses by the longest prefix they know.

## When to avoid it
- You only need to know whether whole words exist; a hash set is simpler and uses much less memory.
- Your strings don't share prefixes, so the trie saves nothing and every node costs memory.

## In PyDSA
- The trie is case-sensitive, so "Cat" and "cat" are different words. Every word needs at least one character.
- Inserting a word that's already in the trie changes nothing.
- The display shows the trie as a tree of characters, with a ✓ on every node that ends a word.
- `Autocomplete` with an empty prefix lists every word, in alphabetical order.
