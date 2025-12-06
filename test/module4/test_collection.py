def verify_collection(collection, *expected):
    expected_list = list(expected)
    assert len(collection) == len(expected_list)
    assert collection.is_empty() == (len(collection) == 0)

    assert list(iter(collection)) == expected_list

    assert repr(collection) == repr(expected_list)

    values_set = set()  # only search for first entry

    for i, value in enumerate(iter(collection)):
        assert expected_list[i] == value
        assert value in collection
        if value not in values_set:
            values_set.add(value)
            assert collection.search(value) == i

    for i, value in enumerate(collection.reversed()):
        assert value == expected_list[len(expected_list) - i - 1]

    for value in expected:
        assert value in collection
        assert collection.search(value) >= 0
