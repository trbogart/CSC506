from collection_interface import CollectionInterface
from linked_list import LinkedList


class Queue:
    """Simple LIFO Queue implemented with LinkedList"""

    def __init__(self):
        self.list = LinkedList()

    def __len__(self):
        return self.list.size

    def __iter__(self):
        return iter(self.list)

    def __contains__(self, value):
        return value in self.list

    def __repr__(self):
        return repr(self.list)

    def push(self, value):
        """Adds an element to the queue"""
        self.list.add_last(value)

    def pop(self):
        """Removes and returns next element from the queue, or raises IndexError if empty"""
        return self.list.remove_first()

    def peek(self):
        """Returns next element from the queue, or raises IndexError if empty"""
        return self.list.get_first()

    def index(self, value):
        """Returns index of value, or raises ValueError if not in list"""
        return self.list.index(value)

    def clear(self):
        """Clears the queue"""
        self.list.clear()


if __name__ == '__main__':
    CollectionInterface("queue", Queue()).execute()
