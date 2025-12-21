import random

from module6.binary_search_tree import BinarySearchTree, TraversalOrder


def test_empty():
    bst = BinarySearchTree()
    assert len(bst) == 0
    assert bst.get_height() == -1
    assert bst.search(1) is None
    assert list(bst.traverse()) == []


def test_insert_one_element():
    bst = BinarySearchTree()
    bst.insert(1)
    assert len(bst) == 1
    assert bst.get_height() == 0
    assert list(bst.traverse()) == [1]
    assert bst.search(1) == 1
    assert bst.search(2) is None
    assert bst.search(0) is None


def test_insert_bigger_element():
    bst = BinarySearchTree()
    bst.insert(1)
    bst.insert(2)
    assert len(bst) == 2
    assert bst.get_height() == 1
    assert list(bst.traverse()) == [1, 2]
    assert bst.search(1) == 1
    assert bst.search(2) == 2
    assert bst.search(0) is None
    assert bst.search(3) is None


def test_insert_smaller_element():
    bst = BinarySearchTree()
    bst.insert(2)
    bst.insert(1)
    assert len(bst) == 2
    assert bst.get_height() == 1
    assert list(bst.traverse()) == [1, 2]
    assert bst.search(1) == 1
    assert bst.search(2) == 2
    assert bst.search(0) is None
    assert bst.search(3) is None


def test_insert_multi():
    bst = BinarySearchTree()
    bst.insert(2)
    bst.insert(1)
    bst.insert(3)
    bst.insert(5)
    bst.insert(4)
    assert len(bst) == 5
    assert bst.get_height() == 3
    assert list(bst.traverse()) == [1, 2, 3, 4, 5]
    for i in range(1, 6):
        assert bst.search(i) == i


def test_insert_duplicate():
    bst = BinarySearchTree()
    bst.insert(2)
    bst.insert(1)
    bst.insert(3)
    bst.insert(3)
    bst.insert(1)
    assert len(bst) == 5
    assert bst.get_height() == 2
    assert list(bst.traverse()) == [1, 1, 2, 3, 3]
    assert bst.search(1) == 1
    assert bst.search(2) == 2
    assert bst.search(3) == 3


def test_insert_linear_right():
    bst = BinarySearchTree()
    num_elements = 100
    for i in range(num_elements):
        bst.insert(i)
        assert len(bst) == i + 1
    assert len(bst) == num_elements
    assert bst.get_height() == num_elements - 1
    assert list(bst.traverse()) == [i for i in range(num_elements)]


def test_insert_linear_left():
    bst = BinarySearchTree()
    num_elements = 100
    for i in range(num_elements - 1, -1, -1):
        bst.insert(i)
        assert len(bst) == 100 - i
    assert len(bst) == num_elements
    assert bst.get_height() == num_elements - 1
    assert list(bst.traverse()) == [i for i in range(num_elements)]


def test_balance():
    bst = BinarySearchTree()
    bst.insert(10)
    assert bst.get_height() == 0
    assert bst.get_balanced_height() == 0
    assert bst.get_balance_factor() == 1.0
    bst.insert(5)
    assert bst.get_height() == 1
    assert bst.get_balanced_height() == 1
    assert bst.get_balance_factor() == 1.0
    bst.insert(3)
    assert bst.get_height() == 2
    assert bst.get_balanced_height() == 1
    assert bst.get_balance_factor() == 2.0
    bst.insert(15)
    assert bst.get_height() == 2
    assert bst.get_balanced_height() == 2
    assert bst.get_balance_factor() == 1.0
    bst.insert(12)
    assert bst.get_height() == 2
    assert bst.get_balanced_height() == 2
    assert bst.get_balance_factor() == 1.0
    bst.insert(1)
    assert bst.get_height() == 3
    assert bst.get_balanced_height() == 2
    assert bst.get_balance_factor() == 3 / 2
    bst.insert(2)
    assert bst.get_height() == 4
    assert bst.get_balanced_height() == 2
    assert bst.get_balance_factor() == 2.0
    bst.insert(8)
    assert bst.get_height() == 4
    assert bst.get_balanced_height() == 3
    assert bst.get_balance_factor() == 4 / 3


def test_traverse():
    bst = _get_test_tree()
    #     ______6__
    #    /         \
    #   2____       8__
    #  /     \     /   \
    # 1       5   7     10
    #        /         /
    #       4         9
    #      /
    #     3
    assert list(bst.traverse()) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert list(bst.traverse(TraversalOrder.IN_ORDER)) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert list(bst.traverse(TraversalOrder.PRE_ORDER)) == [6, 2, 1, 5, 4, 3, 8, 7, 10, 9]
    assert list(bst.traverse(TraversalOrder.POST_ORDER)) == [1, 3, 4, 5, 2, 7, 9, 10, 8, 6]


def test_min_max():
    bst = _get_test_tree()
    assert bst.get_min() == 1
    assert bst.get_max() == 10


def test_delete():
    bst = _get_test_tree()
    #     ______6__
    #    /         \
    #   2____       8__
    #  /     \     /   \
    # 1       5   7     10
    #        /         /
    #       4         9
    #      /
    #     3
    _test_tree(bst,
               size=10,
               min=1,
               max=10,
               expected=Node(6,
                             height=4,
                             left=Node(2,
                                       height=3,
                                       left=Node(1),
                                       right=Node(5,
                                                  height=2,
                                                  left=Node(4,
                                                            height=1,
                                                            left=Node(3))),
                                       ),
                             right=Node(8,
                                        height=2,
                                        left=Node(7),
                                        right=Node(10,
                                                   height=1,
                                                   left=Node(9)))
                             ))
    # delete leaf
    assert bst.delete(9) == 9
    #     ______6__
    #    /         \
    #   2____       8__
    #  /     \     /   \
    # 1       5   7     10
    #        /
    #       4
    #      /
    #     3
    _test_tree(bst,
               size=9,
               min=1,
               max=10,
               expected=Node(6,
                             height=4,
                             left=Node(2,
                                       height=3,
                                       left=Node(1),
                                       right=Node(5,
                                                  height=2,
                                                  left=Node(4,
                                                            height=1,
                                                            left=Node(3))),
                                       ),
                             right=Node(8,
                                        height=1,
                                        left=Node(7),
                                        right=Node(10))
                             ))

    # delete node with left child only
    assert bst.delete(4) == 4
    #     ______6__
    #    /         \
    #   2____       8__
    #  /     \     /   \
    # 1       5   7     10
    #        /
    #       3
    _test_tree(bst,
               size=8,
               min=1,
               max=10,
               expected=Node(6,
                             height=3,
                             left=Node(2,
                                       height=2,
                                       left=Node(1),
                                       right=Node(5,
                                                  height=1,
                                                  left=Node(3)),
                                       ),
                             right=Node(8,
                                        height=1,
                                        left=Node(7),
                                        right=Node(10))
                             ))

    # delete node with 2 children
    assert bst.delete(2) == 2
    #     ______6__
    #    /         \
    #   3____       8__
    #  /     \     /   \
    # 1       5   7     10

    _test_tree(bst,
               size=7,
               min=1,
               max=10,
               expected=Node(6,
                             height=2,
                             left=Node(3,
                                       height=1,
                                       left=Node(1),
                                       right=Node(5),
                                       ),
                             right=Node(8,
                                        height=1,
                                        left=Node(7),
                                        right=Node(10))
                             ))

    # delete root with 2 children
    assert bst.delete(6) == 6
    #     5__
    #    /   \
    #   3     8
    #  /     / \
    # 1     7   10
    _test_tree(bst,
               size=6,
               min=1,
               max=10,
               expected=Node(5,
                             height=2,
                             left=Node(3,
                                       height=1,
                                       left=Node(1)
                                       ),
                             right=Node(8,
                                        height=1,
                                        left=Node(7),
                                        right=Node(10))
                             ))

    assert bst.delete(7) == 7
    #     5__
    #    /   \
    #   3     8
    #  /       \
    # 1         10
    _test_tree(bst,
               size=5,
               min=1,
               max=10,
               expected=Node(5,
                             height=2,
                             left=Node(3,
                                       height=1,
                                       left=Node(1)
                                       ),
                             right=Node(8,
                                        height=1,
                                        right=Node(10))
                             ))

    # delete node with right child
    assert bst.delete(10) == 10
    #     5__
    #    /   \
    #   3     8
    #  /
    # 1
    _test_tree(bst,
               size=4,
               min=1,
               max=8,
               expected=Node(5,
                             height=2,
                             left=Node(3,
                                       height=1,
                                       left=Node(1)
                                       ),
                             right=Node(8)
                             ))

    assert bst.delete(8) == 8
    #     5
    #    /
    #   3
    #  /
    # 1
    _test_tree(bst,
               size=3,
               min=1,
               max=5,
               expected=Node(5,
                             height=2,
                             left=Node(3,
                                       height=1,
                                       left=Node(1)
                                       )))

    # delete root with left child
    assert bst.delete(5) == 5
    #  3
    # /
    # 1
    _test_tree(bst,
               size=2,
               min=1,
               max=3,
               expected=Node(3,
                             height=1,
                             left=Node(1)
                             ))
    # delete root with left child
    assert bst.delete(3) == 3
    # 1
    assert type(bst.root) == BinarySearchTree.Node
    assert len(bst) == 1
    assert bst.root.element == 1
    assert bst.get_height() == 0
    assert bst.root.height == 0

    _test_tree(bst, min=1, max=1, size=1, expected=Node(1))

    # delete last node
    assert bst.delete(1) == 1
    assert len(bst) == 0
    assert bst.get_height() == -1
    assert list(bst) == []
    assert bst.root is None

def test_insert_delete_random():
    random.seed(42)
    bst = BinarySearchTree()
    num_elements = 1000
    values = [i for i in range(num_elements)]
    for _ in range(10):
        random.shuffle(values)
        for i, value in enumerate(values):
            bst.insert(value)
            assert len(bst) == i + 1
            assert value in bst

        values.sort()
        assert list(bst) == values

        random.shuffle(values)
        for i, value in enumerate(values):
            bst.delete(value)
            assert value not in bst
            assert len(bst) == num_elements - 1 - i
        assert len(bst) == 0

class Node:
    def __init__(self, element, height=0, left=None, right=None):
        self.element = element
        self.height = height
        self.left = left
        self.right = right


def _test_tree(bst, size, min, max, expected):
    assert len(bst) == size
    assert bst.get_min() == min
    assert bst.get_max() == max
    assert bst.get_height() == expected.height
    _test_node(None, bst.root, expected)


def _test_node(parent, node, expected):
    if expected is None:
        assert node is None
    else:
        assert node is not None
        assert node.parent is parent
        assert node.element == expected.element
        assert node.height == expected.height
        _test_node(node, node.left, expected.left)
        _test_node(node, node.right, expected.right)


def _get_test_tree():
    #     ______6__
    #    /         \
    #   2____       8__
    #  /     \     /   \
    # 1       5   7     10
    #        /         /
    #       4         9
    #      /
    #     3
    bst = BinarySearchTree()
    bst.insert(6)
    bst.insert(2)
    bst.insert(5)
    bst.insert(1)
    bst.insert(8)
    bst.insert(4)
    bst.insert(7)
    bst.insert(10)
    bst.insert(3)
    bst.insert(9)
    return bst
