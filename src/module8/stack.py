from module8.collection import OrderedCollection


class Stack[T](OrderedCollection[T]):
    """Simple stack"""

    def __init__(self):
        self.list = []

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __contains__(self, value):
        return value in self.list

    def __repr__(self):
        return repr(self.list)

    def add_last(self, value: T):
        self.list.append(value)

    def add_first(self, value: T):
        self.list.insert(0, value)

    def remove_last(self) -> T:
        return self.list.pop()

    def remove_first(self) -> T:
        return self.list.pop(0)

    def add(self, value: T) -> bool:
        self.add_last(value)
        return True

    def remove(self, value: T) -> bool:
        try:
            self.list.remove(value)
            return True
        except ValueError:
            return False

    def push(self, value):
        """Adds an element to the stack"""
        self.list.append(value)

    def pop(self):
        """Removes and returns the most recently element from the stack"""
        return self.list.pop()

    def peek(self):
        """Returns the most recently element from the stack"""
        return self.list[-1]

    def index(self, value):
        """Returns index of value, or raises ValueError if not in list"""
        return self.list.index(value)

    def clear(self):
        """Clears the stack"""
        self.list.clear()
