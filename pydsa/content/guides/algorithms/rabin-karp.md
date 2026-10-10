# Rabin-Karp
> Rabin-Karp searches using a rolling hash of each text window. Every equal hash is checked against the real characters, so collisions never become false matches.

## What it is
Rabin-Karp uses a numeric fingerprint to rule out many windows before comparing characters. A [collision](glossary:collision) occurs when different strings have the same fingerprint. An equal hash with unequal characters is called a spurious hit.

## How it works
1. Hash the pattern and the first equally sized text window using character codes, base 256 and a modulus.
2. Display the window hash beside the pattern hash.
3. If the hashes match, compare the actual characters. Record a real match or report a spurious hit.
4. Remove the outgoing character's weighted contribution, multiply by the base and add the incoming character, all modulo the chosen number.
5. Repeat for every window, shifting one position so overlaps remain visible.

A small modulus makes collisions easier to find. Verification preserves correctness, but many collisions can erase the filtering benefit. Many genuine overlapping matches also cost comparisons because each must be verified. Hash arithmetic takes work even when no character comparisons are needed.

## Real-life analogy
Check a quick label on each box before opening it to inspect the contents. Equal labels make a box worth checking, but do not prove that its contents match.

## When to use it
- Hashes can cheaply filter most windows before detailed comparison.
- You want to learn how rolling updates and collisions behave.

## When to avoid it
- An adversarial input or small modulus causes too many hash hits.
- You need KMP's predictable growth on repeated patterns.

## In PyDSA
- Choose the modulus for each run or comparison. The usual example uses 101; choose 2 to demonstrate spurious hits, such as searching for `a` in `acb`.
- Each window shows both hashes, and rolling steps show the outgoing and incoming character codes and the update formula.
- Verified hits mark matching and mismatching characters. The result contains only real match positions.
- The comparison table counts character checks separately from hash arithmetic. Guides, code views, quizzes, predictions and a hash-filtering growth experiment complete the topic.
