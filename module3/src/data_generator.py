import random


def generate_sorted(n: int):
    """
    Generate sorted data of the given size, without duplicates.
    :param n: size of the data to generate
    :return: sorted data of the given size
    """
    return [i + 1 for i in range(n)]


def generate_shuffled(n: int):
    """
    Generate shuffled data of the given size, without duplicates.
    :param n: size of the data to generate
    :return: shuffled data of the given size
    """
    data = generate_sorted(n)
    random.shuffle(data)
    return data


def randomize(data: list[int]):
    """
    Add a random factor to values, possibly adding duplicates.
    :param data: data to modify
    """
    for i in range(1, len(data)):
        data[i] += random.randint(-1, 1)


def generate_partially_sorted(n: int):
    """
    Generate nearly sorted data with duplicates.
    :param n: size of the data to generate
    :return: nearly sorted data of the given size
    """
    data = generate_sorted(n)
    randomize(data)
    return data


def generate_reverse_sorted(n: int):
    """
    Generate reversed data of the given size, without duplicates.
    :param n: size of the data to generate
    """
    return [n - i for i in range(n)]
