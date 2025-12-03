from abc import ABC, abstractmethod
from typing import Iterable


class ICollection[T](ABC):
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

    def __contains__(self, value: T):
        """Returns true if the value is in the collection"""
        return any(element == value for element in self)
