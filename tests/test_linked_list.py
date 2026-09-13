"""Singly and doubly linked lists, checked against a plain list."""

import random

import pytest

from pydsa.core.errors import EmptyError, OutOfBoundsError
from pydsa.core.linked_list import DoublyLinkedList, SinglyLinkedList


def backward_links(dll):
    """Walk to the tail through next links, then back to the head through prev links."""
    node = dll.head
    if node is None:
        return []
    assert node.prev is None
    while node.next:
        node = node.next
    items = []
    while node:
        items.append(node.data)
        node = node.prev
    return items


@pytest.mark.parametrize("list_class", [SinglyLinkedList, DoublyLinkedList], ids=lambda cls: cls.__name__)
def test_random_operations_match_a_list(list_class):
    rng = random.Random(6)
    for _ in range(300):
        linked_list, model = list_class(), []
        for _ in range(40):
            op = rng.choice(["begin", "end", "pos", "del_begin", "del_end", "del_pos", "search"])
            value = rng.randint(0, 20)
            if op == "begin":
                linked_list.insert_at_beginning(value)
                model.insert(0, value)
            elif op == "end":
                linked_list.insert_at_end(value)
                model.append(value)
            elif op == "pos":
                position = rng.randint(-2, len(model) + 2)
                if 0 <= position <= len(model):
                    linked_list.insert_at_position(position, value)
                    model.insert(position, value)
                else:
                    with pytest.raises(OutOfBoundsError):
                        linked_list.insert_at_position(position, value)
            elif op == "search":
                assert linked_list.search(value) == (model.index(value) if value in model else -1)
            elif not model:
                method = {"del_begin": linked_list.delete_from_beginning, "del_end": linked_list.delete_from_end}.get(op)
                with pytest.raises(EmptyError):
                    method() if method else linked_list.delete_from_position(0)
            elif op == "del_begin":
                assert linked_list.delete_from_beginning() == model.pop(0)
            elif op == "del_end":
                assert linked_list.delete_from_end() == model.pop()
            else:
                position = rng.randint(-2, len(model) + 2)
                if 0 <= position < len(model):
                    assert linked_list.delete_from_position(position) == model.pop(position)
                else:
                    with pytest.raises(OutOfBoundsError):
                        linked_list.delete_from_position(position)

            assert list(linked_list) == model
            assert len(linked_list) == len(model)
            if list_class is DoublyLinkedList:
                assert backward_links(linked_list) == model[::-1]
                assert linked_list.backward() == model[::-1]


def test_mixed_types():
    sll = SinglyLinkedList()
    sll.insert_at_end("abc")
    sll.insert_at_end(7)
    sll.insert_at_end(2.5)
    assert sll.search(7) == 1
    assert sll.search("7") == -1
