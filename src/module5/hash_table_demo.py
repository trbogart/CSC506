import random


from module5.hash_table import HashTable

class HashTableDemo:
    def __init__(self):
        self.hashtable = HashTable()
        self.keys = []


    def add(self, num_elements: int = 1):
        for i in range(num_elements):
            key = random.randint(1, 100)
            value = random.randint(101, 200)
            old_value = self.hashtable.insert(key, value)
            self.keys.append(key)
            if old_value is None:
                print(f'Inserted {key}: {value} into hashtable (new value), size {len(self.hashtable)}')
            else:
                print(f'Inserted {key}: {value} into hashtable (replaced old value {old_value}), size {len(self.hashtable)}')
            print(f'- Verify value: {self.hashtable.search(key)}')

    def delete(self):
        random.shuffle(self.keys)

        for key in self.keys:
            old_value = self.hashtable.delete(key)
            print(f'Deleted {key} from hashtable (value {old_value}), size {len(self.hashtable)}')
        self.keys.clear()

    def search(self):
        random.shuffle(self.keys)
        for key in self.keys:
            print(f'Searched for random key {key}: {self.hashtable.search(key)}')

if __name__ == '__main__':
    hash_demo = HashTableDemo()
    hash_demo.add(5)
    hash_demo.search()
    hash_demo.delete()

