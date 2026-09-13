"""Shared helpers for PyDSA: screen clearing and the intro text."""

import os


def clear():
    """Clear the terminal screen."""
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # macOS and Linux (os.name is 'posix')
    else:
        os.system('clear')


def input_verify(condition="all", msg="item"):
    """Prompt for a value and return it, or None if it can't be converted to the requested type.

    condition is "all" (the user picks str, int or float), "str", "num" (the user picks
    int or float), "int" or "float"; msg names the value in the prompts.
    """

    # Any of str, int or float, picked by the user; used in the linked list implementation
    if condition == "all":
        while True:
            choice = input(f"""\n🤔 Please specify the data type of the {msg}:
•1) str
•2) int
•3) float
>>> """)
            # Validate the type code before asking for the item, so the item prompt isn't repeated in every case
            if choice not in ("1", "2", "3"):
                print("\n🚫 Invalid code number! Please use code numbers 1–3.")
                continue
            else:
                break

        item = input(f"\n✍️ Please enter the {msg}.\n>>> ")

        match choice:
            case "1":
                return item
            case "2":
                try:
                    item = int(item)
                except ValueError:
                    return None
                else:
                    return item
            case "3":
                try:
                    item = float(item)
                except ValueError:
                    return None
                else:
                    return item

    # String input only; used in the array and tree implementations
    elif condition == "str":
        item = input(f"\n✍️ Please enter the {msg}. (STRING)\n>>> ")
        return item

    # Numeric input only (int or float, picked by the user); used in the tree implementation
    elif condition == "num":
        while True:
            choice = input("""\n🤔 Please specify the type of NUMERAL data you want to enter:
•1) int
•2) float
>>> """)
            if choice not in ("1", "2"):
                print("\n🚫 Invalid code number! Please use code numbers 1 or 2.")
                continue
            else:
                break

        match choice:
            case "1":
                item = input(f"\n✍️ Please enter the {msg}. (INT)\n>>> ")
                try:
                    item = int(item)
                except ValueError:
                    return None
                else:
                    return item

            case "2":
                item = input(f"\n✍️ Please enter the {msg}. (FLOAT)\n>>> ")
                try:
                    item = float(item)
                except ValueError:
                    return None
                else:
                    return item

    # Integer input only; used in the array implementation
    elif condition == "int":
        item = input(f"\n✍️ Please enter the {msg}. (INT)\n>>> ")
        try:
            item = int(item)
        except ValueError:
            return None
        else:
            return item

    # Float input only; used in the array implementation
    elif condition == "float":
        item = input(f"\n✍️ Please enter the {msg}. (FLOAT)\n>>> ")
        try:
            item = float(item)
        except ValueError:
            return None
        else:
            return item


def order_verify():
    """Ask for a sorting order and return "asc" or "desc"."""
    while True:
        order = input("""\n🤔 Please specify the order.
•1) Ascending
•2) Descending
>>> """)
        if order not in ("1", "2"):
            print("\n🚫 Invalid code number.")
            continue
        if order == "1":
            return "asc"
        else:
            return "desc"


def main_intro():
    """Print the PyDSA banner, welcome message, version, changelog and data structure overview."""
    print(r"""

.-------.  ____     __  ______        .-'''-.    ____     
\  _(`)_ \ \   \   /  /|    _ `''.   / _     \ .'  __ `.  
| (_ o._)|  \  _. /  ' | _ | ) _  \ (`' )/`--'/   '  \  \ 
|  (_,_) /   _( )_ .'  |( ''_'  ) |(_ o _).   |___|  /  | 
|   '-.-'___(_ o _)'   | . (_) `. | (_,_). '.    _.-`   | 
|   |   |   |(_,_)'    |(_    ._) '.---.  \  :.'   _    | 
|   |   |   `-'  /     |  (_.\.' / \    `-'  ||  _( )_  | 
/   )    \      /      |       .'   \       / \ (_ o _) / 
`---'     `-..-'       '-----'`      `-...-'   '.(_,_).'


""")

    print("💻 Welcome to PyDSA, a console-based Python app that strives to assist you in learning data structures! The app is designed to give you a good tour of the all 7 major DSes, giving you an opportunity to wrap your head around their distinctions while on the go! All interaction with the app is based on typing the related number & letter codes in the terminal.\n")
    print("⏳ Version 2.2")
    print("""📝 Changelog for this major release:
   ★ Adding Non-linear Data Structures
   ★ Including Examples
   ★ Showing Array Sorting Steps
   ★ Bug Fixes, Refactorings & Refinements""")
    print("""🌐 All the source code & future updates are available in this GitHub repo:
   ★ https://github.com/najeeb-karimi/pydsa
""")

    print("""🏗️ A data structure is a specialized format for organizing, processing, retrieving, and storing data. It defines the relationship between data and the operations that can be performed on the data. Efficient data structures are crucial for designing efficient algorithms and software systems. They help manage large amounts of data, making it easier to perform tasks such as searching, sorting, and modifying data. Data structures can be classified into various types based on their characteristics and usage, and they play a fundamental role in computer science and programming. Generally, DSes are classified into two parts: Linear & Non-linear.

🌟 Linear data structures are those in which elements are arranged in a sequential manner, where each element is connected to its previous and next element. Examples of linear data structures include arrays, linked lists, stacks, and queues. Arrays store elements in contiguous memory locations, allowing for efficient indexing but fixed size. Linked lists consist of nodes where each node contains data and a reference to the next node, providing dynamic size but slower access. Stacks follow the Last In, First Out (LIFO) principle, where the last element added is the first to be removed. Queues follow the First In, First Out (FIFO) principle, where the first element added is the first to be removed. These structures are simple to implement and useful for various applications.

🌟 Non-linear data structures are those in which elements are not arranged sequentially but in a hierarchical or interconnected manner. Examples include trees, graphs, and hash tables. Trees consist of nodes with a parent-child relationship, where each node can have multiple children but only one parent, forming a hierarchical structure. Binary trees, binary search trees, and heaps are common types of trees used for efficient searching, sorting, and priority management. Graphs consist of vertices (nodes) and edges (connections) that can represent complex relationships between elements. Graphs can be directed or undirected, and they are used in applications such as network routing, social networks, and dependency resolution. Hash tables use a hash function to map keys to values, allowing for efficient data retrieval. They are particularly useful for implementing associative arrays and databases. Non-linear data structures are more complex but provide powerful ways to model and solve real-world problems.

🪜 Algorithms in the context of data structures are step-by-step procedures or formulas for solving problems and performing tasks on data organized within specific structures. These algorithms are designed to manipulate data efficiently, leveraging the properties of the data structures they operate on. For example, sorting algorithms like Quick Sort and Merge Sort organize data in arrays or lists, while search algorithms like Binary Search efficiently locate elements in sorted arrays. Data structures such as trees, graphs, and hash tables have specialized algorithms for traversal, searching, insertion, and deletion, which optimize performance based on the structure's characteristics. The efficiency of these algorithms is often measured in terms of time complexity (how the runtime scales with input size) and space complexity (how much additional memory is required), using notations like Big O (which represents the upper bound or worst-case scenario), Big Theta (which represents the tight bound or average-case scenario) and Big Omega (which represents the lower bound or best-case scenario). Understanding the interplay between algorithms and data structures is fundamental to developing efficient and effective software solutions.\n""")
