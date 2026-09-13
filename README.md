# 🐍 PyDSA
PyDSA is a Python app that runs in your terminal and helps you learn data structures. For each data structure, you get a short explanation, a table of how fast its operations are, a ready-made example to play with, and a list of things you can do with it. Every change is drawn right away as a colorful table or diagram, so you can see what happened. You choose what to do by typing a number.

## ✨ What You Can Learn
**Linear data structures** (items are kept in a line, one after another):
- **Array:** a fixed-size row of items. You can also sort it with six different sorting methods and watch every step, or search it with linear or binary search.
- **Stack:** the last item you add is the first one out, like a stack of plates.
- **Queue:** the first item you add is the first one out, like people waiting in line.
- **Deque:** a queue you can add to and remove from at both ends.
- **Linked List:** items connected like a chain, in singly (one-way) and doubly (two-way) versions. Each one also comes in a circular version, where the last item links back to the first, so you can walk around the loop.

**Non-linear data structures** (items are connected in more complex ways):
- **Tree:** items arranged like a family tree, as a Binary Search Tree (BST) or a self-balancing AVL tree. Trees are drawn from the top down, and you can also walk through them level by level or see their height and size.
- **Heap & Priority Queue:** a min heap always keeps the smallest item on top, and a max heap the largest. You can watch every swap as items move up or down the tree. The priority queue is built on a heap and always serves the most important item first.
- **Trie:** stores words letter by letter, so words that start the same way share their first letters. It can finish words for you (autocomplete).
- **Graph:** points connected by lines with weights, stored as a table (adjacency matrix) or as lists (adjacency list). You can walk through it with BFS or DFS.
- **Hash Table:** stores key-value pairs for fast lookups, using separate chaining or linear probing to handle keys that land in the same spot. There's also a **Hash Set**, which keeps unique items and lets you combine two sets with union, intersection and difference.
- **Disjoint Set:** splits items into groups that don't overlap and quickly tells you whether two items are in the same group (also called Union-Find).

## 📋 Requirements
You need Python 3.10 or newer. To check your version, run `python --version`. The only other package PyDSA needs is [rich](https://github.com/Textualize/rich), which is installed for you automatically.

## 📦 Installation
Download the project and install it:
```bash
git clone https://github.com/najeeb-karimi/pydsa.git
cd pydsa
pip install .
```

## ▶️ How to Use
Start the app:
```bash
pydsa
```
If that command isn't found, run `python -m pydsa` instead.

Then follow the menus on the screen. Type the number next to the option you want and press Enter. In every menu, `0` takes you back or exits.

## 🧪 Running the Tests
If you want to change the code, install the project in editable mode together with the testing tools, then run the tests:
```bash
pip install -e ".[test]"
pytest
```

## 🗂️ Project Structure
All the code is inside the `pydsa` folder:
- `core/`: the data structures themselves.
- `algorithms/`: the sorting and searching algorithms.
- `ui/`: everything you see and type in the terminal, such as menus, prompts and output.
- `content/`: the longer texts, like explanations and ASCII art titles, plus the complexity tables.

The tests are in the `tests` folder.
