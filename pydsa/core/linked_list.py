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


# ---------------------------------------------------------------------------
# Circular linked lists
# ---------------------------------------------------------------------------

class CircularLinkedList(LinkedList):
    """Behavior shared by both circular lists, where the tail links back to the head."""

    def __iter__(self):
        """Yield the items from head to tail, stopping once the loop comes back around to the head."""
        if self.head is None:
            return
        current = self.head
        while True:
            yield current.data
            current = current.next
            if current is self.head:
                return

    def _node_at(self, position):
        """Return the node at position, counting from the head."""
        current = self.head
        for _ in range(position):
            current = current.next
        return current

    def _walk(self, start, steps, link):
        """Return the items of steps nodes, starting at start and following the given link attribute."""
        if steps < 0:
            raise ValueError("The number of steps can't be negative.")
        items = []
        current = start
        if current is None:
            return items
        for _ in range(steps):
            items.append(current.data)
            current = getattr(current, link)
        return items

    def walk(self, steps):
        """Return the items of the first steps nodes visited from the head, going around the loop as often as needed."""
        return self._walk(self.head, steps, "next")


class SinglyCircularLinkedList(CircularLinkedList):
    """Singly circular linked list that accepts items of any type.

    It keeps references to both the head and the tail, whose next link points back to the head.
    """

    def __init__(self):
        super().__init__()
        self.tail = None

    def insert_at_beginning(self, data):
        """Insert a new node before the head."""
        new_node = SLLNode(data)
        if self.head is None:
            new_node.next = new_node
            self.head = self.tail = new_node
            return
        new_node.next = self.head
        self.tail.next = new_node
        self.head = new_node

    def insert_at_end(self, data):
        """Insert a new node after the tail."""
        self.insert_at_beginning(data)
        # The new head sits right after the tail, so moving both references one step makes it the new tail instead
        self.tail = self.head
        self.head = self.head.next

    def insert_at_position(self, position, data):
        """Insert a new node so it ends up at position (0 up to the list length)."""
        length = len(self)
        if not 0 <= position <= length:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        if position == 0:
            self.insert_at_beginning(data)
        elif position == length:
            self.insert_at_end(data)
        else:
            previous = self._node_at(position - 1)
            new_node = SLLNode(data)
            new_node.next = previous.next
            previous.next = new_node

    def delete_from_beginning(self):
        """Delete the head node and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        data = self.head.data
        if self.head is self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.tail.next = self.head
        return data

    def delete_from_end(self):
        """Delete the tail node and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        data = self.tail.data
        if self.head is self.tail:
            self.head = self.tail = None
            return data
        # Without prev links, the node before the tail can only be found by walking from the head
        previous = self.head
        while previous.next is not self.tail:
            previous = previous.next
        previous.next = self.head
        self.tail = previous
        return data

    def delete_from_position(self, position):
        """Delete the node at position and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        length = len(self)
        if not 0 <= position < length:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        if position == 0:
            return self.delete_from_beginning()
        if position == length - 1:
            return self.delete_from_end()
        previous = self._node_at(position - 1)
        target = previous.next
        previous.next = target.next
        return target.data


class DoublyCircularLinkedList(CircularLinkedList):
    """Doubly circular linked list that accepts items of any type; the head's prev link is the tail."""

    def insert_at_end(self, data):
        """Insert a new node between the tail and the head."""
        new_node = DLLNode(data)
        if self.head is None:
            new_node.prev = new_node.next = new_node
            self.head = new_node
            return
        tail = self.head.prev
        new_node.prev = tail
        new_node.next = self.head
        tail.next = new_node
        self.head.prev = new_node

    def insert_at_beginning(self, data):
        """Insert a new node before the head."""
        self.insert_at_end(data)
        # The new node already sits between the tail and the head, so it only has to become the head
        self.head = self.head.prev

    def insert_at_position(self, position, data):
        """Insert a new node so it ends up at position (0 up to the list length)."""
        length = len(self)
        if not 0 <= position <= length:
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        if position == 0:
            self.insert_at_beginning(data)
        elif position == length:
            self.insert_at_end(data)
        else:
            current = self._node_at(position)
            new_node = DLLNode(data)
            new_node.prev = current.prev
            new_node.next = current
            current.prev.next = new_node
            current.prev = new_node

    def _unlink(self, node):
        """Remove node from the loop and return its item."""
        if node.next is node:
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if node is self.head:
                self.head = node.next
        return node.data

    def delete_from_beginning(self):
        """Delete the head node and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        return self._unlink(self.head)

    def delete_from_end(self):
        """Delete the tail node and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        return self._unlink(self.head.prev)

    def delete_from_position(self, position):
        """Delete the node at position and return its item."""
        if self.head is None:
            raise EmptyError("List is empty.")
        if not 0 <= position < len(self):
            raise OutOfBoundsError(f"Position {position} is out of bounds.")
        return self._unlink(self._node_at(position))

    def backward(self):
        """Return the items from tail to head, following the prev links."""
        if self.head is None:
            return []
        return self._walk(self.head.prev, len(self), "prev")

    def walk(self, steps, backward=False):
        """Return the items of the first steps nodes visited around the loop.

        The walk starts at the head and follows the next links, or starts at the tail and follows the
        prev links if backward is True.
        """
        if backward:
            return self._walk(self.head.prev if self.head else None, steps, "prev")
        return self._walk(self.head, steps, "next")
