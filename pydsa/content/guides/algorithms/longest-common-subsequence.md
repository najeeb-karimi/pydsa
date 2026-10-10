# Longest Common Subsequence

> Find a longest sequence that occurs in order in both strings. Its characters do not have to be adjacent.

## What it is
A subsequence preserves character order while allowing gaps; a substring requires adjacent characters.

## How it works
Each cell stores the best length for two prefixes. Matching characters extend the diagonal; a mismatch keeps the longer upper or left answer. Arrows remember the decision. Traceback takes characters on diagonal arrows, then reverses them. Ties move up, so one of several valid longest answers is returned.

## Real-life analogy
Compare two shopping lists and find the longest shared order of purchases, ignoring extra items between them.

## When to use it
Use it for comparing ordered sequences and understanding how a table can rebuild an answer.

## When to avoid it
Avoid it when you need consecutive matching text or when the product of the sequence lengths makes the full table too large.

## In PyDSA
Type two strings of up to 12 characters, including empty strings, or use example or random inputs. Solve fills length cells with direction arrows and rebuilds a subsequence. Python characters are Unicode code points. Wide tables switch to compact indexed rows.
