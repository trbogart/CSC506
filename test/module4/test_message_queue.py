import pytest

from module4.linked_list import LinkedList
from module4.message_queue import MessageQueue
from module4.queue import Queue
from module4.test_collection import verify_collection


@pytest.fixture(params=[Queue, LinkedList])
def message_queue(request) -> MessageQueue:
    # Instantiate the queue implementation and use it build a message queue simulator
    return MessageQueue(request.param())


def test_message_queue(message_queue):
    verify_collection(message_queue.queue)

    message_queue.send_message('a')
    verify_collection(message_queue.queue, 'a')
    assert message_queue.value() == ''

    message_queue.send_message('b')
    verify_collection(message_queue.queue, 'a', 'b')
    assert message_queue.value() == ''

    message_queue.send_message('c')
    verify_collection(message_queue.queue, 'a', 'b', 'c')
    assert message_queue.value() == ''

    message_queue.receive_message()
    verify_collection(message_queue.queue, 'b', 'c')
    assert message_queue.value() == 'a'

    message_queue.receive_message()
    verify_collection(message_queue.queue, 'c')
    assert message_queue.value() == 'ab'

    message_queue.send_message('d')
    verify_collection(message_queue.queue, 'c', 'd')
    assert message_queue.value() == 'ab'

    message_queue.receive_message()
    verify_collection(message_queue.queue, 'd')
    assert message_queue.value() == 'abc'

    message_queue.receive_message()
    verify_collection(message_queue.queue)
    assert message_queue.value() == 'abcd'
