import pytest

from module4.linked_list import LinkedList
from module4.test_collection import verify_collection


# also tested in the other
def test_empty():
    verify_collection(LinkedList())


def test_clear():
    ll = LinkedList()
    ll.insert(1)
    ll.insert(2)
    ll.clear()
    verify_collection(ll)


def test_insert():
    ll = LinkedList()
    ll.insert(1)
    verify_collection(ll, 1)
    ll.insert(2)
    verify_collection(ll, 1, 2)
    ll.insert(3)
    verify_collection(ll, 1, 2, 3)


def test_delete():
    ll = LinkedList()
    ll.insert(1)
    ll.insert(2)
    ll.insert(3)
    ll.insert(4)

    verify_collection(ll, 1, 2, 3, 4)

    with pytest.raises(ValueError):
        ll.delete(5)

    assert ll.delete(2) == 1
    verify_collection(ll, 1, 3, 4)
    assert ll.delete(4) == 2
    verify_collection(ll, 1, 3)
    assert ll.delete(1) == 0
    verify_collection(ll, 3)
    assert ll.delete(3) == 0
    verify_collection(ll)

    with pytest.raises(ValueError):
        ll.delete(1)
