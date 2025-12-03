import pytest

from base_collection_test import verify_collection
from module4.linked_list import LinkedList
from module4.dequeue import IDequeue, Dequeue


@pytest.fixture(params=[Dequeue, LinkedList])
def dequeue(request) -> IDequeue:
    # Instantiate the implementation and return it
    return request.param()

def test_empty(dequeue):
    verify_collection(dequeue)

def test_add_front(dequeue):
    dequeue.add_front(1)
    verify_collection(dequeue, 1)
    dequeue.add_front(3)
    verify_collection(dequeue, 3, 1)
    dequeue.add_front(2)
    verify_collection(dequeue, 2, 3, 1)

def test_add_rear(dequeue):
    dequeue.add_rear(1)
    verify_collection(dequeue, 1)
    dequeue.add_rear(3)
    verify_collection(dequeue, 1, 3)
    dequeue.add_rear(2)
    verify_collection(dequeue, 1, 3, 2)

def test_remove_front(dequeue):
    dequeue.add_rear(1)
    dequeue.add_rear(2)
    dequeue.add_rear(3)
    verify_collection(dequeue, 1, 2, 3)

    assert dequeue.remove_front() == 1
    verify_collection(dequeue, 2, 3)
    assert dequeue.remove_front() == 2
    verify_collection(dequeue, 3)
    assert dequeue.remove_front() == 3
    verify_collection(dequeue)

    with pytest.raises(IndexError):
        dequeue.remove_front()

def test_remove_rear(dequeue):
    dequeue.add_rear(1)
    dequeue.add_rear(2)
    dequeue.add_rear(3)
    verify_collection(dequeue, 1, 2, 3)

    assert dequeue.remove_rear() == 3
    verify_collection(dequeue, 1, 2)
    assert dequeue.remove_rear() == 2
    verify_collection(dequeue, 1)
    assert dequeue.remove_rear() == 1
    verify_collection(dequeue)

    with pytest.raises(IndexError):
        dequeue.remove_rear()

def test_get_front(dequeue):
    with pytest.raises(IndexError):
        dequeue.get_front()

    dequeue.add_rear(1)
    assert dequeue.get_front() == 1

    dequeue.add_rear(2)
    assert dequeue.get_front() == 1

    assert dequeue.remove_front() == 1
    assert dequeue.get_front() == 2

    assert dequeue.remove_front() == 2

    with pytest.raises(IndexError):
        dequeue.get_front()


def test_get_rear(dequeue):
    with pytest.raises(IndexError):
        dequeue.get_rear()

    dequeue.add_rear(1)
    assert dequeue.get_rear() == 1

    dequeue.add_rear(2)
    assert dequeue.get_rear() == 2

    assert dequeue.remove_rear() == 2
    assert dequeue.get_rear() == 1

    assert dequeue.remove_rear() == 1

    with pytest.raises(IndexError):
        dequeue.get_rear()

def test_clear(dequeue):
    dequeue.add_rear(1)
    dequeue.add_rear(2)
    dequeue.clear()
    verify_collection(dequeue)
