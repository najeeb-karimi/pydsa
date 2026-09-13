"""Singly, doubly and circular linked lists, checked against a plain list and by following every link."""

import random

import pytest

from pydsa.core.errors import EmptyError, OutOfBoundsError
from pydsa.core.linked_list import DoublyCircularLinkedList, DoublyLinkedList, SinglyCircularLinkedList, SinglyLinkedList

LIST_CLASSES = [SinglyLinkedList, DoublyLinkedList, SinglyCircularLinkedList, DoublyCircularLinkedList]
CIRCULAR = (SinglyCircularLinkedList, DoublyCircularLinkedList)
DOUBLY = (DoublyLinkedList, DoublyCircularLinkedList)


def check_links(linked_list, model):
    """Follow the next (and prev) links node by node and compare them with the model."""
    assert list(linked_list) == model
    assert len(linked_list) == len(model)
    if not model:
        assert linked_list.head is None
        return

    nodes = [linked_list.head]
    for _ in range(len(model) - 1):
        nodes.append(nodes[-1].next)
    assert [node.data for node in nodes] == model

    circular = isinstance(linked_list, CIRCULAR)
    # The last node links back to the head in a circular list, and to nothing otherwise
    assert nodes[-1].next is (nodes[0] if circular else None)
    if isinstance(linked_list, SinglyCircularLinkedList):
        assert linked_list.tail is nodes[-1]

    if isinstance(linked_list, DOUBLY):
        assert nodes[0].prev is (nodes[-1] if circular else None)
        assert all(nodes[i + 1].prev is nodes[i] for i in range(len(nodes) - 1))
        assert linked_list.backward() == model[::-1]


@pytest.mark.parametrize("list_class", LIST_CLASSES, ids=lambda cls: cls.__name__)
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

            check_links(linked_list, model)


@pytest.mark.parametrize("list_class", CIRCULAR, ids=lambda cls: cls.__name__)
def test_walk_goes_around_the_loop(list_class):
    linked_list = list_class()
    for item in "abc":
        linked_list.insert_at_end(item)
    assert linked_list.walk(7) == list("abcabca")
    assert linked_list.walk(0) == []
    assert list_class().walk(3) == []
    with pytest.raises(ValueError):
        linked_list.walk(-1)


def test_doubly_circular_walks_backward_from_the_tail():
    linked_list = DoublyCircularLinkedList()
    for item in "abc":
        linked_list.insert_at_end(item)
    assert linked_list.walk(4, backward=True) == list("cbac")


def test_mixed_types():
    sll = SinglyLinkedList()
    sll.insert_at_end("abc")
    sll.insert_at_end(7)
    sll.insert_at_end(2.5)
    assert sll.search(7) == 1
    assert sll.search("7") == -1
