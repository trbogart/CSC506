from abc import abstractmethod
from typing import Iterator

from collection import ICollection


class IQueue[T](ICollection[T]):
    @abstractmethod
    def enqueue(self, value: T) -> None:
        """Adds an element to the stack"""
        pass

    @abstractmethod
    def dequeue(self) -> T:
        """Removes and returns the most recently element from the stack"""
        pass

    @abstractmethod
    def front(self) -> T:
        """Returns the most recently add element from the stack"""
        pass


# List-based queue
class Stack[T](IQueue[T]):
    """Simple list-based queue"""

    def __init__(self):
        self.list: list[T] = []

    # Implement ICollection methods
    def __len__(self) -> int:
        return len(self.list)

    def __iter__(self) -> Iterator[T]:
        return iter(self.list)

    def __contains__(self, value: T) -> bool:
        return value in self.list

    def __repr__(self) -> str:
        return repr(self.list)

    def is_empty(self) -> bool:
        return len(self) == 0

    def search(self, value: T) -> int:
        return self.list.index(value)

    def clear(self) -> None:
        self.list.clear()

    # Implement IQueue methods
    def enqueue(self, value: T) -> None:
        self.list.append(value)

    def dequeue(self) -> T:
        return self.list.pop()

    def front(self) -> T:
        return self.list[-1]
