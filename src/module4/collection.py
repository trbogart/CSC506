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
    def __getitem__(self, index: int) -> T:
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
