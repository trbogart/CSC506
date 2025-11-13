import pytest

from stack import Stack

value1 = "value1"
value2 = "value2"
value3 = "value3"

def test_empty():
    stack = Stack()
    _verify_elements(stack)

def test_push():
    stack = Stack()
    stack.push(value1)
    _verify_elements(stack, value1)
    stack.push(value2)
    _verify_elements(stack, value1, value2)

def test_peek():
    stack = Stack()

    # empty
    with pytest.raises(IndexError):
        stack.peek()
    stack.push(value1)
    assert stack.peek() == value1
    stack.push(value2)
    assert stack.peek() == value2

def test_pop():
    stack = Stack()

    # empty
    with pytest.raises(IndexError):
        stack.pop()

    stack.push(value1)

    # removes only element
    assert stack.pop() == value1
    _verify_elements(stack)

    # removes last element if multiple
    stack.push(value1)
    stack.push(value2)
    assert stack.pop() == value2
    _verify_elements(stack, value1)
    assert stack.pop() == value1
    _verify_elements(stack)

def test_index():
    stack = Stack()
    stack.push(value1)
    stack.push(value2)
    with pytest.raises(ValueError):
        stack.index("invalid")
    assert stack.index(value1) == 0
    assert stack.index(value2) == 1

def _verify_elements(stack, *expected):
    assert len(stack) == len(expected)
    expected_list = list(expected)
    assert list(iter(stack)) == expected_list
