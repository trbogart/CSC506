import random
from enum import Enum
from time import perf_counter

from module8.bubble_sort import bubble_sort
from module8.collection import OrderedCollection
from module8.perf_test import perf_test
from module8.queue import Queue
from module8.quickselect import quickselect
from module8.sort import insertion_sort, merge_sort
from module8.stack import Stack


class CollectionType(Enum):
    STACK = 0
    QUEUE = 1


class ConsoleInterface:
    """
    Console interface for testing collections and algorithms.
    """

    def __init__(self):
        self.collection: OrderedCollection[int] = Stack()
        self.type = CollectionType.STACK

    def use_stack(self):
        self.collection = Stack[int]()
        self.type = CollectionType.STACK

    def use_queue(self):
        self.collection = Queue[int]()
        self.type = CollectionType.QUEUE

    def add(self, value):
        self.collection.add(value)

    def remove(self):
        return self.collection.remove()

    def populate_data(self, size, shuffled):
        self.collection.clear()
        data = [i + 1 for i in range(size)]
        if shuffled:
            random.shuffle(data)
        for value in data:
            self.collection.add(value)

    def list_elements(self):
        size = len(self.collection)
        if size == 0:
            print('List is empty')
        else:
            max_items = 50
            num_shown_items = 10 if size > max_items else size
            for i in range(num_shown_items):
                print(f'[{i}]: {self.a[i]}')
            if size > num_shown_items:
                print(f'... {size - num_shown_items * 2} items excluded')
                for i in range(size - num_shown_items, size):
                    print(f'[{i}]: {self.a[i]}')

    def execute(self):
        print_menu = True
        while True:
            try:
                print('-' * 80)
                if self.type == CollectionType.STACK:
                    collections_type = 'Stack'
                else:
                    collections_type = 'Queue'
                print(f'{collections_type} with {len(self.collection)} elements')

                if print_menu:
                    print('q: Quit')
                    print('m: Print this menu')
                    print('st: Use list-based stack')
                    print('q: Use linked-list-based queue')
                    print('add: Add element')
                    print('rem: Remove next element')
                    print('pop: Populate elements (set size and/or shuffle)')
                    print('ls: List elements')
                    print('bs: Bubble sort')
                    print('is: Insertion sort')
                    print('ms: Merge sort')
                    print('qs: Quickselect')
                    print('perf: Performance comparisons')
                    print_menu = False

                cmd = input('Enter command (q to quit or m to print menu)> ')
                if cmd == 'q':
                    break
                elif cmd == 'm':
                    print_menu = True
                elif cmd == 'st':
                    self.use_stack()
                elif cmd == 'qu':
                    self.use_queue()
                elif cmd == 'add':
                    value = int(input('Enter value: '))
                    self.collection.add(value)
                elif cmd == 'rem':
                    value = self.collection.remove_next()
                    print(f'Removed {value}')
                elif cmd == 'pop':
                    size = int(input('Enter size: '))
                    shuffled = int(input('Enter 0 for sorted data or 1 for shuffled data: '))
                    self.populate_data(size, shuffled == 1)
                elif cmd == 'ls':
                    print('Values:')
                    for i, value in enumerate(self.collection):
                        print(f'[{i}] {value}')
                elif cmd == 'bs':
                    if self.type == CollectionType.STACK:
                        print('Running bubble sort...')
                        start_time = perf_counter()
                        bubble_sort(self.collection.list)
                    else:
                        print("Can't sort queue or linked list")
                elif cmd == 'is':
                    if self.type == CollectionType.STACK:
                        print('Running insertion sort...')
                        start_time = perf_counter()
                        insertion_sort(self.collection.list)
                        print(f'Finished in {perf_counter() - start_time:.3f} seconds')
                    else:
                        print("Can't sort queue or linked list")
                elif cmd == 'ms':
                    if self.type == CollectionType.STACK:
                        print('Running merge sort...')
                        start_time = perf_counter()
                        merge_sort(self.collection.list)
                        print(f'Finished in {perf_counter() - start_time:.3f} seconds')
                    else:
                        print("Can't sort queue or linked list")
                elif cmd == 'qs':
                    if self.type == CollectionType.STACK:
                        k = int(input('Enter k (0 for smallest element, 1 for 2nd smallest element, etc.): '))
                        if 0 <= k < len(self.collection):
                            print('Running quickselect...')
                            start_time = perf_counter()
                            value = quickselect(self.collection.list, k)
                            print(f'Finished in {perf_counter() - start_time:.3f} seconds')
                            print(f'Result: {value}')
                        else:
                            print('Invalid value')
                    else:
                        print("Can't run quickselect on queue or linked list")
                elif cmd == 'perf':
                    perf_test()
                else:
                    print('Invalid command, try again')
            except:
                print('Invalid command, try again')


if __name__ == '__main__':
    ConsoleInterface().execute()
