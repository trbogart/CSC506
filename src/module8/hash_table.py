from typing import Iterator, Optional

from sympy import nextprime

from module8.collection import Collection


class HashTable[T](Collection[T]):
    """
    Chained hash table.
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

    def __len__(self) -> int:
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
        self.buckets[index] = HashTable.Bucket(value, bucket)
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
        self.buckets: list[Optional[HashTable.Bucket]] = [None] * num_buckets

    def _get_max_size(self, num_buckets: int) -> int:
        return int(num_buckets * self.load_factor)
