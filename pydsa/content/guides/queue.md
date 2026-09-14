# Queue
> A queue lines items up so the first one to arrive is the first one to leave. You add items at the rear and remove them from the front.

## What it is
A queue is a [data structure](glossary:data-structure) that follows the [FIFO](glossary:fifo) rule: First In, First Out. Items wait in the order they arrived, like people in a line. The oldest item is at the front, and new items join at the rear.

## How it works
A queue has these main operations:
- `Enqueue` adds an item at the rear.
- `Dequeue` removes the item at the front and gives it to you.
- `Peek Front` and `Peek Rear` show you the item at either end without removing it.

Storing a queue in a plain array would mean shifting every item forward after each dequeue, which gets slow. A [circular array](glossary:circular-array) avoids that. The queue remembers which slots hold its front and rear, and both move forward as items come and go. When either one reaches the last slot, it wraps around to slot 0, so the slots freed at the start get reused and no item ever moves.

## Real-life analogy
A line at a ticket counter. People join at the back, the person at the front is served next, and nobody gets to cut in.

## When to use it
- Handling tasks in the order they arrive, like print jobs or messages waiting to be sent.
- Sharing something fairly, like a processor that gives each program a turn.
- Exploring outward one step at a time, as [breadth-first search](glossary:breadth-first-search) does in a graph.
- Holding data that arrives faster than it can be handled, like keystrokes or video frames.

## When to avoid it
- The newest item should be handled first; use a stack.
- Some items are more urgent than others; use a priority queue.
- You need to add or remove items at both ends; use a deque.

## In PyDSA
- The queue is a circular queue with a fixed size. You choose its [capacity](glossary:capacity), and enqueueing onto a full queue is rejected.
- It holds items of any type.
- The display shows every slot, with markers for the front and the rear. A dequeued item stays in its slot, struck out, until a later enqueue overwrites it, just like in a real circular buffer.
- In the example, the first item was already dequeued, so you can see that the front has moved along.
