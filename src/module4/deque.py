from abc import abstractmethod
from typing import Iterator

from module4.collection import ICollection


class IDeque[T](ICollection[T]):
    """
    Abstract base class for deque (double-ended queue) implementations.
    """

    @abstractmethod
    def add_rear(self, value: T) -> None:
        """Adds an element to the deque"""
        pass

    @abstractmethod
    def add_front(self, value: T) -> None:
        """Adds an element to the deque"""
        pass

    @abstractmethod
    def get_front(self) -> T:
        """Returns the element at the front of the deque."""
        pass

    @abstractmethod
    def get_rear(self) -> T:
        """Returns the element at the rear of the deque."""
        pass

    @abstractmethod
    def remove_front(self) -> T:
        """Removes and returns the most recently element from the deque"""
        pass

    @abstractmethod
    def remove_rear(self) -> T:
        """Removes and returns the most recently element from the deque"""
        pass


class Deque[T](IDeque[T]):
    """
    Deque implemented using a circular buffer.
    """

    # Implement ICollection methods
    def __init__(self, capacity: int = 5):
        self.buffer: list[T] = [None] * capacity
        self.start_index = 0
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[T]:
        for i in range(self.size):
            yield self.buffer[self._buffer_index(i)]

    def __contains__(self, value: T) -> bool:
        return value in iter(self)

    def __repr__(self) -> str:
        return f'[{', '.join(map(lambda x: repr(x), iter(self)))}]'

    def __getitem__(self, index: int) -> T:
        return self.buffer[self._buffer_index(index)]

    def reversed(self) -> Iterator[T]:
        for i in range(self.size - 1, -1, -1):
            yield self.buffer[self._buffer_index(i)]

    def is_empty(self) -> bool:
        return self.size == 0

    def search(self, value: T) -> int:
        for i, element in enumerate(iter(self)):
            if element == value:
                return i
        raise ValueError(f'element {value} not in list')

    def clear(self) -> None:
        self.buffer.clear()
        self.size = 0
        self.start_index = 0

    # Implement IDeque methods
    def add_rear(self, value: T) -> None:
        self._maybe_resize_buffer()
        self.size += 1
        self.buffer[self._end_index()] = value

    def add_front(self, value: T) -> None:
        self._maybe_resize_buffer()
        self.size += 1
        if self.start_index > 0:
            self.start_index -= 1
        else:
            self.start_index = len(self.buffer) - 1
        self.buffer[self.start_index] = value

    def get_front(self) -> T:
        return self.buffer[self._buffer_index(0)]

    def get_rear(self) -> T:
        return self.buffer[self._buffer_index(self.size - 1)]

    def remove_front(self) -> T:
        value = self.get_front()
        self.start_index = (self.start_index + 1) % len(self.buffer)
        self.size -= 1
        return value

    def remove_rear(self) -> T:
        value = self.get_rear()
        self.size -= 1
        return value

    def _buffer_index(self, i):
        if 0 <= i < self.size:
            return (self.start_index + i) % len(self.buffer)
        raise IndexError('Index out of range')

    def _end_index(self):
        return self._buffer_index(self.size - 1)

    def _maybe_resize_buffer(self) -> None:
        if self.size == len(self.buffer):
            new_buffer = [None] * len(self.buffer) * 2
            for i in range(self.size):
                new_buffer[i] = self.buffer[self._buffer_index(i)]
            self.start_index = 0
            self.buffer = new_buffer
