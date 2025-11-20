import bisect
import sys

from collection_interface import CollectionInterface


class SortedList:
    def __init__(self):
        self.list = []

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __contains__(self, value):
        return self.list[bisect.bisect_left(self.list, value)] == value

    def __repr__(self):
        return repr(self.list)

    def push(self, value):
        """Adds an element to the stack"""
        bisect.insort_right(self.list, value)

    def pop(self):
        """Removes and returns the largest element from the stack"""
        return self.list.pop()

    def peek(self):
        """Returns the most recently element from the stack"""
        return self.list[-1]

    def index(self, value):
        """Returns index of value, or raises ValueError if not in list"""
        index = bisect.bisect_left(self.list, value)
        if self.list[index] != value:
            raise ValueError("Element not found")
        return index

    def clear(self):
        """Clears the stack"""
        self.list.clear()

    def get_estimated_space(self):
        """
        Helper method to get the estimated space consumed by this list. Includes the size of this object,
        the list itself, and sum of the size of all values
        """
        return sys.getsizeof(self) + sys.getsizeof(self.list) + sum(map(lambda value: sys.getsizeof(value), self))


if __name__ == '__main__':
    # run command-line interface for testing and analysis
    CollectionInterface("Sorted List", SortedList()).execute(num_runs=200_000)
