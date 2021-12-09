import json
import random
from random import randint
from typing import List, Tuple

from itertools import repeat


def find_survival(targets_total: int,
                  targets_values: List[int],
                  weapon_types_amount: List[int],
                  weapon_types_survival_probabilities: List[List[float]],
                  solution: List[int]) -> float:
    """
    Поиск значения выживаемости для заданной задачи и решения.

    :param targets_total: общее число целей
    :param targets_values: значение цели (ее значимость/важность)
    :param weapon_types_amount: число оружий каждого типа
    :param weapon_types_survival_probabilities: вероятности выживания цели от каждого оружия
    :param solution: решение задачи
    :return: значение выживаемости целей.
    """
    survival = 0.

    for target_index, target_value in zip(range(1, targets_total + 1),
                                          targets_values):
        target_survival: float = target_value
        shift = 0
        for type_amount, type_probabilities in zip(weapon_types_amount,
                                                   weapon_types_survival_probabilities):
            # вероятность выживания от оружия этого типа
            probability = type_probabilities[target_index - 1]

            # количество оружий этого типа, нацеленных на эту цель
            aimed = 0
            for selected_target_index in solution[shift:shift + type_amount]:
                if selected_target_index == target_index:
                    aimed += 1

            if probability == 0:
                if aimed > 0:
                    target_survival = 0
            else:
                target_survival *= probability ** aimed

            shift += type_amount

        survival += target_survival

    return survival


def generate_random_solution(n: int, k: int) -> List[int]:
    """
    Генерирует случайно решение для задачи.

    Пример:
        Задача: 3 цели, 3 вида вооружений (5 танков, 2 самолета, 1 судно)

        Решение будет иметь такой вид: [ n n n n n ; n n     ; n    ],
        где n = [1, 3] (индексирование начинается с 1)

        Одно из решений: [ 1 1 1 2 2 ; 3 3 ; 2]

        (3 танка на 1ю цель, 2 танка на 2ю цель,
        2 самолета на 2ю цель, 1 лодка на 2ю цель)

    :param n: количество целей
    :param k: общее число оружий
    :return: случайное решение задачи
    """
    return [
        randint(1, n)
        for _ in range(k)
    ]


DEFAULT_TARGET_NAME = "Цель"
DEFAULT_WEAPON_TYPE = "Испол."


def generate_random_task(min_n_targets: int,
                         max_n_targets: int,
                         min_target_value: int,
                         max_target_value: int,
                         min_n_weapon_type: int,
                         max_n_weapon_type: int,
                         min_n_weapon_amount: int,
                         max_n_weapon_amount: int,
                         min_success_probability: float,
                         max_success_probability: float
                         ) \
        -> Tuple[
            List[str],
            List[int],
            List[str],
            List[int],
            List[List[float]]
        ]:
    n_targets = randint(min_n_targets, max_n_targets)
    n_weapon_types = randint(min_n_weapon_type, max_n_weapon_type)

    targets = [
        f"{DEFAULT_TARGET_NAME} {i + 1}"
        for i in range(n_targets)
    ]
    targets_values = [
        randint(min_target_value, max_target_value)
        for _ in range(n_targets)
    ]
    weapon_types = [
        f"{DEFAULT_WEAPON_TYPE} {i + 1}"
        for i in range(n_weapon_types)
    ]
    weapon_types_amount = [
        randint(min_n_weapon_amount, max_n_weapon_amount)
        for _ in range(n_weapon_types)
    ]
    weapon_types_success_probabilities = [
        [
            round(random.uniform(min_success_probability, max_success_probability), 3)
            for _ in range(n_targets)
        ]
        for _ in range(n_weapon_types)
    ]

    return (
        targets,
        targets_values,
        weapon_types,
        weapon_types_amount,
        weapon_types_success_probabilities
    )


def assert_task_is_correct(targets: List[str],
                           targets_values: List[int],
                           weapon_types: List[str],
                           weapon_types_amount: List[int],
                           weapon_types_success_probabilities: List[List[float]]) -> None:
    """
    Проверяет входные данные задачи на корректность.

    :param targets: список целей
    :param targets_values: список значимости каждой цели
    :param weapon_types: список типов оружий
    :param weapon_types_amount: список количества оружий каждого типа
    :param weapon_types_success_probabilities: список списков вероятности поражения целей для каждого типа оружия
    """
    assert len(targets) != 0, "Не указаны цели!"
    assert len(weapon_types) != 0, "Не указаны типы оружий!"
    assert len(targets) == len(targets_values), \
        f"Каждой цели {targets} должно соответствовать ее значимость {targets_values}"
    assert len(weapon_types) == len(weapon_types_amount), \
        f"Каждому типу оружий {weapon_types} должно соответствовать его количество {weapon_types_amount}"
    assert len(weapon_types_success_probabilities) == len(weapon_types), \
        f"Вероятности поражения целей {weapon_types_success_probabilities} " \
        f"не соответсвуют количеству оружий {len(weapon_types)}"
    for type_probabilities, type_name in zip(weapon_types_success_probabilities, weapon_types):
        assert len(type_probabilities) == len(targets), \
            f"Вероятности поражения {type_probabilities} для типа \"{type_name}\" не соответсвуют количеству целей"


def weapons(weapon_types: List[str],
            weapon_types_amount: List[int]) -> List[str]:
    """
    :param weapon_types: список типов оружий
    :param weapon_types_amount: список количества оружий каждого типа
    :return: список всех оружий с учетом их повторения
    """
    res = []
    for weapon_type, amount in zip(weapon_types, weapon_types_amount):
        res.extend(repeat(weapon_type, amount))
    return res


def solution_matrix(solution: List[int], n: int) -> List[List[str]]:
    """
    :param solution: решение задачи
    :param n: количество целей
    :return: матрица назначения
    """
    return [
        [
            "1" if index == index_selected - 1 else "0"
            for index in range(n)
        ]
        for index_selected in solution
    ]

