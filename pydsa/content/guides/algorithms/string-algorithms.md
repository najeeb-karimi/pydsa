# String Algorithms
> String search finds every place where a pattern occurs in a longer text. Naive search, KMP and Rabin-Karp return the same matches while choosing different ways to avoid unnecessary comparisons.

## What it is
A text is a sequence of characters, and a pattern is the sequence you want to find inside it. Matches are reported by their starting indexes. Overlapping occurrences count separately: searching for `aa` in `aaaa` gives `[0, 1, 2]`.

## How it works
- Naive search places the pattern at every possible start and compares characters until a mismatch.
- KMP first records which pattern prefixes are also suffixes. It uses that table to shift while keeping comparisons it already knows are matches.
- Rabin-Karp rolls a numeric hash across fixed-size windows. Equal hashes are verified character by character because different strings can collide.

An empty pattern matches every boundary, including after the last character. A pattern longer than the text has no matches. Searches are case-sensitive and count Python Unicode characters, so spaces are part of the input.

## Real-life analogy
Find a phrase on a page. You can check every starting letter, remember repeated pieces of the phrase, or use a quick fingerprint to choose which candidate phrases need a closer look.

## When to use it
- Locate words, motifs or markers in text.
- Compare how repeated patterns or hash collisions change search work.

## When to avoid it
- You need fuzzy spelling, case folding or regular-expression rules; these searches use exact equality.
- Your goal is only ordinary text lookup in an application; Python's built-in search is usually simpler.

## In PyDSA
- Type text and pattern, use the repeated-prefix example or generate random strings. Empty input and spaces are preserved.
- Text is capped at eighty characters and the pattern at twenty to keep step views readable.
- Watch alignments, the KMP prefix table and rolling hashes. Choose modulus 2 to expose collisions on purpose.
- Compare search, prefix-table and total character comparisons on identical input. Hash arithmetic is excluded from this table.
- Guides, code views, quizzes, predictions and growth experiments are available for all three searches.
