# PyDSA v4 roadmap: learning experience

## Context
PyDSA 3.4 covers 15 data structures and 20 algorithms, drawn with rich. The explanations and the console flow still get in the way of learning:
- **Missing explanations:** only the sorts, the searches, linked list search and the graph algorithms explain themselves before they run. Every other operation (stack push, AVL insert, hash probing, union/find, …) runs silently, and no operation shows its cost when it runs.
- **Hard-to-read text:**
  - The texts are long single paragraphs in mixed tones, and they repeat complexity numbers that already live in the tables.
  - The ~550-word intro reprints on every trip home.
  - Every topic reprints its full definition each time it opens.
- **Steps don't explain themselves:**
  - Sorting steps are bare snapshots of the list, and search probes are bare positions.
  - Tree rotations, BFS/DFS, Dijkstra and minimum spanning trees show only their final results.
- **Rough edges in the console:**
  - Ctrl+C and Ctrl+D end in a traceback.
  - There are no shortcuts, settings, command-line options, progress or practice.

v4 makes PyDSA a guided learning tool, in five phases:
1. A safer, friendlier console, with shortcuts, settings, command-line options and random data.
2. Structured guides, a glossary and a guide for choosing a data structure.
3. Notes for every operation, plus a way to see its code.
4. Narrated steps you can watch one at a time.
5. Practice: quizzes, predictions, Big-O experiments and progress tracking.

New data structures and algorithms follow in [roadmap-v5.md](roadmap-v5.md), once v4 is finished.

## Decisions (from Q&A)
- **Explanations:**
  - Structured guides replace today's definitions and algorithm explanations, written in plain, consistent language.
  - Complexity numbers live only in `content/complexity.py`, so the prose never repeats or contradicts them.
  - Every operation gets a short note, pseudocode and a view of its real Python source.
  - A glossary and a "which data structure should I use?" guide are reachable from the main menu.
- **Content format:**
  - Guides, the glossary and the choosing guide are Markdown files rendered with `rich.markdown` and packaged as package data.
  - Operation notes, pseudocode, quizzes and narration templates are structured Python data that tests validate.
- **Opening a topic:** it shows the ASCII title, a 2–3 sentence summary and the complexity table. A **Read the Guide** option opens the full guide. The long intro shows only once per session.
- **Step-through:** before a multi-step operation runs, PyDSA asks "Watch it step by step?", and pressing Enter shows everything at once. The default can be changed in Settings.
- **Interactive features:** quizzes with explained answers, "predict the result" challenges on live data, Big-O experiments, and progress saved between sessions.
- **Usability:** shortcuts and a clean exit, a Settings menu saved between sessions, random data in every create flow, and command-line options.
- **Dependencies:** no new runtime dependencies. rich already brings Markdown rendering and syntax highlighting (through pygments). Python stays at 3.10 or newer.
- **Workflow:** the same as v3. Claude prepares each phase and runs the checks, then hands over a conventional commit message, and the user commits. Each phase bumps the version shown in the intro and adds a changelog entry: 4.0, 4.1, 4.2, 4.3 and 4.4. The last commit of Phase 5 deletes this file and keeps `docs/plans/.gitkeep`.

## Target layout (new or reshaped parts)
```
pydsa/
  app.py                  # argparse options, main menu: data structure categories, Algorithms, Practice, Learning Tools, Settings
  topics.py               # Topic registry: id, title, category, screen module, content keys
  settings.py             # Settings dataclass; JSON load/save under PYDSA_HOME or ~/.pydsa
  progress.py             # visited topics, quiz scores and challenges, saved as JSON next to the settings
  algorithms/trace.py     # TraceEvent: the structured step events shared by core and algorithms
  practice/
    quiz.py               # Question and Challenge types, scoring
    challenges.py         # "predict the result" generators built on pydsa.core
    experiments.py        # Big-O experiment definitions and runner
  content/
    guides/               # <topic>.md, algorithms/<algorithm>.md, glossary.md, choosing.md
    registry.py           # loads guides with importlib.resources, pulls out the summary, checks sections
    notes.py              # OperationNote for every operation
    narration.py          # caption templates that turn TraceEvents into sentences
    quizzes.py            # multiple-choice questions for every topic
    texts.py              # only the banner, ASCII titles, welcome and changelog
    complexity.py         # unchanged role, now the only home of Big-O numbers
  ui/
    console.py            # shortcuts, clean exit and help (raises QuitRequested or BackRequested)
    stepper.py            # the step player, which follows the step setting
    random_data.py        # random values, words, lists, graphs and unions for create flows
    screens/settings.py  tools.py  practice.py
```

## Phase 1 — Console foundation & usability (v4.0)
- **Clean exit:**
  - `app.run` catches `KeyboardInterrupt`, `EOFError` and a new `QuitRequested`, then prints the usual goodbye instead of a traceback.
  - The same happens if Ctrl+C is pressed in the middle of a step playback.
- **Shortcuts:** they work everywhere through `console.ask_code` (menus) and `console.ask` (typed values).
  - **In menus**, where only numbers are valid answers:
    - `h` or `?` opens help: the shortcuts, where you are, and how to read the guide;
    - `b` goes back one level (in an operation menu, that's the topic list);
    - `q` quits.
  - **At typed-value prompts**, where `q` could be a real value, the shortcuts are `:h`, `:b` and `:q`:
    - `:b` cancels the current operation and returns to its menu, through a `BackRequested` that `Menu.select` catches;
    - `:q` quits.
  - Every menu footer shows a one-line hint about the shortcuts.
- **Topic registry:** `pydsa/topics.py` lists every topic with its id (`stack`, `avl-tree`, `dijkstra`, …), title, category and screen. `app.py` builds its category menus from it, and the `--topic` option and progress tracking both use its ids.
- **Command-line options:** `app.run(argv=None)` parses them with argparse:
  - `--version` prints the version;
  - `--no-color` turns colors off for this run;
  - `--list-topics` prints every topic id;
  - `--topic ID` opens that topic directly, and leaving it shows the main menu;
  - `--reset-settings` restores the default settings.
- **Settings:**
  - `settings.py` defines the settings: detail (`brief`/`detailed`), steps (`ask`/`all`/`pause`), colors (on/off), clear-screen between screens (on/off) and intro (`once`/`always`).
  - They're saved as versioned JSON in `PYDSA_HOME`, or in `~/.pydsa/settings.json` when that isn't set.
  - A missing, corrupt or unwritable file falls back to the defaults, with one short notice.
  - A **Settings** screen on the main menu changes each setting, explains what it does, and can restore the defaults.
- **Less repetition:**
  - The full intro shows once per session; later trips home show a compact header.
  - Operation menus show their title only once, so reprinting after each action stays short.
- **Consistent labels:**
  - One home label, "Main Menu", everywhere.
  - Every restart label names its own topic; for example, the hash set's says "New Hash Set" instead of "New Hash Table".
- **Random data:** `ui/random_data.py` gives every create flow a "Fill with random values" option:
  - the size is asked for, and values are ints or short words, matching the structure's data type;
  - lists for sorting and searching can be random, sorted, reversed or full of duplicates;
  - graphs get random weighted edges, optionally connected;
  - disjoint sets get random unions, and tries get random words.
- **Tests:**
  - An autouse fixture points `PYDSA_HOME` at `tmp_path` and uses settings suited to scripted runs, so tests never touch the real home folder.
  - New tests cover the shortcuts, Ctrl+C and Ctrl+D (by making the scripted input raise), argparse options, loading corrupt or unwritable settings, and every random generator's shape.

## Phase 2 — Guides & learning tools (v4.1)
- **Guide format:** one Markdown file per data structure topic, plus one per algorithm under `algorithms/`. The sections are fixed:
  ```markdown
  # Stack
  > One to three sentences shown when the topic opens.
  ## What it is
  ## How it works
  ## Real-life analogy
  ## When to use it
  ## When to avoid it
  ## In PyDSA            (what this implementation allows, e.g. fixed capacity, duplicate keys)
  ```
- **Writing style:** plain words, short sentences, second person, one concrete analogy, terms defined on first use (and linked to the glossary by name), and no Big-O numbers; the complexity table is shown right below the guide.
- **Content registry:** `content/registry.py` loads guides through `importlib.resources`, returns the summary and the sections, and renders them with `rich.markdown.Markdown` inside the existing panel style.
  - `pyproject.toml` declares the guide files as package data.
  - `render.intro` and `render.definition` take a topic id instead of raw text.
- **Rewrite:**
  - Every `*_DEFINITION` and `*_INFO` text in `texts.py` becomes a guide.
  - `WELCOME` and `OVERVIEW` are rewritten in the same tone; the overview becomes `guides/overview.md`, reachable from Learning Tools.
  - `texts.py` keeps only the banner, ASCII titles and changelog.
- **Opening a topic:** it shows the ASCII title, the summary and the complexity table. The operation menu's "Definition" option becomes **Read the Guide**, which shows the whole guide in the terminal's pager when it's longer than the screen.
- **Algorithm explanations:** they follow the detail setting. `brief` shows the guide's summary plus a "Read the full guide" hint, and `detailed` shows the How it works section before the algorithm runs.
- **Learning Tools** on the main menu:
  - **Glossary:** `glossary.md` with `## Term` entries. You can list the terms A–Z or type part of one to look it up, e.g. "amort" finds amortized.
  - **Which data structure should I use?:** `choosing.md`, a table of common needs, e.g. "undo history → stack, because…", with the topic id to open.
  - **Overview:** the rewritten overview.
- **Tests:**
  - Every registered topic and algorithm has a guide with all required sections and a non-empty summary.
  - No guide contains `O(`.
  - Every glossary term named in a guide exists.
  - The guides are included in the built wheel: build it with `pip wheel . -w` into a temporary folder and list its files.
  - Screen tests are updated for the new entry flow.

## Phase 3 — Operation notes & code view (v4.2)
- **Note data:** `content/notes.py` defines `OperationNote(topic, operation, summary, steps, complexity_row, pseudocode, source)`:
  - `summary` is one sentence;
  - `steps` are the numbered "how it works" lines;
  - `complexity_row` names the row in the topic's `ComplexityTable`, so the cost shown is read from the table instead of copied;
  - `pseudocode` is a few plain lines;
  - `source` points at the code, e.g. `"pydsa.core.stack:Stack.push"`.
- **Running an operation:**
  - `operation_menu` takes the topic id and shows each operation's note before its action runs.
  - `brief` shows one line: "How it works: … · Cost: O(1)". `detailed` shows the numbered steps and the cost.
  - Display-only operations get a summary without pseudocode.
- **Show the Code:** a new option in every operation menu. You pick an operation, then see its pseudocode panel and the real source from `inspect.getsource`, highlighted with `rich.syntax.Syntax`, with a note about what the source adds beyond the idea (type checks, errors).
- **Coverage:** notes for every operation of every existing topic, plus pseudocode and source for each sort, search and graph algorithm.
- **Tests:**
  - Every non-navigation label in every operation menu has a note (checked by building each screen's operation list without running it).
  - Every `complexity_row` exists in its table, and every `source` reference resolves to a function.

## Phase 4 — Step-through narration (v4.3)
- **Event model:** `algorithms/trace.py` defines `TraceEvent(kind, snapshot, marks, data)`:
  - `kind` is e.g. `compare`, `swap`, `write`, `pivot`, `probe`, `visit`, `rotate`, `relax`, `accept` or `skip`;
  - `snapshot` is a copy of the state to draw: a list, a tree as nested tuples, a table or a queue;
  - `marks` maps a position or node to its role;
  - `data` holds the values a caption needs.
- **Wording stays out of core:** core and algorithms only emit events. `content/narration.py` holds a caption template per kind, e.g. "{a} > {b}, so they swap places."
- **Existing contracts:** return values stay the same. Sorting generators yield TraceEvents instead of bare lists, and `event.snapshot` holds the list, so tests and `render.sorting_steps` are updated. `HeapStep` is replaced by TraceEvent. Other structures and algorithms take an optional `trace` list, like the searches' `probes` argument today.
- **Coverage:**
  - **Sorts:** compare/swap/write events, with pivot, gap, range or digit shown, and consecutive compares folded into the next change so the steps stay readable.
  - **Searches:** low/mid/high and the reason for each move.
  - **Heaps:** sift-up and sift-down.
  - **BST and AVL trees:**
    - the insert path;
    - the delete case (leaf, one child, or two children with the successor);
    - AVL rotations named LL/LR/RL/RR, with the tree before and after.
  - **Hash tables:** collisions and probing, and rehashing after a delete.
  - **Disjoint set:** find with path compression, and union by rank.
  - **Trie:** the insert and search paths, and pruning.
  - **Graphs:**
    - BFS/DFS with queue or stack contents;
    - Dijkstra's heap pops and relaxations, with the distance table;
    - Kahn's in-degree updates;
    - cycle detection states;
    - Prim and Kruskal edges accepted or skipped.
- **Step player:** `ui/stepper.py` `play(events, draw)` follows the steps setting.
  - `ask` asks "Watch it step by step?", where Enter shows everything at once.
  - `pause` waits after each step: Enter shows the next, `a` shows the rest, `s` stops and jumps to the result.
  - More than 200 steps offers a summary instead.
- **Tests:**
  - Exact event sequences for small inputs (e.g. bubble sort on `[3, 2, 1]`, AVL rotation cases, Dijkstra on the example graph).
  - Every event kind has a narration template.
  - Pause-mode screen tests script Enter, `a` and `s`.

## Phase 5 — Practice & progress (v4.4)
- **Quizzes:**
  - `content/quizzes.py` defines `Question(id, topic, prompt, choices, answer, explanation)`, with at least 5 questions per topic and algorithm family.
  - `practice/quiz.py` asks them with shuffled choices a–d, explains each answer, offers to retry the missed ones, and ends with a score.
- **Predict the result:** `practice/challenges.py` builds a random structure, shows it, asks what an operation will produce and checks against the real core result. For example:
  - the next pop, dequeue or extract;
  - an inorder or level-order sequence;
  - the slot a probing insert lands in;
  - a find root;
  - the array after one bubble pass;
  - a shortest distance, or which edge Kruskal takes next.
- **Practice option:** in every operation menu (questions and challenges for that topic), plus a **Practice** entry on the main menu for a mixed session across the topics you've visited.
- **Big-O experiments:**
  - `practice/experiments.py` defines `Experiment(id, topic, name, expected, sizes, make_input, run)`, where `run` returns a work count:
    - comparisons and writes from `SortStats`;
    - search probes;
    - heap swaps;
    - nodes visited in BST or AVL inserts;
    - hash table probes;
    - parent hops in a disjoint set.
  - The table shows n, work, work ÷ expected(n) and a small █ bar, with a note that a steady ratio means the growth matches the expected Big-O.
  - Inputs can be random, sorted or reversed, e.g. to watch a BST go from O(log n) to O(n).
  - Sizes are capped so each run takes about two seconds at most, for example 2,000 for the O(n²) sorts. Time in milliseconds is shown only as a secondary column, with a caveat.
- **Progress:**
  - `progress.py` saves versioned JSON next to the settings: when each topic was last visited, best quiz scores and attempts, and challenges solved.
  - The main menu shows a line like "12 of 20 topics visited · quiz average 80%", and topic lists mark visited topics with ✓.
  - Settings can reset progress, after confirming.
- **Wrap-up:** update the README (shortcuts, settings, learning tools, practice), set the version to 4.4 and **delete `docs/plans/roadmap-v4.md`**, keeping `docs/plans/.gitkeep`.
- **Tests:**
  - Every quiz has a valid answer index, unique choices and an explanation.
  - Challenge answers match the core results across many random seeds.
  - Experiments run quickly at small sizes, and their ratios behave as expected (e.g. merge sort's work ÷ (n log n) stays within a band).
  - Progress round-trips, ignores corrupt files and is written only under `tmp_path`.

## Verification (every phase)
- `pip install -e ".[test]"`, then `pytest`: all tests pass, and new content is covered by the completeness tests.
- `pydsa` and `python -m pydsa` start, and the new command-line options work. A scripted stdin run walks every new menu path to Exit without tracebacks, including Ctrl+C at a prompt.
- A run at 90 and 45 columns and with `NO_COLOR` has no lines wider than the terminal apart from ASCII titles.
- `python -W error -c "import pydsa"` gives no warnings, and a built wheel contains every guide file.
