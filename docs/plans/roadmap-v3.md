# PyDSA v3 roadmap

## Context
PyDSA now matches its original v2.2 behavior, and the old quirks have been fixed. It covers 7 data structures (array, stack, queue, singly/doubly linked lists, BST/AVL, matrix/list graphs, chaining/probing hash tables) as flat top-level scripts. Every class mixes logic with `print()`/`input()`, and every menu is a copy-pasted `while True` + `match` loop. "New X" options recurse into `*_main()`.

This roadmap grows the app in five larger phases:
1. Rebuild the foundation: an installable package, logic split from the console UI, a shared menu framework and a pytest suite.
2. Give the console a polished look with `rich`.
3. Add the remaining classic data structures.
4. Add heaps, tries and tree extras.
5. Add more sorting, searching and graph algorithms.

The app keeps its educational, emoji-rich tone. Text is polished, not rewritten.

## Decisions (from Q&A)
- **Scope:** code foundation, new data structures and new algorithms. CI and lint tooling are out of scope.
- **Dependencies:** runtime dependencies are allowed. `rich` handles the visuals: panels, tables, colors and diagrams. The menu flow is unchanged, so this is not a full TUI.
- **Running the app:** `pyproject.toml` installs a `pydsa` command, and `python -m pydsa` also works. `requires-python >= 3.10` (the code uses `match`).
- **Tests:** a pytest suite in the repo covers every data structure and algorithm.
- **Text:** keep the style, but make emoji use, wording and numbering consistent, and add complexity info where it's missing.
- **Workflow:** same as before. Each phase is one or a few larger commits. Claude prepares the files, runs the checks, and hands over a conventional commit message (body paragraphs on single lines); the user commits and tags. Each phase bumps the version shown in the intro and adds a changelog entry: 3.0, 3.1, 3.2, 3.3, 3.4.
- **This plan** lives at `docs/plans/roadmap-v3.md`. The last commit of Phase 5 deletes it, and `docs/plans/.gitkeep` stays.

## Target layout
```
pyproject.toml                # name "pydsa", dependencies: rich; [project.optional-dependencies] test = ["pytest"]
pydsa/
  __init__.py                 # __version__
  __main__.py                 # python -m pydsa  -> app.run()
  app.py                      # category menu (Linear / Non-linear / Algorithms)
  core/                       # pure logic: no print/input, returns values or raises
    errors.py                 # PyDSAError, OutOfBoundsError, CapacityError, EmptyError, NotFoundError, InvalidTypeError
    array.py  stack.py  queue.py  linked_list.py  tree.py  graph.py  hash_table.py
  algorithms/
    sorting.py  searching.py  graph_algorithms.py
  ui/
    console.py                # shared rich Console, clear(), ask_choice/ask_int/ask_value/ask_order (replaces utility.input_verify/order_verify)
    menu.py                   # Menu helper + Nav result (BACK, NEW, HOME, EXIT)
    render.py                 # rich renderers: arrays, stack/queue, linked lists, matrices, hash tables, trees
    screens/                  # one console screen per data structure (array.py, stack.py, ...)
  content/
    texts.py                  # ASCII art, definitions, algorithm explanations, intro (moved from the modules as-is)
tests/
  test_<structure>.py ...
```
The top-level `main.py`, `utility.py` and the other data structure scripts are removed in Phase 1. The README documents `pip install .` / `pydsa`.

## Phase 1 — Foundation (v3.0)
**Goal:** the same app, the same menus and the same behavior, rebuilt on the new layout.
- **Packaging:** add `pyproject.toml` (setuptools, `[project.scripts] pydsa = "pydsa.app:run"`). Add build and test artifacts (`*.egg-info/`, `build/`, `dist/`, `.pytest_cache/`) to `.gitignore`.
- **Core split:** move every class into `pydsa/core/` with its algorithms unchanged: `Array`, `Stack`, `Queue`, `SinglyLinkedList`/`DoublyLinkedList`, `BinarySearchTree`/`AVLTree`, `MatrixDirectedWeightedGraph`/`ListDirectedWeightedGraph`, `ChainingHashTable`/`LinearProbingHashTable`. Methods return results or raise `core/errors.py` exceptions instead of printing. For example, `Stack.pop()` returns the item or raises `EmptyError`, and `LinearProbingHashTable.delete()` returns the number of rehashed keys.
- **Sorting steps:** sorting and searching move to `algorithms/`. Each sorting algorithm becomes a generator that yields a snapshot of the array per step, the same moments where `🔹` prints today, and ends with the sorted list. Screens print the steps; tests just consume them.
- **Menu framework:** `ui/menu.py` replaces the copy-pasted loops. A `Menu(title, options)` handles invalid codes and the shared navigation entries: Definition, New, New Data Structure, Exit. Handlers return `Nav` values instead of calling `*_main()` recursively, which removes the recursion from "New X".
- **Prompts:** `ui/console.py` ports `utility.input_verify` (all/str/num/int/float) and `order_verify` into `ask_value(kind)` / `ask_order()` / `ask_int(min_value=...)`. That centralizes the "size ≥ 1" and "index must be an int" validation added in the quirk fixes.
- **Content:** move the ASCII art, definitions, algorithm explanations and the intro into `content/texts.py` word for word, keeping raw strings.
- **Tests:** port the model-based random-operation tests used during the replay into pytest:
  - sorting against `sorted()`, and search against `list.index()`;
  - SLL/DLL against a Python list, checking both `next` and `prev` links;
  - BST/AVL order and balance invariants, including duplicate keys;
  - matrix/list graphs against reference BFS/DFS;
  - hash tables against a dict, including a full probing table and rehash on delete.

  Add a few screen-flow tests that feed scripted input through `monkeypatch` and assert the menus reach Exit without errors.
- **Wrap-up:** update the README (install, run, feature list), set the intro version to 3.0, and remove the old top-level scripts.

## Phase 2 — Rich visuals & text polish (v3.1)
- **Rendering:** `ui/render.py` draws every structure with `rich`:
  - arrays, stacks and queues as indexed tables, with top/front/rear markers;
  - linked lists as boxed nodes with `→` or `⇄` arrows;
  - adjacency matrices as grid tables with vertex headers;
  - adjacency lists and hash tables as tables (bucket/slot, contents);
  - BST/AVL as a `rich.tree.Tree` for now (the top-down diagram arrives in Phase 4).
- **Screens:** intros and definitions go in `Panel`s. Success/error/info messages get consistent styling through `console.success()/error()/info()` helpers. Sorting steps become a table: step #, array state, and the swapped/compared indices highlighted.
- **Emoji and wording:**
  - ✅ success, 🚫 invalid input or rejected operation, ❌ not found, ℹ️ info;
  - the same wording for equivalent actions across structures;
  - consistent menu numbering, with the navigation options always last.
- **Complexity tables:** each definition screen gets a small time/space complexity table for its operations.
- **Terminals:** rendering stays readable when output is piped or the terminal has no color, since rich strips styles automatically.

## Phase 3 — New linear & set structures (v3.2)
- **Deque** (`core/deque.py`): a fixed-capacity circular-array deque with `push_front/push_back/pop_front/pop_back/peek_front/peek_back`, is_empty/is_full and a size check. It's listed under Linear.
- **Circular linked lists** (`core/linked_list.py`): `SinglyCircularLinkedList` and `DoublyCircularLinkedList`, with the same operations as the existing lists plus "traverse N steps around the loop". The linked-list type menu grows to four types, matching what the intro definition already describes.
- **Hash Set** (`core/hash_set.py`): built on `ChainingHashTable`, with add, remove, contains, union, intersection, difference and subset checks. It's listed under Non-linear → Hash Table as a third option.
- **Disjoint Set** (`core/disjoint_set.py`): Union-Find with union by rank and path compression, plus `find`, `union`, `connected` and set listing. It renders the parent/rank arrays and the groups. It's listed under Non-linear, and Kruskal reuses it in Phase 5.
- **Content and tests:** definitions and ASCII titles for each structure; model-based tests for each (deque against `collections.deque`, the set against Python `set`, the disjoint set against naive grouping).

## Phase 4 — Heap, Priority Queue, Trie & tree extras (v3.3)
- **Heap** (`core/heap.py`): `MinHeap` and `MaxHeap` backed by an array, with insert, extract, peek, heapify-from-list and size. The steps (sift-up/sift-down swaps) are shown as both the array and the tree diagram.
- **Priority Queue:** built on the heap, with enqueue(item, priority), dequeue, peek and change-priority. Equal priorities are served first-in first-out.
- **Trie** (`core/trie.py`): insert, search, delete (pruning empty branches), `starts_with`, autocomplete, and a word count. It renders as a `rich` tree.
- **Tree extras** for BST, AVL and Heap:
  - level-order (BFS) traversal;
  - height, min/max, node count and leaf count;
  - a shared **top-down ASCII tree diagram** renderer (`ui/render.py`) that replaces the Phase 2 `rich.tree` view for binary trees;
  - AVL shows balance factors on the diagram.
- **Menus:** Heap & Priority Queue and Trie are listed under Non-linear.
- **Tests:** heap invariants against `heapq`, priority order and FIFO ties, trie against a set of words (prefix queries), and tree metrics against brute force.

## Phase 5 — Algorithms (v3.4)
- **Category:** a new top-level **Algorithms** category next to Linear and Non-linear. It works on user-built or example data, and the existing per-structure menus also link to the relevant algorithms.
- **Sorting:** merge sort (steps per merge), counting sort (ints, including negatives through an offset) and radix sort (non-negative ints, one step per digit), each with an explanation.
  - **Comparison mode:** runs every algorithm on copies of the same input and shows a table of comparisons, swaps/writes and steps, using counters built into the sorting generators.
- **Searching:** jump, interpolation and exponential search. Like binary search, they run on a sorted copy and report the original first index, each with an explanation.
- **Graph algorithms** (`algorithms/graph_algorithms.py`, working on both representations through a shared neighbors/weights adapter):
  - graphs gain a **directed/undirected** choice at creation, and undirected edges are stored both ways;
  - Dijkstra shortest paths using the Phase 4 `MinHeap`, which rejects negative weights, showing the distance table and the path to a chosen vertex;
  - topological sort (Kahn), which reports when the graph has a cycle;
  - cycle detection: DFS coloring for directed graphs, Disjoint Set for undirected;
  - minimum spanning tree with Prim (heap) and Kruskal (Phase 3 Disjoint Set), undirected graphs only, showing the chosen edges and total weight.
- **Tests:** algorithms against brute-force or reference results (Dijkstra against Bellman-Ford on small random graphs, topological order validity, MST weight against brute force on small graphs, searches against `list.index`).
- **Final commit:** update the README feature list, set the version to 3.4, and **delete `docs/plans/roadmap-v3.md`**, keeping `docs/plans/.gitkeep`.

## Verification (every phase)
- `pip install -e ".[test]"`, then `pytest`: all tests pass, and new structures and algorithms come with their own tests.
- `pydsa` and `python -m pydsa` start. A scripted stdin run walks every new menu path to Exit without tracebacks, and a manual run checks the rich rendering in a real terminal on Windows.
- `python -W error -c "import pydsa"` gives no SyntaxWarnings.
- Behavior parity in Phase 1: the same menu options and results as the current top-level scripts, checked by running the same scripted inputs against both before the old scripts are removed.
