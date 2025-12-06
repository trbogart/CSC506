from abc import abstractmethod
from typing import Iterator

from module4.collection import ICollection


class IStack[T](ICollection[T]):
    """
    Abstract class for stack implementations.
    """

    @abstractmethod
    def push(self, value: T) -> None:
        """Adds an element to the end of the stack"""
        pass

    @abstractmethod
    def pop(self) -> T:
        """Removes and returns the last element from the stack"""
        pass

    @abstractmethod
    def peek(self) -> T:
        """Returns the last element from the stack"""
        pass


# List-based stack (slightly modified from module 1)
class Stack[T](IStack[T]):
    """
    Simple list-based stack.
    """

    # Implement ICollection methods
    def __init__(self):
        self.list: list[T] = []

    def __len__(self) -> int:
        return len(self.list)

    def __iter__(self) -> Iterator[T]:
        return iter(self.list)

    def __contains__(self, value: T) -> bool:
        return value in self.list

    def __repr__(self) -> str:
        return repr(self.list)

    def __getitem__(self, index: int) -> T:
        return self.list[index]

    def reversed(self) -> Iterator[T]:
        for i in range(len(self.list) - 1, -1, -1):
            yield self.list[i]

    def is_empty(self) -> bool:
        return len(self) == 0

    def search(self, value: T) -> int:
        return self.list.index(value)

    def clear(self) -> None:
        self.list.clear()

    # Implement IStack methods
    def push(self, value: T) -> None:
        self.list.append(value)

    def pop(self) -> T:
        return self.list.pop()

    def peek(self) -> T:
        return self.list[-1]
