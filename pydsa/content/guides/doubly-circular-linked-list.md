# Doubly Circular Linked List
> A doubly circular linked list links every node both ways and closes the loop in both directions: the tail's next link is the head, and the head's prev link is the tail. Both ends are always one step away.

## What it is
This list combines the other kinds. Each [node](glossary:node) has next and prev [links](glossary:link), like a doubly linked list, and its ends are joined into a loop, like a singly circular linked list. Walking forward from the tail brings you to the [head](glossary:head-and-tail), and walking backward from the head brings you to the tail.

## How it works
The list only needs to remember its head, because the tail is always the head's prev node.
- Inserting at the end links the new node in between the tail and the head.
- Inserting at the beginning does exactly the same, then makes the new node the head.
- Deleting any node connects its prev and next neighbors directly to each other.

Since the tail is a single link away from the head and every node knows both of its neighbors, inserting and deleting at either end is quick, and you can walk around the loop in both directions.

## Real-life analogy
A round table where every guest can pass a dish to the left or to the right. Nobody sits at the end of the table, and a dish can travel all the way around in either direction.

## When to use it
- You need quick work at both ends and also want to go around again, like a deque that wraps.
- Carousels and image sliders that move forward or backward and wrap around at the ends.
- Schedulers and memory managers that scan a loop of items in both directions.

## When to avoid it
- A simpler list does the job. Every extra link takes more memory and is one more thing to keep correct.
- You need to reach positions quickly; use an array.

## In PyDSA
- The list keeps only its head and reaches the tail through the head's prev link.
- `Display Backward` starts at the tail and follows the prev links around to the head.
- `Walk Around the Loop` asks which way to go: forward from the head along the next links, or backward from the tail along the prev links.
