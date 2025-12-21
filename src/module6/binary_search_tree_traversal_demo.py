from random import shuffle, seed

from module6.binary_search_tree import BinarySearchTree, TraversalOrder

if __name__ == '__main__':
    bst = BinarySearchTree()

    keys = [i + 1 for i in range(7)]
    seed(422)
    shuffle(keys)

    print('Basic testing for BST traversal.')
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
