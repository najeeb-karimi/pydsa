# 🐍 PyDSA
PyDSA is a Python app that runs in your terminal and helps you learn data structures and algorithms. Every topic opens with a short summary and a table of how fast its operations are, and a full guide explains it in plain words: what it is, how it works, a real-life analogy, and when to use it or avoid it. You then get a ready-made example to play with and a list of things you can do with it. Every change is drawn right away as a colorful table or diagram, so you can see what happened. You choose what to do by typing a number.

It's made for students and self-learners who want to *see* how data structures and algorithms behave, not just read about them. You don't need to write any code to use it.

## 🚀 Quick Start
If you already have Python 3.10 or newer:
```bash
git clone https://github.com/najeeb-karimi/pydsa.git
cd pydsa
pip install .
pydsa
```
New to Python or the terminal? Follow the step-by-step [Installation](#-installation) below instead.

## ✨ What You Can Learn
**Linear data structures** (items are kept in a line, one after another):
- **Array:** a fixed-size row of items. You can also sort it with nine different sorting methods and watch every step, or search it with five different searching methods.
- **Stack:** the last item you add is the first one out, like a stack of plates.
- **Queue:** the first item you add is the first one out, like people waiting in line.
- **Deque:** a queue you can add to and remove from at both ends.
- **Linked List:** items connected like a chain, in singly (one-way) and doubly (two-way) versions. Each one also comes in a circular version, where the last item links back to the first, so you can walk around the loop.

**Non-linear data structures** (items are connected in more complex ways):
- **Tree:** items arranged like a family tree, as a Binary Search Tree (BST) or a self-balancing AVL tree. Trees are drawn from the top down, and you can also walk through them level by level or see their height and size.
- **Heap & Priority Queue:** a min heap always keeps the smallest item on top, and a max heap the largest. You can watch every swap as items move up or down the tree. The priority queue is built on a heap and always serves the most important item first.
- **Trie:** stores words letter by letter, so words that start the same way share their first letters. It can finish words for you (autocomplete).
- **Graph:** points connected by lines with weights, stored as a table (adjacency matrix) or as lists (adjacency list). The lines can be one-way (directed) or two-way (undirected). You can walk through it with BFS or DFS, and run the graph algorithms below on it.
- **Hash Table:** stores key-value pairs for fast lookups, using separate chaining or linear probing to handle keys that land in the same spot. There's also a **Hash Set**, which keeps unique items and lets you combine two sets with union, intersection and difference.
- **Disjoint Set:** splits items into groups that don't overlap and quickly tells you whether two items are in the same group (also called Union-Find).

**Algorithms** (step-by-step recipes for solving common problems):
- **Sorting:** nine ways to put a list in order: Bubble, Selection, Insertion, Quick, Heap, Shell, Merge, Counting and Radix Sort. Watch every step, or compare how much work each one does on the same list.
- **Searching:** five ways to find an item: Linear, Binary, Jump, Interpolation and Exponential Search. Each search shows which positions it checked.
- **Graph Algorithms:** find the shortest routes (Dijkstra), put tasks in an order that respects what depends on what (Topological Sort), spot loops (Cycle Detection), and connect every point as cheaply as possible (Prim and Kruskal).

**Learning Tools** (on the main menu):
- **Overview:** a friendly introduction to data structures, algorithms and how their speed is measured.
- **Browse the Guides:** read the guide of any topic or algorithm without opening it first.
- **Glossary:** short explanations of every term the guides use, which you can list from A to Z or look up by typing part of a word.
- **Which Data Structure Should I Use?:** common needs, like an undo history or autocomplete, matched with the topic that fits them.

## 👀 A Quick Look
Here's a short session, trimmed to fit: the user opens the stack, loads the example and pops the top item. The numbers after `>>>` are what the user typed.
```text
📂 What do you want to learn?
  1) Linear data structures
  2) Non-linear data structures
  3) Algorithms

  4) Learning Tools
  5) Settings

  0) Exit
>>> 1

🏁 Which linear data structure do you want to learn?
  1) Array
  2) Stack
  ...
>>> 2

(The stack's title, summary and complexity table appear here.)

🛠️ Do you want to create a stack yourself or use the preloaded example?
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

⚔️ What do you want to do with the stack?
   1) Read the Guide
   2) Push
   3) Pop
   ...
>>> 3

✅ Popped 'Messi' from the top.
```

## 📋 Requirements
- **Python 3.10 or newer.** To check your version, run `python --version` (on Windows, you can also try `py --version`).
- **A terminal that can show emojis and box-drawing lines.** Windows Terminal, the macOS Terminal and most Linux terminals work well. The old Windows Command Prompt window may show empty boxes instead of emojis.
- **[rich](https://github.com/Textualize/rich)**, the package that draws the colors and tables. You don't need to install it yourself; it's installed together with PyDSA.

## 📦 Installation
1. **Download the project** with Git, or download it as a ZIP file from GitHub and unzip it:
   ```bash
   git clone https://github.com/najeeb-karimi/pydsa.git
   cd pydsa
   ```
2. **Create a virtual environment** (recommended). This keeps PyDSA and its package separate from the rest of your computer:
   ```bash
   # Windows
   py -m venv .venv
   .venv\Scripts\activate

   # macOS and Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Your terminal prompt now starts with `(.venv)`. Run the `activate` line again whenever you open a new terminal.
3. **Install PyDSA:**
   ```bash
   pip install .
   ```

## ▶️ How to Use
Start the app:
```bash
pydsa
```
If the terminal says the command isn't found, make sure your virtual environment is active, or run `python -m pydsa` instead.

### 🧭 Moving Around
- Type the number next to an option and press Enter.
- In menus where you pick a topic or a type, `0) Go Back` returns to the previous menu.
- Once you're working with a data structure or an algorithm, its menu offers:
  - **Read the Guide:** shows the topic's whole guide and its complexity table. Where a menu has more than one guide, such as a kind of tree and trees in general, you pick which one to read.
  - **New ...** (such as **New Stack**): starts that topic over with fresh data.
  - **Main Menu:** goes back to the first menu.
  - **`0) Exit`:** closes the app.
- A guide that's longer than your terminal pauses after each screenful: press Enter to keep reading, `a` to show the rest or `s` to stop.
- If you type something that isn't allowed, PyDSA tells you what went wrong and asks again, so you can't break anything.

### ⌨️ Shortcuts
These work in every menu:

| In a menu | While typing a value | What it does |
| --- | --- | --- |
| `h` or `?` | `:h` | Shows help and where you are |
| `b` | `:b` | Goes back to the previous menu, cancelling what you were typing |
| `q` | `:q` | Quits PyDSA |

While typing a value, the shortcuts start with `:`, so you can still enter a real `q` or `b`. Pressing Ctrl+C also quits cleanly.

### ✍️ Typing Values
- **Examples, random values or your own data:** every topic lets you start with a preloaded example, fill it with random values of the size you choose, or create your own, so you can explore before typing anything.
- **Data types:** when you add an item, PyDSA may ask whether it's a `str` (text), an `int` (whole number) or a `float` (decimal number). Text is shown in quotes, so `'7'` is the text 7 and `7` is the number.
- **Lists:** when PyDSA asks for several values at once, such as a list to sort, separate them with commas: `5, 3, 8, 1`.

### 📚 Learning Tools
Choose **Learning Tools** on the main menu to read the overview, browse every guide, look up a term in the glossary, or find the data structure that fits what you need. Words shown in bold in a guide are explained in the glossary.

### ⚙️ Settings
Choose **Settings** on the main menu to change how PyDSA behaves. Your choices are saved in a `.pydsa` folder in your home folder, so they last between sessions:
- **Explanations:** before an algorithm runs, Brief shows a short summary of it, and Detailed shows how it works, step by step.
- **Colors:** turn colors off if your terminal shows strange symbols.
- **Clear the Screen:** turn it off to keep everything on screen and scroll back through it.
- **Welcome Intro:** show the long intro once per session, or every time you return to the main menu.

### 🚩 Command-Line Options
```bash
pydsa --topic stack        # open a topic directly
pydsa --list-topics        # show the ID of every topic
pydsa --no-color           # turn colors off for this run
pydsa --reset-settings     # restore the default settings
pydsa --version            # show the version
```

### 🎨 Display Tips
- Make the terminal window wider if a table looks cramped. Wide arrays, trees and tables switch to a taller layout when the window is narrow.
- To turn off colors for good, use Settings, or set the `NO_COLOR` environment variable before starting the app.

## 🔄 Updating and Uninstalling
To get the latest version, run these commands inside the `pydsa` folder, with your virtual environment active:
```bash
git pull
pip install .
```
To remove PyDSA, run `pip uninstall pydsa`, or simply delete the `pydsa` folder if you used a virtual environment.

## 🧪 Running the Tests
If you want to change the code, install the project in editable mode together with the testing tools, then run the tests:
```bash
pip install -e ".[test]"
pytest
```

## 🗂️ Project Structure
All the code is inside the `pydsa` folder:
- `core/`: the data structures themselves.
- `algorithms/`: the sorting, searching and graph algorithms.
- `ui/`: everything you see and type in the terminal, such as menus, prompts and output.
- `content/`: the guides and the glossary (Markdown files in `content/guides`), the ASCII art titles and the complexity tables.

The tests are in the `tests` folder.
