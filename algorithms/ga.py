import random
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List, Iterator, Tuple

from .algorithm import Algorithm
from .chromosome import Chromosome
from .targets import assert_task_is_correct, find_survival
from .utils import invert_probabilities, max_value_index


class GeneticAlgorithm(Algorithm, ABC):

    def __init__(self,
                 targets: List[str],
                 targets_values: List[int],
                 weapon_types: List[str],
                 weapon_types_amount: List[int],
                 weapon_types_success_probabilities: List[List[float]],
                 np: int,
                 ni: int,
                 mp: float):
        """
        :param targets: список целей
        :param targets_values: список значимости каждой цели
        :param weapon_types: список типов оружий
        :param weapon_types_amount: список количества оружий каждого типа
        :param weapon_types_success_probabilities: список списков вероятности
        поражения целей для каждого типа оружия
        :param np: количество хромосом в популяции
        :param ni: число выполняемых итераций без улучшений
        :param mp: вероятность мутации
        """
        super(GeneticAlgorithm, self).__init__()
        assert_task_is_correct(
            targets=targets,
            targets_values=targets_values,
            weapon_types=weapon_types,
            weapon_types_amount=weapon_types_amount,
            weapon_types_success_probabilities=weapon_types_success_probabilities
        )
        assert np > 0, "Размер популяции должен быть больше 0"
        assert ni > 0, "Максимальное число итераций без улучшений должно быть больше 0"
        assert 0 <= mp <= 1, "Вероятность мутации должна лежать в отрезке [0, 1](оптимальное значение = 0.23)"

        self.targets = targets
        self.targets_values = targets_values
        self.weapon_types = weapon_types
        self.weapon_types_amount = weapon_types_amount
        self.weapon_types_success_probabilities = weapon_types_success_probabilities
        self.weapon_types_survival_probabilities = invert_probabilities(weapon_types_success_probabilities)
        self.max_survival = sum(targets_values)
        self.np = np
        self.ni = ni
        self.mp = mp

        self.iterations_passed = 0
        self.iterations_with_no_improvement = 0
        self.best_value = 0.
        self.best_chromosome: Chromosome = None

        self.population: List[Chromosome] = []
        self.population_fitness: List[float] = []

    def run(self) -> Iterator[Tuple[int, float, List[int]]]:
        while not self.done:
            yield self.run_iteration()

    @property
    def done(self) -> bool:
        """:return: выполнилось ли условие остановки алгоритма"""
        return self.iterations_with_no_improvement >= self.ni

    @property
    def targets_amount(self) -> int:
        """:return: общее число целей"""
        return len(self.targets)

    @property
    @lru_cache(maxsize=1)
    def weapons_total_amount(self) -> int:
        """:return: общее число оружий всех типов"""
        return sum(self.weapon_types_amount)

    def run_iteration(self) -> Tuple[int, float, List[int]]:
        if self.iterations_passed == 0:
            self.initialize_population()
        self.run_selection()
        self.mutate_population()
        self.population_fitness = self.find_chromosomes_fitness(self.population)
        self.update_state()
        return self.iterations_passed, self.best_value, self.best_chromosome.genes

    def initialize_population(self):
        self.population = self.generate_chromosomes()
        self.population_fitness = self.find_chromosomes_fitness(
            chromosomes=self.population
        )

    def generate_chromosomes(self) -> List[Chromosome]:
        """:return: генерация случайных хромосом."""
        return [
            Chromosome(
                targets_amount=self.targets_amount,
                weapons_total_amount=self.weapons_total_amount)
            for _ in range(self.np)
        ]

    def find_chromosomes_fitness(self, chromosomes: List[Chromosome]) -> List[float]:
        """
        :param chromosomes: популяция хромосом, для которых необходимо найти приспособленность
        :return: список значения приспособленности для каждой хромосомы заданной популяции
        """
        return [
            self.find_chromosome_fitness(chromosome)
            for chromosome in chromosomes
        ]

    @abstractmethod
    def run_selection(self):
        """Выполняет селекцию, в ходе которой старая популяция заменяется новой."""
        ...

    def mutate_population(self):
        """Мутирует хромосомы популяции с заданной вероятностью."""
        for chromosome in self.population:
            if random.random() <= self.mp:
                chromosome.mutate()

    def find_chromosome_fitness(self, chromosome: Chromosome) -> float:
        """
        :param chromosome: хромосома, для которой необходимо найти приспособленность
        :return: значение приспособленности заданного хромосомы
        """
        max_survival = self.max_survival
        survival = self.find_survival(chromosome)
        return (max_survival - survival) / max_survival

    def find_survival(self, chromosome: Chromosome) -> float:
        """
        :param chromosome: хромосома, для которой ищется значение выживаемости.
        :return: значение выживаемости целей
        """
        return find_survival(
            targets_total=len(self.targets),
            targets_values=self.targets_values,
            weapon_types_amount=self.weapon_types_amount,
            weapon_types_survival_probabilities=self.weapon_types_survival_probabilities,
            solution=chromosome.genes
        )

    def update_state(self):
        """Обновляет состояние алгоритма."""
        current_best_value, current_best_index = max_value_index(self.population_fitness)
        current_best_chromosome = self.population[current_best_index]

        if self.best_value < current_best_value:
            self.best_value = current_best_value
            self.best_chromosome = current_best_chromosome
            self.iterations_with_no_improvement = 0
        else:
            self.iterations_with_no_improvement += 1

        self.iterations_passed += 1
