from abc import abstractmethod
from typing import Iterator

from collection import ICollection


class IDequeue[T](ICollection[T]):
    @abstractmethod
    def add_rear(self, value: T) -> None:
        """Adds an element to the dequeue"""
        pass

    @abstractmethod
    def add_front(self, value: T) -> None:
        """Adds an element to the dequeue"""
        pass

    @abstractmethod
    def get_front(self) -> T:
        """Returns the element at the front of the dequeue."""
        pass

    @abstractmethod
    def get_rear(self) -> T:
        """Returns the element at the rear of the dequeue."""
        pass

    @abstractmethod
    def remove_front(self) -> T:
        """Removes and returns the most recently element from the dequeue"""
        pass

    @abstractmethod
    def remove_rear(self) -> T:
        """Removes and returns the most recently element from the dequeue"""
        pass


# List-based double-ended queue
class Dequeue[T](IDequeue[T]):
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

    # Implement IDequeue methods
    def add_rear(self, value: T) -> None:
        self.list.append(value)

    def add_front(self, value: T) -> None:
        self.list.insert(value, 0)

    def get_front(self) -> T:
        return self.list[0]

    def get_rear(self) -> T:
        return self.list[-1]

    def remove_front(self) -> T:
        return self.list.pop(0)

    def remove_rear(self) -> T:
        return self.list.pop()
