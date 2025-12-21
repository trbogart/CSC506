from random import shuffle, seed

from module6.tree_map import TreeMap

if __name__ == '__main__':
    tm = TreeMap()

    def print_map():
        print(f'Map has {len(tm)} elements, height is {tm.bst.get_height()}, min height (perfectly balanced) is {tm.bst.get_balanced_height()}')
        print(tm.bst)


    keys = [i for i in range(7)]
    seed(431)
    shuffle(keys)

    print('Basic testing for TreeMap operations.')
    print('Additional testing (including larger counts) is done in unit test: test_tree_map.py')
    print()

    print(f'Inserting {len(keys)} values in random order')
    for key in keys:
        tm[key] = str(key) * 2
    print_map()

    print('Inserting an existing key updates value')
    tm[0] = 'u0'
    tm[3] = 'u3'
    tm[5] = 'u5'
    print_map()

    low = -1
    high = 100
    print(f'Searching for 2: {tm[2]}')
    print(f'Searching for 3: {tm[3]}')

    print()
    print('Deleting keys in random order')
    shuffle(keys)
    for key in keys:
        print(f'Deleting {key}')
        del tm[key]
        print_map()
