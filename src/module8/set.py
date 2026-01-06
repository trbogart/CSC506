from typing import Optional, Iterator

from sympy import nextprime

from module8.collection import Collection


class Set[T](Collection[T]):
    """
    Set implemented with a chained hash table.
    """
    load_factor = .75
    start_num_buckets = 11

    class Bucket:
        def __init__(self, value: T, next_bucket=None):
            self.value = value
            self.next_bucket = next_bucket

        def __contains__(self, value: T):
            return self.value == value or self.next_bucket is not None and value in self.next_bucket

    def __init__(self):
        self.old_bucket_sizes = []
        self._init_buckets(self.start_num_buckets)

    def __len__(self):
        return self.size

    def __contains__(self, value: T) -> bool:
        bucket = self.buckets[self._get_index(value)]
        return bucket is not None and value in bucket

    def __iter__(self) -> Iterator[T]:
        for bucket in self.buckets:
            while bucket is not None:
                yield bucket.value
                bucket = bucket.next_bucket

    def __repr__(self) -> str:
        return f'[{', '.join(map(lambda x: repr(x), iter(self)))}]'

    def clear(self) -> None:
        """
        Removes all items.
        """
        self._init_buckets(self.start_num_buckets)

    def add(self, value: T) -> bool:
        """
        Adds a value.
        :param value: value to add
        :return: true if value was added
        """
        index = self._get_index(value)
        bucket = self.buckets[index]
        if bucket is not None and value in bucket:
            return False
        self.size += 1
        self.buckets[index] = Set.Bucket(value, bucket)
        self._maybe_resize_up()

        return True

    def remove(self, value: T) -> bool:
        """
        Removes a value.
        :param value: value to remove
        :return: true if value was removed
        """
        index = self._get_index(value)
        bucket = self.buckets[index]
        if bucket is None:
            return False
        if bucket.value == value:
            self.size -= 1
            self.buckets[index] = bucket.next_bucket
            self._maybe_resize_down()
            return True

        while bucket.next_bucket is not None:
            if bucket.next_bucket.value == value:
                self.size -= 1
                bucket.next_bucket = bucket.next_bucket.next_bucket
                self._maybe_resize_down()
                return True
            bucket = bucket.next_bucket
        return False

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

    def _get_index(self, key: T) -> int:
        return hash(key) % len(self.buckets)

    def _maybe_resize_up(self):
        if self.size > self.max_size:
            old_buckets = self.buckets
            self.old_bucket_sizes.append(len(old_buckets))
            self._init_buckets(nextprime(len(self.buckets) * 2))

            self._restore_buckets(old_buckets)

    def _maybe_resize_down(self):
        if self.size < self.min_size:
            old_buckets = self.buckets
            num_buckets = self.old_bucket_sizes.pop()
            self._init_buckets(num_buckets)
            self._restore_buckets(old_buckets)

    def _restore_buckets(self, old_buckets: list[Optional[Bucket]]):
        # reinsert values
        for bucket in old_buckets:
            while bucket is not None:
                self.add(bucket.value)
                bucket = bucket.next_bucket

    def _init_buckets(self, num_buckets: int):
        if len(self.old_bucket_sizes) == 0:
            self.min_size = 0
        else:
            self.min_size = self._get_max_size(self.old_bucket_sizes[-1])
        self.max_size = self._get_max_size(num_buckets)

        self.size = 0
        self.buckets: list[Optional[Set.Bucket]] = [None] * num_buckets

    def _get_max_size(self, num_buckets: int) -> int:
        return int(num_buckets * self.load_factor)
