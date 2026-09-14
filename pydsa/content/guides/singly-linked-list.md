# Singly Linked List
> A singly linked list links every node to the next one only, so you can walk it in one direction, from the head to the tail. It's the simplest kind of linked list.

## What it is
In a singly linked list, each [node](glossary:node) holds an item and one [link](glossary:link), called next. The list itself only remembers its [head](glossary:head-and-tail). The tail is the node whose next link is empty, which PyDSA shows as `None`.

## How it works
- Inserting at the beginning creates a node whose next link points at the old head, then makes it the new head. Nothing else changes, so this is fast however long the list is.
- Inserting at a position walks to the node just before that position and links the new node in after it.
- Inserting at the end walks all the way to the tail first, because the list doesn't keep a reference to it.
- Deleting from the beginning makes the second node the new head.
- Deleting from the end has to find the node before the tail. With no links pointing backward, the only way is to walk there from the head.

## Real-life analogy
A one-way street where every house has a sign pointing to the next house. You can always go forward, but to get back to an earlier house, you have to start again from the first one.

## When to use it
- You mostly add and remove items at the front, as a stack does.
- You only ever go through the items in one direction.
- You want the smallest possible nodes, with just one link each.

## When to avoid it
- You often work at the end of the list or need to step backward. A doubly linked list handles both better.
- You need to reach positions quickly; use an array.

## In PyDSA
- The list keeps only its head, so `Insert at End` and `Delete from End` walk the whole list.
- The display draws the nodes from the head on the left to `None` on the right.
- You can insert at positions 0 to the length, and delete from positions 0 to the length minus 1.
