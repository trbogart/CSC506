from random import shuffle, seed
from sys import argv
from os.path import basename

from module6.binary_search_tree import BinarySearchTree

if __name__ == '__main__':
    bst = BinarySearchTree()

    def print_tree():
        print(f'BST has {len(bst)} elements, height is {bst.get_height()}, min height (perfectly balanced) is {bst.get_balanced_height()}')
        print(bst)


    keys = [i for i in range(7)]
    seed(42)
    shuffle(keys)

    print(f'Output from {basename(argv[0])}')
    print('Basic testing for BST operations. Additional testing is done in unit test: test_binary_search_tree.py')

    print(f'Inserting {len(keys)} values in random order')
    for key in keys:
        bst.insert(key)
    print_tree()



    low = -1
    high = 100
    print(f'Searching for key ({keys[0]}): {bst.search(keys[0])}')
    print(f'Searching for low missing key ({low}): {bst.search(low)}')
    print(f'Searching for high missing key ({high}): {bst.search(high)}')
    print('Deleting keys in random order')
    shuffle(keys)
    for key in keys:
        print(f'Deleting {key}')
        bst.delete(key)
        print_tree()
