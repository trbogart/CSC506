from abc import abstractmethod
from typing import Iterator, Iterable

from module4.collection import ICollection
from module4.deque import Deque


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
class Queue[T](IQueue[T]):
    """
    Queue implemented using a circular buffer.
    """

    def __init__(self, capacity: int = 5):
        self.deque = Deque(capacity)

    # Implement ICollection methods (delegate to deque)
    def is_empty(self) -> bool:
        return self.deque.is_empty()

    def search(self, value: T) -> int:
        return self.deque.search(value)

    def clear(self) -> None:
        self.deque.clear()

    def __iter__(self) -> Iterable[T]:
        return iter(self.deque)

    def __len__(self) -> int:
        return len(self.deque)

    def __contains__(self, value: T) -> bool:
        return value in self.deque

    def __getitem__(self, index: int) -> T:
        return self.deque[index]

    def __repr__(self) -> str:
        return repr(self.deque)

    def reversed(self) -> Iterator[T]:
        return self.deque.reversed()

    # Implement IQueue methods
    def enqueue(self, value: T) -> None:
        self.deque.add_rear(value)

    def dequeue(self) -> T:
        return self.deque.remove_front()

    def front(self) -> T:
        return self.deque.get_front()
