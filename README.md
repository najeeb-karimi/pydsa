# 🐍 PyDSA

PyDSA is a Python app that runs in your terminal and helps you learn data structures and algorithms. Each topic has a short summary, a table showing how its work grows with input size, and a guide explaining what it is, how it works, and when to use it. Start with an example, generate random data or type your own inputs. Then choose an operation by typing its number and watch the results in tables, diagrams and narrated steps.

It's made for students and self-learners who want to *see* how data structures and algorithms behave, not just read about them. You don't need to write any code to use it.

## 🚀 Quick Start

With Python 3.10 or newer, Git and an activated virtual environment, run:

```bash
git clone https://github.com/najeeb-karimi/pydsa.git
cd pydsa
python -m pip install .
pydsa
```

Need to set up Python or a virtual environment first? Follow [Requirements](#-requirements) and [Installation](#-installation) below.

## ✨ What You Can Learn

**Linear structures** (items are kept in a line, one after another):

- **Array:** a fixed-size row of items. You can also sort it with nine different sorting methods and watch every step, or search it with five different searching methods.
- **Stack:** the last item you add is the first one out, like a stack of plates.
- **Queue:** the first item you add is the first one out, like people waiting in line.
- **Deque:** a queue you can add to and remove from at both ends.
- **Linked List:** items connected like a chain, in singly (one-way) and doubly (two-way) versions. Each one also comes in a circular version, where the last item links back to the first, so you can walk around the loop.
- **Skip List:** sorted keys with express lanes above the base list. Watch seeded coin flips choose node heights and searches move right and down.

**Trees & heaps** (keys arranged in branches or by priority):

- **Tree:** items arranged like a family tree, as a Binary Search Tree (BST) or a self-balancing AVL tree. Trees are drawn from the top down, and you can also walk through them level by level or see their height and size.
- **Red-Black Tree:** a balanced search tree with red and black nodes. Watch recoloring and rotations after insertions and deletions; R/B markers keep colors readable in plain output.
- **B-Tree:** a search tree with several keys per node. Choose its minimum degree, then watch full nodes split or deletion borrow keys and merge siblings.
- **Segment Tree:** stores sums, minima or maxima for array ranges. Watch queries select covered nodes and point updates refresh a leaf and its ancestors.
- **Fenwick Tree:** stores block sums for prefix and range queries. Binary index jumps show the lowest set bit being removed during queries and added during point updates.
- **Heap & Priority Queue:** a min heap always keeps the smallest item on top, and a max heap the largest. You can watch every swap as items move up or down the tree. The priority queue is built on a heap and always serves the most important item first.
- **Trie:** stores words letter by letter, so words that start the same way share their first letters. It can finish words for you (autocomplete).

**Graphs & sets** (connections and groups):

- **Graph:** points connected by lines with weights, stored as a table (adjacency matrix) or as lists (adjacency list). The lines can be one-way (directed) or two-way (undirected). You can walk through it with BFS or DFS, and run the graph algorithms below on it.
- **Disjoint Set:** splits items into groups that don't overlap and quickly tells you whether two items are in the same group (also called Union-Find).

**Hashing & caches** (keys mapped to storage positions):

- **Hash Table:** stores key-value pairs for fast lookups, using separate chaining or linear probing to handle keys that land in the same spot. There's also a **Hash Set**, which keeps unique items and lets you combine two sets with union, intersection and difference.
- **Bloom Filter:** rules out absent words using stable salted hashes and a bit array. Positive results explain false positives; an experiment compares their measured rate with the usual formula.
- **LRU Cache:** keeps a limited number of key-value pairs. Get and Put mark entries as recently used, and a new entry evicts the least recent one when full.

**Algorithms** (step-by-step recipes for solving common problems):

- **Sorting:** nine ways to put a list in order: Bubble, Selection, Insertion, Quick, Heap, Shell, Merge, Counting and Radix Sort. Watch every step, or compare how much work each one does on the same list.
- **Searching:** five ways to find an item: Linear, Binary, Jump, Interpolation and Exponential Search. Each search shows which positions it checked.
- **Graph Algorithms:** find shortest routes with Dijkstra for non-negative weights, or Bellman-Ford when weights can be negative. Bellman-Ford also shows reachable negative cycles. Floyd-Warshall shows distances between every pair of vertices after each intermediate vertex and rebuilds chosen paths. A* draws routes through grids with typed or random walls and compares how many cells it explores with Dijkstra. You can also order dependent tasks (Topological Sort), spot loops (Cycle Detection), and connect every point cheaply (Prim and Kruskal).
- **String Algorithms:** find every occurrence of a pattern with Naive Search, KMP or Rabin-Karp. Watch alignments, prefix-table construction and reused comparisons, or rolling hashes and verified collisions. Type text and pattern, use an example or generate random strings, then compare character checks on the same input.
- **Dynamic Programming:** compare Fibonacci recursion, memoization and tabulation by actual call counts. Fill 0/1 knapsack, longest common subsequence and coin-change tables step by step, then trace chosen items, subsequence characters or minimum coins. Coin change also counts unordered combinations.
- **Recursion & Backtracking:** move Tower of Hanoi disks with every peg state recorded, follow permutation recursion trees, and watch N-Queens placements and backtracks while counting solutions. Typed, example and random inputs stay small enough to explore.

**Learning Tools** (on the main menu):

- **Overview:** a friendly introduction to data structures, algorithms and how their speed is measured.
- **Browse the Guides:** read the guide of any topic or algorithm without opening it first.
- **Glossary:** short explanations of every term the guides use, which you can list from A to Z or look up by typing part of a word.
- **Which Data Structure Should I Use?:** common needs, like an undo history or autocomplete, matched with the topic that fits them.

**Practice** (on the main menu and in every topic's operation menu):

- **Quizzes:** five explained questions for every topic and algorithm, with shuffled choices and a chance to retry missed answers.
- **Predict the Result:** inspect fresh practice data and predict an operation's result. The real implementation checks the answer.
- **Big-O Experiments:** compare actual work as input sizes grow. Some experiments let you compare random, sorted and reversed inputs; others keep a fixed example to show a particular behavior. Most tables show work counts, growth ratios, bars and elapsed time. The Bloom filter experiment compares measured false positives with the expected rate.
- **Progress:** visited topics, best quiz scores, quiz attempts and solved predictions are saved between sessions.

## 👀 A Quick Look

Here's a short session, trimmed to fit: the user opens the stack, loads the example and pops the top item. The numbers after `>>>` are what the user typed.

```text
📂 What do you want to learn?
  1) Linear structures
  2) Trees & heaps
  3) Graphs & sets
  4) Hashing & caches
  5) Algorithms

  6) Learning Tools
  7) Settings
  8) Practice

  0) Exit
>>> 1

🏁 Which linear data structure do you want to learn?
  1) Array
  2) Stack
  ...
>>> 2

(The stack's title, summary and complexity table appear here.)

🛠️  Do you want to create a stack yourself or use the preloaded example?
  1) Create a stack
  2) Use the example
  3) Fill with random values

  0) Go Back
>>> 2

✅ Loaded the example stack.
┌───────┬───────────┬───────┐
│ Index │   Item    │       │
├───────┼───────────┼───────┤
│     4 │   empty   │       │
│     3 │   empty   │       │
│     2 │   empty   │       │
│     1 │  'Messi'  │ ← top │
│     0 │    10     │       │
└───────┴───────────┴───────┘

⚔️  What do you want to do with the stack?
   1) Read the Guide
   2) Push
   3) Pop
   ...
>>> 3

💡 Pop: Takes the top item off the stack and gives it to you. · Cost: Time O(1) · Extra space O(1)

✅ Popped 'Messi' from the top.
```

## 📋 Requirements

- **Python 3.10 or newer.** To check your version, run `python --version` (on Windows, you can also try `py --version`).
- **A terminal that can show emojis and box-drawing lines.** Windows Terminal, the macOS Terminal and most Linux terminals work well. The old Windows Command Prompt window may show empty boxes instead of emojis.
- **[rich](https://github.com/Textualize/rich)**, the package that draws the colors and tables. You don't need to install it yourself; it's installed together with PyDSA.

## 📦 Installation

1. **Install Python 3.10 or newer** if you do not have it yet. Use the version command in Requirements to check it.
2. **Download the project.** If you have Git, run:

   ```bash
   git clone https://github.com/najeeb-karimi/pydsa.git
   cd pydsa
   ```

   You can also download the repository as a ZIP file from GitHub. Unzip it, then open a terminal in the folder containing `pyproject.toml`.
3. **Create and activate a virtual environment.** This gives PyDSA its own Python packages. Choose the commands for your terminal.

   Windows PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Windows Command Prompt:

   ```bat
   py -m venv .venv
   .venv\Scripts\activate.bat
   ```

   macOS and Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Your prompt usually starts with `(.venv)` after activation. When you open a new terminal, return to the project folder and run only the activation command for your terminal again.

   If PowerShell blocks activation, you can use the environment directly: run `.\.venv\Scripts\python.exe -m pip install .`, then `.\.venv\Scripts\python.exe -m pydsa`. Activation is optional when you use that full interpreter path.
4. **Install PyDSA** with the environment active:

   ```bash
   python -m pip install .
   ```

   This also installs the `rich` package used for tables and colors.

## ▶️ How to Use

With your virtual environment active, start the app from any folder:

```bash
pydsa
```

If the terminal says the command isn't found, activate your virtual environment and try again. You can also start the app with `python -m pydsa` using the same environment.

### 🧭 Moving Around

- Type the number next to an option and press Enter.
- In menus where you pick a topic or a type, `0) Go Back` returns to the previous menu.
- Once you're working with a data structure or an algorithm, its menu offers:
  - **Read the Guide:** shows the topic's whole guide and its complexity table. Where a menu has more than one guide, such as a kind of tree and trees in general, you pick which one to read.
  - **Show the Code:** pick an operation to see its pseudocode next to the real Python code that runs it.
  - **Practice:** take a quiz, predict a result on fresh data, or run a work-count experiment where one is available.
  - **New ...** (such as **New Stack**): starts that topic over with fresh data.
  - **Main Menu:** goes back to the first menu.
  - **`0) Exit`:** closes the app.
- Before an operation runs, a short note tells you what it does and what it costs.
- Operations that take several steps, such as a sort, an AVL rotation or a graph search, tell you what happens in each step. With the default Steps setting, PyDSA asks whether you want to watch them one at a time: press Enter to see them all at once, or type `y` to watch. At a step, Enter shows the next one, `a` shows the rest and `s` stops playback. The operation has already run, so stopping playback keeps its result.
- Runs with more than 200 steps show the first and last three captions by default. In an interactive terminal, you can choose to watch the whole run. Sorting captions group comparisons and writes between changes, and search captions show the active bounds and why the search moves. Piped or scripted sessions never pause for playback or long guides.
- A guide that's longer than your terminal pauses after each screenful: press Enter to keep reading, `a` to show the rest or `s` to stop.
- If you type an invalid value, PyDSA explains the problem. Input prompts let you try again; rejected operations, such as popping an empty stack, return to the operation menu.

### ⌨️ Shortcuts

These work in every menu:

| In a menu | While typing a value | What it does |
| --- | --- | --- |
| `h` or `?` | `:h` | Shows help and where you are |
| `b` | `:b` | Goes back to the previous menu, cancelling what you were typing |
| `q` | `:q` | Quits PyDSA |

While typing a value, the shortcuts start with `:`, so you can still enter a real `q` or `b`. Pressing Ctrl+C also quits cleanly.
In quizzes, type `a`, `b`, `c` or `d` to answer; use `:b` to leave because `b` is an answer choice. Help and quit still work with `h` and `q`.

### ✍️ Typing Values

- **Examples, random values or your own data:** every topic lets you start with a preloaded example, generate random inputs, or create your own, so you can explore before typing anything.
- **Data types:** when you add an item, PyDSA may ask whether it's a `str` (text), an `int` (whole number) or a `float` (decimal number). Text is shown in quotes, so `'7'` is the text 7 and `7` is the number.
- **Lists:** when PyDSA asks for several values at once, such as a list to sort, separate them with commas: `5, 3, 8, 1`.
- **Text:** string-search and LCS inputs keep spaces, including at the beginning and end. Press Enter for an empty string. Matches are case-sensitive, and indexes count Python characters.
- **Indexes:** array positions and grid coordinates start at 0. Range queries include both ends. The Fenwick block display uses internal indexes starting at 1, but its input prompts use array positions starting at 0.
- **Input limits:** follow the range shown in each prompt. Fibonacci is capped at index 16, Hanoi at 10 disks, permutations at 4 items and N-Queens at board size 8 to keep interactive runs manageable.

### 📚 Learning Tools

Choose **Learning Tools** on the main menu to read the overview, browse every guide, look up a term in the glossary, or find the data structure that fits what you need. Words shown in bold in a guide are explained in the glossary.

### 🧩 Practice and Progress

Choose **Practice** in a topic's operation menu to work on that topic. On the main menu, Practice offers a mixed quiz across visited topics, a prediction on a visited topic, all experiments, a topic browser and your progress. If you have not visited a topic yet, start with the browser.

Each quiz explains every answer and ends with a score. You can retry missed questions; the saved score comes from the completed first round. Leaving a quiz early does not save a partial score. The quiz average uses your best score for each practiced topic.

Predictions show new practice data, so they do not change the structure you were working with. Enter a number, a word, `true` or `false`, or a list such as `[1, 2, 3]`. Put quotes around words in a list, such as `['car', 'card']`. Correct predictions add to your solved count.

Most experiments count work such as comparisons, writes, visited nodes, recursive calls, table cells or disk moves. Each experiment explains what it counts and what n means. A steady **work ÷ expected(n)** ratio suggests that the count follows the chosen growth pattern. Input sizes are capped to keep runs short. Elapsed milliseconds also depend on machine speed and tracing; input construction is excluded from timing. For binary search, probes are counted, while copying, sorting and mapping indexes still contribute to elapsed time. Bloom filter practice instead compares the observed false positive rate with an approximate formula.

The main menu shows how many topics you have visited, and topic lists mark visits with `✓`. Progress is saved in `progress.json` beside your settings, under `~/.pydsa` or the folder named by `PYDSA_HOME`. Settings offers **Reset Progress**, with confirmation. Restoring settings defaults keeps your progress.

### ⚙️ Settings

Choose **Settings** on the main menu to change how PyDSA behaves. Choices are saved immediately in `settings.json`, under `~/.pydsa` or the folder named by `PYDSA_HOME`, so they last between sessions:

- **Explanations:** before an operation or algorithm runs, Brief shows a one-line note or a short summary, and Detailed also shows how it works, step by step.
- **Steps:** Ask Each Time, All at Once or Pause After Each One. With Ask Each Time or Pause After Each One, runs longer than 200 steps ask before playing every step in an interactive terminal.
- **Colors:** turn colors off for plain output. Markers such as `*` still show changes.
- **Clear the Screen:** turn it off to keep everything on screen and scroll back through it.
- **Welcome Intro:** show the long intro once per session, or every time you return to the main menu.
- **Restore the Defaults:** reset settings after confirmation. Your learning progress stays saved.
- **Reset Progress:** clear visited topics, quiz scores and solved predictions after confirming.

### 🚩 Command-Line Options

```bash
pydsa --topic stack        # open a topic directly
pydsa --list-topics        # show the ID of every topic
pydsa --no-color           # turn colors off for this run
pydsa --reset-settings     # restore the default settings
pydsa --version            # show the version
pydsa --help               # show all command-line options
```

Use `--list-topics` to find an ID, then pass it to `--topic`. Some algorithm IDs, such as `kmp` or `bellman-ford`, open their shared algorithm screen; choose the algorithm from its operation menu. IDs such as `fibonacci` and `n-queens` open that problem directly.

`--no-color` applies only to that run. `--reset-settings` saves the default settings before starting the app and keeps your progress. These options also work with `python -m pydsa`, for example `python -m pydsa --topic stack --no-color`.

### 🎨 Display Tips

- Make the terminal window wider if a table looks cramped. Wide arrays, trees and tables switch to a taller layout when the window is narrow.
- To turn off colors for good, use Settings, or set the `NO_COLOR` environment variable before starting the app.
- If emojis or box-drawing characters look wrong, use a terminal and font that support them. Turning colors off only removes color; it does not replace these characters.

## 🔄 Updating and Uninstalling

If you cloned the repository with Git, update it from inside the project folder with your virtual environment active:

```bash
git pull
python -m pip install .
```

If you downloaded a ZIP, download and unzip the new copy, then repeat the installation steps. Your settings and progress are stored separately from the project.

To uninstall PyDSA from the active environment, run `python -m pip uninstall pydsa`. This keeps the project files, settings and saved progress.

## 🧪 Running the Tests

From the project folder, with your virtual environment active, install the testing tools and run the tests:

```bash
python -m pip install -e ".[test]"
python -m pytest
```

Editable mode lets the app use your source changes without reinstalling after each edit.

## 🗂️ Project Structure

All the code is inside the `pydsa` folder:

- `core/`: the data structures themselves.
- `algorithms/`: sorting, searching, graphs, string search, dynamic programming and recursive algorithms.
- `practice/`: quiz sessions, predictions checked against core operations, and bounded work-count experiments.
- `ui/`: everything you see and type in the terminal, such as menus, prompts and output.
- `content/`: the guides and the glossary (Markdown files in `content/guides`), the notes shown before every operation, the sentence for every kind of step, the ASCII art titles and the complexity tables.
- `progress.py`: versioned learning records saved next to the settings.
- `settings.py`: loads and saves app preferences.
- `topics.py`: topic IDs, categories and the screens they open.

The tests are in `tests/`. [AGENTS.md](AGENTS.md) records the repository's implementation, testing and commit-message conventions for coding agents.
