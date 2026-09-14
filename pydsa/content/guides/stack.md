# Stack
> A stack keeps items in a pile where you can only add or remove the top one. The last item you put on is always the first one to come off.

## What it is
A stack is a [data structure](glossary:data-structure) that follows the [LIFO](glossary:lifo) rule: Last In, First Out. You can only reach the item on top. To get to an item further down, you first have to take off every item above it.

## How it works
A stack has three main operations:
- `Push` puts a new item on top.
- `Pop` takes the top item off and gives it to you.
- `Peek` shows you the top item without taking it off.

A stack stored in an array only needs to remember where its top is. Pushing writes the item into the next free slot and moves the top up by one, and popping moves the top back down by one. No other item ever moves, so every operation is equally fast, no matter how many items the stack holds.

A stack with a fixed size can run out of room. Pushing onto a full stack is called [overflow](glossary:overflow-and-underflow), and popping from an empty one is called underflow.

## Real-life analogy
A stack of plates in a cafeteria. Clean plates go on top, and people take plates from the top. The plate at the bottom went on first and will come off last.

## When to use it
- Undo history, where the most recent change is the first one to undo.
- Checking that brackets such as `( [ ] )` are balanced: push every opening bracket, and pop it when its closing bracket arrives.
- Going back the way you came, like the Back button in a browser or backtracking out of a dead end in a maze.
- Your programs already rely on one: the [call stack](glossary:call-stack) keeps track of the functions that are running.

## When to avoid it
- You need items in the order they arrived; use a queue.
- You need to look at or change items in the middle, since a stack only lets you reach the top.

## In PyDSA
- You choose the stack's [capacity](glossary:capacity) when you create it. Pushing onto a full stack is rejected instead of making the stack bigger.
- The stack holds items of any type. When you type a whole number, PyDSA asks whether to store it as an `int` or a `str`.
- The display shows the stack from the top down, with an arrow next to the top item.
- The items are kept in a Python list, and the end of the list is the top of the stack.
