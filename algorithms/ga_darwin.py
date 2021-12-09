import random

import math

from .chromosome import Chromosome
from .ga import GeneticAlgorithm


def sort_related(lst1: list,
                 lst2: list,
                 reverse: bool = False) -> tuple[list, list]:
    """
    Возвращает сортированные версии заданных списков.
    Сортируются списки по значениям 1го списка. Значения 2го списка связаны со значениями 1го.
    """
    lst1, lst2 = zip(*sorted(zip(lst1, lst2), key=lambda a: a[0], reverse=reverse))
    return lst1, lst2


class GADarwin(GeneticAlgorithm):
    ELITE_SIZE = 0.01  # количество элитных хромосом

    def run_selection(self):
        new_population = []
        new_fitness = []

        n = self.np
        n_elite = math.ceil(n * self.ELITE_SIZE)
        n_children = n - n_elite  # количество порождаемых хромосом
        n_parents = n_children + (n_children % 2) * 1
        assert n_parents % 2 == 0

        # сортировка хромосом популяции по значению приспособленности
        self.population_fitness, self.population = \
            sort_related(
                self.population_fitness,
                self.population,
                reverse=True
            )

        # элитные хромосомы становятся частью популяции
        new_population.extend(self.population[:n_elite])
        new_fitness.extend(self.population_fitness[:n_elite])

        # выбор родителей
        parents = [
            self.tournament()
            for _ in range(n_parents)
        ]

        # скрещивание родительских хромосом
        for i in range(0, n_parents, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            child1, child2 = Chromosome.crossover(parent1, parent2)
            new_population.append(child1)
            new_population.append(child2)
        if len(new_population) > n:
            del new_population[-1]

        self.population = new_population
        self.population_fitness = new_fitness

    def tournament(self) -> Chromosome:
        """Турнир размера 4."""
        best_rival = self.population[-1]
        best_rival_fitness = self.population_fitness[-1]
        for _ in range(4):
            i = random.randint(0, self.np - 1)
            rival = self.population[i]
            rival_fitness = self.population_fitness[i]
            if rival_fitness > best_rival_fitness:
                best_rival = rival
                best_rival_fitness = rival_fitness

        return best_rival
