# 🐍 PyDSA
PyDSA is a Python app that runs in your terminal and helps you learn data structures. For each data structure, you get a short explanation, a ready-made example to play with, and a list of things you can do with it. You choose what to do by typing a number.

## ✨ What You Can Learn
**Linear data structures** (items are kept in a line, one after another):
- **Array:** a fixed-size row of items. You can also sort it with six different sorting methods and watch every step, or search it with linear or binary search.
- **Stack:** the last item you add is the first one out, like a stack of plates.
- **Queue:** the first item you add is the first one out, like people waiting in line.
- **Linked List:** items connected like a chain, in singly (one-way) and doubly (two-way) versions.

**Non-linear data structures** (items are connected in more complex ways):
- **Tree:** items arranged like a family tree, as a Binary Search Tree (BST) or a self-balancing AVL tree.
- **Graph:** points connected by lines with weights, stored as a table (adjacency matrix) or as lists (adjacency list). You can walk through it with BFS or DFS.
- **Hash Table:** stores key-value pairs for fast lookups, using separate chaining or linear probing to handle keys that land in the same spot.

## 📋 Requirements
You need Python 3.10 or newer. To check your version, run `python --version`.

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

Then follow the menus on the screen. Type the number next to the option you want and press Enter.

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
- `content/`: the longer texts, like explanations and ASCII art titles.

The tests are in the `tests` folder.
