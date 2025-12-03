from abc import abstractmethod

from module4.collection import ICollection, ListBasedCollection


class IDeque[T](ICollection[T]):
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


# List-based double-ended queue
class Deque[T](ListBasedCollection[T], IDeque[T]):
    """Simple list-based double-ended queue"""

    # Implement IDeque methods
    def add_rear(self, value: T) -> None:
        self.list.append(value)

    def add_front(self, value: T) -> None:
        self.list.insert(0, value)

    def get_front(self) -> T:
        return self.list[0]

    def get_rear(self) -> T:
        return self.list[-1]

    def remove_front(self) -> T:
        return self.list.pop(0)

    def remove_rear(self) -> T:
        return self.list.pop()
