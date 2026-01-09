from module8.collection import OrderedCollection
from module8.linked_list import LinkedList


class Queue[T](OrderedCollection[T]):
    """Simple FIFO Queue implemented using an internal LinkedList"""

    def __init__(self):
        self.list = LinkedList()

    def __len__(self):
        return self.list.size

    def __iter__(self):
        return iter(self.list)

    def __contains__(self, value: T):
        return value in self.list

    def __repr__(self):
        return repr(self.list)

    def push(self, value: T):
        """Adds an element to the queue"""
        self.list.add_last(value)

    def pop(self):
        """Removes and returns next element from the queue, or raises IndexError if empty"""
        return self.list.remove_first()

    def peek(self):
        """Returns next element from the queue, or raises IndexError if empty"""
        return self.list.get_first()

    def index(self, value: T):
        """Returns index of value, or raises ValueError if not in list"""
        return self.list.index(value)

    def clear(self):
        """Clears the queue"""
        self.list.clear()

    def add_last(self, value: T):
        self.list.add_last(value)

    def add_first(self, value: T):
        self.list.add_first(value)

    def remove_last(self) -> T:
        return self.list.remove_last()

    def remove_first(self) -> T:
        return self.list.remove_first()

    def add(self, value: T) -> bool:
        return self.list.add(value)

    def remove(self, value: T) -> bool:
        return self.list.remove(value)
