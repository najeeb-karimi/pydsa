# Doubly Linked List
> A doubly linked list links every node to both its next and its previous node. You can walk it in either direction, and a node can be unlinked using only its own links.

## What it is
In a doubly linked list, each [node](glossary:node) holds an item and two [links](glossary:link): next, which points to the following node, and prev, which points to the one before it. The head's prev link and the tail's next link are empty.

## How it works
Inserting a node updates up to four links: the new node's prev and next links, the next link of the node before it, and the prev link of the node after it. Deleting a node connects its two neighbors directly to each other, so the chain skips it in both directions.

Because every node knows the node before it, you can delete a node you've already reached without searching for its neighbor, and you can read the whole list backward, from the tail to the [head](glossary:head-and-tail).

## Real-life analogy
A train, where each car is coupled to the car in front of it and the car behind it. You can walk through the train in either direction, and taking a car out means coupling its two neighbors together.

## When to use it
- You need to move both forward and backward, like the history of a web browser or a music playlist.
- You remove items from the middle once you've found them, as a cache does when it throws out the item used longest ago.
- You're building a deque out of nodes.

## When to avoid it
- One direction is enough; a singly linked list uses less memory.
- You need to jump to positions; use an array.

## In PyDSA
- Like the singly linked list, this list only keeps its head, so reaching the end still means walking the whole list.
- `Display Forward` follows the next links. `Display Backward` finds the tail and then follows the prev links back to the head.
- Every change updates both the next and the prev links, so reading the list in either direction always gives the same items.
