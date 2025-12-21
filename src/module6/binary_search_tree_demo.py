from random import shuffle, seed

from module6.binary_search_tree import BinarySearchTree

if __name__ == '__main__':
    bst = BinarySearchTree()


    def print_tree():
        print(
            f'BST has {len(bst)} elements, height is {bst.get_height()}, min height (perfectly balanced) is {bst.get_balanced_height()}')
        print(bst)


    values = [i + 1 for i in range(8)]
    seed(4321)
    shuffle(values)

    print('Basic testing for BST operations.')
    print('Additional testing (including larger counts and more edge cases) is done in unit test: test_binary_search_tree.py')
    print()

    print_tree()

    print(f'Inserting {len(values)} values in random order')
    for value in values:
        print(f'Inserting {value}')
        bst.insert(value)
        print_tree()

    duplicate_value = 6
    print(f'Inserting duplicate {duplicate_value}')
    bst.insert(duplicate_value)
    print_tree()

    low = 0
    high = 100
    print(f'Searching for value ({values[0]}): {bst.search(values[0])}')
    print(f'Searching for low missing value ({low}): {bst.search(low)}')
    print(f'Searching for high missing value ({high}): {bst.search(high)}')
    print()
    print(f'Min value: {bst.get_min_value()}')
    print(f'Max value: {bst.get_max_value()}')
    print()
    print('Deleting in random order')
    shuffle(values)
    for value in values:
        print(f'Deleting {value}')
        bst.delete(value)
        print_tree()
    bst.delete(duplicate_value)
    print_tree()
