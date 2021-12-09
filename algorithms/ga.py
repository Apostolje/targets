import random

from algorithms import Solution, Task
from abc import ABC, abstractmethod
from typing import Iterator

from .algorithm import Algorithm
from .chromosome import Chromosome
from .utils import max_value_index


class GeneticAlgorithm(Algorithm, ABC):

    def __init__(self, task: Task, np: int, ni: int, mp: float):
        """
        :param np: количество хромосом в популяции
        :param ni: число выполняемых итераций без улучшений
        :param mp: вероятность мутации
        """
        super(GeneticAlgorithm, self).__init__()
        assert np > 0, "Размер популяции должен быть больше 0"
        assert ni > 0, "Максимальное число итераций без улучшений должно быть больше 0"
        assert 0 <= mp <= 1, "Вероятность мутации должна лежать в отрезке [0, 1](оптимальное значение = 0.23)"

        self.task = task
        self.np = np
        self.ni = ni
        self.mp = mp

        self.iterations_passed = 0
        self.iterations_with_no_improvement = 0
        self.best_value = 0.
        self.best_chromosome = Chromosome(
            targets_amount=self.task.targets_amount,
            weapons_total_amount=self.task.weapons_total_amount
        )

        self.population: list[Chromosome] = []
        self.population_fitness: list[float] = []

    def run(self) -> Iterator[Solution]:
        while not self.done:
            yield self.run_iteration()

    @property
    def done(self) -> bool:
        """:return: выполнилось ли условие остановки алгоритма"""
        return self.iterations_with_no_improvement >= self.ni

    def run_iteration(self) -> Solution:
        if self.iterations_passed == 0:
            self.initialize_population()
        self.run_selection()
        self.mutate_population()
        self.population_fitness = self.find_chromosomes_fitness(self.population)
        self.update_state()
        return Solution(
            self.task,
            self.iterations_passed,
            self.best_value,
            tuple(self.best_chromosome.genes)
        )

    def initialize_population(self):
        self.population = [
            Chromosome(
                targets_amount=self.task.targets_amount,
                weapons_total_amount=self.task.weapons_total_amount
            )
            for _ in range(self.np)
        ]
        self.population_fitness = self.find_chromosomes_fitness(
            chromosomes=self.population
        )

    def find_chromosomes_fitness(self, chromosomes: list[Chromosome]) -> list[float]:
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
        return self.task.objective_function(chromosome.genes)

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
