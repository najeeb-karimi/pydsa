# Linked List
> A linked list is a chain of nodes, where each node holds an item and a link to the next node. It grows and shrinks one node at a time without ever moving the other items.

## What it is
A linked list is a [data structure](glossary:data-structure) that keeps items in order, like an array, but stores each item in its own [node](glossary:node). A node holds its item and a [link](glossary:link) to the next node. The first node is called the [head](glossary:head-and-tail), and the last one the tail.

Linked lists come in four kinds:
- A singly linked list links each node to the next one, so you can only move forward.
- A doubly linked list also links each node to the previous one, so you can move both ways.
- A singly circular linked list links the tail back to the head, forming a loop.
- A doubly circular linked list links both ways and closes the loop in both directions.

## How it works
The nodes can be anywhere in memory, because each link says where the next node is. To insert a node, you create it and change a couple of links so the chain passes through it. Removing a node is the reverse: you change the links around it so the chain skips it. The other nodes stay where they are.

The catch is reaching a position. There are no indexes to jump to, so getting to the tenth node means starting at the head and following nine links. That's also why searching a linked list checks the nodes one by one.

## Real-life analogy
A treasure hunt, where each clue tells you where to find the next one. Adding a stop only means rewriting one clue, but to reach the tenth clue, you have to follow the first nine.

## When to use it
- You often add or remove items at the front, or right next to a node you've already reached.
- The number of items changes a lot, and you don't want to reserve space in advance.
- You're building other structures out of it, such as stacks, queues or the chains of a hash table.

## When to avoid it
- You need to jump to items by position; an array gets there right away.
- Memory is tight, since every node needs extra room for its links.
- Speed matters for large lists. Nodes scattered around memory are slower for the computer to read than values stored side by side.

## In PyDSA
- After the linked list opens, you pick one of the four kinds. You can also open a kind directly with its topic ID, such as `singly-linked-list`.
- Every kind holds items of any type and can start empty, from the example or with random items.
- Positions count from 0 at the head, and inserting at a position equal to the length adds the item at the end.
- `Search` uses Linear Search, following the links from the head until it finds the item.
