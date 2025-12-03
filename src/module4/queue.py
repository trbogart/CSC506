from abc import abstractmethod

from module4.collection import ICollection, ListBasedCollection


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
class Queue[T](ListBasedCollection[T], IQueue[T]):
    """Simple list-based queue"""

    # Implement IQueue methods
    def enqueue(self, value: T) -> None:
        self.list.append(value)

    def dequeue(self) -> T:
        return self.list.pop(0)

    def front(self) -> T:
        return self.list[0]
