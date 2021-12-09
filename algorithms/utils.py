from random import randint, uniform
from typing import TypeVar

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


def max_value_index(lst: list[T]) -> tuple[T, int]:
    """
    :param lst: список, в котором ищется максимальное значение
    :return: максимальное значение и индекс, по которому это значение находится
    """
    max_value = max(lst)
    max_index = lst.index(max_value)
    return max_value, max_index


def int_in_bounds(lower, higher) -> tuple[int, int]:
    """
    :param higher: нижняя граница
    :param lower: верхняя граница
    :return: пара целых чисел:
    1) находящихся на отрезке [lower, higher]
    2) x != y
    """
    x = randint(lower, higher)
    y = randint(lower, higher)
    if x == y:
        if x == higher:
            y = lower
        else:
            y += 1
    return x, y


def ints_in_bounds_ordered(lower: int, higher: int) -> tuple[int, int]:
    """
    :param lower: нижняя граница
    :param higher: верхняя граница
    :return: пара целых чисел:
    1) находящихся на отрезке [lower, higher]
    2) x < y
    """
    x, y = int_in_bounds(lower, higher)
    if x > y:
        return y, x
    else:
        return x, y


def random_coefficients(n: int) -> list[float]:
    floats = [0, uniform(0, 1)]
    for i in range(n - 2):
        floats.append(uniform(floats[i + 1], 1))
    floats.append(1)

    result = []
    for i in range(len(floats) - 1):
        result.append(floats[i + 1] - floats[i])
    return result
