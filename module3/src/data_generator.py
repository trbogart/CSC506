import random


def generate_sorted(n: int) -> list[int]:
    """
    Generate sorted data of the given size, without duplicates.
    :param n: size of the data to generate
    :return: sorted data of the given size
    """
    return [i + 1 for i in range(n)]


def generate_shuffled(n: int) -> list[int]:
    """
    Generate shuffled data of the given size, without duplicates.
    :param n: size of the data to generate
    :return: shuffled data of the given size
    """
    data = generate_sorted(n)
    random.shuffle(data)
    return data


def slightly_shuffle(data: list[int], max_adjustment: int = 1) -> None:
    """
    Adds a random factor  each value in an integer list, possibly adding duplicates.
    :param data: data to modify
    :param max_adjustment: maximum adjustment in either direction
    :return: None
    """
    for i in range(1, len(data)):
        data[i] += random.randint(-max_adjustment, max_adjustment)


def generate_partially_sorted(n: int) -> list[int]:
    """
    Generate nearly sorted data with duplicates.
    :param n: size of the data to generate
    :return: nearly sorted data of the given size
    """
    data = generate_sorted(n)
    slightly_shuffle(data)
    return data


def generate_reverse_sorted(n: int) -> list[int]:
    """
    Generate reversed data of the given size, without duplicates.
    :param n: size of the data to generate
    """
    return [n - i for i in range(n)]
