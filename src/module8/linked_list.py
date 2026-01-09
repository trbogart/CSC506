import itertools
from typing import Iterator, Optional

from module8.collection import OrderedCollection


# Doubly linked list.
class LinkedList[T](OrderedCollection[T]):
    """Doubly linked list"""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[T]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next_node

    def __contains__(self, value: T) -> bool:
        return any(element == value for element in self)

    def __repr__(self) -> str:
        return f'[{', '.join(map(lambda x: repr(x), iter(self)))}]'

    def get_first(self):
        """Returns the first element, or raise IndexError if index invalid"""
        self._validate_non_empty()
        return self.head.value

    def get_last(self):
        """Returns the last element, or raise IndexError if index invalid"""
        self._validate_non_empty()
        return self.tail.value

    def get(self, index):
        """Returns the element with the given index, or raise IndexError if index invalid"""
        return self._get_node_by_index(index).value

    def add_first(self, value):
        """Add element to front of list"""
        node = self.Node(value, next_node=self.head)
        if self.head is not None:
            self.head.prev_node = node
        self.head = node
        if self.tail is None:
            # first element
            self.tail = node
        self.size += 1

    def add(self, value: T) -> bool:
        """Add element to end of list and returns true."""
        self.add_last(value)
        return True

    def add_last(self, value: T):
        """Add element to end of list."""
        node = self.Node(value, prev_node=self.tail)
        if self.tail is not None:
            self.tail.next_node = node
        self.tail = node
        if self.head is None:
            # first element
            self.head = node
        self.size += 1

    def remove_first(self):
        """Remove and return first element, or raise IndexError if empty"""
        self._validate_non_empty()
        return self._remove_node(self.head)

    def remove_last(self):
        """Remove and return last element, or raise IndexError if empty"""
        self._validate_non_empty()
        return self._remove_node(self.tail)

    def remove_next(self) -> T:
        """Remove and return last element, or raise IndexError if empty"""
        return self.remove_last()

    def remove(self, value: T) -> bool:
        """Remove given element. Returns true if removed, or false if not in list."""
        node = self._get_node_by_value(value, required=False)
        if node is None:
            return False
        self._remove_node(self._get_node_by_value(value))
        return True

    def pop(self, index: Optional[int] = None):
        """Remove and return the element with the given index, or raise IndexError if index invalid"""
        if index is None:
            return self.remove_last()
        return self._remove_node(self._get_node_by_index(index))

    def push(self, value):
        """Add element to end of list (same as add_last)"""
        self.add_last(value)

    def peek(self):
        """Returns the last element, or raise IndexError if index invalid (synonym for get_first)"""
        return self.get_last()

    def index(self, value):
        """Returns index of value, or raises ValueError if not in list"""
        for i, element in enumerate(self):
            if element == value:
                return i
        raise ValueError(f'element {value} not in list')

    def iter_reverse(self):
        """Iterate values in reverse order, for testing"""
        node = self.tail
        while node is not None:
            yield node.value
            node = node.prev_node

    def clear(self):
        """Clears the queue"""
        self.size = 0
        self.head = None
        self.tail = None

    def _validate_non_empty(self):
        """Raises an IndexError if the list is empty"""
        if self.size == 0:
            raise IndexError('List is empty')

    def _iter_nodes(self):
        """Iterate over nodes"""
        node = self.head
        while node is not None:
            yield node
            node = node.next_node

    def _get_node_by_index(self, index: int):
        """Internal method to return the node at the given index, or raise an IndexError if out of range"""
        if index < 0 or index >= len(self):
            raise IndexError('Index out of range')
        return next(itertools.islice(self._iter_nodes(), index, None))

    def _get_node_by_value(self, value: T, required: bool = True):
        """Internal method to return the first node with the given value, or raise a ValueError if absent"""
        node_iter = filter(lambda next_node: next_node.value == value, self._iter_nodes())
        node = next(node_iter, None)
        if required and node is None:
            raise ValueError(f'element {value} not in list')
        return node

    def _remove_node(self, node):
        """Remove given node, which must not be None"""
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

    class Node:
        """Internal data structure representing a linked list node"""

        def __init__(self, value: T, prev_node=None, next_node=None):
            self.value = value
            self.prev_node = prev_node
            self.next_node = next_node
