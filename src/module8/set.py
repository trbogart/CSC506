from typing import Optional, Iterator

from sympy import nextprime

from module8.collection import ICollection


class Set[T](ICollection[T]):
    """
    Set implemented with a chained hash table.
    """
    load_factor = .75
    start_num_buckets = 11

    class Bucket:
        def __init__(self, key: T, next_bucket=None):
            self.key = key
            self.next_bucket = next_bucket

        def __contains__(self, key: T):
            return self.key == key or self.next_bucket is not None and key in self.next_bucket

    def __init__(self):
        self.min_size = 0
        self.max_size = int(self.load_factor * self.start_num_buckets)
        self.old_bucket_sizes = []
        self._init_buckets(self.start_num_buckets)

    def __len__(self):
        return self.size

    def __contains__(self, key: T) -> bool:
        bucket = self.buckets[self._get_index(key)]
        return bucket is not None and key in bucket

    def __iter__(self) -> Iterator[T]:
        for bucket in self.buckets:
            while bucket is not None:
                yield bucket.key
                bucket = bucket.next_bucket

    def clear(self) -> None:
        self._init_buckets(self.start_num_buckets)

    def __repr__(self) -> str:
        return f'[{', '.join(map(lambda x: repr(x), iter(self)))}]'

    def add(self, key: T) -> bool:
        index = self._get_index(key)
        bucket = self.buckets[index]
        if bucket is not None and key in bucket:
            return False
        self.size += 1
        self.buckets[index] = Set.Bucket(key, bucket)
        self._maybe_resize_up()

        return True

    def remove(self, key: T) -> bool:
        index = self._get_index(key)
        bucket = self.buckets[index]
        if bucket is None:
            return False
        if bucket.key == key:
            self.size -= 1
            self.buckets[index] = bucket.next_bucket
            self._maybe_resize_down()
            return True

        while bucket.next_bucket is not None:
            if bucket.next_bucket.key == key:
                self.size -= 1
                bucket.next_bucket = bucket.next_bucket.next_bucket
                self._maybe_resize_down()
                return True
            bucket = bucket.next_bucket
        return False

    def union(self, other):
        s = Set()
        for key in self:
            s.add(key)
        for key in other:
            s.add(key)
        return s

    def intersection(self, other):
        s = Set()
        for key in other:
            if key in self:
                s.add(key)
        return s

    def difference(self, other):
        s = Set()
        for key in self:
            if key not in other:
                s.add(key)
        return s

    def symmetric_difference(self, other):
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

    def _maybe_resize_up(self) -> None:
        if self.size > self.max_size:
            old_buckets = self.buckets

            self.min_size = self.max_size
            self.old_bucket_sizes.append(len(old_buckets))

            num_buckets = nextprime(len(self.buckets) * 2)
            self.max_size = int(num_buckets * self.load_factor)

            self._init_buckets(num_buckets)

            # reinsert values
            for bucket in old_buckets:
                while bucket is not None:
                    self.add(bucket.key)
                    bucket = bucket.next_bucket

    def _maybe_resize_down(self):
        if self.size < self.min_size:
            old_buckets = self.buckets

            num_buckets = self.old_bucket_sizes.pop()

            if len(self.old_bucket_sizes) == 0:
                self.min_size = 0
            else:
                self.min_size = int(self.old_bucket_sizes[-1] * self.load_factor)

            self.max_size = int(num_buckets * self.load_factor)
            self._init_buckets(num_buckets)

            # reinsert values
            for bucket in old_buckets:
                while bucket is not None:
                    self.add(bucket.key)
                    bucket = bucket.next_bucket

    def _init_buckets(self, num_buckets: int) -> None:
        self.size = 0
        self.buckets: list[Optional[Set.Bucket]] = [None] * num_buckets
