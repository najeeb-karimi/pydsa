"""A note for every operation in PyDSA's menus: what it does, how it works, what it costs and where its code is.

Costs aren't written here: complexity_rows names rows of the topic's tables in content/complexity.py, so the
cost shown is always the one in the table. Algorithms that show their own explanation from a guide are marked
explained, so only their cost is shown before they run.
"""

import importlib
import textwrap
from typing import NamedTuple


class OperationNote(NamedTuple):
    """How one operation of a topic's menu works."""

    topic: str  # The topic ID
    operation: str  # The label in the topic's menu
    summary: str  # One sentence
    steps: tuple = ()  # The numbered "how it works" lines
    complexity_rows: tuple = ()  # Names of rows in the topic's complexity tables
    pseudocode: tuple = ()  # A few plain lines; empty for operations that only show something
    sources: tuple = ()  # The functions that do the work, as "module:qualified.name"
    explained: bool = False  # True when the operation shows its own explanation from a guide


NOTES = []


def add(topic, operation, summary, steps=(), rows=(), pseudocode="", sources=(), explained=False):
    """Add a note; rows and sources can be one string, and pseudocode is one indented block of text."""
    as_tuple = lambda value: (value,) if isinstance(value, str) else tuple(value)
    lines = tuple(textwrap.dedent(pseudocode).strip("\n").splitlines())
    NOTES.append(OperationNote(topic, operation, summary, tuple(steps), as_tuple(rows), lines, as_tuple(sources), explained))


def display(topic, summary, operation="Display", rows=()):
    """Add the note of an operation that only shows something."""
    add(topic, operation, summary, rows=rows)


CORE = "pydsa.core"
ARRAY = f"{CORE}.array:Array"
STACK = f"{CORE}.stack:Stack"
QUEUE = f"{CORE}.queue:Queue"
DEQUE = f"{CORE}.deque:Deque"
LINKED = f"{CORE}.linked_list"
TREE = f"{CORE}.tree"
HEAP = f"{CORE}.heap"
PRIORITY_QUEUE = f"{CORE}.priority_queue:PriorityQueue"
TRIE = f"{CORE}.trie:Trie"
GRAPH = f"{CORE}.graph"
HASH_TABLE = f"{CORE}.hash_table"
HASH_SET = f"{CORE}.hash_set:HashSet"
DISJOINT_SET = f"{CORE}.disjoint_set:DisjointSet"
SORTING = "pydsa.algorithms.sorting"
SEARCHING = "pydsa.algorithms.searching"
GRAPH_ALGORITHMS = "pydsa.algorithms.graph_algorithms"


def capacity_checks(topic, name, cls):
    """Add the notes of Check if Empty, Check if Full and Size for a structure with a fixed capacity."""
    add(topic, "Check if Empty", f"Tells you whether the {name} has no items.",
        ["Compare the number of items with 0."], "Check if empty or full",
        """
        is_empty():
            return count == 0
        """, f"{cls}.is_empty")
    add(topic, "Check if Full", f"Tells you whether the {name} has reached its capacity.",
        ["Compare the number of items with the capacity."], "Check if empty or full",
        """
        is_full():
            return count == capacity
        """, f"{cls}.is_full")
    add(topic, "Size", f"Shows how many items the {name} holds and how many it can hold.",
        ["Return the count of items, which every change keeps up to date."], "Size",
        """
        size():
            return count
        """, f"{cls}.__len__")


# ---------------------------------------------------------------------------
# Array
# ---------------------------------------------------------------------------

add("array", "Insert", "Stores a value at an index, replacing the value that was there.",
    ["Check that the index is between 0 and the size minus 1.",
     "Work out where that slot is from the index.",
     "Write the value into the slot, or into every slot one by one when you fill the whole array."],
    "Insert at an index",
    """
    insert(index, value):
        if value isn't of the array's type: error "wrong type"
        if index < 0 or index >= size: error "out of bounds"
        items[index] = value
    """, f"{ARRAY}.insert")
add("array", "Delete", "Clears an index by resetting it to the default value.",
    ["Check that the index is between 0 and the size minus 1.",
     "Write the default value into that slot; the other values don't move."],
    "Delete at an index",
    """
    delete(index):
        if index < 0 or index >= size: error "out of bounds"
        items[index] = default value
    """, f"{ARRAY}.remove")
add("array", "Get by Index", "Reads the value at an index.",
    ["Check that the index is between 0 and the size minus 1.",
     "Read the value straight from that slot."],
    "Get by index",
    """
    get(index):
        if index < 0 or index >= size: error "out of bounds"
        return items[index]
    """, f"{ARRAY}.get")
add("array", "Sort", "Sorts the array in place with a sorting algorithm you pick, showing every step.")
add("array", "Search", "Looks for a value with a searching algorithm you pick, showing the positions it checked.")
display("array", "Shows how many elements the array has, which never changes after it's created.", "Size")
display("array", "Shows the one data type every element of the array must have.", "Data Type")
display("array", "Draws every element under its index.")

# ---------------------------------------------------------------------------
# Stack, queue and deque
# ---------------------------------------------------------------------------

add("stack", "Push", "Puts an item on top of the stack.",
    ["If the stack is full, refuse the item.",
     "Add the item right after the current top.",
     "The new item is now the top."],
    "Push",
    """
    push(item):
        if count == capacity: error "stack is full"
        add item after the top
    """, f"{STACK}.push")
add("stack", "Pop", "Takes the top item off the stack and gives it to you.",
    ["If the stack is empty, there's nothing to pop.",
     "Remove the item that was added last.",
     "The item below it becomes the new top."],
    "Pop",
    """
    pop():
        if count == 0: error "stack is empty"
        remove the top item and return it
    """, f"{STACK}.pop")
add("stack", "Peek", "Shows the top item without taking it off.",
    ["If the stack is empty, there's nothing to see.",
     "Return the item that was added last, leaving it where it is."],
    "Peek",
    """
    peek():
        if count == 0: error "stack is empty"
        return the top item
    """, f"{STACK}.peek")
capacity_checks("stack", "stack", STACK)
display("stack", "Draws the stack from the top down, marking the top item.")

add("queue", "Enqueue", "Adds an item at the rear of the queue.",
    ["If the queue is full, refuse the item.",
     "Move the rear one slot forward, wrapping around to slot 0 after the last slot.",
     "Write the item into that slot and count one more item."],
    "Enqueue",
    """
    enqueue(item):
        if count == capacity: error "queue is full"
        rear = (rear + 1) mod capacity
        slots[rear] = item
        count = count + 1
    """, f"{QUEUE}.enqueue")
add("queue", "Dequeue", "Removes the item at the front of the queue and gives it to you.",
    ["If the queue is empty, there's nothing to dequeue.",
     "Take the item in the front slot.",
     "Move the front one slot forward, wrapping around after the last slot, and count one item less."],
    "Dequeue",
    """
    dequeue():
        if count == 0: error "queue is empty"
        item = slots[front]
        front = (front + 1) mod capacity
        count = count - 1
        return item
    """, f"{QUEUE}.dequeue")
add("queue", "Peek Front", "Shows the item at the front without removing it.",
    ["If the queue is empty, there's nothing to see.",
     "Return the item in the front slot."],
    "Peek front or rear",
    """
    peek_front():
        if count == 0: error "queue is empty"
        return slots[front]
    """, f"{QUEUE}.get_front")
add("queue", "Peek Rear", "Shows the item at the rear without removing it.",
    ["If the queue is empty, there's nothing to see.",
     "Return the item in the rear slot."],
    "Peek front or rear",
    """
    peek_rear():
        if count == 0: error "queue is empty"
        return slots[rear]
    """, f"{QUEUE}.get_rear")
capacity_checks("queue", "queue", QUEUE)
display("queue", "Draws every slot of the circular array, marking the front and the rear.")

add("deque", "Push Front", "Adds an item before the front of the deque.",
    ["If the deque is full, refuse the item.",
     "Step the front back one slot, wrapping around from slot 0 to the last slot.",
     "Write the item into that slot and count one more item."],
    "Push front or back",
    """
    push_front(item):
        if count == capacity: error "deque is full"
        front = (front - 1) mod capacity
        slots[front] = item
        count = count + 1
    """, f"{DEQUE}.push_front")
add("deque", "Push Back", "Adds an item after the back of the deque.",
    ["If the deque is full, refuse the item.",
     "Find the free slot after the back: as many slots after the front as there are items, wrapping around.",
     "Write the item into that slot and count one more item."],
    "Push front or back",
    """
    push_back(item):
        if count == capacity: error "deque is full"
        slots[(front + count) mod capacity] = item
        count = count + 1
    """, f"{DEQUE}.push_back")
add("deque", "Pop Front", "Removes the front item and gives it to you.",
    ["If the deque is empty, there's nothing to pop.",
     "Take the item in the front slot.",
     "Step the front forward one slot, wrapping around, and count one item less."],
    "Pop front or back",
    """
    pop_front():
        if count == 0: error "deque is empty"
        item = slots[front]
        front = (front + 1) mod capacity
        count = count - 1
        return item
    """, (f"{DEQUE}.pop_front", f"{DEQUE}.peek_front"))
add("deque", "Pop Back", "Removes the back item and gives it to you.",
    ["If the deque is empty, there's nothing to pop.",
     "Take the item in the back slot, which is count minus 1 slots after the front.",
     "Count one item less; the front doesn't move."],
    "Pop front or back",
    """
    pop_back():
        if count == 0: error "deque is empty"
        item = slots[(front + count - 1) mod capacity]
        count = count - 1
        return item
    """, (f"{DEQUE}.pop_back", f"{DEQUE}.peek_back"))
add("deque", "Peek Front", "Shows the front item without removing it.",
    ["If the deque is empty, there's nothing to see.",
     "Return the item in the front slot."],
    "Peek front or back",
    """
    peek_front():
        if count == 0: error "deque is empty"
        return slots[front]
    """, f"{DEQUE}.peek_front")
add("deque", "Peek Back", "Shows the back item without removing it.",
    ["If the deque is empty, there's nothing to see.",
     "Return the item in the back slot, count minus 1 slots after the front."],
    "Peek front or back",
    """
    peek_back():
        if count == 0: error "deque is empty"
        return slots[(front + count - 1) mod capacity]
    """, f"{DEQUE}.peek_back")
capacity_checks("deque", "deque", DEQUE)
display("deque", "Draws every slot of the circular array, marking the front and the back.")

# ---------------------------------------------------------------------------
# Linked lists
# ---------------------------------------------------------------------------

SLL = f"{LINKED}:SinglyLinkedList"
DLL = f"{LINKED}:DoublyLinkedList"
SCLL = f"{LINKED}:SinglyCircularLinkedList"
DCLL = f"{LINKED}:DoublyCircularLinkedList"
CIRCULAR = f"{LINKED}:CircularLinkedList"


def linked_list_search(topic, circular):
    stop = "you're back at the head" if circular else "the list ends"
    add(topic, "Search", "Looks for an item by following the links from the head.",
        rows="Search or display",
        pseudocode=f"""
        search(target):
            position = 0
            node = head
            until {stop}:
                if node.item == target: return position
                node = node.next
                position = position + 1
            return not found
        """,
        sources=(f"{LINKED}:LinkedList.search", f"{CIRCULAR}.__iter__") if circular else f"{LINKED}:LinkedList.search",
        explained=True)


add("singly-linked-list", "Insert at Beginning", "Adds a new node before the head.",
    ["Create a node for the item.",
     "Point its next link at the current head.",
     "Make the new node the head."],
    "Insert at beginning",
    """
    insert_at_beginning(item):
        node = new node holding item
        node.next = head
        head = node
    """, f"{SLL}.insert_at_beginning")
add("singly-linked-list", "Insert at Position", "Adds a new node so it ends up at the position you choose.",
    ["Position 0 is the same as inserting at the beginning.",
     "Otherwise, walk from the head to the node just before the position.",
     "Point the new node's next link at the node after it.",
     "Point that node's next link at the new node."],
    "Insert at position",
    """
    insert_at_position(position, item):
        if position == 0: insert_at_beginning(item) and stop
        before = head
        repeat position - 1 times: before = before.next
        if before is empty: error "out of bounds"
        node = new node holding item
        node.next = before.next
        before.next = node
    """, f"{SLL}.insert_at_position")
add("singly-linked-list", "Insert at End", "Adds a new node after the last node.",
    ["If the list is empty, the new node becomes the head.",
     "Otherwise, walk from the head until you reach the node whose next link is empty.",
     "Point that node's next link at the new node."],
    "Insert at end",
    """
    insert_at_end(item):
        node = new node holding item
        if head is empty: head = node and stop
        last = head
        while last.next isn't empty: last = last.next
        last.next = node
    """, f"{SLL}.insert_at_end")
add("singly-linked-list", "Delete from Beginning", "Removes the head node and gives you its item.",
    ["If the list is empty, there's nothing to delete.",
     "Remember the head's item.",
     "Make the head's next node the new head."],
    "Delete from beginning",
    """
    delete_from_beginning():
        if head is empty: error "list is empty"
        item = head.item
        head = head.next
        return item
    """, f"{SLL}.delete_from_beginning")
add("singly-linked-list", "Delete from Position", "Removes the node at the position you choose and gives you its item.",
    ["Position 0 is the same as deleting from the beginning.",
     "Otherwise, walk from the head to the node just before the position.",
     "Point its next link past the node being removed, at the node after it."],
    "Delete from position",
    """
    delete_from_position(position):
        if position == 0: return delete_from_beginning()
        before = head
        repeat position - 1 times: before = before.next
        if before.next is empty: error "out of bounds"
        item = before.next.item
        before.next = before.next.next
        return item
    """, f"{SLL}.delete_from_position")
add("singly-linked-list", "Delete from End", "Removes the last node and gives you its item.",
    ["If the head is the only node, the list becomes empty.",
     "Otherwise, walk from the head to the second-to-last node.",
     "Clear its next link, which cuts off the last node."],
    "Delete from end",
    """
    delete_from_end():
        if head is empty: error "list is empty"
        if head.next is empty: item = head.item, head = empty, return item
        before = head
        while before.next.next isn't empty: before = before.next
        item = before.next.item
        before.next = empty
        return item
    """, f"{SLL}.delete_from_end")
linked_list_search("singly-linked-list", circular=False)
display("singly-linked-list", "Draws every node from the head to the tail.", rows="Search or display")

add("doubly-linked-list", "Insert at Beginning", "Adds a new node before the head.",
    ["Create a node for the item and point its next link at the current head.",
     "If there is a head, point its prev link back at the new node.",
     "Make the new node the head."],
    "Insert at beginning",
    """
    insert_at_beginning(item):
        node = new node holding item
        node.next = head
        if head isn't empty: head.prev = node
        head = node
    """, f"{DLL}.insert_at_beginning")
add("doubly-linked-list", "Insert at Position", "Adds a new node so it ends up at the position you choose.",
    ["Position 0 is the same as inserting at the beginning.",
     "Otherwise, walk from the head to the node now at the position; just past the last node means inserting at the end.",
     "Link the new node in between that node and the node before it, updating four links."],
    "Insert at position",
    """
    insert_at_position(position, item):
        if position == 0: insert_at_beginning(item) and stop
        current = head
        repeat position times: current = current.next (error if the list ends too early)
        if current is empty: insert_at_end(item) and stop
        node = new node holding item
        node.prev = current.prev
        node.next = current
        current.prev.next = node
        current.prev = node
    """, f"{DLL}.insert_at_position")
add("doubly-linked-list", "Insert at End", "Adds a new node after the last node.",
    ["If the list is empty, the new node becomes the head.",
     "Otherwise, walk from the head to the last node.",
     "Link the two both ways: the last node's next link and the new node's prev link."],
    "Insert at end",
    """
    insert_at_end(item):
        node = new node holding item
        if head is empty: head = node and stop
        last = head
        while last.next isn't empty: last = last.next
        last.next = node
        node.prev = last
    """, f"{DLL}.insert_at_end")
add("doubly-linked-list", "Delete from Beginning", "Removes the head node and gives you its item.",
    ["If the list is empty, there's nothing to delete.",
     "Make the head's next node the new head.",
     "Clear the new head's prev link."],
    "Delete from beginning",
    """
    delete_from_beginning():
        if head is empty: error "list is empty"
        item = head.item
        head = head.next
        if head isn't empty: head.prev = empty
        return item
    """, f"{DLL}.delete_from_beginning")
add("doubly-linked-list", "Delete from Position", "Removes the node at the position you choose and gives you its item.",
    ["Walk from the head to the node at the position.",
     "Point its next node's prev link at its previous node.",
     "Point its previous node's next link at its next node, or make its next node the head if it was the head."],
    "Delete from position",
    """
    delete_from_position(position):
        current = head
        repeat position times: current = current.next (error if the list ends)
        if current.next isn't empty: current.next.prev = current.prev
        if current.prev isn't empty: current.prev.next = current.next
        else: head = current.next
        return current.item
    """, f"{DLL}.delete_from_position")
add("doubly-linked-list", "Delete from End", "Removes the last node and gives you its item.",
    ["If the head is the only node, the list becomes empty.",
     "Otherwise, walk from the head to the last node.",
     "Clear the next link of the node before it, which the last node's prev link leads to."],
    "Delete from end",
    """
    delete_from_end():
        if head is empty: error "list is empty"
        if head.next is empty: item = head.item, head = empty, return item
        last = head
        while last.next isn't empty: last = last.next
        last.prev.next = empty
        return last.item
    """, f"{DLL}.delete_from_end")
linked_list_search("doubly-linked-list", circular=False)
display("doubly-linked-list", "Draws every node from the head to the tail, following the next links.",
        "Display Forward", "Search or display")
add("doubly-linked-list", "Display Backward", "Lists the items from the tail back to the head by following the prev links.",
    ["Walk from the head to the last node.",
     "Follow the prev links back, collecting each item, until you pass the head."],
    "Search or display",
    """
    backward():
        node = head
        while node.next isn't empty: node = node.next
        while node isn't empty:
            collect node.item
            node = node.prev
    """, f"{DLL}.backward")

add("singly-circular-linked-list", "Insert at Beginning", "Adds a new node before the head and closes the loop again.",
    ["If the list is empty, the new node links to itself and becomes both the head and the tail.",
     "Otherwise, point the new node's next link at the head.",
     "Point the tail's next link at the new node and make the new node the head."],
    "Insert at beginning",
    """
    insert_at_beginning(item):
        node = new node holding item
        if head is empty: node.next = node, head = tail = node, stop
        node.next = head
        tail.next = node
        head = node
    """, f"{SCLL}.insert_at_beginning")
add("singly-circular-linked-list", "Insert at Position", "Adds a new node so it ends up at the position you choose.",
    ["Position 0 inserts at the beginning, and a position equal to the length inserts at the end.",
     "Otherwise, walk from the head to the node just before the position.",
     "Link the new node in after it."],
    "Insert at position",
    """
    insert_at_position(position, item):
        if position < 0 or position > length: error "out of bounds"
        if position == 0: insert_at_beginning(item) and stop
        if position == length: insert_at_end(item) and stop
        before = the node at position - 1
        node = new node holding item
        node.next = before.next
        before.next = node
    """, f"{SCLL}.insert_at_position")
add("singly-circular-linked-list", "Insert at End", "Adds a new node after the tail, using the tail reference instead of walking.",
    ["Insert the node at the beginning, which places it between the tail and the head.",
     "Move the tail forward to the new node, and the head forward to the node after it."],
    "Insert at end",
    """
    insert_at_end(item):
        insert_at_beginning(item)
        tail = head
        head = head.next
    """, (f"{SCLL}.insert_at_end", f"{SCLL}.insert_at_beginning"))
add("singly-circular-linked-list", "Delete from Beginning", "Removes the head node and gives you its item.",
    ["If the head is the only node, the list becomes empty.",
     "Otherwise, move the head forward one node.",
     "Point the tail's next link at the new head, closing the loop again."],
    "Delete from beginning",
    """
    delete_from_beginning():
        if head is empty: error "list is empty"
        item = head.item
        if head is tail: head = tail = empty
        else: head = head.next, tail.next = head
        return item
    """, f"{SCLL}.delete_from_beginning")
add("singly-circular-linked-list", "Delete from Position", "Removes the node at the position you choose and gives you its item.",
    ["Position 0 deletes from the beginning, and the last position deletes from the end.",
     "Otherwise, walk from the head to the node just before the position.",
     "Point its next link past the node being removed."],
    "Delete from position",
    """
    delete_from_position(position):
        if position < 0 or position >= length: error "out of bounds"
        if position == 0: return delete_from_beginning()
        if position == length - 1: return delete_from_end()
        before = the node at position - 1
        item = before.next.item
        before.next = before.next.next
        return item
    """, f"{SCLL}.delete_from_position")
add("singly-circular-linked-list", "Delete from End", "Removes the tail node and gives you its item.",
    ["If the head is the only node, the list becomes empty.",
     "Otherwise, walk from the head to the node just before the tail, since there are no prev links.",
     "Point that node's next link at the head and make it the new tail."],
    "Delete from end",
    """
    delete_from_end():
        if head is empty: error "list is empty"
        item = tail.item
        if head is tail: head = tail = empty, return item
        before = head
        while before.next isn't tail: before = before.next
        before.next = head
        tail = before
        return item
    """, f"{SCLL}.delete_from_end")
linked_list_search("singly-circular-linked-list", circular=True)
display("singly-circular-linked-list", "Draws every node from the head to the tail, ending with an arrow back to the head.",
        rows="Search or display")
add("singly-circular-linked-list", "Walk Around the Loop",
    "Visits as many nodes as you choose, starting at the head and going around the loop as often as needed.",
    ["Start at the head.",
     "Record the node's item and follow its next link.",
     "Repeat for the number of nodes you chose; after the tail, the next link leads back to the head."],
    "Walk k nodes around the loop",
    """
    walk(steps):
        node = head
        repeat steps times:
            collect node.item
            node = node.next
    """, (f"{CIRCULAR}.walk", f"{CIRCULAR}._walk"))

add("doubly-circular-linked-list", "Insert at Beginning", "Adds a new node before the head.",
    ["Insert the node at the end, between the tail and the head.",
     "Make the new node the head, which is all it takes, since the loop has no real end."],
    "Insert at beginning",
    """
    insert_at_beginning(item):
        insert_at_end(item)
        head = head.prev
    """, (f"{DCLL}.insert_at_beginning", f"{DCLL}.insert_at_end"))
add("doubly-circular-linked-list", "Insert at Position", "Adds a new node so it ends up at the position you choose.",
    ["Position 0 inserts at the beginning, and a position equal to the length inserts at the end.",
     "Otherwise, walk from the head to the node now at the position.",
     "Link the new node in just before it, updating four links."],
    "Insert at position",
    """
    insert_at_position(position, item):
        if position < 0 or position > length: error "out of bounds"
        if position == 0: insert_at_beginning(item) and stop
        if position == length: insert_at_end(item) and stop
        current = the node at position
        node = new node holding item
        node.prev = current.prev
        node.next = current
        current.prev.next = node
        current.prev = node
    """, f"{DCLL}.insert_at_position")
add("doubly-circular-linked-list", "Insert at End", "Adds a new node between the tail and the head.",
    ["If the list is empty, the new node's links both point to itself, and it becomes the head.",
     "Otherwise, find the tail through the head's prev link.",
     "Link the new node in between the tail and the head, updating four links."],
    "Insert at end",
    """
    insert_at_end(item):
        node = new node holding item
        if head is empty: node.prev = node.next = node, head = node, stop
        tail = head.prev
        node.prev = tail
        node.next = head
        tail.next = node
        head.prev = node
    """, f"{DCLL}.insert_at_end")
add("doubly-circular-linked-list", "Delete from Beginning", "Removes the head node and gives you its item.",
    ["If the list is empty, there's nothing to delete.",
     "Connect the head's prev and next nodes directly to each other.",
     "Make the next node the head, or leave the list empty if the head only linked to itself."],
    "Delete from beginning",
    """
    delete_from_beginning():
        if head is empty: error "list is empty"
        return unlink(head)

    unlink(node):
        if node.next is node: head = empty
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if node is head: head = node.next
        return node.item
    """, (f"{DCLL}.delete_from_beginning", f"{DCLL}._unlink"))
add("doubly-circular-linked-list", "Delete from Position", "Removes the node at the position you choose and gives you its item.",
    ["Walk from the head to the node at the position.",
     "Connect its prev and next nodes directly to each other.",
     "If it was the head, the next node becomes the head."],
    "Delete from position",
    """
    delete_from_position(position):
        if head is empty: error "list is empty"
        if position < 0 or position >= length: error "out of bounds"
        return unlink(the node at position)
    """, (f"{DCLL}.delete_from_position", f"{DCLL}._unlink"))
add("doubly-circular-linked-list", "Delete from End", "Removes the tail node and gives you its item, without walking the list.",
    ["If the list is empty, there's nothing to delete.",
     "Find the tail through the head's prev link.",
     "Connect the tail's prev node and the head directly to each other."],
    "Delete from end",
    """
    delete_from_end():
        if head is empty: error "list is empty"
        return unlink(head.prev)
    """, (f"{DCLL}.delete_from_end", f"{DCLL}._unlink"))
linked_list_search("doubly-circular-linked-list", circular=True)
display("doubly-circular-linked-list", "Draws every node from the head to the tail, ending with an arrow back to the head.",
        "Display Forward", "Search or display")
add("doubly-circular-linked-list", "Display Backward",
    "Lists the items from the tail back around to the head by following the prev links.",
    ["Find the tail through the head's prev link.",
     "Follow the prev links, collecting one item per node, until every node has been visited once."],
    "Search or display",
    """
    backward():
        node = head.prev
        repeat length times:
            collect node.item
            node = node.prev
    """, (f"{DCLL}.backward", f"{CIRCULAR}._walk"))
add("doubly-circular-linked-list", "Walk Around the Loop",
    "Visits as many nodes as you choose, forward from the head or backward from the tail, going around as often as needed.",
    ["Start at the head to walk forward, or at the tail, the head's prev node, to walk backward.",
     "Record the node's item and follow its next or prev link.",
     "Repeat for the number of nodes you chose."],
    "Walk k nodes around the loop",
    """
    walk(steps, backward):
        node = head.prev if backward else head
        repeat steps times:
            collect node.item
            node = node.prev if backward else node.next
    """, (f"{DCLL}.walk", f"{CIRCULAR}._walk"))

# ---------------------------------------------------------------------------
# Trees
# ---------------------------------------------------------------------------

BST = f"{TREE}:BinarySearchTree"
AVL = f"{TREE}:AVLTree"
BINARY_TREE = f"{TREE}:BinaryTree"

add("bst", "Insert", "Adds a key as a new leaf, in the spot the ordering rule leads to.",
    ["If the tree is empty, the key becomes the root.",
     "Otherwise, start at the root and go left when the key is smaller than the node's key, and right when it's larger or equal.",
     "When the side you'd go to is empty, attach the key there as a new leaf."],
    "Insert",
    """
    insert(node, key):
        if key < node.key:
            if node.left is empty: node.left = new node holding key
            else: insert(node.left, key)
        else:
            if node.right is empty: node.right = new node holding key
            else: insert(node.right, key)
    """, (f"{BST}.insert", f"{BST}._insert"))
add("bst", "Delete", "Removes one copy of a key and reconnects the tree around the gap.",
    ["Search down from the root for the node holding the key.",
     "A node with no children or one child is replaced by that child, or by nothing.",
     "A node with two children takes the key of its in-order successor, the smallest key in its right subtree, and the successor is deleted from that subtree instead."],
    "Delete",
    """
    delete(node, key):
        if key < node.key: node.left = delete(node.left, key)
        else if key > node.key: node.right = delete(node.right, key)
        else:
            if node.left is empty: return node.right
            if node.right is empty: return node.left
            successor = the leftmost node of node.right
            node.key = successor.key
            node.right = delete(node.right, successor.key)
        return node
    """, (f"{BST}.delete", f"{BST}._delete"))


def tree_shared(topic, search_summary):
    add(topic, "Search", search_summary,
        ["Start at the root.",
         "If the node holds the key, you've found it.",
         "Otherwise, go left if the key is smaller and right if it's larger, until you run out of nodes."],
        "Search",
        """
        search(key):
            node = root
            while node isn't empty and node.key != key:
                node = node.left if key < node.key else node.right
            return node
        """, f"{BINARY_TREE}.search")
    add(topic, "Traversals", "Lists every key in the order of the traversal you pick.",
        ["Inorder visits the left subtree, then the node, then the right subtree.",
         "Preorder visits the node before its subtrees, and postorder visits it after them.",
         "Level order uses a queue to visit the tree one level at a time."],
        ("Inorder, preorder or postorder", "Level order"),
        """
        inorder(node):
            if node is empty: stop
            inorder(node.left)
            visit node.key
            inorder(node.right)
        """, (f"{BINARY_TREE}._inorder", f"{BINARY_TREE}.level_order"))


tree_shared("bst", "Looks for a key by going left or right at every node.")
add("bst", "Tree Stats", "Shows the tree's height, its numbers of nodes and leaves, and its smallest and largest keys.",
    ["The height is 1 more than the taller subtree's height, which means visiting every node.",
     "Counting the nodes and the leaves also visits every node.",
     "The smallest key is found by always going left, and the largest by always going right."],
    ("Height", "Node or leaf count", "Smallest or largest key"),
    """
    height(node):
        if node is empty: return 0
        return 1 + max(height(node.left), height(node.right))
    """, (f"{BINARY_TREE}._height", f"{BINARY_TREE}.min"))
display("bst", "Draws the tree from the top down.")

add("avl-tree", "Insert", "Adds a key like a binary search tree does, then rotates on the way back up to keep the tree balanced.",
    ["Insert the key as a new leaf, going left or right just like in a binary search tree.",
     "On the way back up, update each node's height and balance factor.",
     "If a balance factor reaches 2 or -2, fix it with one rotation for the Left Left and Right Right cases, or two for the Left Right and Right Left cases."],
    "Insert",
    """
    insert(node, key):
        if node is empty: return new node holding key
        insert key into node.left or node.right, as in a BST
        node.height = 1 + max(height(node.left), height(node.right))
        balance = height(node.left) - height(node.right)
        if balance > 1 and key < node.left.key: return rotate_right(node)
        if balance < -1 and key >= node.right.key: return rotate_left(node)
        if balance > 1: node.left = rotate_left(node.left), return rotate_right(node)
        if balance < -1: node.right = rotate_right(node.right), return rotate_left(node)
        return node
    """, (f"{AVL}.insert", f"{AVL}._insert", f"{AVL}._rebalance", f"{AVL}._left_rotate", f"{AVL}._right_rotate"))
add("avl-tree", "Delete", "Removes one copy of a key like a binary search tree does, then rotates on the way back up to rebalance.",
    ["Delete the key as in a binary search tree, using the in-order successor for a node with two children.",
     "On the way back up, update each node's height and balance factor.",
     "Rotate every node whose balance factor reached 2 or -2, picking the case from its taller child's balance factor."],
    "Delete",
    """
    delete(node, key):
        delete key from node's subtree, as in a BST
        node.height = 1 + max(height(node.left), height(node.right))
        balance = height(node.left) - height(node.right)
        if balance > 1: rotate right, first rotating node.left left if it leans right
        if balance < -1: rotate left, first rotating node.right right if it leans left
        return node
    """, (f"{AVL}.delete", f"{AVL}._delete", f"{AVL}._rebalance"))
tree_shared("avl-tree", "Looks for a key by going left or right at every node, along a path the balance keeps short.")
add("avl-tree", "Tree Stats", "Shows the tree's height, its numbers of nodes and leaves, and its smallest and largest keys.",
    ["The height is read straight from the root, since every AVL node stores its own height.",
     "Counting the nodes and the leaves visits every node.",
     "The smallest key is found by always going left, and the largest by always going right."],
    ("Height", "Node or leaf count", "Smallest or largest key"),
    """
    height():
        if root is empty: return 0
        return root.height
    """, (f"{AVL}.height", f"{BINARY_TREE}.min"))
display("avl-tree", "Draws the tree from the top down, with each node's balance factor.")

# ---------------------------------------------------------------------------
# Heaps and the priority queue
# ---------------------------------------------------------------------------

for topic, cls, short, smaller, smallest, largest, other in (
    ("min-heap", "MinHeap", "Min", "smaller", "smallest", "largest", "max"),
    ("max-heap", "MaxHeap", "Max", "larger", "largest", "smallest", "min"),
):
    add(topic, "Insert", f"Adds a key as the last leaf, then sifts it up while it's {smaller} than its parent.",
        ["Append the key to the end of the array, which is the next free leaf.",
         f"While the key is {smaller} than its parent, at index (i − 1) ÷ 2, swap the two.",
         "Stop at the root, or as soon as the parent belongs above the key."],
        "Insert (sift up)",
        """
        insert(key):
            append key to items
            i = last index
            while i > 0 and items[i] belongs above items[(i - 1) // 2]:
                swap items[i] and items[(i - 1) // 2]
                i = (i - 1) // 2
        """, (f"{HEAP}:Heap.insert", f"{HEAP}:Heap._sift_up", f"{HEAP}:{cls}._above"))
    add(topic, f"Extract {short}", f"Removes the root, which holds the {smallest} key, and repairs the heap.",
        ["Remember the root's key.",
         "Move the last leaf into the root's place.",
         f"Sift it down: while one of its children is {smaller}, swap it with its {smallest} child."],
        "Extract the root (sift down)",
        """
        extract():
            if items is empty: error "heap is empty"
            root = items[0]
            items[0] = remove the last item
            i = 0
            while a child of i belongs above items[i]:
                c = the child that belongs highest
                swap items[i] and items[c]
                i = c
            return root
        """, (f"{HEAP}:Heap.extract", f"{HEAP}:Heap._sift_down", f"{HEAP}:{cls}._above"))
    add(topic, f"Peek {short}", f"Shows the {smallest} key, which is always at the root.",
        ["If the heap is empty, there's nothing to see.",
         "Return the key at index 0."],
        "Peek at the root",
        """
        peek():
            if items is empty: error "heap is empty"
            return items[0]
        """, f"{HEAP}:Heap.peek")
    add(topic, "Build from a List", "Replaces the heap's keys with a list you type and turns it into a heap with heapify.",
        ["Put the keys into the array in the order you typed them.",
         "Sift down every parent, starting with the last one, at index n ÷ 2 − 1, and working back to the root.",
         "Once the root has been sifted down, the whole array is a heap."],
        "Build from a list (heapify)",
        """
        heapify(keys):
            items = keys
            for i from len(items) // 2 - 1 down to 0:
                sift_down(i)
        """, (f"{HEAP}:Heap.heapify", f"{HEAP}:Heap._sift_down"))
    add(topic, "Level Order", "Lists the keys level by level, which is simply the array from left to right.",
        ["Read the array from index 0 to the end."],
        "Level order",
        """
        level_order():
            return a copy of items
        """, f"{HEAP}:Heap.level_order")
    add(topic, "Tree Stats", "Shows the heap's height, its numbers of nodes and leaves, and its smallest and largest keys.",
        ["The height and the node and leaf counts follow from the number of keys, because the tree is complete.",
         f"The {smallest} key is the root.",
         f"The {largest} key is always a leaf, so only the leaves, the second half of the array, are checked."],
        ("Height, node or leaf count", "Peek at the root", "The other extreme (largest in a min heap)"),
        f"""
        height():
            return the number of bits in len(items)
        leaf_count():
            return len(items) - len(items) // 2
        {other}():
            return the {largest} of items[len(items) // 2:]
        """, (f"{HEAP}:Heap.height", f"{HEAP}:Heap.leaf_count", f"{HEAP}:{cls}.{other}"))
    display(topic, "Draws the heap as a tree and as the array that stores it.")

add("priority-queue", "Enqueue", "Adds an item with its priority, then sifts its entry up the min heap.",
    ["Make an entry from the priority, the next arrival number and the item.",
     "Add the entry to the min heap as its last leaf.",
     "Sift it up while it should be served before its parent, which means a smaller priority."],
    "Enqueue",
    """
    enqueue(item, priority):
        entry = (priority, next arrival number, item)
        heap.insert(entry)
    """, (f"{PRIORITY_QUEUE}.enqueue", f"{HEAP}:Heap.insert", f"{HEAP}:Heap._sift_up"))
add("priority-queue", "Dequeue", "Removes the item that should be served next, from the root of the heap.",
    ["If the queue is empty, there's nothing to dequeue.",
     "Extract the heap's root, which moves the last leaf up and sifts it down.",
     "Give back the root entry's item and priority."],
    "Dequeue",
    """
    dequeue():
        if heap is empty: error "priority queue is empty"
        entry = heap.extract()
        return entry.item, entry.priority
    """, (f"{PRIORITY_QUEUE}.dequeue", f"{HEAP}:Heap.extract", f"{HEAP}:Heap._sift_down"))
add("priority-queue", "Peek", "Shows the item that will be served next, without removing it.",
    ["If the queue is empty, there's nothing to see.",
     "Return the item and priority of the heap's root."],
    "Peek",
    """
    peek():
        if heap is empty: error "priority queue is empty"
        return heap.peek().item, heap.peek().priority
    """, f"{PRIORITY_QUEUE}.peek")
add("priority-queue", "Change Priority", "Gives an item a new priority and moves it to its new place in the heap.",
    ["Search the heap's array for the item, taking the copy that arrived first.",
     "Replace its entry's priority, keeping its arrival number.",
     "Sift the entry up if it now belongs above its parent, or down otherwise."],
    "Change priority",
    """
    change_priority(item, priority):
        i = the index of the earliest entry holding item (error if there's none)
        items[i] = items[i] with the new priority
        if i > 0 and items[i] belongs above its parent: sift_up(i)
        else: sift_down(i)
    """, (f"{PRIORITY_QUEUE}.change_priority", f"{HEAP}:Heap.update"))
add("priority-queue", "Size", "Shows how many items are waiting in the priority queue.",
    ["Return the number of entries in the heap."],
    "Size",
    """
    size():
        return the number of entries in heap
    """, f"{PRIORITY_QUEUE}.__len__")
display("priority-queue", "Draws the heap and lists the items in the order they'll be served.")

# ---------------------------------------------------------------------------
# Trie
# ---------------------------------------------------------------------------

add("trie", "Insert a Word", "Adds a word by following its characters from the root and creating the nodes that are missing.",
    ["Start at the root.",
     "For each character, follow the child for that character, creating it if it doesn't exist yet.",
     "Mark the last node as the end of a word, unless it's marked already."],
    "Insert a word",
    """
    insert(word):
        node = root
        for each char in word:
            if node has no child for char: create one
            node = node.children[char]
        if node.is_word: error "already in the trie"
        node.is_word = true
    """, f"{TRIE}.insert")
add("trie", "Delete a Word", "Removes a word's mark, then prunes the nodes that no longer lead to any word.",
    ["Follow the word's characters from the root, remembering the path.",
     "If the path is missing or its last node isn't marked, the word isn't in the trie.",
     "Remove the mark, then walk back toward the root, deleting each node that ends no word and has no children."],
    "Delete a word",
    """
    delete(word):
        path = the nodes along word's characters (error if the word isn't there)
        path.last.is_word = false
        for depth from len(word) down to 1:
            if path[depth] ends a word or has children: stop
            remove path[depth] from its parent's children
    """, f"{TRIE}.delete")
add("trie", "Search a Word", "Checks whether a word was inserted by following its characters from the root.",
    ["Follow the word's characters from the root.",
     "If a character has no child, the word isn't there.",
     "Otherwise, the word is there only if the last node is marked as the end of a word."],
    "Search a word",
    """
    search(word):
        node = root
        for each char in word:
            node = node.children[char], or return false if there's none
        return node.is_word
    """, (f"{TRIE}.search", f"{TRIE}._find"))
add("trie", "Prefix Check", "Checks whether any word starts with a prefix.",
    ["Follow the prefix's characters from the root.",
     "If the whole path exists and leads to a word or to more nodes, some word starts with the prefix."],
    "Check a prefix",
    """
    starts_with(prefix):
        node = the node at the end of prefix's path, or return false
        return node.is_word or node has children
    """, (f"{TRIE}.starts_with", f"{TRIE}._find"))
add("trie", "Autocomplete", "Lists every word that starts with a prefix, in alphabetical order.",
    ["Follow the prefix's characters from the root.",
     "From the node where the prefix ends, visit every node below it, taking the children in character order.",
     "Collect the spelling of every marked node you visit."],
    "Autocomplete",
    """
    autocomplete(prefix):
        node = the node at the end of prefix's path, or return no words
        collect(node, prefix)

    collect(node, spelled):
        if node.is_word: add spelled to the words
        for each char in node's children, sorted:
            collect(node.children[char], spelled + char)
    """, (f"{TRIE}.autocomplete", f"{TRIE}._collect"))
add("trie", "Word Count", "Shows how many words the trie holds and how many nodes it uses.",
    ["Return the word count, which every insert and delete keeps up to date.",
     "Count the nodes by visiting every node below the root."],
    "Word count",
    """
    word_count():
        return count
    """, (f"{TRIE}.__len__", f"{TRIE}.node_count"))
display("trie", "Draws the trie as a tree of characters, marking the nodes that end a word.")

# ---------------------------------------------------------------------------
# Graphs
# ---------------------------------------------------------------------------

MATRIX = f"{GRAPH}:MatrixGraph"
LIST = f"{GRAPH}:ListGraph"

add("adjacency-matrix-graph", "Add Vertex", "Adds the next numbered vertex, with no edges.",
    ["Add a 0 to the end of every row, which adds a column for the new vertex.",
     "Add a new row of zeros at the bottom.",
     "The new vertex's number is the old number of vertices."],
    "Add vertex",
    """
    add_vertex():
        for each row in matrix: append 0
        append a row of zeros to matrix
        return the number of vertices - 1
    """, f"{MATRIX}.add_vertex")
add("adjacency-matrix-graph", "Remove Vertex", "Removes a vertex and all of its edges, so the vertices after it move down by one number.",
    ["Check that the vertex exists.",
     "Delete its row from the matrix.",
     "Delete its column from every row that's left."],
    "Remove vertex",
    """
    remove_vertex(v):
        if v isn't a vertex: error "out of bounds"
        remove row v from matrix
        for each row in matrix: remove the value in column v
    """, f"{MATRIX}.remove_vertex")
add("adjacency-matrix-graph", "Add Edge", "Adds an edge with a weight, or changes the weight of an existing edge.",
    ["Check that both vertices exist.",
     "Write the weight into the cell in row u and column v.",
     "For an undirected graph, also write it into row v and column u."],
    "Add or remove an edge",
    """
    add_edge(u, v, weight):
        matrix[u][v] = weight
        if undirected: matrix[v][u] = weight
    """, f"{MATRIX}.add_edge")
add("adjacency-matrix-graph", "Remove Edge", "Removes an edge by setting its cell back to 0.",
    ["Check that both vertices exist and that the cell isn't 0 already.",
     "Set the cell in row u and column v to 0.",
     "For an undirected graph, also set row v and column u to 0."],
    "Add or remove an edge",
    """
    remove_edge(u, v):
        if matrix[u][v] == 0: return false
        matrix[u][v] = 0
        if undirected: matrix[v][u] = 0
    """, f"{MATRIX}.remove_edge")
add("adjacency-matrix-graph", "Search Edge", "Looks up the weight of the edge from one vertex to another.",
    ["Check that both vertices exist.",
     "Read the cell in row u and column v, where 0 means there's no edge."],
    "Search an edge",
    """
    search_edge(u, v):
        return matrix[u][v], or nothing if it's 0
    """, f"{MATRIX}.search_edge")
add("adjacency-list-graph", "Add Vertex", "Adds a vertex with the number you choose and an empty list of edges.",
    ["If the vertex already exists, refuse it.",
     "Give the vertex a new, empty list of edges."],
    "Add vertex",
    """
    add_vertex(v):
        if v is already a vertex: error "already exists"
        lists[v] = empty list
    """, f"{LIST}.add_vertex")
add("adjacency-list-graph", "Remove Vertex", "Removes a vertex, its list and every edge that points to it.",
    ["Check that the vertex exists.",
     "Go through every vertex's list and drop the edges that lead to it.",
     "Delete the vertex's own list."],
    "Remove vertex",
    """
    remove_vertex(v):
        if v isn't a vertex: error "not found"
        for each vertex u: remove the edges to v from lists[u]
        delete lists[v]
    """, f"{LIST}.remove_vertex")
add("adjacency-list-graph", "Add Edge", "Adds an edge with a weight, or replaces the weight of an existing edge.",
    ["Check that both vertices exist.",
     "Remove any old edge to v from u's list, then add the new edge.",
     "For an undirected graph, do the same in v's list."],
    "Add or remove an edge",
    """
    add_edge(u, v, weight):
        remove any edge to v from lists[u], then add (v, weight)
        if undirected: remove any edge to u from lists[v], then add (u, weight)
    """, (f"{LIST}.add_edge", f"{LIST}._link"))
add("adjacency-list-graph", "Remove Edge", "Removes an edge from the lists that hold it.",
    ["Check that both vertices exist and that u's list has an edge to v.",
     "Remove that edge from u's list.",
     "For an undirected graph, also remove the edge to u from v's list."],
    "Add or remove an edge",
    """
    remove_edge(u, v):
        if lists[u] has no edge to v: return false
        remove the edge to v from lists[u]
        if undirected: remove the edge to u from lists[v]
    """, (f"{LIST}.remove_edge", f"{LIST}._link"))
add("adjacency-list-graph", "Search Edge", "Looks through a vertex's list for an edge to another vertex.",
    ["Check that the first vertex exists.",
     "Go through its list until an entry's neighbor is the second vertex, and give back that entry's weight."],
    "Search an edge",
    """
    search_edge(u, v):
        for each (neighbor, weight) in lists[u]:
            if neighbor == v: return weight
        return nothing
    """, f"{LIST}.search_edge")

for topic, cls, neighbors in (("adjacency-matrix-graph", MATRIX, "means reading its whole row"),
                              ("adjacency-list-graph", LIST, "is just its list")):
    add(topic, "Traversals", "Visits every vertex that can be reached from a start vertex, breadth-first or depth-first.",
        ["BFS keeps a queue: it visits the start vertex, then all its unvisited neighbors, spreading out in rings.",
         "DFS follows one neighbor as deep as it can go before backing up to try the next one.",
         f"Finding a vertex's neighbors {neighbors}."],
        "BFS or DFS",
        """
        bfs(start):
            mark start as visited
            queue = [start]
            while queue isn't empty:
                v = take the front of queue
                visit v
                for each neighbor n of v:
                    if n isn't visited: mark n as visited and add it to queue
        """, (f"{cls}.bfs", f"{cls}.dfs"))
    display(topic, "Lets you pick a graph algorithm that fits the graph's direction and runs it.", "Graph Algorithms")

display("adjacency-matrix-graph", "Draws the adjacency matrix as a grid.")
display("adjacency-list-graph", "Lists every vertex with its edges.")

# ---------------------------------------------------------------------------
# Hash tables and the hash set
# ---------------------------------------------------------------------------

CHAINING = f"{HASH_TABLE}:ChainingHashTable"
PROBING = f"{HASH_TABLE}:LinearProbingHashTable"

add("chaining-hash-table", "Insert", "Adds a key-value pair to the chain of the key's bucket, or updates the key's value.",
    ["Hash the key and wrap the number around to the table's size to get its bucket.",
     "Go through the bucket's chain, and if the key is there, replace its value.",
     "Otherwise, add the pair to the end of the chain."],
    "Insert",
    """
    insert(key, value):
        bucket = table[hash(key) mod size]
        for each pair in bucket:
            if pair.key == key: pair.value = value and stop
        append (key, value) to bucket
    """, (f"{CHAINING}.insert", f"{CHAINING}.hash_function"))
add("chaining-hash-table", "Delete", "Removes a key's pair from the chain of its bucket.",
    ["Find the key's bucket with the hash function.",
     "Go through the chain until you find the key.",
     "Remove that pair from the chain; no other bucket changes."],
    "Delete",
    """
    delete(key):
        bucket = table[hash(key) mod size]
        remove the pair with key from bucket (error if it isn't there)
    """, f"{CHAINING}.delete")
add("chaining-hash-table", "Search", "Finds a key's value by looking only in the chain of its bucket.",
    ["Find the key's bucket with the hash function.",
     "Go through the chain until you find the key, and give back its value."],
    "Search",
    """
    lookup(key):
        bucket = table[hash(key) mod size]
        for each pair in bucket:
            if pair.key == key: return pair.value
        error "not found"
    """, f"{CHAINING}.lookup")
display("chaining-hash-table", "Draws every bucket with its chain of pairs.")

add("linear-probing-hash-table", "Insert", "Stores a key-value pair in the key's home slot, or in the next free slot after it.",
    ["Hash the key to find its home slot.",
     "Probe forward one slot at a time, wrapping around, until you reach an empty slot or the same key.",
     "Store the pair there, or refuse it if you came all the way back around, because the table is full."],
    "Insert",
    """
    insert(key, value):
        i = hash(key) mod size
        while slots[i] isn't empty:
            if slots[i].key == key: slots[i] = (key, value) and stop
            i = (i + 1) mod size
            if i is the home slot again: error "table is full"
        slots[i] = (key, value)
    """, (f"{PROBING}.insert", f"{PROBING}.hash_function"))
add("linear-probing-hash-table", "Delete", "Removes a key's pair, then rehashes the rest of its cluster so no search stops at the gap.",
    ["Find the key by probing from its home slot.",
     "Empty its slot.",
     "Take out every pair in the slots right after it, up to the next empty slot, and insert each one again."],
    "Delete",
    """
    delete(key):
        i = find(key)
        slots[i] = empty
        j = (i + 1) mod size
        while slots[j] isn't empty:
            take the pair out of slots[j] and remember it
            j = (j + 1) mod size
        insert every remembered pair again
    """, (f"{PROBING}.delete", f"{PROBING}._find"))
add("linear-probing-hash-table", "Search", "Finds a key by probing from its home slot until it reaches the key or an empty slot.",
    ["Hash the key to find its home slot.",
     "Check slot after slot, wrapping around, until you find the key.",
     "An empty slot, or coming back to the home slot, means the key isn't in the table."],
    "Search",
    """
    find(key):
        i = hash(key) mod size
        while slots[i] isn't empty:
            if slots[i].key == key: return i
            i = (i + 1) mod size
            if i is the home slot again: stop
        error "not found"
    """, (f"{PROBING}.lookup", f"{PROBING}._find"))
display("linear-probing-hash-table", "Draws every slot with its key, its value and the key's home slot.")

add("hash-set", "Add", "Adds an item to set A or set B, unless the set already holds it.",
    ["Hash the item to find its bucket.",
     "If the bucket's chain already holds the item, nothing changes.",
     "Otherwise, add the item to the chain."],
    "Add",
    """
    add(item):
        insert item as a key with no value into the hash table
        return whether it was new
    """, (f"{HASH_SET}.add", f"{CHAINING}.insert"))
add("hash-set", "Remove", "Removes an item from set A or set B.",
    ["Hash the item to find its bucket.",
     "Remove the item from that bucket's chain."],
    "Remove",
    """
    remove(item):
        delete item from the hash table (error if it isn't there)
    """, (f"{HASH_SET}.remove", f"{CHAINING}.delete"))
add("hash-set", "Check Membership", "Checks whether an item is in set A and whether it's in set B.",
    ["Hash the item to find its bucket in each set.",
     "Look through that bucket's chain for the item."],
    "Check membership",
    """
    contains(item):
        return whether the hash table can look up item
    """, (f"{HASH_SET}.__contains__", f"{CHAINING}.lookup"))
add("hash-set", "Union", "Builds a new set with every item that's in A or in B.",
    ["Create a new, empty set.",
     "Add every item of A, then every item of B; adding an item that's already there changes nothing."],
    "Union",
    """
    union(A, B):
        result = new set
        for each item in A, then in B: result.add(item)
        return result
    """, f"{HASH_SET}.union")
add("hash-set", "Intersection", "Builds a new set with the items that are in both A and B.",
    ["Go through the items of A.",
     "Keep each one that B also contains."],
    "Intersection",
    """
    intersection(A, B):
        return a new set of every item in A that B contains
    """, f"{HASH_SET}.intersection")
add("hash-set", "Difference", "Builds a new set with the items of one set that aren't in the other.",
    ["Go through the items of the first set.",
     "Keep each one that the second set doesn't contain."],
    "Difference",
    """
    difference(A, B):
        return a new set of every item in A that B doesn't contain
    """, f"{HASH_SET}.difference")
add("hash-set", "Subset Check", "Checks whether every item of A is in B, and whether every item of B is in A.",
    ["Go through the items of the first set.",
     "The answer is no as soon as one of them is missing from the second set."],
    "Subset check",
    """
    is_subset(A, B):
        for each item in A:
            if B doesn't contain item: return false
        return true
    """, f"{HASH_SET}.is_subset")
display("hash-set", "Draws the buckets of both sets and writes each set in set notation.")

# ---------------------------------------------------------------------------
# Disjoint set
# ---------------------------------------------------------------------------

add("disjoint-set", "Union", "Merges the sets of two elements, attaching the shorter tree under the taller one.",
    ["Find the root of each element.",
     "If the roots are the same, the elements are already in the same set.",
     "Otherwise, make the root with the lower rank point at the other root, and add 1 to that root's rank if both ranks were equal."],
    "Union",
    """
    union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb: return false
        if rank[ra] < rank[rb]: swap ra and rb
        parent[rb] = ra
        if rank[ra] == rank[rb]: rank[ra] = rank[ra] + 1
    """, (f"{DISJOINT_SET}.union", f"{DISJOINT_SET}.find"))
add("disjoint-set", "Find", "Finds the root of an element's set and points every element on the way straight at it.",
    ["Follow the parent links up from the element until you reach an element that is its own parent: the root.",
     "Walk the same path again, pointing each element directly at the root."],
    "Find",
    """
    find(x):
        root = x
        while parent[root] != root: root = parent[root]
        while parent[x] != root:
            next = parent[x]
            parent[x] = root
            x = next
        return root
    """, (f"{DISJOINT_SET}.find", f"{DISJOINT_SET}.root_of"))
add("disjoint-set", "Check if Connected", "Checks whether two elements are in the same set by comparing their roots.",
    ["Find the root of each element, compressing both paths.",
     "The elements are connected when their roots are the same."],
    "Check if connected",
    """
    connected(a, b):
        return find(a) == find(b)
    """, (f"{DISJOINT_SET}.connected", f"{DISJOINT_SET}.find"))
add("disjoint-set", "List Sets", "Lists every set with its root and its members.",
    ["Follow each element up to its root, without compressing any paths.",
     "Group the elements by their root."],
    "List sets",
    """
    groups():
        for each element x:
            add x to the group of root_of(x)
    """, (f"{DISJOINT_SET}.groups", f"{DISJOINT_SET}.root_of"))
display("disjoint-set", "Draws the parent and rank arrays, followed by every set.")

# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

add("sorting", "Bubble Sort", "Swaps neighbors that are out of order, pass after pass, until a pass makes no swaps.",
    rows="Bubble sort", explained=True, sources=f"{SORTING}:bubble_sort", pseudocode="""
    bubble_sort(items):
        for each pass:
            swapped = false
            for j from 0 to the end of the unsorted part - 1:
                if items[j] > items[j + 1]:
                    swap them
                    swapped = true
            if not swapped: stop
    """)
add("sorting", "Selection Sort", "Finds the smallest value of the unsorted part and swaps it to the front of that part.",
    rows="Selection sort", explained=True, sources=f"{SORTING}:selection_sort", pseudocode="""
    selection_sort(items):
        for i from 0 to n - 1:
            smallest = i
            for j from i + 1 to n - 1:
                if items[j] < items[smallest]: smallest = j
            swap items[i] and items[smallest]
    """)
add("sorting", "Insertion Sort", "Takes each value in turn and slides it back into place among the sorted values before it.",
    rows="Insertion sort", explained=True, sources=f"{SORTING}:insertion_sort", pseudocode="""
    insertion_sort(items):
        for i from 1 to n - 1:
            key = items[i]
            j = i - 1
            while j >= 0 and items[j] > key:
                items[j + 1] = items[j]
                j = j - 1
            items[j + 1] = key
    """)
add("sorting", "Quick Sort", "Partitions the values around the last value as the pivot, then sorts both sides the same way.",
    rows="Quick sort", explained=True,
    sources=(f"{SORTING}:quick_sort", f"{SORTING}:_quick_sort", f"{SORTING}:_partition"), pseudocode="""
    quick_sort(low, high):
        if low >= high: stop
        pivot = items[high]
        i = low - 1
        for j from low to high - 1:
            if items[j] <= pivot:
                i = i + 1
                swap items[i] and items[j]
        swap items[i + 1] and items[high]
        quick_sort(low, i)
        quick_sort(i + 2, high)
    """)
add("sorting", "Heap Sort", "Builds a max heap, then keeps swapping its root to the end and sifting the new root down.",
    rows="Heap sort", explained=True, sources=(f"{SORTING}:heap_sort", f"{SORTING}:_heapify"), pseudocode="""
    heap_sort(items):
        for i from n // 2 - 1 down to 0:
            sift_down(i, n)
        for end from n - 1 down to 1:
            swap items[0] and items[end]
            sift_down(0, end)
    """)
add("sorting", "Shell Sort", "Does a gapped insertion sort, halving the gap every round until it's 1.",
    rows="Shell sort", explained=True, sources=f"{SORTING}:shell_sort", pseudocode="""
    shell_sort(items):
        gap = n // 2
        while gap > 0:
            for i from gap to n - 1:
                value = items[i]
                j = i
                while j >= gap and items[j - gap] > value:
                    items[j] = items[j - gap]
                    j = j - gap
                items[j] = value
            gap = gap // 2
    """)
add("sorting", "Merge Sort", "Splits the list in half, sorts each half and merges the two sorted halves.",
    rows="Merge sort", explained=True, sources=(f"{SORTING}:merge_sort", f"{SORTING}:_merge_sort"), pseudocode="""
    merge_sort(low, high):
        if high - low < 2: stop
        mid = (low + high) // 2
        merge_sort(low, mid)
        merge_sort(mid, high)
        merged = empty list
        while both halves have values:
            move the smaller front value to merged, taking the left one on a tie
        add what's left of both halves to merged
        copy merged back into items[low:high]
    """)
add("sorting", "Counting Sort", "Counts how often each value appears, then writes the values back in order.",
    rows="Counting sort", explained=True,
    sources=(f"{SORTING}:counting_sort", f"{SORTING}:_counting_sort", f"{SORTING}:accepts"), pseudocode="""
    counting_sort(items):
        offset = min(items)
        counts = one 0 for every value from min(items) to max(items)
        for each value in items: counts[value - offset] += 1
        index = 0
        for each position in counts, in order:
            repeat counts[position] times:
                items[index] = position + offset
                index = index + 1
    """)
add("sorting", "Radix Sort", "Deals the numbers into ten buckets by one digit at a time, starting with the ones digit.",
    rows="Radix sort", explained=True, sources=(f"{SORTING}:radix_sort", f"{SORTING}:_radix_sort"), pseudocode="""
    radix_sort(items):
        place = 1
        while max(items) // place > 0:
            buckets = ten empty lists
            for each value in items: add value to buckets[value // place mod 10]
            items = buckets 0 to 9, joined in order
            place = place * 10
    """)
add("sorting", "Compare All Algorithms", "Runs every sorting algorithm on its own copy of the list and compares the work each one did.",
    ["Copy the list once for every algorithm.",
     "Sort each copy, counting its comparisons, writes and steps.",
     "Show the counts side by side, marking the algorithms that can't sort the list."])
display("sorting", "Draws the list under its indexes.")

# ---------------------------------------------------------------------------
# Searching
# ---------------------------------------------------------------------------

add("searching", "Linear Search", "Checks the values one by one from the start until it finds the target.",
    rows="Linear search", explained=True, sources=f"{SEARCHING}:linear_search", pseudocode="""
    linear_search(items, target):
        for i from 0 to n - 1:
            if items[i] == target: return i
        return not found
    """)
add("searching", "Binary Search", "Checks the middle of the sorted range and throws away the half that can't hold the target.",
    rows="Binary search", explained=True,
    sources=(f"{SEARCHING}:binary_search", f"{SEARCHING}:_on_sorted_copy", f"{SEARCHING}:_binary"), pseudocode="""
    binary_search(values, target):
        low = 0
        high = n - 1
        while low <= high:
            mid = (low + high) // 2
            if values[mid] == target: return mid
            if values[mid] < target: low = mid + 1
            else: high = mid - 1
        return not found
    """)
add("searching", "Jump Search", "Jumps ahead in blocks as long as the square root of the length, then checks one block value by value.",
    rows="Jump search", explained=True, sources=(f"{SEARCHING}:jump_search", f"{SEARCHING}:_jump"), pseudocode="""
    jump_search(values, target):
        step = the whole-number square root of n
        start = 0
        end = step
        while values[end - 1] < target:
            start = end
            if start >= n: return not found
            end = min(end + step, n)
        for i from start to end - 1:
            if values[i] == target: return i
        return not found
    """)
add("searching", "Interpolation Search", "Guesses the target's position from its value and narrows the range around each guess.",
    rows="Interpolation search", explained=True,
    sources=(f"{SEARCHING}:interpolation_search", f"{SEARCHING}:_interpolation"), pseudocode="""
    interpolation_search(values, target):
        low = 0
        high = n - 1
        while low <= high and values[low] <= target <= values[high]:
            pos = low + (target - values[low]) * (high - low) // (values[high] - values[low])
            if values[pos] == target: return pos
            if values[pos] < target: low = pos + 1
            else: high = pos - 1
        return not found
    """)
add("searching", "Exponential Search", "Doubles the position it checks until it passes the target, then binary searches the last range.",
    rows="Exponential search", explained=True,
    sources=(f"{SEARCHING}:exponential_search", f"{SEARCHING}:_exponential"), pseudocode="""
    exponential_search(values, target):
        if values[0] == target: return 0
        bound = 1
        while bound < n and values[bound] < target: bound = bound * 2
        if bound < n and values[bound] == target: return bound
        return binary_search(values, target, bound // 2 + 1, min(bound - 1, n - 1))
    """)
display("searching", "Draws the list under its indexes.")

# ---------------------------------------------------------------------------
# Graph algorithms
# ---------------------------------------------------------------------------

add("graph-algorithms", "Dijkstra's Shortest Paths", "Finds the shortest path from a vertex you choose to every other vertex.",
    rows="Dijkstra's shortest paths (min heap)", explained=True,
    sources=(f"{GRAPH_ALGORITHMS}:dijkstra", f"{GRAPH_ALGORITHMS}:shortest_path"), pseudocode="""
    dijkstra(source):
        distance[v] = infinity for every vertex v
        distance[source] = 0
        heap = [(0, source)]
        while heap isn't empty:
            (d, u) = take the smallest entry from heap
            if d > distance[u]: skip it
            for each edge from u to v with weight w:
                if d + w < distance[v]:
                    distance[v] = d + w
                    previous[v] = u
                    add (distance[v], v) to heap
    """)
add("graph-algorithms", "Topological Sort", "Lines up the vertices so every edge points forward, or reports that the graph has a cycle.",
    rows="Topological sort (Kahn)", explained=True, sources=f"{GRAPH_ALGORITHMS}:topological_sort", pseudocode="""
    topological_sort():
        in_degree[v] = the number of edges into v, for every v
        queue = every vertex whose in_degree is 0
        while queue isn't empty:
            u = take the front of queue
            add u to order
            for each edge from u to v:
                in_degree[v] = in_degree[v] - 1
                if in_degree[v] == 0: add v to queue
        if order misses some vertices: error "the graph has a cycle"
    """)
add("graph-algorithms", "Cycle Detection", "Finds a cycle with a depth-first search on a directed graph, or with a disjoint set on an undirected graph.",
    rows=("Cycle detection, directed (DFS)", "Cycle detection, undirected (disjoint set)"), explained=True,
    sources=(f"{GRAPH_ALGORITHMS}:find_cycle", f"{GRAPH_ALGORITHMS}:_directed_cycle", f"{GRAPH_ALGORITHMS}:_undirected_cycle"),
    pseudocode="""
    directed, visit(u):
        put u on the current path
        for each edge from u to v:
            if v is on the current path: found a cycle
            if v isn't finished: visit(v)
        take u off the path and mark it finished

    undirected:
        for each edge between u and v:
            if find(u) == find(v): found a cycle
            union(u, v)
    """)
add("graph-algorithms", "Minimum Spanning Tree (Prim)",
    "Grows a minimum spanning tree from the first vertex, always adding the lightest edge that reaches a new vertex.",
    rows="Minimum spanning tree (Prim, min heap)", explained=True, sources=f"{GRAPH_ALGORITHMS}:prim", pseudocode="""
    prim():
        for each vertex start that isn't in a tree yet:
            add start to the tree, and its edges to a min heap
            while heap isn't empty:
                (weight, u, v) = take the lightest edge from heap
                if v is in the tree: skip the edge
                add the edge and v to the tree
                add v's edges to vertices outside the tree to heap
    """)
add("graph-algorithms", "Minimum Spanning Tree (Kruskal)",
    "Adds the edges from lightest to heaviest, skipping every edge that would close a cycle.",
    rows="Minimum spanning tree (Kruskal, disjoint set)", explained=True, sources=f"{GRAPH_ALGORITHMS}:kruskal",
    pseudocode="""
    kruskal():
        sets = a disjoint set with every vertex on its own
        for each edge (u, v, weight), from lightest to heaviest:
            if union(u, v) merged two sets: add the edge to the tree
            else: skip the edge, since it would close a cycle
    """)
display("graph-algorithms", "Draws the graph as an adjacency list.")


_BY_KEY = {(note.topic, note.operation): note for note in NOTES}


def find(topic, operation):
    """Return the note of an operation in a topic's menu; raise KeyError if it has none."""
    try:
        return _BY_KEY[(topic, operation)]
    except KeyError:
        raise KeyError(f"There's no note for {operation!r} in the {topic!r} menu.") from None


def resolve(reference):
    """Return the function a source reference such as "pydsa.core.stack:Stack.push" points to."""
    module_name, _, qualified_name = reference.partition(":")
    target = importlib.import_module(module_name)
    for part in qualified_name.split("."):
        target = getattr(target, part)
    return target
