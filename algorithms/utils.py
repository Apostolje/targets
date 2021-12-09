from random import randint, uniform
from typing import TypeVar, List, Tuple, Union

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


def max_value_index(lst: List[T]) -> Tuple[T, int]:
    """
    :param lst: список, в котором ищется максимальное значение
    :return: максимальное значение и индекс, по которому это значение находится
    """
    max_value = max(lst)
    max_index = lst.index(max_value)
    return max_value, max_index


def int_in_bounds(lower, higher) -> Tuple[int, int]:
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


def ints_in_bounds_ordered(lower: int, higher: int) -> Tuple[int, int]:
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


def random_coefficients(n: int) -> List[float]:
    floats = [0, uniform(0, 1)]
    for i in range(n - 2):
        floats.append(uniform(floats[i + 1], 1))
    floats.append(1)

    result = []
    for i in range(len(floats) - 1):
        result.append(floats[i + 1] - floats[i])
    return result


def invert_probabilities(success_probabilities: List[List[float]]) -> List[List[float]]:
    """
    :param success_probabilities: матрица вероятностей выполнения
    :return: матрица вероятностей провала
    """
    return [
        [1 - success_probability for success_probability in row]
        for row in success_probabilities
    ]


def sort_related(lst1: List[T1],
                 lst2: List[T2],
                 reverse: bool = False) -> Tuple[List[T1], List[T2]]:
    """
    Возвращает сортированные версии заданных списков.
    Сортируются списки по значениям 1го списка. Значения 2го списка связаны со значениями 1го.
    """
    lst1, lst2 = zip(*sorted(zip(lst1, lst2), key=lambda a: a[0], reverse=reverse))
    return lst1, lst2


def int_or_float(s: str) -> Union[int, float]:
    try:
        return int(s)
    except ValueError:
        return float(s)


def parse_int_param(param_name: str, s: str) -> int:
    try:
        n = int(s)
    except ValueError:
        raise ValueError(f"Параметр {param_name} должен быть "
                         f"целым числом! (задано значение {s})")
    return n


def parse_float_param(param_name: str, s: str) -> float:
    try:
        n = float(s)
    except ValueError:
        raise ValueError(f"Параметр {param_name} должен быть "
                         f"вещественным числом! (задано значение {s})")
    return n
