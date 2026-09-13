# PyDSA — Replay the history of `old/` as realistic commits

## Context
`old/` holds PyDSA, a console app for learning data structures that went up to GitHub in one upload with no history. The goal is to rebuild it at the top level of the repo as a series of commits that follow how the app would really have been built: set up the project, add one data structure at a time, then polish. Each commit is one feature, roughly 50–400 lines. No one-liners and no dumps of a whole file set.

The last commit must **behave exactly like today's `old/` code**. Comments, docstrings, spacing and layout are cleaned up to a professional standard along the way (see "Style pass" below). That cleaned-up version is the baseline for the later standardization and new features.

The code itself tells us how to order the replay. `utility.main_intro()` says **Version 2.2**, and its changelog lists "Adding Non-linear DSes", "Including Examples", "Showing Array Sorting Steps" and "Bug Fixes". So the order is: v1.0 with the linear DSes only → the non-linear DSes → v2.2 polish.

## Workflow
- The repo is already set up on branch `main`. `old/` stays where it is and is hidden from git through `.git/info/exclude`, so it never shows up in any commit or in `.gitignore`.
- One step per pass. Claude writes the files for that step, runs the checks, and then hands over a **conventional commit message**:
  - The title is `type(scope): summary`.
  - The body is one or two short, plain-language paragraphs on what changed. Each paragraph goes on a single line with no hard wraps, and paragraphs are separated by one blank line.

  The user reviews and makes the commit (and any tag). Claude doesn't run `git commit`.
- Commit dates are simply when the commits are made. Nothing gets pushed. Pushing (force-push over the existing repo or a new repo) is decided later.

## Ground rules
- **No LICENSE file in history at all.** README.md goes in with its current 2 lines.
- **This plan is in the first commit** at `docs/plans/history-replay.md`. The last commit deletes it and adds `docs/plans/.gitkeep`, so the folder stays around for future plans.
- Top-level imports drop the `old.` prefix (`import utility`, `import my_array`, …). `main.py` has `import queue`, which picks up the local `queue.py` when run as `python main.py`, so it stays as is.
- **Code logic stays exactly the same.** Existing quirks stay: hash table definition text copied from graph, BST/AVL search only working for `num` (the nested `if` under `elif`), the `bst = AVLTree("str")` typo, duplicate `Node` classes, recursive `main()` on Go Back, `!= None` comparisons, `type` used as a variable name, and non-raw ASCII-art strings with invalid escapes. Fixes belong to later standardization phases.
- **User-facing strings don't change.** Emojis in `print()`/`input()` text, menus, ASCII art and info paragraphs are app output, so they stay exactly as they are. That includes the "under MIT license" line in `main_intro()`, which can be reconsidered later.
- Every step must run: `python main.py` starts, and every menu option wired up so far works. A menu only lists DSes that exist at that step.

## Style pass (applied to every file as it's written)
This changes comments, docstrings and whitespace only. It never touches executable code.

**Comments**
- No emojis in comments. Emoji section banners like `# 🟥 =====> AVL Tree <=====` or `# 🎯 The Stack class` become plain headers, for example:
  ```python
  # ---------------------------------------------------------------------------
  # AVL Tree
  # ---------------------------------------------------------------------------
  ```
  Short labels like `# 🟢 Operation selection loop` become `# Operation selection loop`.
- Rewrite casual or first-person remarks as neutral technical notes that keep the meaning:
  - "IMHO" becomes a plain statement.
  - "Using fingers as nodes … can help big time!" becomes a short note on index handling, or is dropped.
  - "Auto continue with the While True in full swing!" becomes a clean note or is removed.
- `##` sub-comments become regular `#` comments. Comment case and punctuation are consistent: sentence case, no trailing `!`.
- Remove commented-out dead code (`# return kv[1]`, `# for i in range(self.size): …`, `# print(... .index(row) ...)`). Keep the *reason* from those comments as prose when it's useful. For example, the display note becomes "Row index is tracked separately; `list.index()` would repeat indices for identical rows."
- Fix spelling in comments ("funcion", "initialzing"). Menu text is output and stays as is.

**Docstrings**
- One consistent style: triple double quotes, a one-line summary in the imperative mood ending with a period, with extra lines only where they add something. Examples: `"""Insert an element at the given index."""`, `"""Return True if the stack is empty."""`.
- Add a short module docstring at the top of each file, replacing the old `# Stack Implementation (static, dynamic-typed)` header comment.
- Add missing one-line docstrings to classes and functions that have none (e.g. `SinglyLinkedList`, graph methods, `*_main` functions), matching that style.

**Whitespace and layout (PEP 8)**
- 4-space indentation everywhere. This fixes the 3-, 7- and 2-space blocks, e.g. the traversal `match` blocks in `tree.py`/`graph.py` and the `case "2":` example bodies. Nesting must stay the same.
- 2 blank lines between top-level definitions, 1 between methods, no runs of 3+ blank lines.
- Spaces after commas and around operators in code, e.g. `[[10, 0, 30, 19], …]`, `dll_items = []`, `n - i - 1`.
- No trailing whitespace. Each file ends with exactly one newline.
- Imports go at the top in one group, followed by 2 blank lines.
- String literals are left alone. Long info paragraphs stay on one line: no line-length wrapping that could change output.

## Commit sequence (21 commits)

### Phase 0 — Project setup
1. `chore: initial project setup` — `README.md` (current 2 lines), `.gitignore` (standard Python: `__pycache__/`, `*.pyc`, `.venv/`, `.vscode/`, `.idea/`), `docs/plans/history-replay.md`.
2. `feat: add entry point with intro banner and main menu` — `utility.py`: `clear()` and a minimal `main_intro()` (PyDSA ASCII banner, short welcome, "Version 1.0", GitHub link). `main.py`: a flat "Which data structure?" loop with invalid-input handling. Array is the only entry, printing "coming soon" until commit 3.

### Phase 1 — Linear data structures (ends at tag `v1.0`)
3. `feat(array): implement fixed-size typed array` — `my_array.py`: `Array.__init__/insert/remove/get/display/size_check/type_check`, `array_intro()`, and `array_main()` with the type/size create flow (no example option yet). The operation menu covers definition, insertion, deletion, indexing, size, type, display, new array, and exit. Wired into `main.py`.
4. `feat(array): add sorting algorithms` — `sort`, `bubble_sort`, `selection_sort`, `insertion_sort`, `quick_sort`, `heapify`/`heap_sort`, `shell_sort`, each with its info explanation, plus `utility.order_verify()`. No step prints and no `sort_intro/sort_outro` yet: those come in commit 18.
5. `feat(array): add linear and binary search` — `linear_search`, `binary_search`, searching submenu. Adds the `"str"`, `"int"` and `"float"` branches to `utility.input_verify()`.
6. `feat(stack): implement fixed-size stack` — `stack.py` (class, menu, intro, no example). Wired into main.
7. `feat(queue): implement circular queue` — `queue.py` (wraparound, strikeout dequeue, front/rear, no example). Wired into main.
8. `feat(linked-list): add singly linked list` — `linked_list.py`: SLL `Node`, `SinglyLinkedList`, `sll_main`, `ll_intro`. `linked_list_main()` opens SLL directly. Adds the `"all"` branch to `utility.input_verify()`.
9. `feat(linked-list): add doubly linked list and list type selection` — DLL `Node`, `DoublyLinkedList`, `dll_main`, and the type-selection loop in `linked_list_main()`.
10. `feat(intro): expand intro with data structure overview` — `main_intro()` gets the long general-DS, linear-DS and algorithms paragraphs, still v1.0. → tag `v1.0`

### Phase 2 — Non-linear data structures
11. `feat(tree): add binary search tree and split menu by category` — `main.py` gets its final two-level layout with "Go Back". `tree.py` has the BST `Node`, `BinarySearchTree`, `bst_main` (type selection with no example wrapper), and `tree_intro`. Adds `input_verify("num")`.
12. `feat(tree): add AVL tree and tree type selection` — AVL `Node`, `AVLTree` with rotations, `avl_main`, and the `tree_main()` selection loop.
13. `feat(graph): add adjacency matrix directed weighted graph` — `graph.py`: `MatrixDirectedWeightedGraph`, `adj_matrix_main`, `graph_intro`, helpers `get_u/get_v/get_weight`. `display()` first uses `self.adj_matrix.index(row)` for the row number (fixed in commit 17).
14. `feat(graph): add adjacency list representation` — `ListDirectedWeightedGraph`, `adj_list_main`, and the `graph_main()` representation selection.
15. `feat(hash-table): add separate chaining hash table` — `hash_table.py`: `ChainingHashTable`, `chaining_main`, `hash_table_intro` (with the copied definition text, verbatim), helpers `get_key/get_value`. `display()` uses the same `.index()` row numbering as the matrix. Wired into main.
16. `feat(hash-table): add linear probing hash table` — `LinearProbingHashTable` with rehash-on-delete (same `.index()` display), `linear_probing_main`, and the `hash_table_main()` selection loop.

### Phase 3 — v2.2 polish (ends at tag `v2.2` = baseline)
17. `fix: show correct row indices in matrix and hash table displays` — switch the three `display()` methods to the `indices.pop(0)` pattern and add the explaining comment.
18. `feat(array): show intermediate sorting steps` — step prints inside each algorithm, `sort_intro()`/`sort_outro()`, and the menu cases calling them.
19. `feat: add preloaded examples to linear data structures` — the "create yourself or use the example" loop in `array_main`, `stack_main` and `queue_main`.
20. `feat: add preloaded examples to non-linear data structures` — the same loop for BST, AVL, adjacency matrix, adjacency list, chaining and linear probing. This includes the create-flow nesting and the info notes.
21. `chore(release): v2.2` — final `main_intro()`: non-linear paragraph, "all 7 major DSes", Version 2.2 changelog. Deletes `docs/plans/history-replay.md` and adds `docs/plans/.gitkeep`. → tag `v2.2`

## How to write each commit
Work forward. For each step, write the top-level files as they should look at that point, taking the code from the matching `old/` file with the style pass applied, and leaving out anything that belongs to a later step. Style is applied from the first commit, so no "cleanup" commit shows up in the replay. Before commit 21 is handed over, run the AST check below against `old/` so no logic drift can creep in.

## Verification
- **Every step:** `python -m py_compile *.py`, then a scripted smoke run such as `printf '1\n1\n1\n5\n11\n' | python main.py` that walks into the newest DS and exits. Also check that no comment line contains an emoji, and review `git status` so only the intended files are part of the step.
- **Final baseline check (step 21):** a throwaway script, kept outside the repo, that for each `.py` file compares `ast.dump()` of `old/<f>` and `<f>` after:
  - removing module, class and function docstrings;
  - renaming the `old.` import prefix.

  All files must match, which proves only comments, docstrings and whitespace changed. `git diff --no-index old/README.md README.md` must be empty.
- After commit 21: `git log --oneline --stat` shows sensible commit sizes, and `git tag` shows `v1.0` and `v2.2`. Then delete `old/` (with confirmation first) and remove its line from `.git/info/exclude`.
