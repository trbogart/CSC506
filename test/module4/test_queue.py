import pytest

from module4.linked_list import LinkedList
from module4.queue import IQueue, Queue
from module4.test_collection import verify_collection


@pytest.fixture(params=[Queue, LinkedList])
def queue(request) -> IQueue:
    # Instantiate the implementation and return it
    return request.param()

def test_empty(queue):
    verify_collection(queue)

def test_enqueue(queue):
    queue.enqueue(1)
    verify_collection(queue, 1)
    queue.enqueue(3)
    verify_collection(queue, 1, 3)
    queue.enqueue(2)
    verify_collection(queue, 1, 3, 2)

def test_dequeue(queue):
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    verify_collection(queue, 1, 2, 3)

    assert queue.dequeue() == 1
    verify_collection(queue, 2, 3)
    assert queue.dequeue() == 2
    verify_collection(queue, 3)
    assert queue.dequeue() == 3
    verify_collection(queue)

    with pytest.raises(IndexError):
        queue.dequeue()

def test_front(queue):
    with pytest.raises(IndexError):
        queue.front()

    queue.enqueue(1)
    assert queue.front() == 1

    queue.enqueue(2)
    assert queue.front() == 1

    assert queue.dequeue() == 1
    assert queue.front() == 2

    assert queue.dequeue() == 2

    with pytest.raises(IndexError):
        queue.front()



def test_clear(queue):
    queue.enqueue(1)
    queue.enqueue(1)
    queue.clear()
    verify_collection(queue)
