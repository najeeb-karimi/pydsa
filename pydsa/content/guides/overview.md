# Data Structures and Algorithms
> A data structure is a way of organizing data so it's easy to use, and an algorithm is a step-by-step recipe for solving a problem. Choosing the right ones is the difference between a program that answers instantly and one that never seems to finish.

## Data structures
A [data structure](glossary:data-structure) decides how data is stored, and with it, which operations are quick. An array can jump to any position instantly but can't grow. A linked list grows easily but has to walk to reach a position. No structure is best at everything, so learning data structures is really learning their trade-offs.

## Linear data structures
In a linear data structure, the items form a line: each item has at most one item before it and one after it.
- An array stores items side by side, numbered by position.
- A stack only lets you reach the item added last, and a queue only the item added first.
- A deque lets you add and remove items at both ends.
- A linked list chains items together with links, so it can grow and shrink one item at a time.

## Non-linear data structures
In a non-linear data structure, an item can connect to several others.
- Trees arrange items in a hierarchy. Binary search trees keep keys sorted, and AVL trees also keep themselves balanced.
- Heaps keep the smallest or largest item on top, which makes them ideal for priority queues.
- A trie stores words letter by letter, so words with the same beginning share their nodes.
- Graphs model any kind of connection, like roads, friendships or dependencies.
- Hash tables and hash sets use a hash function to find items almost instantly.
- A disjoint set keeps track of which items belong to the same group.

## Algorithms
An [algorithm](glossary:algorithm) is a precise list of steps that solves a problem, like sorting a list, finding a value or planning a route. The same problem can be solved by many algorithms, and some are far faster than others. PyDSA includes sorting, searching and graph algorithms, and every one of them shows its work as it runs.

## Measuring speed and memory
To compare algorithms, you look at how their work grows as the input grows, instead of timing them on one computer. That growth is called [time complexity](glossary:time-complexity), and the growth of the memory they need is their [space complexity](glossary:space-complexity). Both are written in [Big O notation](glossary:big-o-notation), which captures the growth while ignoring small details.

The cost often depends on the input itself, not just its size, so costs are often given for the [best, average and worst case](glossary:best-average-and-worst-case). Every topic in PyDSA shows its costs in a complexity table, right below its guide.

## How to learn with PyDSA
1. Open a topic from the main menu and read its short summary.
2. Start with the example, or fill the topic with random values.
3. Try every operation and watch what changes after each one.
4. Choose Read the Guide to learn how it works, and when to use it or avoid it.
5. Look up any word you don't know in the Glossary, under Learning Tools.
