def verify_collection(collection, *expected):
    expected_list = list(expected)
    assert len(collection) == len(expected_list)
    assert collection.is_empty() == (len(collection) == 0)

    assert list(iter(collection)) == expected_list

    assert repr(collection) == repr(expected_list)

    for i, value in enumerate(expected_list):
        assert collection[i] == value
        assert value in collection
        assert collection.search(value) == i
