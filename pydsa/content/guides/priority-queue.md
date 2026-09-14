# Priority Queue
> A priority queue serves items by priority instead of arrival time, so the most important item always leaves first. In PyDSA, a smaller number means a higher priority, and items with equal priorities leave in the order they arrived.

## What it is
A priority queue is a queue where every item comes with a [priority](glossary:priority). `Dequeue` doesn't return the oldest item, as a normal queue does, but the item with the highest priority. When several items share the highest priority, a fair priority queue serves them in [FIFO](glossary:fifo) order.

## How it works
PyDSA builds its priority queue on a min heap. Each entry holds a priority, an arrival number and the item, and entries are compared by priority first and by arrival number second. That way, the entry at the heap's [root](glossary:root) is always the one to serve next, and ties go to whichever item arrived first.
- `Enqueue` inserts a new entry into the heap and [sifts it up](glossary:sifting).
- `Dequeue` extracts the root and sifts the last leaf down into its place.
- `Peek` reads the root.
- `Change Priority` first searches the heap for the item, then gives its entry the new priority and sifts it up or down, depending on which way the priority changed.

## Real-life analogy
Boarding a plane. Passengers board by group, not by when they reached the gate, and within the same group, people board in the order they lined up.

## When to use it
- Serving the most urgent work first, like support tickets, hospital patients or network traffic.
- Simulations that handle events in the order of the time they happen.
- Graph algorithms that always explore the closest vertex or the cheapest edge next.

## When to avoid it
- Every item is equally important; a plain queue is simpler.
- You need to see every item in order at once, not just the next one; sort them instead.

## In PyDSA
- Items can be of any type, and priorities are whole numbers. A smaller number is served first.
- Items with the same priority leave in the order they arrived, as the example shows with two tasks of priority 1.
- `Change Priority` changes the copy of an item that arrived first. The item keeps its arrival number, so among items with the same priority, it's still served according to when it first arrived.
- The display shows the heap and a table of the order the items will be served in.
