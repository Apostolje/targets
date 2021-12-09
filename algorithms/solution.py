from dataclasses import dataclass
from functools import cached_property
from random import randint

from algorithms import Task


@dataclass(frozen=True)
class Solution:
    task: Task
    iterations_passed: int  # число_выполненных_итераций
    value: float  # значение_цф
    assignment: tuple[int]  # список_назначений

    def __eq__(self, other):
        return \
            other is not None and \
            self.task == other.task and \
            self.value == other.value and \
            self.assignment == other.assignment

    @cached_property
    def solution_matrix(self) -> list[list[str]]:
        """:return: матрица назначения"""
        return [
            [
                "1" if index == index_selected - 1 else "0"
                for index in range(self.task.targets_amount)
            ]
            for index_selected in self.assignment
        ]

    @cached_property
    def text(self) -> str:
        assignment = self.assignment
        targets = self.task.targets
        individual_weapons = self.task.individual_weapons

        return "\n".join([
            f'{weapon}: {targets[target_index - 1]}'
            for weapon, target_index in zip(individual_weapons, assignment)
        ])

    @staticmethod
    def generate_random_solution(task: Task):
        assignment = Solution.generate_random_assignment(
            task.targets_amount,
            task.weapons_total_amount
        )
        solution = Solution(
            task,
            0,
            task.objective_function(assignment),
            assignment
        )
        return solution

    @staticmethod
    def generate_random_assignment(
            n: int,
            k: int,
            mutable=False
    ) -> tuple[int, ...] | list[int]:
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
        if not mutable:
            return tuple(
                randint(1, n)
                for _ in range(k)
            )
        else:
            return [
                randint(1, n)
                for _ in range(k)
            ]
