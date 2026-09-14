# Hash Set
> A hash set stores unique items and can tell you almost instantly whether an item is in it. It's a hash table that keeps keys without values.

## What it is
A hash set is a collection where every item appears at most once, in no particular order. Adding an item that's already there changes nothing. It's built like a hash table: a [hash function](glossary:hash-function) decides which [bucket](glossary:bucket) each item belongs in, so checking whether an item is present only means looking in one bucket.

Sets also support the operations you may know from math class:
- The union of A and B, written A ∪ B, holds every item that's in either set.
- The intersection, A ∩ B, holds the items that are in both sets.
- The difference, A − B, holds the items in A that aren't in B.
- A is a subset of B, written A ⊆ B, when every item of A is also in B.

## How it works
Adding, removing and checking an item work just like inserting, deleting and searching for a key in a hash table. The set operations are built from those checks:
- The union adds every item of both sets to a new set, ignoring duplicates along the way.
- The intersection goes through A and keeps each item that B contains.
- The difference goes through A and keeps each item that B doesn't contain.
- The subset check goes through A and stops as soon as it finds an item that B doesn't contain.

## Real-life analogy
The guest list of a party. Each name is on it once, the order doesn't matter, and the person at the door only needs to answer one question: is this name on the list? Comparing two guest lists shows who was invited to both parties, or to only one of them.

## When to use it
- Removing duplicates from a collection.
- Remembering what you've already seen, like the vertices you've visited in a graph search.
- Comparing groups, like finding the customers who bought both of two products.

## When to avoid it
- You need to count how often each item appears, or store something with each item; use a hash table.
- You need the items in sorted order, or in the order they were added.

## In PyDSA
- The hash set is built on the separate chaining hash table, and each item is stored as a key without a value.
- PyDSA gives you two sets, A and B, so you can try unions, intersections, differences and subset checks.
- Items can be of any type. The random sets use numbers from 1 to 20, so they overlap and repeated numbers are easy to spot.
