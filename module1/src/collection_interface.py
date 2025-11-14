from complexity_analyzer import ComplexityAnalyzer


class CollectionInterface:
    """
    Command-line interface to test a collection with the following methods:
    1 - push(value) - add an element to the collection
    2 - pop() - remove and return an element from the collection
    3 - peek() - return an element from the collection
    4 - index(value) - search for the given value and return an index or raise a ValueException if not found
    5 - clear() - remove all elements from the collection

    The collection should also support len() and iter()
    """

    def __init__(self, collection_type, collection):
        """
        Create a collection interface.
        :param collection_type: description of interface (e.g. "linked list" or "stack")
        :param collection: collection to test
        """
        self.collection_type = collection_type
        self.collection = collection

    def execute(self):
        while True:
            print('--------------------------------------------------------------')
            print(f'{self.collection_type} has {len(self.collection)} elements:')
            print('Enter a command')
            print('  a) Add an element')
            print('  r) Remove an element')
            print('  s) Search for an element')
            print('  l) List all elements')
            print('  c) Clear (remove all elements)')
            print('  ac) Analyze complexity')
            print('  q) Quit')
            cmd = input('> ').lower()
            if cmd == 'a':
                cmd = input('Enter value to add: ')
                self.collection.push(cmd)
            elif cmd == 'r':
                try:
                    value = self.collection.pop()
                    print(f'Removed {value}')
                except IndexError:
                    print('No element to remove')
            elif cmd == 's':
                try:
                    cmd = input('Enter value to search: ')
                    index = self.collection.index(cmd)
                    print(f'Value found at index {index}')
                except ValueError:
                    print(f'Value not found')
            elif cmd == 'l':
                print('Values:')
                for i, value in enumerate(self.collection):
                    print(f'[{i}] {value}')
            elif cmd == 'c':
                self.collection.clear()
            elif cmd == 'ac':
                self.collection.clear()
                ComplexityAnalyzer(plot = True).execute(self.collection)
            elif cmd == 'q':
                return
            else:
                print('Invalid command')
