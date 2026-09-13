"""Singly and doubly linked lists."""

from pydsa.core.errors import EmptyError, OutOfBoundsError


class LinkedList:
    """Behavior shared by both linked lists: iteration, length and searching."""

    def __init__(self):
        self.head = None

    def __iter__(self):
        """Yield the items from head to tail."""
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self):
        return sum(1 for _ in self)

    def is_empty(self):
        """Return True if the list has no nodes."""
        return self.head is None

    def search(self, target):
        """Return the position of the first item equal to target, or -1 (Linear Search)."""
        for position, data in enumerate(self):
            if data == target:
                return position
        return -1


# ---------------------------------------------------------------------------
# Singly Linked List
# ---------------------------------------------------------------------------

class SLLNode:
    """Node of a singly linked list."""

    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList(LinkedList):
    """Singly linked list that accepts items of any type."""

    def insert_at_beginning(self, data):
        """Insert a new node before the head."""
        new_node = SLLNode(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        """Insert a new node after the last node."""
        new_node = SLLNode(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def insert_at_position(self, position, data):
        """Insert a new node so it ends up at position (0 up to the list length)."""
        if position < 0:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        # Position 0 is the same as inserting at the beginning
        if position == 0:
            self.insert_at_beginning(data)
            return
        current = self.head
        # Walk to the node before the position, stopping if the list ends two or more positions early
        for _ in range(position - 1):
            if current is None:
                raise OutOfBoundsError(f"Position {position} is out of bounds.")
            current = current.next
        # Stop if the list ends exactly one position early
        if current is None:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        new_node = SLLNode(data)
        new_node.next = current.next
        current.next = new_node

    def delete_from_beginning(self):
        """Delete the head node and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        data = self.head.data
        self.head = self.head.next
        return data

    def delete_from_end(self):
        """Delete the last node and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        # Only the head is left
        if self.head.next is None:
            data = self.head.data
            self.head = None
            return data
        # Otherwise, unlink the last node from the second-to-last one
        second_last = self.head
        while second_last.next.next:
            second_last = second_last.next
        data = second_last.next.data
        second_last.next = None
        return data

    def delete_from_position(self, position):
        """Delete the node at position and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        if position < 0:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        # Position 0 removes the head
        if position == 0:
            return self.delete_from_beginning()
        current = self.head
        # Walk to the node before the position, stopping if the list ends two or more positions early
        for _ in range(position - 1):
            if current.next is None:
                raise OutOfBoundsError(f"Position {position} is out of bounds.")
            current = current.next
        # Stop if the position is right after the last node
        if current.next is None:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        data = current.next.data
        current.next = current.next.next
        return data


# ---------------------------------------------------------------------------
# Doubly Linked List
# ---------------------------------------------------------------------------

class DLLNode:
    """Node of a doubly linked list."""

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList(LinkedList):
    """Doubly linked list that accepts items of any type."""

    def insert_at_beginning(self, data):
        """Insert a new node before the head."""
        new_node = DLLNode(data)
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node

    def insert_at_end(self, data):
        """Insert a new node after the last node."""
        new_node = DLLNode(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last

    def insert_at_position(self, position, data):
        """Insert a new node so it ends up at position (0 up to the list length)."""
        if position < 0:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        if position == 0:
            self.insert_at_beginning(data)
            return
        current = self.head
        # Walk to the node currently at the position, stopping if the list ends too early
        for _ in range(position):
            if current is None:
                raise OutOfBoundsError(f"Position {position} is out of bounds.")
            current = current.next
        # The position right after the last node is handled by insert_at_end()
        if current is None:
            self.insert_at_end(data)
            return
        new_node = DLLNode(data)
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node

    def delete_from_beginning(self):
        """Delete the head node and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        data = self.head.data
        self.head = self.head.next
        if self.head is not None:
            self.head.prev = None
        return data

    def delete_from_end(self):
        """Delete the last node and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        if self.head.next is None:
            data = self.head.data
            self.head = None
            return data
        last = self.head
        while last.next:
            last = last.next
        last.prev.next = None
        return last.data

    def delete_from_position(self, position):
        """Delete the node at position and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        if position < 0:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        current = self.head
        for _ in range(position):
            current = current.next
            if current is None:
                raise OutOfBoundsError(f"Position {position} is out of bounds.")
        if current.next:
            current.next.prev = current.prev
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        return current.data

    def backward(self):
        """Return the items from tail to head, following the prev links."""
        current = self.head
        if current is None:
            return []
        # Move to the last node first, then follow the prev links back
        while current.next:
            current = current.next
        items = []
        while current:
            items.append(current.data)
            current = current.prev
        return items
