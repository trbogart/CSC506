import pytest

from module4.linked_list import LinkedList
from module4.stack import IStack, Stack
from module4.test_collection import verify_collection


@pytest.fixture(params=[Stack, LinkedList])
def stack(request) -> IStack:
    # Instantiate the implementation and return it
    return request.param()

def test_empty(stack):
    verify_collection(stack)

def test_push(stack):
    stack.push(1)
    verify_collection(stack, 1)
    stack.push(3)
    verify_collection(stack, 1, 3)
    stack.push(2)
    verify_collection(stack, 1, 3, 2)

def test_pop(stack):
    stack.push(1)
    stack.push(2)
    stack.push(3)
    verify_collection(stack, 1, 2, 3)

    assert stack.pop() == 3
    verify_collection(stack, 1, 2)
    assert stack.pop() == 2
    verify_collection(stack, 1)
    assert stack.pop() == 1
    verify_collection(stack)

    with pytest.raises(IndexError):
        stack.pop()

def test_peek(stack):
    with pytest.raises(IndexError):
        stack.peek()

    stack.push(1)
    assert stack.peek() == 1

    stack.push(2)
    assert stack.peek() == 2

    assert stack.pop() == 2
    assert stack.peek() == 1

    assert stack.pop() == 1

    with pytest.raises(IndexError):
        stack.peek()



def test_clear(stack):
    stack.push(1)
    stack.push(2)
    stack.clear()
    verify_collection(stack)
