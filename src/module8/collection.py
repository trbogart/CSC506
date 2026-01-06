from abc import ABC, abstractmethod
from typing import Iterable


# Base class for collections in this module.

class ICollection[T](ABC):
    """
    Abstract base class for collections.
    """

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
    def __repr__(self) -> str:
        """Returns a string representation of the collection"""
        pass
