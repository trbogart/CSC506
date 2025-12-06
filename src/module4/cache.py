import argparse
from typing import Iterable, Tuple


# Example algorithm using a slightly modified version of LinkedList
# Builds a simple LRU cache using a dictionary of key to nodes and a linked list
# Adding a new item above capacity will delete the item at the tail of the list
# So far this functions like a deque, but accessing a key will move the corresponding node to the front of the list

class Cache[K, V]:
    """
    Simple LRU (Least Recently Used) cache implementation that combines a dictionary and a linked list.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.head = None
        self.tail = None
        self.node_map = {}

    def __getitem__(self, key: K) -> V:
        node = self.node_map[key]
        self._move_to_front(node)
        return node.value

    def __setitem__(self, key: K, value: V):
        if key in self.node_map:
            node = self.node_map[key]
            node.value = value
            # remove node so it will be added at the front below
            self._move_to_front(node)
        else:
            # create new node and add to front of list
            node = self.Node(key, value)
            self._add_front(node)
            self.node_map[key] = node

            # remove least recently used node if over capacity
            if len(self.node_map) > self.capacity:
                lru_node = self.tail
                self._remove_node(lru_node)
                del self.node_map[lru_node.key]

    def __contains__(self, key: K) -> bool:
        return key in self.node_map

    def __repr__(self) -> str:
        items = [f'{repr(key)}: {repr(value)}' for key, value in self.items()]
        return '{' + ', '.join(items) + '}'

    def __len__(self) -> int:
        return len(self.node_map)

    def keys(self) -> Iterable[K]:
        node = self.head
        while node is not None:
            yield node.key
            node = node.next_node

    def values(self) -> Iterable[V]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next_node

    def items(self) -> Iterable[Tuple[K, V]]:
        node = self.head
        while node is not None:
            yield node.key, node.value
            node = node.next_node

    class Node:
        def __init__(self, key: K, value: V):
            self.key = key
            self.value = value
            self.next_node = None
            self.prev_node = None

    def _move_to_front(self, node: Node) -> None:
        if node != self.head:
            self._remove_node(node)
            self._add_front(node)

    def _add_front(self, node: Node) -> None:
        node.next_node = self.head
        if self.head is not None:
            self.head.prev_node = node
        self.head = node
        if self.tail is None:
            # first element
            self.tail = node

    def _remove_node(self, node: Node) -> None:
        if node.prev_node is None:
            # removing head
            self.head = node.next_node
        else:
            node.prev_node.next_node = node.next_node
        if node.next_node is None:
            # removing tail
            self.tail = node.prev_node
        else:
            node.next_node.prev_node = node.prev_node


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='cache',
        usage='LRU cache',
        add_help=True,  # add -h/--help option
    )
    parser.add_argument('-c', '--capacity', type=int, default=5,
                        help='Capacity of the cache')
    args = parser.parse_args()
    cache = Cache[str, str](capacity=args.capacity)
    while True:
        print('--------------------------------------')
        print(f'Cache: {cache}')
        cmd = input('Enter command (s=set, g=get, q=quit): ')
        if cmd == 'q':
            break
        elif cmd == 's':
            key = input('Enter key: ')
            value = input('Enter value: ')
            cache[key] = value
        elif cmd == 'g':
            key = input('Enter key: ')
            print(f'Value of {key}: {cache[key]}')
