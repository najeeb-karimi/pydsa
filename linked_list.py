"""Linked list implementations: singly and doubly linked lists."""

import utility


# ---------------------------------------------------------------------------
# Singly Linked List
# ---------------------------------------------------------------------------

class SLLNode:
    """Node of a singly linked list."""

    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """Singly linked list that accepts items of any type."""

    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        """Insert a new node before the head."""
        new_node = SLLNode(data)
        new_node.next = self.head
        self.head = new_node
        print("\n✅ Insertion successful.", end="")
        self.traverse()

    def insert_at_end(self, data):
        """Insert a new node after the last node."""
        new_node = SLLNode(data)
        if self.head is None:
            self.head = new_node
            print("\n✅ Insertion successful.", end="")
            self.traverse()
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        print("\n✅ Insertion successful.", end="")
        self.traverse()

    def insert_at_position(self, position, data):
        """Insert a new node at the given position."""
        # Position 0 is the same as inserting at the beginning
        if position == 0:
            self.insert_at_beginning(data)
            return
        new_node = SLLNode(data)
        current = self.head
        # Walk to the node before the position, stopping if the list ends two or more positions early
        for _ in range(position - 1):
            if current is None:
                print("\n🚫 Position out of bounds. Insertion unsuccessful.")
                return
            current = current.next
        # Stop if the list ends exactly one position early
        if current is None:
            print("\n🚫 Position out of bounds. Insertion unsuccessful.")
            return
        new_node.next = current.next
        current.next = new_node
        print("\n✅ Insertion successful.", end="")
        self.traverse()

    def delete_from_beginning(self):
        """Delete the head node."""
        if self.head is None:
            print("\n🚫 List is empty.")
        # An else branch is used here instead of returning early from the if block
        else:
            self.head = self.head.next
            print("\n✅ Deletion successful.", end="")
            self.traverse()

    def delete_from_end(self):
        """Delete the last node."""
        # Empty list
        if self.head is None:
            print("\n🚫 List is empty.")
            return
        # Only the head is left
        if self.head.next is None:
            self.head = None
            print("\n✅ Deletion successful.", end="")
            self.traverse()
            return
        # Otherwise, unlink the last node from the second-to-last one
        second_last = self.head
        while second_last.next.next:
            second_last = second_last.next
        second_last.next = None
        print("\n✅ Deletion successful.", end="")
        self.traverse()

    def delete_from_position(self, position):
        """Delete the node at the given position."""
        # Empty list
        if self.head is None:
            print("\n🚫 List is empty.")
            return
        # Position 0 removes the head
        if position == 0:
            self.head = self.head.next
            print("\n✅ Deletion successful.", end="")
            self.traverse()
            return
        current = self.head
        # Walk to the node before the position, stopping if the list ends two or more positions early
        for _ in range(position - 1):
            if current.next is None:
                print("\n🚫 Position out of bounds. Deletion unsuccessful.")
                return
            current = current.next
        # Stop if the position is right after the last node
        if current.next is None:
            print("\n🚫 Position out of bounds. Deletion unsuccessful.")
            return
        current.next = current.next.next
        print("\n✅ Deletion successful.", end="")
        self.traverse()

    def traverse(self):
        """Print all items from head to tail, joined by arrows."""
        current = self.head
        if current is None:
            print("\n❌ List is empty.")
            return
        # Collect the items as strings first, then join them, so no arrow is printed after the last item
        sll_items = []
        while current:
            sll_items.append(str(current.data))
            current = current.next
        print("\n👉", " => ".join(sll_items))

    def search(self, target):
        """Search the list using Linear Search, the only practical option for linked lists."""
        current = self.head
        position = 0
        while current:
            if current.data == target:
                print(f"\n✅ Item found at position {position}.")
                return position
            current = current.next
            position += 1
        print("\n❌ Item not found.")
        return -1


def sll_main():
    """Run the singly linked list operation menu."""
    # Start with an empty list
    sll = SinglyLinkedList()

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the SINGLY LINKED LIST?
★0) Definition
★1) Insertion at the Beginning
★2) Insertion at a Specific Point
★3) Insertion at the End
★4) Deletion from the Beginning
★5) Deletion from a Specific Point
★6) Deletion from the End
★7) Traversing/Displaying
★8) Searching
★9) New Linked List
★10) New Data Structure
★11) Exiting the Program

>>> """)

        match opr:

            # Definition
            case "0":
                ll_intro("def")

            # Insertion at the beginning
            case "1":
                item = utility.input_verify()
                if item is not None:
                    sll.insert_at_beginning(item)
                else:
                    print("\n🚫 Invalid data type; item not inserted.")

            # Insertion at a specific point
            case "2":
                # Index validation loop
                while True:
                    index = input("\n🔟 Please enter the index.\n>>> ")
                    try:
                        index = int(index)
                    except ValueError:
                        print("\n🚫 Invalid index!")
                        continue
                    else:
                        break

                item = utility.input_verify()
                if item is not None:
                    sll.insert_at_position(index, item)
                else:
                    print("\n🚫 Invalid data type; item not inserted.")

            # Insertion at the end
            case "3":
                item = utility.input_verify()
                if item is not None:
                    sll.insert_at_end(item)
                else:
                    print("\n🚫 Invalid data type; item not inserted.")

            # Deletion from the beginning
            case "4":
                sll.delete_from_beginning()

            # Deletion from a specific point
            case "5":
                # Index validation loop
                while True:
                    index = input("\n🔟 Please enter the index.\n>>> ")
                    try:
                        index = int(index)
                    except ValueError:
                        print("\n🚫 Invalid index!")
                        continue
                    else:
                        break

                sll.delete_from_position(index)

            # Deletion from the end
            case "6":
                sll.delete_from_end()

            # Traversing
            case "7":
                sll.traverse()

            # Searching
            case "8":
                print("\nℹ️ Linear Search in the context of a linked list involves traversing the list node by node, starting from the head, and comparing each node’s data with the target value until the desired element is found or the end of the list is reached. Since linked lists do not provide direct access to their elements, each node must be accessed sequentially, making the search process inherently linear. The time complexity of linear search in a linked list is O(n), where n is the number of nodes in the list, because in the worst case, every node must be checked. The space complexity is O(1) as it requires no additional memory beyond the input list. Linear search is simple to implement and works well for small or unsorted linked lists, but it is inefficient for large lists compared to more advanced search algorithms.")
                target = utility.input_verify(msg="target element")
                if target is not None:
                    sll.search(target)
                else:
                    print("\n🚫 Invalid data type; nothing to search for.")

            # New linked list
            case "9":
                utility.clear()
                utility.main_intro()
                linked_list_main()
                break

            # New data structure
            case "10":
                utility.clear()
                utility.main_intro()
                break

            # Exit the program
            case "11":
                exit()

            # Invalid
            case _:
                print("\n🚫 Invalid operation code!")


# ---------------------------------------------------------------------------
# Doubly Linked List
# ---------------------------------------------------------------------------

class DLLNode:
    """Node of a doubly linked list."""

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Doubly linked list that accepts items of any type."""

    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        """Insert a new node before the head."""
        new_node = DLLNode(data)
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node
        print("\n✅ Insertion successful.", end="")
        self.traverse_forward()

    def insert_at_end(self, data):
        """Insert a new node after the last node."""
        new_node = DLLNode(data)
        if self.head is None:
            self.head = new_node
            print("\n✅ Insertion successful.", end="")
            self.traverse_forward()
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last
        print("\n✅ Insertion successful.", end="")
        self.traverse_forward()

    def insert_at_position(self, position, data):
        """Insert a new node at the given position."""
        if position == 0:
            self.insert_at_beginning(data)
            return
        new_node = DLLNode(data)
        current = self.head
        # Walk to the node currently at the position, stopping if the list ends too early
        for _ in range(position):
            if current is None:
                print("\n🚫 Position out of bounds. Insertion unsuccessful.")
                return
            current = current.next
        # The position right after the last node is handled by insert_at_end()
        if current is None:
            self.insert_at_end(data)
            return
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node
        print("\n✅ Insertion successful.", end="")
        self.traverse_forward()

    def delete_from_beginning(self):
        """Delete the head node."""
        if self.head is None:
            print("\n🚫 List is empty.")
            return
        self.head = self.head.next
        if self.head is not None:
            self.head.prev = None
        print("\n✅ Deletion successful.", end="")
        self.traverse_forward()

    def delete_from_end(self):
        """Delete the last node."""
        if self.head is None:
            print("\n🚫 List is empty.")
            return
        if self.head.next is None:
            self.head = None
            print("\n✅ Deletion successful.", end="")
            self.traverse_forward()
            return
        last = self.head
        while last.next:
            last = last.next
        last.prev.next = None
        print("\n✅ Deletion successful.", end="")
        self.traverse_forward()

    def delete_from_position(self, position):
        """Delete the node at the given position."""
        if self.head is None:
            print("\n🚫 List is empty.")
            return
        current = self.head
        for _ in range(position):
            current = current.next
            if current is None:
                print("\n🚫 Position out of bounds. Deletion unsuccessful.")
                return
        if current.next:
            current.next.prev = current.prev
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        print("\n✅ Deletion successful.", end="")
        self.traverse_forward()

    def traverse_forward(self):
        """Print all items from head to tail."""
        current = self.head
        if current is None:
            print("\n👉 List is empty.")
        else:
            dll_items = []
            while current:
                dll_items.append(str(current.data))
                current = current.next
            print("\n👉", " <=> ".join(dll_items))

    def traverse_backward(self):
        """Print all items from tail to head."""
        current = self.head
        if current is None:
            print("\n👉 List is empty.")
            return
        # Move to the last node first, then follow the prev links back
        while current.next:
            current = current.next
        dll_items = []
        while current:
            dll_items.append(str(current.data))
            current = current.prev
        print("\n👉", " <=> ".join(dll_items))

    def search(self, target):
        """Search the list using Linear Search, the only practical option for linked lists."""
        current = self.head
        position = 0
        while current:
            if current.data == target:
                print(f"\n✅ Item found at position {position}.")
                return position
            current = current.next
            position += 1
        print("\n❌ Item not found.")
        return -1


def dll_main():
    """Run the doubly linked list operation menu."""
    # Start with an empty list
    dll = DoublyLinkedList()

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the DOUBLY LINKED LIST?
★0) Definition
★1) Insertion at the Beginning
★2) Insertion at a Specific Point
★3) Insertion at the End
★4) Deletion from the Beginning
★5) Deletion from a Specific Point
★6) Deletion from the End
★7) Traversing Forward
★8) Traversing Backward
★9) Searching
★10) New Linked List
★11) New Data Structure
★12) Exiting the Program

>>> """)

        match opr:

            # Definition
            case "0":
                ll_intro("def")

            # Insertion at the beginning
            case "1":
                item = utility.input_verify()
                if item is not None:
                    dll.insert_at_beginning(item)
                else:
                    print("\n🚫 Invalid data type; item not inserted.")

            # Insertion at a specific point
            case "2":
                # Index validation loop
                while True:
                    index = input("\n🔟 Please enter the index.\n>>> ")
                    try:
                        index = int(index)
                    except ValueError:
                        print("\n🚫 Invalid index!")
                        continue
                    else:
                        break

                item = utility.input_verify()
                if item is not None:
                    dll.insert_at_position(index, item)
                else:
                    print("\n🚫 Invalid data type; item not inserted.")

            # Insertion at the end
            case "3":
                item = utility.input_verify()
                if item is not None:
                    dll.insert_at_end(item)
                else:
                    print("\n🚫 Invalid data type; item not inserted.")

            # Deletion from the beginning
            case "4":
                dll.delete_from_beginning()

            # Deletion from a specific point
            case "5":
                # Index validation loop
                while True:
                    index = input("\n🔟 Please enter the index.\n>>> ")
                    try:
                        index = int(index)
                    except ValueError:
                        print("\n🚫 Invalid index!")
                        continue
                    else:
                        break

                dll.delete_from_position(index)

            # Deletion from the end
            case "6":
                dll.delete_from_end()

            # Traversing forward
            case "7":
                dll.traverse_forward()

            # Traversing backward
            case "8":
                dll.traverse_backward()

            # Searching
            case "9":
                target = utility.input_verify(msg="target element")
                if target is not None:
                    dll.search(target)
                else:
                    print("\n🚫 Invalid data type; nothing to search for.")

            # New linked list
            case "10":
                utility.clear()
                utility.main_intro()
                linked_list_main()
                break

            # New data structure
            case "11":
                utility.clear()
                utility.main_intro()
                break

            # Exit the program
            case "12":
                exit()

            # Invalid
            case _:
                print("\n🚫 Invalid operation code!")


# ---------------------------------------------------------------------------
# Linked list main and intro functions
# ---------------------------------------------------------------------------

def linked_list_main():
    """Show the linked list intro and let the user pick a singly or doubly linked list.

    Once the chosen list's menu returns, control goes back to the main menu in main.py.
    """
    ll_intro("full")

    # Linked list type selection loop
    while True:
        list_type = input("""\n🧪 Which type of linked list do you want?
★1) Singly Linked List
★2) Doubly Linked List
    
>>> """)

        match list_type:
            # Singly
            case "1":
                sll_main()
                break

            # Doubly
            case "2":
                dll_main()
                break

            # Invalid
            case _:
                print("\n🚫 Invalid!")


def ll_intro(condition):
    """Print the ASCII art and definition ("full") or only the definition ("def")."""
    ll_ascii = r"""

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

    ll_def = """\n🎯 A linked list is a dynamic data structure used to store a collection of elements, called nodes, in a sequential manner. Each node in a linked list contains data and a reference (or link) to the next node, forming a chain. Unlike arrays, linked lists do not require contiguous memory allocation, which allows for efficient insertion and deletion of nodes as there is no need to shift elements. This flexibility makes linked lists suitable for applications where the data size varies dynamically and frequent modifications are required.

🌟 Linked lists come in several types, each serving different purposes:

🔹 Singly Linked List: Each node has a single link to the next node, allowing one-way traversal.
🔹 Doubly Linked List: Nodes have two links, one to the next node and one to the previous, enabling traversal in both directions.
🔹 Singly Circular Linked List: Similar to a singly linked list, but the last node links back to the first node, forming a loop for circular traversal.
🔹 Doubly Circular Linked List: An extension of the doubly linked list where the last node links to the first, and the first node links to the last, allowing circular traversal in both directions."""

    if condition == "full":
        print(ll_ascii)
        print(ll_def)
    elif condition == "def":
        print(ll_def)


# Run the linked list module on its own
if __name__ == "__main__":
    linked_list_main()
