from abc import ABC, abstractmethod
from typing import Iterable


class Collection[T](ABC, Iterable[T]):
    """
    Abstract base class for collections.
    """

    @abstractmethod
    def __len__(self) -> int:
        """Returns the length of the collection"""
        pass

    @abstractmethod
    def __contains__(self, value: T) -> bool:
        """Returns true if the value is in the collection"""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Returns a string representation of the collection"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Removes all items.
        """
        pass

    @abstractmethod
    def add(self, value: T) -> bool:
        """
        Adds a value.
        :param value: value to add
        :return: true if value was added
        """
        pass

    @abstractmethod
    def remove(self, value: T) -> bool:
        """
        Removes a value.
        :param value: value to remove
        :return: true if value was removed
        """
        pass
