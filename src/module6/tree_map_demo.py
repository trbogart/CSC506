from random import shuffle, seed

from module6.tree_map import TreeMap

if __name__ == '__main__':
    tm = TreeMap()


    def print_map():
        print(
            f'Map has {len(tm)} elements, height is {tm.bst.get_height()}, min height (perfectly balanced) is {tm.bst.get_balanced_height()}')
        print(tm)


    keys = [i + 1 for i in range(7)]
    seed(431)
    shuffle(keys)

    print('Basic testing for TreeMap operations.')
    print('Additional testing (including larger counts and more edge cases) is done in unit test: test_tree_map.py')
    print()
    print_map()

    print(f'Inserting {len(keys)} values in random order')
    for key in keys:
        value = f'o{key}'
        print(f'Inserting key {key} with value {value}')
        tm[key] = value
        print_map()

    print('Updating existing keys with new values')
    updated_keys = [1, 3, 5]
    for key in updated_keys:
        value = f'u{key}'
        print(f'Updating key {key} from {tm[key]} to {value}')
        tm[key] = value
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
