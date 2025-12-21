from random import shuffle, seed
from sys import argv
from os.path import basename
from module6.binary_search_tree import BinarySearchTree, TraversalOrder

if __name__ == '__main__':
    bst = BinarySearchTree()

    keys = [i for i in range(6)]
    seed(422)
    shuffle(keys)

    print('Basic testing for BST traversal.')
    print('Additional testing (including larger counts) is done in unit test: test_binary_search_tree.py')
    print()

    print(f'Inserting {len(keys)} values in random order')
    for key in keys:
        bst.insert(key)
    print(f'Tree has {len(bst)} values, height {bst.get_height()}')
    print(bst)
    print('In-order traversal:')
    for i, value in enumerate(bst.traverse(TraversalOrder.IN_ORDER)):
        print(f'  [{i}] {value}')
    print('Pre-order traversal:')
    for i, value in enumerate(bst.traverse(TraversalOrder.PRE_ORDER)):
        print(f'  [{i}] {value}')
    print('Post-order traversal:')
    for i, value in enumerate(bst.traverse(TraversalOrder.POST_ORDER)):
        print(f'  [{i}] {value}')

