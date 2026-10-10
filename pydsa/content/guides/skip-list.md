# Skip List
> A skip list keeps sorted keys in a linked base lane and adds shorter express lanes above it. Seeded coin flips decide how many lanes each new node joins.

## What it is
A skip list is a sorted linked collection with several forward links per node. Level 1 contains every key. Higher levels contain subsets that let a search skip over many base nodes. PyDSA keeps duplicates, with a separate node for every insertion.

## How it works
A search starts at the head of the highest lane. It moves right while the next key is smaller than the target, then drops one level. At the base it checks the next node for equality. Insertion remembers each lane's predecessor, then links a new node after those predecessors. A duplicate goes before existing equal keys. Deletion finds the first occurrence and unlinks it from every lane it belongs to.

Every new node starts at level 1. A fair coin promotes it on heads and stops on tails, up to a level cap. About half of the nodes reach level 2, a quarter reach level 3, and so on. A seed makes the sequence of flips repeatable for the same sequence of insertions. These probabilities, rather than rotations, keep searches short on average; an unlucky layout can still require a long walk. This follows [William Pugh's skip-list design](https://rtheunissen.github.io/bst/docs/references/1989_pugh.pdf).

## Real-life analogy
Think of a train network. Local trains stop at every station, while express routes stop at selected stations. Travel quickly on an express route, then change to a more detailed route near your destination.

## When to use it
Use it to explore randomized balancing, ordered searches and updates without tree rotations. Its base lane also makes sorted iteration straightforward.

## When to avoid it
Use an AVL or Red-Black tree when you need guaranteed balancing rather than expected performance. Additional forward links use memory, and a small level cap can limit how well very large collections scale.

## In PyDSA
Create finite numeric or string keys with a seed, load the example with seed 7 or generate random data. Insertion narrates each heads or tails result and each lane link. Searches show rightward moves and drops; deletion removes one occurrence. Levels are aligned above the base lane, or shown as wrapped forward-link rows when wide. The default core cap is 32 levels; a chosen core cap from 1 to 64 is supported. Practice includes quizzes, predictions and a search-work experiment. The complexity table describes expected growth when the cap is high enough for the input; a fixed tiny cap can force long scans.
