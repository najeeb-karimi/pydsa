# Permutations

> List all arrangements of input positions. A recursion tree shows each growing prefix and its branches.

## What it is
A permutation is an ordering of every input position exactly once.

## How it works
Choose any unused position for the next place. Recurse with its value appended to the prefix, then remove it and mark that position unused again. A full prefix is an answer. Distinct positions remain separate even if their values are equal, so equal-valued inputs can produce repeated arrangements.

## Real-life analogy
Try every possible seating order by placing one guest, seating the remaining guests, then clearing that choice for the next trial.

## When to use it
Use it to enumerate small arrangements or teach systematic choice and undo.

## When to avoid it
Avoid generating all arrangements for many items; factorial growth quickly overwhelms memory and time.

## In PyDSA
Type up to 4 integer items from -30 to 30, use three items or generate random inputs. Solve narrates branches and completed arrangements, counts results and shows first and last answers. The full recursion tree is drawn for every supported input size. Empty input has one empty permutation; the separate growth experiment runs up to 6 items without retaining trace snapshots.
