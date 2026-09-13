# PyDSA v5 roadmap: new data structures & algorithms

## Context
[roadmap-v4.md](roadmap-v4.md) turns PyDSA into a guided learning tool with guides, operation notes, narrated steps, quizzes, experiments and progress. v5 builds on that to widen what learners can explore: balanced and range-query trees, caches and probabilistic structures, more graph algorithms, string search, dynamic programming, and recursion with backtracking.

**Start v5 only after every v4 phase is done**, since each new topic depends on the v4 frameworks.

## Decisions (from Q&A)
- **New data structures:**
  - Red-Black Tree and B-Tree;
  - Segment Tree and Fenwick Tree;
  - LRU Cache and Skip List;
  - Bloom Filter.
- **New algorithms:**
  - Bellman-Ford, Floyd–Warshall and A* on a grid;
  - dynamic programming (Fibonacci three ways, 0/1 knapsack, longest common subsequence, coin change);
  - string search (naive, KMP, Rabin-Karp);
  - recursion and backtracking (Tower of Hanoi, permutations, N-Queens).
- **Definition of done for every new topic:** a topic ships only when it has all of:
  - pure core code with model-based tests;
  - a screen with a preloaded example and random data;
  - a Markdown guide with all required sections, and a complexity table;
  - notes, pseudocode and source references for every operation;
  - trace events with narration for every multi-step operation;
  - at least 5 quiz questions and at least 1 predict-the-result challenge;
  - Big-O experiments where the growth is worth seeing;
  - an ASCII title in the same `flower_power` font, a topic registry entry and a README entry.

  The v4 completeness tests enforce this automatically.
- **Menu layout:** with about 30 topics, the two data structure categories become four, grouped by what the structures are for. `--topic` ids stay stable across the regrouping.
- **Workflow:** the same as v4. Claude prepares each phase and runs the checks, then hands over a conventional commit message, and the user commits. Versions go 5.0 to 5.5. The last commit of Phase 6 deletes this file and keeps `docs/plans/.gitkeep`.

## Phase 1 — Menu regroup & balanced trees (v5.0)
- **Categories:** the main menu becomes:
  - **Linear structures:** array, stack, queue, deque, linked list, skip list;
  - **Trees & heaps:** BST/AVL, Red-Black tree, B-tree, heap and priority queue, trie, segment and Fenwick trees;
  - **Graphs & sets:** graph, disjoint set;
  - **Hashing & caches:** hash table, hash set, Bloom filter, LRU cache;
  - **Algorithms:** sorting, searching, graph algorithms, string algorithms, dynamic programming, recursion and backtracking.

  Topics from later phases appear in these categories when they land.
- **Red-Black Tree** (`core/red_black_tree.py`):
  - insert, delete, search, traversals and tree stats;
  - the insert fix-up and delete fix-up cases are traced, naming each recolor or rotation;
  - nodes are drawn red or black, with an `R`/`B` marker when colors are off;
  - tests check the red-black rules (the root is black, no red node has a red child, every path has the same black height) against a sorted-list model.
- **B-Tree** (`core/b_tree.py`):
  - the minimum degree `t` is chosen when the tree is created;
  - search shows its path; insert splits full nodes on the way down; delete borrows from or merges with a sibling;
  - `render._diagram` grows to draw nodes with several keys and children, like `[10 | 20 | 30]`;
  - tests check key counts per node, that all leaves are at the same depth, and sorted order against a model.

## Phase 2 — Range-query trees (v5.1)
- **Segment Tree** (`core/segment_tree.py`):
  - built from an array, answering range sum, min or max (chosen when it's created);
  - point update;
  - each node is shown with the range it covers;
  - query traces mark nodes as fully inside, partly overlapping or outside the range.
- **Fenwick Tree** (`core/fenwick_tree.py`):
  - prefix sum, range sum and point update;
  - the index jumps are shown in binary, so learners can see the lowest set bit being added or removed.
- **Tests:** both are checked against brute-force sums over random arrays and updates. Experiments compare query work with summing the range directly.

## Phase 3 — LRU Cache, Skip List & Bloom Filter (v5.2)
- **LRU Cache** (`core/lru_cache.py`):
  - built from the existing chaining hash table plus a doubly linked list;
  - get and put, with evictions narrated;
  - drawn as the key table next to the list from most to least recently used;
  - tested against `collections.OrderedDict`.
- **Skip List** (`core/skip_list.py`):
  - search, insert and delete;
  - the random level of each new node comes from a seeded coin flip that's shown on screen;
  - the levels are drawn as express lanes stacked over each other, with the search path traced across them;
  - tested against a sorted list, plus the expected level distribution over many inserts.
- **Bloom Filter** (`core/bloom_filter.py`):
  - the number of bits m and hash functions k are chosen when it's created;
  - add and might-contain;
  - the hash functions come from salted SHA-256, so bit positions stay the same between runs (Python's `hash()` for strings changes every run);
  - "might contain" results explain false positives;
  - an experiment compares the measured false positive rate with the formula as more items are added;
  - tests check it never gives a false negative, against a Python set.

## Phase 4 — Graph algorithms II (v5.3)
- **Bellman-Ford:**
  - a relaxation table after every pass;
  - negative weights are allowed, and a negative cycle is detected and shown as the cycle itself;
  - Dijkstra's negative-weight error now suggests Bellman-Ford;
  - tested against the Dijkstra results on non-negative graphs, and against a brute-force search for negative cycles on small graphs.
- **Floyd–Warshall:**
  - the all-pairs distance matrix after each intermediate vertex k, with the cells that improved highlighted;
  - path reconstruction, and negative cycles detected from the diagonal;
  - tested against running Bellman-Ford from every vertex.
- **A\* on a grid:**
  - you choose a grid size, place walls (random or typed row by row), and pick the start and goal;
  - the Manhattan distance is the heuristic;
  - each step draws the open and closed cells and the current path;
  - a comparison with Dijkstra (A* with a heuristic of 0) shows how many fewer cells A* expands;
  - tested for path length against a BFS on the grid.
- **Screens:** all three go on the Graph Algorithms screen and in the graph screen's Graph Algorithms menu, using the existing graph adapter (`vertices()` and `edges(v)`) for Bellman-Ford and Floyd–Warshall.

## Phase 5 — String algorithms (v5.4)
- **Screen:** a new String Algorithms screen, where you type the text and the pattern or use an example.
- **Naive search:** the pattern is drawn under the text at each shift, with matching and mismatching characters marked.
- **KMP:**
  - the prefix table is built step by step, with each entry explained;
  - the search shows each shift the prefix table allows, and the comparisons it saves.
- **Rabin-Karp:**
  - a rolling hash with a modulus you can see;
  - each window's hash, with hash matches that aren't real matches (spurious hits) called out;
  - a small modulus is available to show collisions on purpose.
- **Comparison:** a table of the character comparisons each algorithm made on the same input.
- **Tests:** every occurrence is checked against a reference built from `str.find`, including overlapping matches, empty inputs and a pattern longer than the text.

## Phase 6 — Dynamic programming & recursion (v5.5)
- **Dynamic Programming screen:**
  - **Fibonacci:** plain recursion, memoization and a table, compared by call counts, with the call tree drawn for small n.
  - **0/1 knapsack:** the table filled cell by cell, with the chosen items traced back.
  - **Longest common subsequence:** the table with direction arrows and the subsequence rebuilt.
  - **Coin change:** the fewest coins and the number of ways, each table filled step by step.
- **Recursion & Backtracking screen:**
  - **Tower of Hanoi:** the pegs drawn after every move, with the total of 2ⁿ − 1 moves explained.
  - **Permutations:** the recursion tree.
  - **N-Queens:** the board after each placement and each backtrack, plus a count of solutions.
  - Input sizes are capped so recursion stays readable and fast, e.g. n ≤ 8 for N-Queens and n ≤ 10 for Hanoi's step view.
- **Tests:**
  - DP results are checked against brute force on small inputs.
  - Hanoi's moves are valid and number 2ⁿ − 1.
  - Permutations are checked against `itertools.permutations`.
  - N-Queens solution counts match the known values for n from 1 to 8.
- **Wrap-up:** update the README feature list, set the version to 5.5 and **delete `docs/plans/roadmap-v5.md`**, keeping `docs/plans/.gitkeep`.

## Verification (every phase)
- `pip install -e ".[test]"`, then `pytest`: all tests pass, including the v4 completeness tests for every new topic (guide, notes, narration, quiz, registry entry).
- A scripted stdin run walks every new menu path, including step-through and practice, to Exit without tracebacks.
- A run at 90 and 45 columns and with `NO_COLOR` has no lines wider than the terminal apart from ASCII titles. New diagrams (B-tree nodes, skip list lanes, DP tables, grids) switch to a compact layout when they're too wide.
- `python -W error -c "import pydsa"` gives no warnings, and a built wheel contains the new guide files.
