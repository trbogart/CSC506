import pytest

from module1.linked_list import LinkedList

value1 = "value1"
value2 = "value2"
value3 = "value3"
value4 = "value4"


def test_empty():
    ll = LinkedList()
    _verify_elements(ll)


def test_add_first():
    ll = LinkedList()
    ll.add_first(value1)
    _verify_elements(ll, value1)
    ll.add_first(value2)
    _verify_elements(ll, value2, value1)
    ll.add_first(value3)
    _verify_elements(ll, value3, value2, value1)


def test_add_last():
    ll = LinkedList()
    ll.add_last(value1)
    _verify_elements(ll, value1)
    ll.add_last(value2)
    _verify_elements(ll, value1, value2)
    ll.add_last(value3)
    _verify_elements(ll, value1, value2, value3)


def test_mixed_add():
    ll = LinkedList()
    ll.add_first(value1)
    _verify_elements(ll, value1)
    ll.add_last(value2)
    _verify_elements(ll, value1, value2)
    ll.add_first(value3)
    _verify_elements(ll, value3, value1, value2)


def test_get_first():
    ll = LinkedList()

    # empty
    with pytest.raises(IndexError):
        ll.get_first()

    ll.add_first(value1)
    assert ll.get_first() == value1
    ll.add_first(value2)
    assert ll.get_first() == value2
    ll.add_last(value3)
    assert ll.get_first() == value2


def test_get_last():
    ll = LinkedList()

    # empty
    with pytest.raises(IndexError):
        ll.get_last()

    ll.add_first(value1)
    assert ll.get_last() == value1
    ll.add_first(value2)
    assert ll.get_last() == value1
    ll.add_last(value3)
    assert ll.get_last() == value3


def test_get_empty():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(0)
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(1)


def test_get():
    ll = _init_list_with_4_elements()
    with pytest.raises(IndexError):
        ll.get(-1)
    assert ll.get(0) == value1
    assert ll.get(1) == value2
    assert ll.get(2) == value3
    assert ll.get(3) == value4
    with pytest.raises(IndexError):
        ll.get(4)


def test_remove_first_empty():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.remove_first()


def test_remove_first():
    ll = _init_list_with_4_elements()
    assert ll.remove_first() == value1
    _verify_elements(ll, value2, value3, value4)
    assert ll.remove_first() == value2
    _verify_elements(ll, value3, value4)
    assert ll.remove_first() == value3
    _verify_elements(ll, value4)
    assert ll.remove_first() == value4
    _verify_elements(ll)

    with pytest.raises(IndexError):
        ll.remove_first()


def test_remove_last():
    ll = _init_list_with_4_elements()
    assert ll.remove_last() == value4
    _verify_elements(ll, value1, value2, value3)
    assert ll.remove_last() == value3
    _verify_elements(ll, value1, value2)
    assert ll.remove_last() == value2
    _verify_elements(ll, value1)
    assert ll.remove_last() == value1
    _verify_elements(ll)
    with pytest.raises(IndexError):
        ll.remove_last()


def test_pop_no_index():
    ll = _init_list_with_4_elements()
    assert ll.pop() == value4
    _verify_elements(ll, value1, value2, value3)
    assert ll.pop() == value3
    _verify_elements(ll, value1, value2)
    assert ll.pop() == value2
    _verify_elements(ll, value1)
    assert ll.pop() == value1
    _verify_elements(ll)
    with pytest.raises(IndexError):
        ll.pop()


def test_pop_with_index():
    ll = _init_list_with_4_elements()
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(5)

    # remove from middle
    assert ll.pop(2) == value3
    _verify_elements(ll, value1, value2, value4)

    # remove first
    assert ll.pop(0) == value1
    _verify_elements(ll, value2, value4)

    # remove last
    assert ll.pop(1) == value4
    _verify_elements(ll, value2)

    # remove only
    assert ll.pop(0) == value2
    _verify_elements(ll)

    # remove empty
    with pytest.raises(IndexError):
        ll.remove_last()


def test_remove():
    ll = _init_list_with_4_elements()
    # remove invalid
    with pytest.raises(ValueError):
        ll.remove("invalid")
    # remove middle
    ll.remove(value3)
    _verify_elements(ll, value1, value2, value4)
    # remove first
    ll.remove(value1)
    _verify_elements(ll, value2, value4)
    # remove last
    ll.remove(value4)
    _verify_elements(ll, value2)
    # remove only
    ll.remove(value2)
    _verify_elements(ll)
    # remove element twice
    with pytest.raises(ValueError):
        ll.remove(value2)


def test_remove_first_element():
    ll = _init_list_with_4_elements()
    ll.add_last(value1)
    _verify_elements(ll, value1, value2, value3, value4, value1)
    ll.remove(value1)
    _verify_elements(ll, value2, value3, value4, value1)
    ll.remove(value1)
    _verify_elements(ll, value2, value3, value4)
    with pytest.raises(ValueError):
        ll.remove(value1)


def test_index():
    ll = _init_list_with_4_elements()
    assert ll.index(value1) == 0
    assert ll.index(value2) == 1
    assert ll.index(value3) == 2
    assert ll.index(value4) == 3
    with pytest.raises(ValueError):
        ll.index("invalid")


def test_clear():
    ll = _init_list_with_4_elements()
    ll.clear()
    _verify_elements(ll)


def _init_list_with_4_elements():
    ll = LinkedList()
    ll.add_last(value1)
    ll.add_last(value2)
    ll.add_last(value3)
    ll.add_last(value4)
    _verify_elements(ll, value1, value2, value3, value4)
    return ll


def _verify_elements(ll, *expected):
    assert len(ll) == len(expected)
    expected_list = list(expected)
    assert list(iter(ll)) == expected_list
    expected_list.reverse()
    rev = list(ll.iter_reverse())
    assert rev == expected_list
