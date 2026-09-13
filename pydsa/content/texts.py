"""Long-form console text: ASCII titles, definitions, algorithm explanations and the intro.

ASCII art uses raw strings so its backslashes stay literal.
"""

# ---------------------------------------------------------------------------
# Main intro
# ---------------------------------------------------------------------------

BANNER = r"""

.-------.  ____     __  ______        .-'''-.    ____     
\  _(`)_ \ \   \   /  /|    _ `''.   / _     \ .'  __ `.  
| (_ o._)|  \  _. /  ' | _ | ) _  \ (`' )/`--'/   '  \  \ 
|  (_,_) /   _( )_ .'  |( ''_'  ) |(_ o _).   |___|  /  | 
|   '-.-'___(_ o _)'   | . (_) `. | (_,_). '.    _.-`   | 
|   |   |   |(_,_)'    |(_    ._) '.---.  \  :.'   _    | 
|   |   |   `-'  /     |  (_.\.' / \    `-'  ||  _( )_  | 
/   )    \      /      |       .'   \       / \ (_ o _) / 
`---'     `-..-'       '-----'`      `-...-'   '.(_,_).'


"""

WELCOME = "Welcome to PyDSA, a console-based Python app that strives to assist you in learning data structures and algorithms! The app is designed to give you a good tour of the major DSes, giving you an opportunity to wrap your head around their distinctions while on the go! All interaction with the app is based on typing the related number codes in the terminal."

CHANGELOG = """📝 Changelog for this release:
   ★ Shortcuts everywhere: h for help, b to go back & q to quit, plus a clean exit on Ctrl+C
   ★ A Settings menu that remembers your choices between sessions
   ★ Command-line options: --topic, --list-topics, --no-color, --reset-settings & --version
   ★ Fill any data structure or list with random values"""

SOURCE_CODE = """🌐 All the source code & future updates are available in this GitHub repo:
   ★ https://github.com/najeeb-karimi/pydsa"""

OVERVIEW = """A data structure is a specialized format for organizing, processing, retrieving, and storing data. It defines the relationship between data and the operations that can be performed on the data. Efficient data structures are crucial for designing efficient algorithms and software systems. They help manage large amounts of data, making it easier to perform tasks such as searching, sorting, and modifying data. Data structures can be classified into various types based on their characteristics and usage, and they play a fundamental role in computer science and programming. Generally, DSes are classified into two parts: Linear & Non-linear.

🌟 Linear data structures are those in which elements are arranged in a sequential manner, where each element is connected to its previous and next element. Examples of linear data structures include arrays, linked lists, stacks, and queues. Arrays store elements in contiguous memory locations, allowing for efficient indexing but fixed size. Linked lists consist of nodes where each node contains data and a reference to the next node, providing dynamic size but slower access. Stacks follow the Last In, First Out (LIFO) principle, where the last element added is the first to be removed. Queues follow the First In, First Out (FIFO) principle, where the first element added is the first to be removed. These structures are simple to implement and useful for various applications.

🌟 Non-linear data structures are those in which elements are not arranged sequentially but in a hierarchical or interconnected manner. Examples include trees, graphs, and hash tables. Trees consist of nodes with a parent-child relationship, where each node can have multiple children but only one parent, forming a hierarchical structure. Binary trees, binary search trees, and heaps are common types of trees used for efficient searching, sorting, and priority management. Graphs consist of vertices (nodes) and edges (connections) that can represent complex relationships between elements. Graphs can be directed or undirected, and they are used in applications such as network routing, social networks, and dependency resolution. Hash tables use a hash function to map keys to values, allowing for efficient data retrieval. They are particularly useful for implementing associative arrays and databases. Non-linear data structures are more complex but provide powerful ways to model and solve real-world problems.

🪜 Algorithms in the context of data structures are step-by-step procedures or formulas for solving problems and performing tasks on data organized within specific structures. These algorithms are designed to manipulate data efficiently, leveraging the properties of the data structures they operate on. For example, sorting algorithms like Quick Sort and Merge Sort organize data in arrays or lists, while search algorithms like Binary Search efficiently locate elements in sorted arrays. Data structures such as trees, graphs, and hash tables have specialized algorithms for traversal, searching, insertion, and deletion, which optimize performance based on the structure's characteristics. The efficiency of these algorithms is often measured in terms of time complexity (how the runtime scales with input size) and space complexity (how much additional memory is required), using notations like Big O (which represents the upper bound or worst-case scenario), Big Theta (which represents the tight bound or average-case scenario) and Big Omega (which represents the lower bound or best-case scenario). Understanding the interplay between algorithms and data structures is fundamental to developing efficient and effective software solutions."""

# ---------------------------------------------------------------------------
# Array
# ---------------------------------------------------------------------------

ARRAY_ASCII = r"""

   ____    .-------.    .-------.       ____       ____     __  
 .'  __ `. |  _ _   \   |  _ _   \    .'  __ `.    \   \   /  / 
/   '  \  \| ( ' )  |   | ( ' )  |   /   '  \  \    \  _. /  '  
|___|  /  ||(_ o _) /   |(_ o _) /   |___|  /  |     _( )_ .'   
   _.-`   || (_,_).' __ | (_,_).' __    _.-`   | ___(_ o _)'    
.'   _    ||  |\ \  |  ||  |\ \  |  |.'   _    ||   |(_,_)'     
|  _( )_  ||  | \ `'   /|  | \ `'   /|  _( )_  ||   `-'  /      
\ (_ o _) /|  |  \    / |  |  \    / \ (_ o _) / \      /       
 '.(_,_).' ''-'   `'-'  ''-'   `'-'   '.(_,_).'   `-..-'
"""

ARRAY_DEFINITION = "An array is a fundamental linear data structure in computer science, consisting of a collection of elements, each identified by at least one array index or key. These elements are of the same data type and are stored in contiguous memory locations, allowing for efficient access and manipulation of data. Arrays are characterized by their fixed size, which is defined at the time of creation, and the ability to directly access any element in constant time using its index. This makes arrays particularly useful for implementing algorithms that require quick retrieval and update operations, as well as for storing data that can be easily sorted and searched."

BUBBLE_SORT_INFO = "Bubble Sort is a straightforward comparison-based sorting algorithm that repeatedly traverses the list, comparing adjacent elements and swapping them if they are in the wrong order. This process continues until the list is sorted. The algorithm is named because smaller elements \"bubble\" to the top of the list while larger elements sink to the bottom with each pass. Despite its simplicity and ease of implementation, Bubble Sort is inefficient for large datasets due to its average and worst-case time complexity of O(n²), where n is the number of items being sorted. Additionally, its best-case time complexity is O(n) when the list is already sorted, and it has a space complexity of O(1) since it only requires a constant amount of additional memory space. Bubble Sort is mainly used for educational purposes and small datasets where its simplicity is advantageous."

SELECTION_SORT_INFO = "Selection Sort is a simple comparison-based sorting algorithm that divides the input list into two parts: a sorted sublist of items which is built up from left to right at the front of the list, and a sublist of the remaining unsorted items. The algorithm repeatedly selects the smallest (or largest, depending on the order) element from the unsorted sublist, swaps it with the leftmost unsorted element, and moves the sublist boundaries one element to the right. This process continues until the entire list is sorted. Selection Sort has an average and worst-case time complexity of O(n²), where n is the number of items being sorted, and a best-case time complexity of O(n²) as well, since it always performs the same number of comparisons regardless of the initial order of the elements. Its space complexity is O(1) because it only requires a constant amount of additional memory space. Selection Sort is not suitable for large datasets but is easy to understand and implement, making it useful for educational purposes."

INSERTION_SORT_INFO = "Insertion Sort is a straightforward comparison-based sorting algorithm that builds the final sorted array one item at a time. It works by dividing the array into a sorted and an unsorted part. Initially, the sorted part contains only the first element, and the unsorted part contains the rest. The algorithm repeatedly takes the first element from the unsorted part, compares it with the elements in the sorted part, and inserts it into its correct position. This process continues until all elements are sorted. Insertion Sort has an average and worst-case time complexity of O(n²), where n is the number of items being sorted, and a best-case time complexity of O(n) when the array is already sorted. Its space complexity is O(1) because it requires only a constant amount of additional memory space. Insertion Sort is efficient for small datasets and nearly sorted arrays, making it useful for scenarios where simplicity and ease of implementation are important."

QUICK_SORT_INFO = "Quick Sort is an efficient, comparison-based sorting algorithm that uses the divide-and-conquer strategy to sort elements. It works by selecting a ‘pivot’ element from the array and partitioning the other elements into two sub-arrays, according to whether they are less than or greater than the pivot. The sub-arrays are then recursively sorted. This process continues until the base case of an empty or single-element sub-array is reached, which is inherently sorted. Quick Sort has an average and best-case time complexity of O(n log n), making it faster than other O(n²) algorithms like Bubble Sort and Selection Sort for large datasets. However, its worst-case time complexity is O(n²), which occurs when the smallest or largest element is always chosen as the pivot. The space complexity of Quick Sort is O(log n) due to the stack space used by the recursive calls. Despite its worst-case scenario, Quick Sort is widely used because of its efficiency and performance in practice."

HEAP_SORT_INFO = "Heap Sort is a comparison-based sorting algorithm that uses a binary heap data structure to sort elements. It works by first building a max heap (or min heap for descending order) from the input array, which ensures that the largest (or smallest) element is at the root of the heap. The root element is then swapped with the last element of the heap, and the heap size is reduced by one. The heapify process is applied to the root to restore the heap property, and this process is repeated until the heap size is reduced to one. Heap Sort has an average, best-case, and worst-case time complexity of O(n log n), where n is the number of items being sorted, making it more efficient than O(n²) algorithms like Bubble Sort and Selection Sort. Its space complexity is O(1) because it sorts the array in place without requiring additional memory. Heap Sort is particularly useful for large datasets where consistent performance is important."

SHELL_SORT_INFO = "Shell Sort is an in-place comparison-based sorting algorithm that generalizes insertion sort to allow the exchange of items that are far apart. The algorithm starts by sorting elements that are a certain gap distance apart, then progressively reduces the gap and performs a gapped insertion sort for each gap size. This process continues until the gap is reduced to one, at which point it becomes a standard insertion sort. The choice of gap sequence can significantly affect the performance of Shell Sort. Its average and worst-case time complexity can vary depending on the gap sequence used, but it generally ranges from O(n^1.5) to O(n²). The best-case time complexity is O(n log n) when using an optimal gap sequence. Shell Sort has a space complexity of O(1) because it sorts the array in place without requiring additional memory. It is more efficient than simple quadratic algorithms like bubble sort and insertion sort, especially for medium-sized datasets."

LINEAR_SEARCH_INFO = "Linear Search is a straightforward search algorithm that checks each element in a list sequentially until the desired element is found or the list ends. It starts at the first element and compares each element with the target value. If a match is found, the search is successful, and the index of the element is returned. If the end of the list is reached without finding the target, the search concludes that the element is not present. Linear Search has a time complexity of O(n), where n is the number of elements in the list, because in the worst case, it may need to check every element. Its space complexity is O(1) since it requires no additional memory beyond the input list. Linear Search is simple to implement and works well for small or unsorted datasets, but it is inefficient for large lists compared to more advanced search algorithms like binary search."

BINARY_SEARCH_INFO = "Binary Search is an efficient algorithm for finding an element in a sorted array by repeatedly dividing the search interval in half. It begins by comparing the target value to the middle element of the array. If the target value matches the middle element, the search is successful. If the target value is less than the middle element, the search continues on the left half of the array; otherwise, it continues on the right half. This process is repeated until the target value is found or the search interval is empty. Binary Search has a time complexity of O(log n), where n is the number of elements in the array, because it halves the search space with each step. Its space complexity is O(1) for the iterative version, as it requires a constant amount of additional memory. The best-case time complexity is O(1) when the target value is at the middle of the array."

# ---------------------------------------------------------------------------
# Stack
# ---------------------------------------------------------------------------

STACK_ASCII = r"""

   .-'''-. ,---------.    ____        _______   .--.   .--.   
  / _     \          \ .'  __ `.    /   __  \  |  | _/  /    
 (`' )/`--' `--.  ,---'/   '  \  \  | ,_/  \__) | (`' ) /     
(_ o _).       |   \   |___|  /  |,-./  )       |(_ ()_)      
 (_,_). '.     :_ _:      _.-`   |\  '_ '`)     | (_,_)   __  
.---.  \  :    (_I_)   .'   _    | > (_)  )  __ |  |\ \  |  | 
\    `-'  |   (_(=)_)  |  _( )_  |(  .  .-'_/  )|  | \ `'   / 
 \       /     (_I_)   \ (_ o _) / `-'`-'     / |  |  \    /  
  `-...-'      '---'    '.(_,_).'    `._____.'  `--'   `'-'
"""

STACK_DEFINITION = "A stack is a linear data structure that operates on the Last In, First Out (LIFO) principle, akin to a stack of plates where the last plate placed on top is the first one to be removed. It supports two primary operations: push, which adds an element to the top of the stack, and pop, which removes the most recently added element from the top. Additionally, stacks often provide a peek operation to view the top element without removing it, and utility functions to check if the stack is empty or full. This structure is widely used in computer science for tasks such as managing function calls, undo mechanisms in applications, and algorithmic problems like parsing expressions. PyDSA implements a fixed-size stack that accepts items of any type."

# ---------------------------------------------------------------------------
# Queue
# ---------------------------------------------------------------------------

QUEUE_ASCII = r"""

    ,-----.      ___    _     .-''-.    ___    _     .-''-.   
  .'  .-,  '.  .'   |  | |  .'_ _   \ .'   |  | |  .'_ _   \  
 / ,-.|  \ _ \ |   .'  | | / ( ` )   '|   .'  | | / ( ` )   ' 
;  \  '_ /  | :.'  '_  | |. (_ o _)  |.'  '_  | |. (_ o _)  | 
|  _`,/ \ _/  |'   ( \.-.||  (_,_)___|'   ( \.-.||  (_,_)___| 
: (  '\_/ \   ;' (`. _` /|'  \   .---.' (`. _` /|'  \   .---. 
 \ `"/  \  )  \| (_ (_) _) \  `-'    /| (_ (_) _) \  `-'    / 
  '. \_/``"/)  )\ /  . \ /  \       /  \ /  . \ /  \       /  
    '-----' `-'  ``-'`-''    `'-..-'    ``-'`-''    `'-..-'
"""

QUEUE_DEFINITION = "A queue is a linear data structure that adheres to the First In, First Out (FIFO) principle, much like customers waiting in line where the first person in line is the first to be served. It supports two primary operations: enqueue, which adds an element to the end of the queue, and dequeue, which removes the element from the front. This structure is essential in various computing scenarios, such as task scheduling, data processing, and resource management, due to its ability to maintain order in processing tasks or data. Queues are implemented in software using arrays or linked lists and are integral in algorithms that require sequential data processing, ensuring that elements are handled in the exact order they were added. PyDSA implements a fixed-size circular queue that accepts items of any type."

# ---------------------------------------------------------------------------
# Deque
# ---------------------------------------------------------------------------

DEQUE_ASCII = r"""

 ______         .-''-.      ,-----.      ___    _     .-''-.
|    _ `''.   .'_ _   \   .'  .-,  '.  .'   |  | |  .'_ _   \
| _ | ) _  \ / ( ` )   ' / ,-.|  \ _ \ |   .'  | | / ( ` )   '
|( ''_'  ) |. (_ o _)  |;  \  '_ /  | :.'  '_  | |. (_ o _)  |
| . (_) `. ||  (_,_)___||  _`,/ \ _/  |'   ( \.-.||  (_,_)___|
|(_    ._) ''  \   .---.: (  '\_/ \   ;' (`. _` /|'  \   .---.
|  (_.\.' /  \  `-'    / \ `"/  \  )  \| (_ (_) _) \  `-'    /
|       .'    \       /   '. \_/``"/)  )\ /  . \ /  \       /
'-----'`       `'-..-'      '-----' `-'  ``-'`-''    `'-..-'
"""

DEQUE_DEFINITION = """A deque (pronounced "deck"), short for double-ended queue, is a linear data structure that lets you add and remove elements at both ends: the front and the back. It combines the abilities of a stack and a queue, since pushing and popping at the same end gives Last In, First Out (LIFO) behavior, while pushing at one end and popping at the other gives First In, First Out (FIFO) behavior. Deques are used for undo and redo histories, sliding window algorithms, schedulers that take tasks from either end, and palindrome checks. When a deque is stored in a circular array, both ends can wrap around the array, so every push, pop and peek takes O(1) time without shifting any elements. PyDSA implements a fixed-size circular deque that accepts items of any type."""

# ---------------------------------------------------------------------------
# Linked list
# ---------------------------------------------------------------------------

LINKED_LIST_ASCII = r"""

  .---.    .-./`) ,---.   .--..--.   .--.      .-''-.   ______               .---.    .-./`)    .-'''-. ,---------.  
  | ,_|    \ .-.')|    \  |  ||  | _/  /     .'_ _   \ |    _ `''.           | ,_|    \ .-.')  / _     \          \ 
,-./  )    / `-' \|  ,  \ |  || (`' ) /     / ( ` )   '| _ | ) _  \        ,-./  )    / `-' \ (`' )/`--' `--.  ,---' 
\  '_ '`)   `-'`"`|  |\_ \|  ||(_ ()_)     . (_ o _)  ||( ''_'  ) |        \  '_ '`)   `-'`"`(_ o _).       |   \    
 > (_)  )   .---. |  _( )_\  || (_,_)   __ |  (_,_)___|| . (_) `. |         > (_)  )   .---.  (_,_). '.     :_ _:    
(  .  .-'   |   | | (_ o _)  ||  |\ \  |  |'  \   .---.|(_    ._) '        (  .  .-'   |   | .---.  \  :    (_I_)    
 `-'`-'|___ |   | |  (_,_)\  ||  | \ `'   / \  `-'    /|  (_.\.' /          `-'`-'|___ |   | \    `-'  |   (_(=)_)   
  |        \|   | |  |    |  ||  |  \    /   \       / |       .'            |        \|   |  \       /     (_I_)    
  `--------`'---' '--'    '--'`--'   `'-'     `'-..-'  '-----'`              `--------`'---'   `-...-'      '---'
"""

LINKED_LIST_DEFINITION = """A linked list is a dynamic data structure used to store a collection of elements, called nodes, in a sequential manner. Each node in a linked list contains data and a reference (or link) to the next node, forming a chain. Unlike arrays, linked lists do not require contiguous memory allocation, which allows for efficient insertion and deletion of nodes as there is no need to shift elements. This flexibility makes linked lists suitable for applications where the data size varies dynamically and frequent modifications are required.

🌟 Linked lists come in several types, each serving different purposes:

🔹 Singly Linked List: Each node has a single link to the next node, allowing one-way traversal.
🔹 Doubly Linked List: Nodes have two links, one to the next node and one to the previous, enabling traversal in both directions.
🔹 Singly Circular Linked List: Similar to a singly linked list, but the last node links back to the first node, forming a loop for circular traversal.
🔹 Doubly Circular Linked List: An extension of the doubly linked list where the last node links to the first, and the first node links to the last, allowing circular traversal in both directions."""

LINKED_LIST_SEARCH_INFO = "Linear Search in the context of a linked list involves traversing the list node by node, starting from the head, and comparing each node’s data with the target value until the desired element is found or the end of the list is reached. Since linked lists do not provide direct access to their elements, each node must be accessed sequentially, making the search process inherently linear. The time complexity of linear search in a linked list is O(n), where n is the number of nodes in the list, because in the worst case, every node must be checked. The space complexity is O(1) as it requires no additional memory beyond the input list. Linear search is simple to implement and works well for small or unsorted linked lists, but it is inefficient for large lists compared to more advanced search algorithms."

# ---------------------------------------------------------------------------
# Tree
# ---------------------------------------------------------------------------

TREE_ASCII = r"""

,---------. .-------.        .-''-.      .-''-.   
\          \|  _ _   \     .'_ _   \   .'_ _   \  
 `--.  ,---'| ( ' )  |    / ( ` )   ' / ( ` )   ' 
    |   \   |(_ o _) /   . (_ o _)  |. (_ o _)  | 
    :_ _:   | (_,_).' __ |  (_,_)___||  (_,_)___| 
    (_I_)   |  |\ \  |  |'  \   .---.'  \   .---. 
   (_(=)_)  |  | \ `'   / \  `-'    / \  `-'    / 
    (_I_)   |  |  \    /   \       /   \       /  
    '---'   ''-'   `'-'     `'-..-'     `'-..-'
"""

TREE_DEFINITION = """A specialized type of graph, the tree is a hierarchical, non-linear data structure consisting of nodes connected by edges. It starts with a single node called the root, from which all other nodes branch out. Each node can have zero or more child nodes, and nodes with no children are called leaf nodes. Trees are used to represent hierarchical relationships and are fundamental in various applications such as file systems, databases, and network routing. They facilitate efficient data retrieval and manipulation through various traversal methods like in-order, pre-order, post-order and level-order traversal.

Trees come in many types, and the most important one is the binary tree, in which each node has at most two children. The most popular kinds of binary trees are the BST and the AVL tree, and PyDSA implements both of them.

🌟 A Binary Search Tree (BST) is a specialized type of binary tree where each node has at most two children, referred to as the left and right child. The key property of a BST is that for any given node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater. This property allows for efficient searching, insertion, and deletion operations, typically with a time complexity of O(log n) if the tree is balanced. If not balanced, it's possible for the BST to develop a big difference between its left & right subtrees in which case the time complexity will degrade to O(n). That's why self-balancing BSTs like AVL & Red-Black tree are used. BSTs are widely used in applications that require dynamic data sets and quick lookups, such as databases and search engines.

🌟 An AVL tree is a self-balancing binary search tree named after its inventors, Georgy Adelson-Velsky and Evgenii Landis. In an AVL tree, the heights of the left and right subtrees of any node differ by at most one, ensuring the tree remains balanced. This balance is maintained through rotations during insertion and deletion operations. The AVL tree's balanced nature guarantees that operations such as search, insertion, and deletion have a time complexity of O(log n), making it highly efficient for applications requiring frequent data modifications and lookups."""

BST_INFO = "PyDSA's BST holds keys of one data type (numbers or strings) and stores duplicate keys in the right subtree."

AVL_INFO = "PyDSA's AVL tree holds keys of one data type (numbers or strings) and allows duplicate keys."

# ---------------------------------------------------------------------------
# Heap and priority queue
# ---------------------------------------------------------------------------

HEAP_ASCII = r"""

.---.  .---.     .-''-.     ____    .-------.
|   |  |_ _|   .'_ _   \  .'  __ `. \  _(`)_ \
|   |  ( ' )  / ( ` )   '/   '  \  \| (_ o._)|
|   '-(_{;}_). (_ o _)  ||___|  /  ||  (_,_) /
|      (_,_) |  (_,_)___|   _.-`   ||   '-.-'
| _ _--.   | '  \   .---..'   _    ||   |
|( ' ) |   |  \  `-'    /|  _( )_  ||   |
(_{;}_)|   |   \       / \ (_ o _) //   )
'(_,_) '---'    `'-..-'   '.(_,_).' `---'
"""

HEAP_DEFINITION = """A heap is a tree-based data structure that keeps the heap property: in a min heap, every parent's key is smaller than or equal to its children's keys, so the smallest key is always at the root, and in a max heap, every parent's key is larger than or equal to its children's keys, so the largest key is at the root. The most common kind is the binary heap, a complete binary tree in which every level is full except possibly the last one, which is filled from left to right. Heaps are used to build priority queues, in heap sort, in graph algorithms such as Dijkstra's shortest paths and Prim's minimum spanning tree, and to find the k smallest or largest items in a collection.

🌟 Because a binary heap is complete, it can be stored in a plain array without any links: the children of the node at index i sit at indexes 2i + 1 and 2i + 2, and its parent sits at index (i − 1) // 2. Reading the array from left to right is the same as reading the tree level by level.

🌟 Inserting a key places it in the next free spot at the bottom of the tree and sifts it up, swapping it with its parent until the heap property holds again. Extracting the root moves the last leaf to the root and sifts it down, swapping it with its smaller child (or its larger child in a max heap). Both take O(log n) time, because the tree is only log n levels tall. Building a heap from a list with heapify sifts down every parent, from the last one up to the root, which takes only O(n) time in total.

🌟 A priority queue is a queue in which every item has a priority, and the item with the highest priority is always served first, no matter when it arrived. A heap is the classic way to build one, since the item that should be served next is always at the root. PyDSA's priority queue is a min heap in which a smaller number means a higher priority, and items with equal priorities are served in the order they arrived (First In, First Out)."""

HEAP_INFO = "PyDSA's heaps hold keys of one data type (numbers or strings) and allow duplicate keys."

PRIORITY_QUEUE_INFO = "PyDSA's priority queue serves the smallest priority number first, and items with the same priority leave in the order they arrived. Items can be of any type, and priorities are whole numbers."

# ---------------------------------------------------------------------------
# Trie
# ---------------------------------------------------------------------------

TRIE_ASCII = r"""

,---------. .-------.   .-./`)     .-''-.
\          \|  _ _   \  \ .-.')  .'_ _   \
 `--.  ,---'| ( ' )  |  / `-' \ / ( ` )   '
    |   \   |(_ o _) /   `-'`"`. (_ o _)  |
    :_ _:   | (_,_).' __ .---. |  (_,_)___|
    (_I_)   |  |\ \  |  ||   | '  \   .---.
   (_(=)_)  |  | \ `'   /|   |  \  `-'    /
    (_I_)   |  |  \    / |   |   \       /
    '---'   ''-'   `'-'  '---'    `'-..-'
"""

TRIE_DEFINITION = """A trie (pronounced "try"), also called a prefix tree, is a tree-based data structure that stores strings character by character. Each edge from a node stands for one character, so every path from the root spells out a prefix, and words that share a prefix share the same nodes. A node is marked when the path to it spells a complete word, which is how a trie tells the word "car" apart from the start of "card". Tries are used for autocomplete, spell checkers, word games, IP routing tables and dictionaries.

🌟 Inserting, searching and deleting a word of length L take O(L) time, no matter how many words the trie holds. Checking whether any word starts with a prefix is just as fast, since it only follows the prefix's path, and autocomplete then collects every word below the node where that path ends.

🌟 Deleting a word removes its mark and then prunes the nodes that no longer lead to any word, walking back up toward the root. Nodes that other words still use stay in place. PyDSA's trie is case-sensitive, so "Cat" and "cat" are different words."""

# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

GRAPH_ASCII = r"""

  .-_'''-.   .-------.       ____    .-------. .---.  .---.  
 '_( )_   \  |  _ _   \    .'  __ `. \  _(`)_ \|   |  |_ _|  
|(_ o _)|  ' | ( ' )  |   /   '  \  \| (_ o._)||   |  ( ' )  
. (_,_)/___| |(_ o _) /   |___|  /  ||  (_,_) /|   '-(_{;}_) 
|  |  .-----.| (_,_).' __    _.-`   ||   '-.-' |      (_,_)  
'  \  '-   .'|  |\ \  |  |.'   _    ||   |     | _ _--.   |  
 \  `-'`   | |  | \ `'   /|  _( )_  ||   |     |( ' ) |   |  
  \        / |  |  \    / \ (_ o _) //   )     (_{;}_)|   |  
   `'-...-'  ''-'   `'-'   '.(_,_).' `---'     '(_,_) '---'
"""

GRAPH_DEFINITION = """A graph is a non-linear data structure consisting of vertices (nodes) and edges that connect pairs of vertices. Graphs are used to model relationships between entities, making them essential in various fields such as computer science, biology, social networks, and transportation. Graphs can be directed or undirected, weighted or unweighted, and can contain cycles or be acyclic. The versatility of graphs allows them to represent complex structures and relationships, enabling efficient problem-solving and analysis. Graphs can be represented using either an Adjacency Matrix or an Adjacency List.

🌟 An adjacency matrix is a 2D array used to represent a graph, where the rows and columns correspond to vertices. The element at row (i) and column (j) indicates the presence and weight of an edge between vertices (i) and (j). For an undirected graph, the matrix is symmetric, while for a directed graph, it is not. The adjacency matrix allows for quick edge lookups with a time complexity of O(1), but it requires O(V²) space, making it more suitable for dense graphs where the number of edges is close to the maximum possible.

🌟 An adjacency list represents a graph using an array of lists. Each element in the array corresponds to a vertex, and the list at each index contains the vertices adjacent to that vertex. This representation is more space-efficient for sparse graphs, as it only stores existing edges, resulting in a space complexity of O(V + E). Adjacency lists allow for efficient traversal of the graph, making them ideal for algorithms like Depth-First Search (DFS) and Breadth-First Search (BFS). However, edge lookups can be slower compared to an adjacency matrix, with a time complexity proportional to the degree of the vertex."""

MATRIX_GRAPH_INFO = "PyDSA implements a weighted graph using an adjacency matrix, and you choose whether its edges are directed or undirected. For an unweighted graph, simply set every weight to 1."

LIST_GRAPH_INFO = "PyDSA implements a weighted graph using an adjacency list, and you choose whether its edges are directed or undirected. For an unweighted graph, simply set every weight to 1."

# ---------------------------------------------------------------------------
# Hash table
# ---------------------------------------------------------------------------

HASH_TABLE_ASCII = r"""

.---.  .---.    ____       .-'''-. .---.  .---.         ,---------.    ____     _______     .---.       .-''-.   
|   |  |_ _|  .'  __ `.   / _     \|   |  |_ _|         \          \ .'  __ `. \  ____  \   | ,_|     .'_ _   \  
|   |  ( ' ) /   '  \  \ (`' )/`--'|   |  ( ' )          `--.  ,---'/   '  \  \| |    \ | ,-./  )    / ( ` )   ' 
|   '-(_{;}_)|___|  /  |(_ o _).   |   '-(_{;}_)            |   \   |___|  /  || |____/ / \  '_ '`) . (_ o _)  | 
|      (_,_)    _.-`   | (_,_). '. |      (_,_)             :_ _:      _.-`   ||   _ _ '.  > (_)  ) |  (_,_)___| 
| _ _--.   | .'   _    |.---.  \  :| _ _--.   |             (_I_)   .'   _    ||  ( ' )  \(  .  .-' '  \   .---. 
|( ' ) |   | |  _( )_  |\    `-'  ||( ' ) |   |            (_(=)_)  |  _( )_  || (_{;}_) | `-'`-'|___\  `-'    / 
(_{;}_)|   | \ (_ o _) / \       / (_{;}_)|   |             (_I_)   \ (_ o _) /|  (_,_)  /  |        \       /  
'(_,_) '---'  '.(_,_).'   `-...-'  '(_,_) '---'             '---'    '.(_,_).' /_______.'   `--------` `'-..-'
"""

HASH_TABLE_DEFINITION = """A hash table is a non-linear data structure that stores key-value pairs and uses a hash function to turn each key into an index of an underlying array, whose positions are called buckets or slots. Because the index is computed directly from the key, inserting, searching and deleting take O(1) time on average, which makes hash tables ideal for dictionaries, caches, database indexes and symbol tables. When two different keys hash to the same index, a collision occurs, so every hash table needs a collision resolution technique. The two main families are Open Hashing (Separate Chaining) and Closed Hashing (Open Addressing).

🌟 Separate Chaining stores every entry that hashes to the same index in a secondary structure attached to that bucket, usually a list. Colliding keys are simply added to the bucket's chain, so the table never fills up and can hold more entries than it has buckets. Inserting, searching and deleting take O(1) time on average, but degrade to O(n) in the worst case when many keys land in the same bucket. The trade-off is the extra memory used by the chains.

🌟 Linear Probing is an Open Addressing technique in which every entry is stored directly in one of the table's slots. When a key's home slot is taken, the table checks the next slot, then the next, wrapping around to the start, until it finds an empty one, and lookups follow the same path until they find the key or reach an empty slot. Linear probing is cache-friendly and needs no extra memory, but the table can hold at most as many entries as it has slots, and occupied slots tend to form clusters that make probing slower. Deleting also needs care, since emptying a slot would break the probe path of the keys after it, which is why PyDSA rehashes the rest of the cluster after every deletion."""

CHAINING_INFO = "Separate chaining keeps colliding keys in lists, so the table never fills up and you don't need to worry about running out of space."

# ---------------------------------------------------------------------------
# Hash set
# ---------------------------------------------------------------------------

HASH_SET_ASCII = r"""

.---.  .---.    ____       .-'''-. .---.  .---.            .-'''-.     .-''-. ,---------.
|   |  |_ _|  .'  __ `.   / _     \|   |  |_ _|           / _     \  .'_ _   \\          \
|   |  ( ' ) /   '  \  \ (`' )/`--'|   |  ( ' )          (`' )/`--' / ( ` )   '`--.  ,---'
|   '-(_{;}_)|___|  /  |(_ o _).   |   '-(_{;}_)        (_ o _).   . (_ o _)  |   |   \
|      (_,_)    _.-`   | (_,_). '. |      (_,_)          (_,_). '. |  (_,_)___|   :_ _:
| _ _--.   | .'   _    |.---.  \  :| _ _--.   |         .---.  \  :'  \   .---.   (_I_)
|( ' ) |   | |  _( )_  |\    `-'  ||( ' ) |   |         \    `-'  | \  `-'    /  (_(=)_)
(_{;}_)|   | \ (_ o _) / \       / (_{;}_)|   |          \       /   \       /    (_I_)
'(_,_) '---'  '.(_,_).'   `-...-'  '(_,_) '---'           `-...-'     `'-..-'     '---'
"""

HASH_SET_DEFINITION = """A hash set is a collection of unique items that uses a hash function to decide where each item is stored, so it can tell whether an item is in the set in O(1) time on average. Unlike a list, a set keeps no particular order and ignores duplicates: adding an item that's already there changes nothing. Hash sets are used to remove duplicates, remember which items have already been visited in a graph search, and test membership quickly, and they are how Python's built-in set type works.

🌟 A hash set is essentially a hash table that stores keys without values. PyDSA builds its hash set on top of the separate chaining hash table, so items that collide share a bucket's chain.

🌟 Sets also support operations from mathematics: the union (A ∪ B) holds every item that is in either set, the intersection (A ∩ B) holds the items that are in both, the difference (A − B) holds the items that are in A but not in B, and A is a subset of B (A ⊆ B) when every item of A is also in B."""

# ---------------------------------------------------------------------------
# Disjoint set
# ---------------------------------------------------------------------------

DISJOINT_SET_ASCII = r"""

 ______     .-./`)    .-'''-.      .-./`)     ,-----.   .-./`) ,---.   .--.,---------.            .-'''-.     .-''-. ,---------.
|    _ `''. \ .-.')  / _     \     \ '_ .') .'  .-,  '. \ .-.')|    \  |  |\          \          / _     \  .'_ _   \\          \
| _ | ) _  \/ `-' \ (`' )/`--'    (_ (_) _)/ ,-.|  \ _ \/ `-' \|  ,  \ |  | `--.  ,---'         (`' )/`--' / ( ` )   '`--.  ,---'
|( ''_'  ) | `-'`"`(_ o _).         / .  \;  \  '_ /  | :`-'`"`|  |\_ \|  |    |   \           (_ o _).   . (_ o _)  |   |   \
| . (_) `. | .---.  (_,_). '.  ___  |-'`| |  _`,/ \ _/  |.---. |  _( )_\  |    :_ _:            (_,_). '. |  (_,_)___|   :_ _:
|(_    ._) ' |   | .---.  \  :|   | |   ' : (  '\_/ \   ;|   | | (_ o _)  |    (_I_)           .---.  \  :'  \   .---.   (_I_)
|  (_.\.' /  |   | \    `-'  ||   `-'  /   \ `"/  \  ) / |   | |  (_,_)\  |   (_(=)_)          \    `-'  | \  `-'    /  (_(=)_)
|       .'   |   |  \       /  \      /     '. \_/``".'  |   | |  |    |  |    (_I_)            \       /   \       /    (_I_)
'-----'`     '---'   `-...-'    `-..-'        '-----'    '---' '--'    '--'    '---'             `-...-'     `'-..-'     '---'
"""

DISJOINT_SET_DEFINITION = """A disjoint set, also called Union-Find, keeps track of elements split into groups that don't overlap, so every element belongs to exactly one set. It supports two main operations: find, which returns the representative (the root) of the set an element belongs to, and union, which merges the sets of two elements into one. Two elements are connected when find returns the same root for both of them. Disjoint sets are used in Kruskal's minimum spanning tree algorithm, cycle detection in undirected graphs, network connectivity checks and image segmentation.

🌟 Each set is stored as a tree inside a parent array: every element points to its parent, and a root points to itself. PyDSA numbers the elements from 0, so the parent array can be a plain list.

🌟 Two optimizations keep the trees flat. Union by rank attaches the root of the shorter tree under the root of the taller one, using a rank that is an upper bound on the tree's height. Path compression makes every element visited during a find point directly at the root, so later finds are faster. Together, they make both operations run in nearly constant amortized time, O(α(n)), where α is the extremely slow-growing inverse Ackermann function."""

# ---------------------------------------------------------------------------
# Sorting algorithms
# ---------------------------------------------------------------------------

SORTING_ASCII = r"""

   .-'''-.     ,-----.    .-------. ,---------. .-./`) ,---.   .--.  .-_'''-.
  / _     \  .'  .-,  '.  |  _ _   \\          \\ .-.')|    \  |  | '_( )_   \
 (`' )/`--' / ,-.|  \ _ \ | ( ' )  | `--.  ,---'/ `-' \|  ,  \ |  ||(_ o _)|  '
(_ o _).   ;  \  '_ /  | :|(_ o _) /    |   \    `-'`"`|  |\_ \|  |. (_,_)/___|
 (_,_). '. |  _`,/ \ _/  || (_,_).' __  :_ _:    .---. |  _( )_\  ||  |  .-----.
.---.  \  :: (  '\_/ \   ;|  |\ \  |  | (_I_)    |   | | (_ o _)  |'  \  '-   .'
\    `-'  | \ `"/  \  ) / |  | \ `'   /(_(=)_)   |   | |  (_,_)\  | \  `-'`   |
 \       /   '. \_/``".'  |  |  \    /  (_I_)    |   | |  |    |  |  \        /
  `-...-'      '-----'    ''-'   `'-'   '---'    '---' '--'    '--'   `'-...-'
"""

SORTING_DEFINITION = """Sorting means arranging a collection of elements in a particular order, such as numbers from smallest to largest or words in alphabetical order. Sorted data is easier for people to read and much faster for computers to work with: it allows binary search, puts duplicates next to each other, and is the first step of many other algorithms. Sorting algorithms differ in speed, in how much extra memory they need, and in whether they keep equal elements in their original order, which is called stability.

🌟 Comparison sorts, such as Bubble, Selection, Insertion, Quick, Heap, Shell and Merge Sort, decide the order by comparing pairs of elements. No comparison sort can beat O(n log n) in the worst case.

🌟 Non-comparison sorts, such as Counting and Radix Sort, look at the values themselves instead of comparing them, which lets them run in linear time when the values are whole numbers in a limited range.

🌟 PyDSA sorts a copy of your list, so you can try every algorithm on the same data, watch each step, and compare how much work each algorithm needs."""

SORT_COMPARISON_INFO = "The comparison runs every sorting algorithm on its own copy of the same list and counts the work each one does. Comparisons are how many times two values were compared, writes are how many times a value was stored in the list (a swap counts as two writes), and steps are the rows each algorithm shows when it runs on its own. Counting Sort and Radix Sort never compare values, so they only have writes. Try an already sorted list, a reversed one and one full of duplicates to see how differently the algorithms react."

MERGE_SORT_INFO = "Merge Sort is an efficient, comparison-based sorting algorithm that uses the divide-and-conquer strategy. It splits the list into two halves, sorts each half recursively until the pieces hold a single element, and then merges the sorted halves back together. Merging repeatedly compares the front elements of the two halves and takes the one that comes first, so two sorted halves become one sorted list in a single pass. Merge Sort has a time complexity of O(n log n) in the best, average and worst case, because the list can only be halved log n times and every level of merging touches all n elements. Its space complexity is O(n), since merging needs room for a temporary copy of the elements. Merge Sort is stable, which means equal elements keep their original order, and it's a popular choice for sorting linked lists and data too large to fit in memory. PyDSA shows the list after every merge."

COUNTING_SORT_INFO = "Counting Sort is a non-comparison sorting algorithm for whole numbers. Instead of comparing elements, it counts how many times each value appears, using one counter for every value between the smallest and the largest. It then walks through the counters in order and writes each value back into the list as many times as it was counted. To handle negative numbers, PyDSA subtracts the smallest value from every value, which turns the smallest value into counter 0. Counting Sort runs in O(n + k) time, where n is the number of elements and k is the distance between the smallest and largest value, and it needs O(k) extra space for the counters. That makes it faster than any comparison sort when the values fall in a small range, but wasteful when they're spread far apart, which is why PyDSA only accepts values less than 10,000 apart. PyDSA shows the list after all copies of a value have been written back."

RADIX_SORT_INFO = "Radix Sort is a non-comparison sorting algorithm that sorts whole numbers one digit at a time. PyDSA's version starts with the least significant digit (the ones), deals every number into one of ten buckets by that digit, and then collects the buckets in order from 0 to 9. It repeats this for the tens, the hundreds and so on, up to the number of digits in the largest value. Because each pass keeps the numbers in the same bucket in the order they arrived, the order from the earlier digits is preserved, and after the last pass the list is fully sorted. Radix Sort runs in O(d · (n + b)) time, where n is the number of elements, d the number of digits and b the number of buckets (10 here), and it needs O(n + b) extra space. It's very fast for large lists of numbers with only a few digits. PyDSA's version sorts numbers that aren't negative and shows the list after every digit."

# ---------------------------------------------------------------------------
# Searching algorithms
# ---------------------------------------------------------------------------

SEARCHING_ASCII = r"""

   .-'''-.     .-''-.     ____    .-------.        _______   .---.  .---..-./`) ,---.   .--.  .-_'''-.
  / _     \  .'_ _   \  .'  __ `. |  _ _   \      /   __  \  |   |  |_ _|\ .-.')|    \  |  | '_( )_   \
 (`' )/`--' / ( ` )   '/   '  \  \| ( ' )  |     | ,_/  \__) |   |  ( ' )/ `-' \|  ,  \ |  ||(_ o _)|  '
(_ o _).   . (_ o _)  ||___|  /  ||(_ o _) /   ,-./  )       |   '-(_{;}_)`-'`"`|  |\_ \|  |. (_,_)/___|
 (_,_). '. |  (_,_)___|   _.-`   || (_,_).' __ \  '_ '`)     |      (_,_) .---. |  _( )_\  ||  |  .-----.
.---.  \  :'  \   .---..'   _    ||  |\ \  |  | > (_)  )  __ | _ _--.   | |   | | (_ o _)  |'  \  '-   .'
\    `-'  | \  `-'    /|  _( )_  ||  | \ `'   /(  .  .-'_/  )|( ' ) |   | |   | |  (_,_)\  | \  `-'`   |
 \       /   \       / \ (_ o _) /|  |  \    /  `-'`-'     / (_{;}_)|   | |   | |  |    |  |  \        /
  `-...-'     `'-..-'   '.(_,_).' ''-'   `'-'     `._____.'  '(_,_) '---' '---' '--'    '--'   `'-...-'
"""

SEARCHING_DEFINITION = """Searching means finding where a target value is stored in a collection, or finding out that it isn't there. Some searching algorithms work on any data, while others need the data to be sorted first and, in exchange, get to skip most of the elements.

🌟 Linear Search checks the elements one by one and works on any list. Binary, Jump, Interpolation and Exponential Search need sorted data, because they use the order to rule out the parts of the list that can't hold the target.

🌟 PyDSA runs the searches that need sorted data on a sorted copy, so your list keeps its order, and reports the index where the target first appears in the original list. After every search, it shows the positions the algorithm checked, in order, so you can see how much of the list each one skipped."""

JUMP_SEARCH_INFO = "Jump Search is a searching algorithm for sorted lists that checks elements in fixed-size jumps instead of one by one. With n elements, it jumps ahead √n positions at a time and looks at the last element of each block. As soon as it reaches a block whose last element is greater than or equal to the target, the target can only be inside that block, so it checks that block from the start with a linear search. Jump Search has a time complexity of O(√n), because it makes at most √n jumps and then checks at most √n elements, and a space complexity of O(1). It's slower than Binary Search but only ever moves forward through the list, which helps when going back is expensive, such as when reading data from a tape."

INTERPOLATION_SEARCH_INFO = "Interpolation Search is a searching algorithm for sorted lists of numbers that guesses where the target should be from its value, much like opening a phone book near the end to find a name starting with W. Instead of always checking the middle like Binary Search, it estimates the position with low + (target − values[low]) × (high − low) ÷ (values[high] − values[low]), then narrows the range to the left or right of that guess and repeats. When the numbers are spread out evenly, its guesses land very close, giving an average time complexity of O(log log n). When the numbers are bunched up unevenly, the guesses can be far off and the worst case degrades to O(n). Its space complexity is O(1). Because it does arithmetic on the values, it only works with numbers."

EXPONENTIAL_SEARCH_INFO = "Exponential Search is a searching algorithm for sorted lists that first finds a range that must contain the target, then runs a Binary Search inside it. It checks the elements at positions 1, 2, 4, 8, 16 and so on, doubling the position each time, until it finds an element that is greater than or equal to the target or runs past the end of the list. The target can then only lie between the last two positions it checked, and Binary Search finishes the job in that range. Exponential Search has a time complexity of O(log i), where i is the position of the target, so it's especially fast when the target is near the start, and it's useful for lists whose length is unknown. Its space complexity is O(1)."

# ---------------------------------------------------------------------------
# Graph algorithms
# ---------------------------------------------------------------------------

GRAPH_ALGORITHMS_ASCII = r"""

  .-_'''-.   .-------.       ____    .-------. .---.  .---.
 '_( )_   \  |  _ _   \    .'  __ `. \  _(`)_ \|   |  |_ _|
|(_ o _)|  ' | ( ' )  |   /   '  \  \| (_ o._)||   |  ( ' )
. (_,_)/___| |(_ o _) /   |___|  /  ||  (_,_) /|   '-(_{;}_)
|  |  .-----.| (_,_).' __    _.-`   ||   '-.-' |      (_,_)
'  \  '-   .'|  |\ \  |  |.'   _    ||   |     | _ _--.   |
 \  `-'`   | |  | \ `'   /|  _( )_  ||   |     |( ' ) |   |
  \        / |  |  \    / \ (_ o _) //   )     (_{;}_)|   |
   `'-...-'  ''-'   `'-'   '.(_,_).' `---'     '(_,_) '---'

   ____      .---.     .-_'''-.       ,-----.    .-------.   .-./`) ,---------. .---.  .---. ,---.    ,---.   .-'''-.
 .'  __ `.   | ,_|    '_( )_   \    .'  .-,  '.  |  _ _   \  \ .-.')\          \|   |  |_ _| |    \  /    |  / _     \
/   '  \  \,-./  )   |(_ o _)|  '  / ,-.|  \ _ \ | ( ' )  |  / `-' \ `--.  ,---'|   |  ( ' ) |  ,  \/  ,  | (`' )/`--'
|___|  /  |\  '_ '`) . (_,_)/___| ;  \  '_ /  | :|(_ o _) /   `-'`"`    |   \   |   '-(_{;}_)|  |\_   /|  |(_ o _).
   _.-`   | > (_)  ) |  |  .-----.|  _`,/ \ _/  || (_,_).' __ .---.     :_ _:   |      (_,_) |  _( )_/ |  | (_,_). '.
.'   _    |(  .  .-' '  \  '-   .': (  '\_/ \   ;|  |\ \  |  ||   |     (_I_)   | _ _--.   | | (_ o _) |  |.---.  \  :
|  _( )_  | `-'`-'|___\  `-'`   |  \ `"/  \  ) / |  | \ `'   /|   |    (_(=)_)  |( ' ) |   | |  (_,_)  |  |\    `-'  |
\ (_ o _) /  |        \\        /   '. \_/``".'  |  |  \    / |   |     (_I_)   (_{;}_)|   | |  |      |  | \       /
 '.(_,_).'   `--------` `'-...-'      '-----'    ''-'   `'-'  '---'     '---'   '(_,_) '---' '--'      '--'  `-...-'
"""

GRAPH_ALGORITHMS_DEFINITION = """Graph algorithms answer questions about the connections in a graph: how to get from one vertex to another as cheaply as possible, in which order to do tasks that depend on each other, whether the connections loop back on themselves, and how to connect every vertex as cheaply as possible. They power maps and navigation, build systems, course planners, network design and much more.

🌟 Dijkstra's algorithm finds the shortest paths from one vertex to all the others in a graph whose weights aren't negative.

🌟 A topological sort orders the vertices of a directed graph so every edge points forward, which is only possible when the graph has no cycles.

🌟 Cycle detection finds a path that leads back to where it started. Directed graphs are checked with a depth-first search, and undirected graphs with a disjoint set.

🌟 A minimum spanning tree connects every vertex of an undirected graph using edges with the smallest possible total weight. Prim's algorithm grows one tree vertex by vertex, while Kruskal's algorithm adds the lightest edges that don't close a cycle."""

GRAPH_ALGORITHMS_INFO = "This screen runs the graph algorithms on an example graph. To run them on a graph you build yourself, open Graph under the non-linear data structures and choose Graph Algorithms."

DIJKSTRA_INFO = "Dijkstra's algorithm finds the shortest path from a source vertex to every other vertex in a weighted graph whose weights aren't negative. It keeps a tentative distance for every vertex, starting at 0 for the source and infinity for the rest, and a min heap of vertices ordered by distance. It repeatedly takes the closest vertex whose distance isn't final yet, makes its distance final, and relaxes each of its edges: if going through this vertex reaches a neighbor with a smaller distance than the neighbor has so far, the neighbor's distance and previous vertex are updated. Following the previous vertices back from any vertex rebuilds its shortest path. With a min heap and an adjacency list, Dijkstra's algorithm runs in O((V + E) log V) time, where V is the number of vertices and E the number of edges. A negative weight could make a finished vertex cheaper to reach later, which breaks the algorithm, so PyDSA refuses to run it on graphs with negative weights."

TOPOLOGICAL_SORT_INFO = "A topological sort arranges the vertices of a directed graph in a line so that every edge goes from an earlier vertex to a later one, like ordering courses so every prerequisite comes before the courses that need it. PyDSA uses Kahn's algorithm, which counts how many edges point into each vertex (its in-degree) and starts with the vertices that have none. It repeatedly places one of those vertices and removes its outgoing edges, which lowers the in-degree of its neighbors, and any neighbor that drops to zero is ready to be placed next. If vertices are left over once no vertex is ready, they're on a cycle or come after one, and the graph has no topological order. Kahn's algorithm runs in O(V + E) time, where V is the number of vertices and E the number of edges."

DIRECTED_CYCLE_INFO = "To find a cycle in a directed graph, PyDSA runs a depth-first search that tracks three states for every vertex: not visited yet, on the current path, and finished. When the search reaches a vertex, the vertex joins the current path, and once all of its edges have been explored, it's marked as finished and leaves the path. If an edge ever leads to a vertex that is still on the current path, the search has found its way back to where it came from, and the part of the path from that vertex onward is a cycle. Edges into finished vertices are safe, because everything reachable from them has already been explored without finding a cycle. This check runs in O(V + E) time, where V is the number of vertices and E the number of edges."

UNDIRECTED_CYCLE_INFO = "To find a cycle in an undirected graph, PyDSA uses a disjoint set (Union-Find) that starts with every vertex in a set of its own. It goes through the edges one by one: if an edge's two vertices are already in the same set, there's already a path between them, so this edge closes a cycle. Otherwise, the edge merges their two sets. Once a cycle is found, PyDSA follows the edges added so far to show the path around it. With union by rank and path compression, this check runs in nearly O(V + E) time, where V is the number of vertices and E the number of edges."

PRIM_INFO = "Prim's algorithm builds a minimum spanning tree: the edges that connect every vertex of an undirected graph with the smallest possible total weight. It starts from a single vertex and grows the tree one vertex at a time. Every edge leaving the tree goes into a min heap, and the algorithm repeatedly takes the lightest one. If that edge leads to a vertex that's already in the tree, it would close a cycle and is left out; otherwise, the edge and its new vertex join the tree, and the new vertex's edges go into the heap. When the graph isn't connected, PyDSA starts a new tree from the next vertex that isn't in one yet, which produces a minimum spanning forest. With a min heap and an adjacency list, Prim's algorithm runs in O(E log V) time, where V is the number of vertices and E the number of edges."

KRUSKAL_INFO = "Kruskal's algorithm builds a minimum spanning tree: the edges that connect every vertex of an undirected graph with the smallest possible total weight. It sorts all edges from lightest to heaviest and goes through them in that order, adding each edge unless it would close a cycle. To check that quickly, it keeps a disjoint set (Union-Find) of the vertices that are already connected: an edge whose two vertices are in the same set is left out, and any other edge merges their sets. When the graph isn't connected, Kruskal's algorithm naturally produces a minimum spanning forest instead. Sorting the edges dominates its running time, which is O(E log E), where E is the number of edges."
