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


def test_resize_rear(deque):
    # add to rear enough times to resize if circular buffer
    expected = []
    for i in range(20):
        deque.add_rear(i)
        expected = [value for value in range(i + 1)]
        verify_collection(deque, *expected)


def test_resize_front(deque):
    # add to front enough times to resize if circular buffer
    for i in range(20):
        deque.add_front(i)
        expected = [value for value in range(i, -1, -1)]
        verify_collection(deque, *expected)


def test_resize_both_directions(deque):
    # add to both front and rear, enough times to resize if circular buffer
    deque.add_front(1)
    verify_collection(deque, 1)
    deque.add_rear(2)
    verify_collection(deque, 1, 2)
    deque.add_front(3)
    verify_collection(deque, 3, 1, 2)
    deque.add_rear(4)
    verify_collection(deque, 3, 1, 2, 4)
    deque.add_front(5)
    verify_collection(deque, 5, 3, 1, 2, 4)
    deque.add_rear(6)
    verify_collection(deque, 5, 3, 1, 2, 4, 6)
    deque.add_front(7)
    verify_collection(deque, 7, 5, 3, 1, 2, 4, 6)
    deque.add_rear(8)
    verify_collection(deque, 7, 5, 3, 1, 2, 4, 6, 8)
    deque.add_front(9)
    verify_collection(deque, 9, 7, 5, 3, 1, 2, 4, 6, 8)
    deque.add_rear(10)
    verify_collection(deque, 9, 7, 5, 3, 1, 2, 4, 6, 8, 10)
    deque.add_front(0)
    verify_collection(deque, 0, 9, 7, 5, 3, 1, 2, 4, 6, 8, 10)


def test_add_front_remove_rear_only(deque):
    deque.add_front(1)
    assert deque.remove_rear() == 1
    verify_collection(deque)


def test_add_front_remove_rear(deque):
    deque.add_front(1)
    for i in range(2, 10):
        deque.add_front(i)
        assert deque.remove_rear() == i - 1
        verify_collection(deque, i)


def test_add_rear_remove_front_only(deque):
    deque.add_rear(1)
    assert deque.remove_front() == 1
    verify_collection(deque)


def test_add_rear_remove_front(deque):
    deque.add_rear(1)
    for i in range(2, 10):
        deque.add_rear(i)
        assert deque.remove_front() == i - 1
        verify_collection(deque, i)


def test_clear(deque):
    deque.add_rear(1)
    deque.add_rear(2)
    deque.clear()
    verify_collection(deque)
