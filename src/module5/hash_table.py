from abc import ABC, abstractmethod
from typing import Optional

from sympy import nextprime

# TODO hash function

class HashTable[K, V]:
    """
    Hash table using linear probing.
    """
    default_num_buckets = 11
    default_load_factor = .75

    class Bucket(ABC):
        """
        Abstract base class for buckets.
        """

        @abstractmethod
        def is_empty(self) -> bool:
            pass

        @abstractmethod
        def get_key(self) -> Optional[K]:
            pass

        @abstractmethod
        def get_value(self) -> Optional[V]:
            pass

    class KeyValuePair(Bucket):
        """
        Key-value pair.
        """

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def is_empty(self) -> bool:
            return False

        def get_key(self) -> Optional[K]:
            return self.key

        def get_value(self) -> Optional[V]:
            return self.value

    class Empty(Bucket):
        """
        Empty bucket.
        """

        def is_empty(self) -> bool:
            return True

        def get_key(self) -> Optional[K]:
            return None

        def get_value(self) -> Optional[V]:
            return None

    EmptyBucket = Empty() # bucket for empty values
    DeletedBucket = Empty() # bucket for deleted values that do not stop linear probing (but still count towards load factor)

    def __init__(self, num_buckets: int = default_num_buckets, load_factor: float = default_load_factor,
                 hash_function = hash):
        if not 0 < load_factor < 1:
            raise ValueError('load_factor must be between 0 and 1, exclusive')

        self.load_factor = load_factor
        self._init_buckets(num_buckets)
        self.hash_function = hash_function

    def __contains__(self, key: K) -> bool:
        return self._get_matching_index(key) >= 0

    def __getitem__(self, key: K) -> Optional[V]:
        if self.get(key) is None:
            raise KeyError(key)

    def __setitem__(self, key: K, value: V):
        self.insert(key, value)

    def __delitem__(self, key: K):
        if self.delete(key) is None:
            raise KeyError(key)

    def __len__(self):
        return self.size

    def get(self, key: K, default_value: Optional[V] = None) -> Optional[V]:
        """
        Returns the value for the given key.
        :param key: key to lookup
        :param default_value: value to use if key not found (None by default)
        :return: the value for the key, or default_value if none
        """
        index = self._get_matching_index(key)
        if index >= 0:
            return self.buckets[index].get_value()
        else:
            # not found
            return default_value

    def insert(self, key: K, value: V, default_value: Optional[V] = None) -> Optional[V]:
        """
        Inserts or updates the given key and value and returns the old value, if any.
        :param key: key to insert
        :param value: value to insert (or update if key already found)
        :param default_value: value to use if key not found (None by default)
        :return: the previous value for the key, or default_value if none
        """
        index = self._get_matching_index(key)
        new_bucket = self.KeyValuePair(key, value)
        if index >= 0:
            # update existing value
            old_value = self.buckets[index].get_value()
            self.buckets[index] = new_bucket
            return old_value
        else:
            if self.size + self.num_deleted + 1 >= self.max_added:
                self._resize(nextprime(2 * len(self.buckets)))
            self._insert_bucket(new_bucket)
            return default_value

    def delete(self, key: K, default_value=None) -> Optional[V]:
        """
        Deletes the given key and returns the old value, if any.
        :param key: key to delete
        :param default_value: value to use if key not found (None by default)
        :return: the previous value for the key, or default_value if none
        """
        index = self._get_matching_index(key)
        if index >= 0:
            old_value = self.buckets[index].get_value()
            self.buckets[index] = self.DeletedBucket
            self.size -= 1
            self.num_deleted += 1
            return old_value
        else:
            # not found
            return default_value

    def _get_matching_index(self, key: K) -> int:
        hash_code = self.hash_function(key)
        for i in range(len(self.buckets)):
            index = (hash_code + i) % len(self.buckets)
            bucket = self.buckets[index]
            if bucket.is_empty():
                if bucket == self.EmptyBucket:
                    return -1 # finish linear probing
            elif bucket.get_key() == key:
                return index # found key
        return -1 # not found

    def _resize(self, num_buckets: int) -> None:
        old_buckets = self.buckets
        self._init_buckets(num_buckets)
        assert len(old_buckets) < self.max_added

        # reinsert values
        for bucket in old_buckets:
            if not bucket.is_empty():
                self._insert_bucket(bucket)

    def _init_buckets(self, num_buckets: int) -> None:
        self.size = 0
        self.num_deleted = 0
        self.buckets: list[HashTable.Bucket] = [self.EmptyBucket] * num_buckets
        self.max_added = min(num_buckets * self.load_factor, num_buckets - 1)
        if self.max_added < 1:
            self.max_added = 1.0

    def _insert_bucket(self, bucket: Bucket) -> None:
        # insert a value for a key that is not already in the hash table and will not cause a resize
        hash_code = self.hash_function(bucket.get_key())
        for i in range(len(self.buckets)):
            index = (hash_code + i) % len(self.buckets)
            old_bucket = self.buckets[index]
            if old_bucket.is_empty():
                self.size += 1
                self.buckets[index] = bucket
                break
        else:
            raise ValueError('Unable to insert') # should not happen, already resized
