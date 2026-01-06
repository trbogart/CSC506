from module8.hash_table import HashTable


class Set[T](HashTable[T]):
    """
    Set implemented as a chained hash table.
    """

    def __init__(self):
        super().__init__()

    def union(self, other):
        """
        Returns the union of two sets.
        :param other: Another set
        :return: new set containing all values in either set
        """
        s = Set()
        for key in self:
            s.add(key)
        for key in other:
            s.add(key)
        return s

    def intersection(self, other):
        """
        Returns the intersection of two sets.
        :param other: Another set
        :return: new set containing all values that are in both sets
        """
        s = Set()
        for key in other:
            if key in self:
                s.add(key)
        return s

    def difference(self, other):
        """
        Returns the difference of this set and another set.
        :param other: Another set
        :return: new set containing all values that are this set and not the other set
        """
        s = Set()
        for key in self:
            if key not in other:
                s.add(key)
        return s

    def symmetric_difference(self, other):
        """
        Returns the symmetric difference of two sets.
        :param other: Another set
        :return: new set containing all values that are in one set but not both sets
        """
        s = Set()
        for key in self:
            if key not in other:
                s.add(key)
        for key in other:
            if key not in self:
                s.add(key)
        return s
