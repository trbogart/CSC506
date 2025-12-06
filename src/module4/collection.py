from abc import ABC, abstractmethod
from typing import Iterable, Iterator


class ICollection[T](ABC):
    """
    Abstract base class for collections.
    """

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Returns true if this collection is empty
        """
        pass

    @abstractmethod
    def search(self, value: T) -> int:
        """Returns index of value, or raises ValueError if not in collection"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clears the collection"""
        pass

    @abstractmethod
    def __iter__(self) -> Iterable[T]:
        """Iterate over values in collection"""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Returns the length of the collection"""
        pass

    @abstractmethod
    def __contains__(self, value: T) -> bool:
        """Returns true if the value is in the collection"""
        pass

    @abstractmethod
    def __getitem__(self, int: int) -> T:
        """Returns the value at the given index, or raised IndexError if invalid"""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Returns a string representation of the collection"""
        pass

    @abstractmethod
    def reversed(self) -> Iterator[T]:
        """Iterate over values in reversed order"""
        pass


class ListBasedCollection[T](ICollection[T]):
    """
    Base class for collections that are built on a Python list.
    """

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
