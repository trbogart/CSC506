from module1.complexity_analyzer import ComplexityAnalyzer


class CollectionInterface:
    """
    Command-line interface to test a collection with the following methods:
    1 - push(value) - add an element to the collection
    2 - pop() - remove and return an element from the collection
    3 - peek() - return an element from the collection
    4 - index(value) - search for the given value and return an index or raise a ValueException if not found
    5 - clear() - remove all elements from the collection
    6 - get_estimated_space() - return the estimated space consumed by the collection (for space complexity analysis)

    The collection should also support len() and iter().
    """

    def __init__(self, collection_type, collection):
        """
        Create a command-line interface to test or analyze a collection.
        :param collection_type: description of what is being tested (e.g. "Linked List" or "Stack")
        :param collection: collection to test (see class description for requirements)
        """
        self.collection_type = collection_type
        self.collection = collection

    def execute(self, num_runs=5_000):
        """Displays a menu to select to manipulate and test the collection."""
        while True:
            print('--------------------------------------------------------------')
            print(f'{self.collection_type} has {len(self.collection)} elements:')
            print('Enter a command')
            print('  a) Add an element')
            print('  r) Remove an element')
            print('  s) Search for an element')
            print('  l) List all elements')
            print('  c) Clear (remove all elements)')
            print('  o) Analyze complexity mode')
            print('  q) Quit')
            cmd = input('> ').lower()
            if cmd == 'a':
                # adds an element to the collection using push()
                cmd = input('Enter value to add: ')
                self.collection.push(cmd)
            elif cmd == 'r':
                # removes an element to the collection using pop()
                try:
                    value = self.collection.pop()
                    print(f'Removed {value}')
                except IndexError:
                    print('No element to remove')
            elif cmd == 's':
                # searches for an element in the collection using index()
                try:
                    cmd = input('Enter value to search: ')
                    index = self.collection.index(cmd)
                    print(f'Value found at index {index}')
                except ValueError:
                    print(f'Value not found')
            elif cmd == 'l':
                # lists elements in collection for testing
                print('Values:')
                for i, value in enumerate(self.collection):
                    print(f'[{i}] {value}')
            elif cmd == 'c':
                # removes all elements in collection
                self.collection.clear()
            elif cmd == 'o':
                # clear list and enter complexity analysis mode, see ComplexityAnalyzer
                self.collection.clear()
                ComplexityAnalyzer(plot=True, default_num_runs=num_runs).execute(self.collection,
                                                                                 collection_type=self.collection_type)
            elif cmd == 'q':
                # quit
                return
            else:
                print('Invalid command')
