"""Fixed-capacity stack, checked against a plain list."""

import random

import pytest

from pydsa.core.errors import CapacityError, EmptyError
from pydsa.core.stack import Stack


def test_random_operations_match_a_list():
    rng = random.Random(4)
    for _ in range(200):
        capacity = rng.randint(1, 6)
        stack, model = Stack(capacity), []
        for _ in range(40):
            op = rng.choice(["push", "push", "pop", "peek"])
            if op == "push":
                item = rng.choice([rng.randint(0, 99), "Messi"])
                if len(model) == capacity:
                    with pytest.raises(CapacityError):
                        stack.push(item)
                else:
                    stack.push(item)
                    model.append(item)
            elif not model:
                with pytest.raises(EmptyError):
                    stack.pop() if op == "pop" else stack.peek()
            elif op == "pop":
                assert stack.pop() == model.pop()
            else:
                assert stack.peek() == model[-1]
            assert stack.items == model
            assert len(stack) == len(model)
            assert stack.is_empty() == (not model)
            assert stack.is_full() == (len(model) == capacity)
