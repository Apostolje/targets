import math
from random import randint

from algorithms import Solution
from .utils import random_coefficients, int_in_bounds, ints_in_bounds_ordered


class Chromosome:

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

    def __len__(self):
        return len(self.genes)

    def __repr__(self):
        return str(self.genes)

    def mutate(self):
        """Оператор мутации хромосомы."""
        n = len(self.genes)
        mutations = int(n * 0.2)  # количество изменений в хромосоме

        coefficients = random_coefficients(3)
        inverse_size = math.ceil(coefficients[0] * mutations)
        swap_size = math.ceil(coefficients[1] * mutations)
        random_size = math.ceil(coefficients[2] * mutations)

        self.inverse(inverse_size)
        self.swap(swap_size)
        self.random(random_size)

    def inverse(self, size: int):
        """
        Оператор зеркальной мутации.
        В результате данной мутации часть генов хромосомы инвертируется.

        :param size: размер инвертируемой области генов.
        """
        if size <= 1:
            return

        a = randint(0, len(self.genes) - 1 - size)
        b = a + size
        self.genes[a:b] = self.genes[a:b][::-1]

    def swap(self, n: int):
        """
        Оператор обменной мутации.
        В результате данной мутации выполняется n обменов генов.

        :param n: количество обменов.
        """
        for _ in range(n):
            a, b = int_in_bounds(0, len(self.genes) - 1)
            self.genes[a], self.genes[b] = self.genes[b], self.genes[a]

    def random(self, n: int):
        """
        Оператор случайной мутации.
        В результате данной мутации n генам присваивается случайное значение
        из отрезка [1, targets_amount].

        :param n: количество изменяемых генов.
        """
        for _ in range(n):
            i = randint(0, len(self.genes) - 1)
            self.genes[i] = randint(1, self.targets_amount)

    @staticmethod
    def crossover(parent1,
                  parent2):
        """
        Оператор двухточечного кроссинговера.

        :param parent1: 1-я родительская хромосома
        :param parent2: 2-я родительская хромосома
        :return: пара дочерних хромосом.
        """
        start, end = ints_in_bounds_ordered(0, len(parent1))

        child1_genes = [*parent1.genes[:start], *parent2.genes[start:end], *parent1.genes[end:]]
        child2_genes = [*parent2.genes[:start], *parent1.genes[start:end], *parent2.genes[end:]]

        child1 = Chromosome(targets_amount=parent1.targets_amount, genes=child1_genes)
        child2 = Chromosome(targets_amount=parent1.targets_amount, genes=child2_genes)

        return child1, child2
