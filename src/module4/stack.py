from abc import abstractmethod

from module4.collection import ICollection, ListBasedCollection


class IStack[T](ICollection[T]):
    @abstractmethod
    def push(self, value: T) -> None:
        """Adds an element to the end of the stack"""
        pass

    @abstractmethod
    def pop(self) -> T:
        """Removes and returns the last element from the stack"""
        pass

    @abstractmethod
    def peek(self) -> T:
        """Returns the last element from the stack"""
        pass


# List-based stack (slightly modified from module 1)
class Stack[T](ListBasedCollection[T], IStack[T]):
    """Simple list-based stack"""

    # Implement IStack methods
    def push(self, value: T) -> None:
        self.list.append(value)

    def pop(self) -> T:
        return self.list.pop()

    def peek(self) -> T:
        return self.list[-1]
