import pytest

from module4.deque import IDeque, Deque
from module4.linked_list import LinkedList
from module4.test_collection import verify_collection


@pytest.fixture(params=[Deque, LinkedList])
def deque(request) -> IDeque:
    # Instantiate the implementation and return it
    return request.param()


def test_empty(deque):
    verify_collection(deque)


def test_add_front(deque):
    deque.add_front(1)
    verify_collection(deque, 1)
    deque.add_front(3)
    verify_collection(deque, 3, 1)
    deque.add_front(2)
    verify_collection(deque, 2, 3, 1)


def test_add_rear(deque):
    deque.add_rear(1)
    verify_collection(deque, 1)
    deque.add_rear(3)
    verify_collection(deque, 1, 3)
    deque.add_rear(2)
    verify_collection(deque, 1, 3, 2)


def test_remove_front(deque):
    deque.add_rear(1)
    deque.add_rear(2)
    deque.add_rear(3)
    verify_collection(deque, 1, 2, 3)

    assert deque.remove_front() == 1
    verify_collection(deque, 2, 3)
    assert deque.remove_front() == 2
    verify_collection(deque, 3)
    assert deque.remove_front() == 3
    verify_collection(deque)

    with pytest.raises(IndexError):
        deque.remove_front()


def test_remove_rear(deque):
    deque.add_rear(1)
    deque.add_rear(2)
    deque.add_rear(3)
    verify_collection(deque, 1, 2, 3)

    assert deque.remove_rear() == 3
    verify_collection(deque, 1, 2)
    assert deque.remove_rear() == 2
    verify_collection(deque, 1)
    assert deque.remove_rear() == 1
    verify_collection(deque)

    with pytest.raises(IndexError):
        deque.remove_rear()


def test_get_front(deque):
    with pytest.raises(IndexError):
        deque.get_front()

    deque.add_rear(1)
    assert deque.get_front() == 1

    deque.add_rear(2)
    assert deque.get_front() == 1

    assert deque.remove_front() == 1
    assert deque.get_front() == 2

    assert deque.remove_front() == 2

    with pytest.raises(IndexError):
        deque.get_front()


def test_get_rear(deque):
    with pytest.raises(IndexError):
        deque.get_rear()

    deque.add_rear(1)
    assert deque.get_rear() == 1

    deque.add_rear(2)
    assert deque.get_rear() == 2

    assert deque.remove_rear() == 2
    assert deque.get_rear() == 1

    assert deque.remove_rear() == 1

    with pytest.raises(IndexError):
        deque.get_rear()


def test_clear(deque):
    deque.add_rear(1)
    deque.add_rear(2)
    deque.clear()
    verify_collection(deque)
