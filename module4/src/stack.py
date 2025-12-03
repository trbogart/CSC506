from abc import abstractmethod
from typing import Iterable

from collection import ICollection


class IStack[T](ICollection[T]):
    @abstractmethod
    def push(self, value: T) -> None:
        """Adds an element to the stack"""
        pass

    @abstractmethod
    def pop(self) -> T:
        """Removes and returns the most recently element from the stack"""
        pass

    @abstractmethod
    def peek(self) -> T:
        """Returns the most recently element from the stack"""
        pass


# List-based stack (slightly modified from module 1)
class Stack[T](IStack[T]):
    """Simple list-based stack"""

    def __init__(self):
        self.list = []

    # Implement ICollection methods
    def __len__(self) -> int:
        return len(self.list)

    def __iter__(self) -> Iterable[T]:
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

    def push(self, value: T) -> None:
        """Adds an element to the stack"""
        self.list.append(value)

    def pop(self) -> T:
        """Removes and returns the most recently element from the stack"""
        return self.list.pop()

    def peek(self) -> T:
        """Returns the most recently element from the stack"""
        return self.list[-1]
