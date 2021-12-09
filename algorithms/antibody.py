from copy import deepcopy
from random import randint

import math

from algorithms import Solution
from .utils import int_in_bounds, random_coefficients, ints_in_bounds_ordered


class Antibody:

    def __init__(
            self,
            targets_amount: int,
            weapons_total_amount: int | None = None,
            genes: list[int] = None
    ):
        """
        :param targets_amount: количество целей
        :param weapons_total_amount: общее число оружий всех типов
        """
        if genes is None:
            if weapons_total_amount is None:
                raise ValueError

            self.genes = Solution.generate_random_assignment(
                targets_amount,
                weapons_total_amount,
                mutable=True
            )
        else:
            self.genes = genes

        self.targets_amount = targets_amount

    def __repr__(self):
        return str(self.genes)

    def clones(self, n: int) -> list:
        """
        :param n: количество клонов, которое нужно создать
        :return n клонов антитела
        """
        return [
            deepcopy(self)
            for _ in range(n)
        ]

    def inverse(self, size: int, bounds: tuple[int, int] = None):
        """
        Оператор зеркальной мутации.
        В результате данной мутации часть генов антитела инвертируется.

        :param size: размер инвертируемой области генов.
        :param bounds: границы области, в которой выполняется мутация.
        По умолчанию мутация выполняется для всех генов.
        """
        if size <= 1:
            return

        if bounds is None:
            start = 0
            stop = len(self.genes) - 1
        else:
            start, stop = bounds

        if stop - size <= start:
            size = stop - start

        a = randint(start, stop - size)
        b = a + size
        self.genes[a:b] = self.genes[a:b][::-1]

    def swap(self, n: int, bounds: tuple[int, int] = None):
        """
        Оператор обменной мутации.
        В результате данной мутации выполняется n обменов генов.

        :param n: количество обменов.
        :param bounds: границы области, в которой выполняется мутация.
        По умолчанию мутация выполняется для всех генов.
        """

        if bounds is None:
            start = 0
            stop = len(self.genes) - 1
        else:
            start, stop = bounds

        for _ in range(n):
            a, b = int_in_bounds(start, stop)
            self.genes[a], self.genes[b] = self.genes[b], self.genes[a]

    def random(self, n: int, bounds: tuple[int, int] = None):
        """
        Оператор случайной мутации.
        В результате данной мутации n генам присваивается случайное значение
        из отрезка [1, targets_amount].

        :param n: количество изменяемых генов.
        :param bounds: границы области, в которой выполняется мутация.
        По умолчанию мутация выполняется для всех генов.
        """
        if bounds is None:
            start = 0
            stop = len(self.genes) - 1
        else:
            start, stop = bounds

        for _ in range(n):
            i = randint(start, stop)
            self.genes[i] = randint(1, self.targets_amount)

    def clonalg_mutate(self, intensity: float):
        """
        Мутация антитела аналогично методу clonalg.

        :param intensity: интенсивность мутации
        """
        n = len(self.genes)
        mutations = int(0.25 * n * intensity)  # количество изменений

        coefficients = random_coefficients(3)
        inverse_size = math.ceil(coefficients[0] * mutations)
        swap_size = math.ceil(coefficients[1] * mutations)
        random_size = math.ceil(coefficients[2] * mutations)

        self.inverse(inverse_size)
        self.swap(swap_size)
        self.random(random_size)

    def mutate(self, intensity: float):
        """
        Мутация случайной части антитела.

        :param intensity: интенсивность мутации
        """
        n = len(self.genes)
        bounds = ints_in_bounds_ordered(0, n - 1)
        mutations = int(n * intensity)  # количество изменений

        coefficients = random_coefficients(3)
        inverse_size = math.ceil(coefficients[0] * mutations)
        swap_size = math.ceil(coefficients[1] * mutations)
        random_size = math.ceil(coefficients[2] * mutations)

        self.inverse(inverse_size, bounds=bounds)
        self.swap(swap_size, bounds=bounds)
        self.random(random_size, bounds=bounds)
