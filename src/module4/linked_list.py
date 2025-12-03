import itertools
from typing import Iterable

from module4.dequeue import IDequeue
from module4.queue import IQueue
from module4.stack import IStack


# Doubly linked list
class LinkedList[T](IStack[T], IQueue[T], IDequeue[T]):
    """
    Doubly linked list (can function as a Stack, Queue, or Deque)
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # implement ICollection methods
    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterable[T]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next_node

    def __contains__(self, value: T) -> bool:
        return any(element == value for element in self)

    def __getitem__(self, index: int) -> T:
        return self._get_node_by_index(index).value

    def __repr__(self):
        return f'[{', '.join(map(lambda x: str(x), iter(self)))}]'

    def is_empty(self) -> bool:
        return self.size == 0

    def search(self, value: T) -> int:
        for i, element in enumerate(iter(self)):
            if element == value:
                return i
        raise ValueError(f'element {value} not in list')

    def clear(self) -> None:
        self.size = 0
        self.head = None
        self.tail = None

    # implement IDequeue methods
    def get_front(self) -> T:
        self._validate_non_empty()
        return self.head.value

    def get_rear(self) -> T:
        self._validate_non_empty()
        return self.tail.value

    def add_front(self, value: T) -> None:
        node = self.Node(value)
        node.next_node = self.head
        if self.head is not None:
            self.head.prev_node = node
        self.head = node
        if self.tail is None:
            # first element
            self.tail = node
        self.size += 1

    def add_rear(self, value: T) -> None:
        node = self.Node(value)
        node.prev_node = self.tail
        if self.tail is not None:
            self.tail.next_node = node
        self.tail = node
        if self.head is None:
            # first element
            self.head = node
        self.size += 1

    def remove_front(self) -> T:
        self._validate_non_empty()
        return self._remove_node(self.head)

    def remove_rear(self) -> T:
        self._validate_non_empty()
        return self._remove_node(self.tail)

    # Implement IStack methods
    def push(self, value: T) -> None:
        self.add_rear(value)

    def pop(self) -> T:
        return self.remove_rear()

    def peek(self) -> T:
        return self.get_rear()

    # Implement IQueue methods
    def enqueue(self, value: T) -> None:
        self.add_rear(value)

    def dequeue(self) -> T:
        return self.remove_front()

    def front(self) -> T:
        return self.get_front()

    class Node:
        """Internal data structure representing a linked list node"""

        def __init__(self, value: T):
            self.value = value
            self.prev_node = None
            self.next_node = None

    def _validate_non_empty(self) -> None:
        """Raises an IndexError if the list is empty"""
        if self.size == 0:
            raise IndexError('List is empty')

    def _iter_nodes(self) -> Iterable[Node]:
        """Iterate over nodes"""
        node = self.head
        while node is not None:
            yield node
            node = node.next_node

    def _get_node_by_index(self, index: int) -> Node:
        """Internal method to return the node at the given index, or raise an IndexError if out of range"""
        if index < 0 or index >= len(self):
            raise IndexError('Index out of range')
        return next(itertools.islice(self._iter_nodes(), index, None))

    def _get_node_by_value(self, value: T) -> Node:
        """Internal method to return the first node with the given value, or raise a ValueError if absent"""
        node_iter = filter(lambda next_node: next_node.value == value, self._iter_nodes())
        node = next(node_iter, None)
        if node is None:
            raise ValueError(f'element {value} not in list')
        return node

    def _remove_node(self, node: Node) -> T:
        if node.prev_node is None:
            # removing head
            self.head = node.next_node
        else:
            node.prev_node.next_node = node.next_node
        if node.next_node is None:
            # removing tail
            self.tail = node.prev_node
        else:
            node.next_node.prev_node = node.prev_node
        self.size -= 1
        return node.value
