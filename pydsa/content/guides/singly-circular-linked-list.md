# Singly Circular Linked List
> A singly circular linked list is a singly linked list whose tail links back to its head, so the nodes form a loop. You can keep walking around it for as long as you like.

## What it is
In a singly circular linked list, every [node](glossary:node) has one next [link](glossary:link), just like in a singly linked list. The difference is at the end: the tail's next link points back to the [head](glossary:head-and-tail) instead of being empty. A loop has no natural end, so the list remembers where it starts.

## How it works
The list keeps a reference to its tail as well as its head, so both ends can be reached right away.
- Inserting at the beginning links the new node between the tail and the old head, then makes it the head.
- Inserting at the end links the new node into the same spot, between the tail and the head, but makes it the tail instead.
- Deleting from the beginning moves the head forward one node and points the tail at the new head.
- Deleting from the end is the slow case: the node before the tail can only be found by walking around from the head.

Walking the loop means following next links for as many steps as you want. Whenever you pass the tail, you're back at the head.

## Real-life analogy
Children sitting in a circle, each passing a ball to the child on their left. The ball keeps going around, and there's no first or last child except the one you decide to start with.

## When to use it
- Taking turns in a fixed order, over and over, like the players of a board game.
- Round-robin scheduling, where each task gets a short turn before the next task's turn comes.
- Playlists and slideshows that should start over once they reach the end.

## When to avoid it
- You often delete from the end; a doubly circular linked list does that faster.
- You don't need the loop. Code that forgets to stop when it comes back to the start runs forever, so a plain list is safer.

## In PyDSA
- The list keeps references to both its head and its tail.
- The display ends with an arrow that points back to the head.
- `Walk Around the Loop` visits as many nodes as you choose, starting at the head, and goes around more than once if you ask for more nodes than the list has.
