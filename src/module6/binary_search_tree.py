import math
from enum import Enum

from module6.TreePrint import pretty_tree


class TraversalOrder(Enum):
    IN_ORDER = 0
    PRE_ORDER = 1
    POST_ORDER = 2


class BinarySearchTree:
    """
    Binary search tree.
    Elements must support the > and < operations.
    """

    class Node:
        def __init__(self, element):
            self.element = element
            self.parent = None
            self.left = None
            self.right = None
            self.height = 0

        def __str__(self):
            return str(self.element)

        def __repr__(self):
            return repr(self.element)

        def set_left(self, new_node):
            """
            Sets the left node, resetting height as needed.
            """
            if new_node is not None:
                new_node.parent = self
            self.left = new_node
            self.reset_height()

        def set_right(self, new_node):
            """
            Sets the rights node, resetting height as needed.
            """
            if new_node is not None:
                new_node.parent = self
            self.right = new_node
            self.reset_height()

        def reset_height(self):
            """
            Recalculates height of node, adjusting ancestors as needed.
            """
            new_height = 1 + max(BinarySearchTree._get_height(self.left), BinarySearchTree._get_height(self.right))
            if self.height != new_height:
                self.height = new_height
                if self.parent is not None:
                    self.parent.reset_height()

        def get_min_node(self):
            """
            Get minimum (left-most) node. Will never be None.
            """
            node = self
            while node.left is not None:
                node = node.left
            return node

        def get_max_node(self):
            """
            Get maximum (right-most) node. Will never be None.
            """
            node = self
            while node.right is not None:
                node = node.right
            return node

        def get_previous_node(self):
            """
            Gets the previous node, or None if this is the first (min) node.
            """
            if self.left is None:
                if self.parent is not None and self.parent.right == self:
                    return self.parent
                return None
            return self.left.get_max_node()

        def get_next_node(self):
            """
            Returns the next node, or None if this is the last (max) node.
            """
            if self.right is None:
                if self.parent is not None and self.parent.left == self:
                    return self.parent
                return None
            return self.right.get_min_node()

        def insert_node(self, new_node):
            """
            Inserts a node below the current node.
            """
            if new_node.element < self.element:
                if self.left is None:
                    self.set_left(new_node)
                else:
                    self.left.insert_node(new_node)
            else:
                if self.right is None:
                    self.set_right(new_node)
                else:
                    self.right.insert_node(new_node)

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return self.search(key) is not None

    def __iter__(self):
        return self.traverse()

    def __str__(self):
        return pretty_tree(self)


    def insert(self, element):
        """
        Inserts an element into the tree.
        :param element: element to insert
        """
        if element is None:
            raise ValueError("element cannot be None")
        new_node = self.Node(element)
        if self.root is None:
            self.root = new_node
        else:
            self.root.insert_node(new_node)
        self.size += 1

    def delete(self, element):
        """
        Deletes a matching element from the tree. Returns the matching element if it exists, or None otherwise.
        """

        def replace_node(node, new_node):
            # replace node with one of its children
            if node.parent is None:
                self.root = new_node
                if new_node is not None:
                    new_node.parent = None
            elif node.parent.left == node:
                node.parent.set_left(new_node)
            elif node.parent.right == node:
                node.parent.set_right(new_node)
            else:
                raise ValueError("Invalid node")

        def delete_node(node):
            # delete this node
            if node.left is None:
                # leaf node or right child only
                replace_node(node, node.right)
            elif node.right is None:
                # left child only
                replace_node(node, node.left)
            else:
                # delete node with 2 children
                if node.right.height > node.left.height:
                    # replace with next node
                    replacement_node = node.get_next_node()
                else:
                    # replace with previous node
                    replacement_node = node.get_previous_node()
                node.element, replacement_node.element = replacement_node.element, node.element
                delete_node(replacement_node)

        def delete_element(node):
            if node is None:
                return None
            if element < node.element:
                return delete_element(node.left)
            elif element > node.element:
                return delete_element(node.right)
            else:
                deleted_element = node.element
                delete_node(node)
                return deleted_element

        if element is None:
            raise ValueError("element cannot be None")
        deleted = delete_element(self.root)
        if deleted is not None:
            self.size -= 1
        return deleted

    def search(self, element):
        """
        Return matching element if present, or None if absent.
        """
        node = self.root
        while node is not None:
            if element > node.element:
                node = node.right
            elif element < node.element:
                node = node.left
            else:
                return node.element  # match
        return None

    def traverse(self, order: TraversalOrder = TraversalOrder.IN_ORDER):
        """
        Returns an in-order iterator.
        """

        def traverse_in_order(node):
            if node is not None:
                if order == TraversalOrder.IN_ORDER:
                    yield from traverse_in_order(node.left)
                    yield node.element
                    yield from traverse_in_order(node.right)
                elif order == TraversalOrder.PRE_ORDER:
                    yield node.element
                    yield from traverse_in_order(node.left)
                    yield from traverse_in_order(node.right)
                elif order == TraversalOrder.POST_ORDER:
                    yield from traverse_in_order(node.left)
                    yield from traverse_in_order(node.right)
                    yield node.element
                else:
                    raise ValueError("Invalid TraversalOrder")

        return traverse_in_order(self.root)

    def get_min(self):
        """
        Returns the minimum element in the tree, or None if empty.
        """
        if self.root is None:
            return None
        return self.root.get_min_node().element

    def get_max(self):
        """
        Returns the maximum value in the tree, or None if empty.
        """
        if self.root is None:
            return None
        return self.root.get_max_node().element

    def get_height(self):
        """
        Returns the height of the tree, or -1 if empty
        """
        return self._get_height(self.root)

    def get_balanced_height(self):
        """
        Returns the minimum possible height of the tree if it was perfectly balanced. Will return -1 for empty tree.
        """
        return int(math.ceil(math.log2(self.size + 1) - 1))

    def get_balance_factor(self):
        """
        Returns the balance factor of this tree (ratio of actual height to minimum height).
        """
        balanced_height = self.get_balanced_height()
        if balanced_height > 0:
            return self.get_height() / balanced_height
        return 1.0

    def is_balanced(self):
        """
        Returns true if this tree is balanced (height is no more than 50% greater than balanced height).
        """
        return self.get_balance_factor() < 1.5

    def clear(self):
        self.root = None
        self.size = 0

    @staticmethod
    def _get_height(node):
        """
        Gets the height of a node, of 0 if None
        """
        return node.height if node is not None else -1