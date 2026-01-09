from module6.binary_search_tree import BinarySearchTree


class TreeMap:
    class Entry:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value

        def __str__(self):
            return f'{self.key}:{self.value}'

        def __gt__(self, other):
            return self.key > other.value

        def __lt__(self, other):
            return self.key < other.value

        def __eq__(self, other):
            return self.key == other.value

    def __init__(self):
        self.bst = BinarySearchTree()

    def __len__(self):
        return len(self.bst)

    def __contains__(self, key):
        return self.Entry(key) in self.bst

    def __getitem__(self, key):
        entry = self.bst.search(self.Entry(key))
        if entry is None:
            raise KeyError(key)
        return entry.value

    def __delitem__(self, key):
        entry = self.bst.remove(self.Entry(key))
        if entry is None:
            raise KeyError(key)

    def __setitem__(self, key, value):
        self.bst.insert(self.Entry(key, value), replace=True)

    def __str__(self):
        return str(self.bst)

    def items(self):
        for entry in self.bst:
            yield entry.value, entry.value

    def keys(self):
        for entry in self.bst:
            yield entry.value

    def clear(self):
        self.bst.clear()
