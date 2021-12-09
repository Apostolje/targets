import math
import random

from algorithms import Solution, Task
from typing import Iterator

from .algorithm import Algorithm
from .antibody import Antibody
from .utils import max_value_index


class ImmuneAlgorithm(Algorithm):
    CLONALG_INTENSITY_COEFFICIENT = 3

    def __init__(self, task: Task, np: int, ni: int, ci: float):
        """
        :param np: количество антител в популяции
        :param ni: число выполняемых итераций без улучшений
        :param ci: коэффициент интенсивности мутации
        """
        super(ImmuneAlgorithm, self).__init__()
        assert np > 0, "Размер популяции должен быть больше 0"
        assert ni > 0, "Максимальное число итераций без улучшений должно быть больше 0"
        assert ci > 0, "Коэффициент интенсивности мутации должен быть больше 0 (оптимальное значение = 2.7)"

        self.task = task
        self.np = np
        self.ni = ni
        self.ci = ci

        self.iterations_passed = 0
        self.iterations_with_no_improvement = 0
        self.best_value = 0.
        self.best_antibody = Antibody(
            targets_amount=self.task.targets_amount,
            weapons_total_amount=self.task.weapons_total_amount
        )

        self.population: list[Antibody] = []
        self.population_affinity: list[float] = []

    def run(self) -> Iterator[Solution]:
        while not self.done:
            yield self.run_iteration()

    @property
    def done(self) -> bool:
        """:return: выполнилось ли условие остановки алгоритма"""
        return self.iterations_with_no_improvement >= self.ni

    def initialize_population(self):
        """Создание начальной популяции, поиск ее аффинности."""
        self.population = [
            Antibody(
                targets_amount=self.task.targets_amount,
                weapons_total_amount=self.task.weapons_total_amount
            )
            for _ in range(self.np)
        ]
        self.population_affinity = self.find_antibodies_affinity(self.population)

    def find_antibodies_affinity(self, antibodies) -> list[float]:
        """
        :param antibodies: популяция антител, для которых необходимо найти аффинность
        :return: список значения аффинности для каждого антитела заданной популяции
        """
        return [
            self.find_antibody_affinity(antibody)
            for antibody in antibodies
        ]

    def run_iteration(self) -> Solution:
        if self.iterations_passed == 0:
            self.initialize_population()
        self.make_clones_and_replace()
        self.update_state()
        return Solution(
            self.task,
            self.iterations_passed,
            self.best_value,
            tuple(self.best_antibody.genes)
        )

    def find_antibody_affinity(self, antibody) -> float:
        """
        :param antibody: антитело, для которого необходимо аффинность
        :return: значение аффинности заданного антитела
        """
        return self.task.objective_function(antibody.genes)

    def make_clones_and_replace(self):
        for i, (antibody, affinity) in enumerate(zip(self.population, self.population_affinity)):
            clones: list[Antibody] = antibody.clones(self.np)

            # мутация случайного клона по схеме clonalg
            clone = random.choice(clones)
            intensity = math.exp(-ImmuneAlgorithm.CLONALG_INTENSITY_COEFFICIENT * affinity)
            clone.clonalg_mutate(intensity)

            # мутация всех клонов
            intensity = (self.iterations_with_no_improvement / self.ni + 0.01) * self.ci
            for clone in clones:
                clone.mutate(intensity)

            # замена оригинального антитела улучшенным клоном
            clones_affinity = self.find_antibodies_affinity(clones)
            best_clone_affinity, best_index = max_value_index(clones_affinity)
            best_clone = clones[best_index]
            if best_clone_affinity > affinity:
                self.population[i] = best_clone
                self.population_affinity[i] = best_clone_affinity

    def update_state(self):
        """Обновляет состояние алгоритма."""
        current_best_value, current_best_index = max_value_index(self.population_affinity)
        current_best_antibody = self.population[current_best_index]

        if self.best_value < current_best_value:
            self.best_value = current_best_value
            self.best_antibody = current_best_antibody
            self.iterations_with_no_improvement = 0
        else:
            self.iterations_with_no_improvement += 1

        self.iterations_passed += 1
