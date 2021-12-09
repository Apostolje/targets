import random
from functools import lru_cache
from typing import List, Iterator, Tuple

import math

from .algorithm import Algorithm
from .antibody import Antibody
from .targets import find_survival, assert_task_is_correct
from .utils import max_value_index, invert_probabilities


class ImmuneAlgorithm(Algorithm):
    CLONALG_INTENSITY_COEFFICIENT = 3

    def __init__(self,
                 targets: List[str],
                 targets_values: List[int],
                 weapon_types: List[str],
                 weapon_types_amount: List[int],
                 weapon_types_success_probabilities: List[List[float]],
                 np: int,
                 ni: int,
                 ci: float
                 ):
        """
        :param targets: список целей
        :param targets_values: список значимости каждой цели
        :param weapon_types: список типов оружий
        :param weapon_types_amount: список количества оружий каждого типа
        :param weapon_types_success_probabilities: список списков вероятности
        поражения целей для каждого типа оружия
        :param np: количество антител в популяции
        :param ni: число выполняемых итераций без улучшений
        :param ci: коэффициент интенсивности мутации
        """
        super(ImmuneAlgorithm, self).__init__()
        assert_task_is_correct(
            targets=targets,
            targets_values=targets_values,
            weapon_types=weapon_types,
            weapon_types_amount=weapon_types_amount,
            weapon_types_success_probabilities=weapon_types_success_probabilities
        )
        assert np > 0, "Размер популяции должен быть больше 0"
        assert ni > 0, "Максимальное число итераций без улучшений должно быть больше 0"
        assert ci > 0, "Коэффициент интенсивности мутации должен быть больше 0 (оптимальное значение = 2.7)"

        self.targets = targets
        self.targets_values = targets_values
        self.weapon_types = weapon_types
        self.weapon_types_amount = weapon_types_amount
        self.weapon_types_success_probabilities = weapon_types_success_probabilities
        self.weapon_types_survival_probabilities = invert_probabilities(weapon_types_success_probabilities)
        self.max_survival = sum(targets_values)
        self.np = np
        self.ni = ni
        self.ci = ci

        self.iterations_passed = 0
        self.iterations_with_no_improvement = 0
        self.best_value = 0.
        self.best_antibody: Antibody = None

        self.population: List[Antibody] = []
        self.population_affinity: List[float] = []

    def run(self) -> Iterator[Tuple[int, float, List[int]]]:
        while not self.done:
            yield self.run_iteration()

    @property
    @lru_cache(maxsize=1)
    def weapons_total_amount(self) -> int:
        """:return: общее число оружий всех типов"""
        return sum(self.weapon_types_amount)

    @property
    def targets_amount(self) -> int:
        """:return: общее число целей"""
        return len(self.targets)

    @property
    def done(self) -> bool:
        """:return: выполнилось ли условие остановки алгоритма"""
        return self.iterations_with_no_improvement >= self.ni

    def generate_antibodies(self) -> List[Antibody]:
        """:return: генерация случайных антител."""
        return [
            Antibody(
                targets_amount=self.targets_amount,
                weapons_total_amount=self.weapons_total_amount)
            for _ in range(self.np)
        ]

    def initialize_population(self):
        """Создание начальной популяции, поиск ее аффинности."""
        self.population = self.generate_antibodies()
        self.population_affinity = self.find_antibodies_affinity(
            antibodies=self.population,
        )

    def find_antibodies_affinity(self, antibodies) -> List[float]:
        """
        :param antibodies: популяция антител, для которых необходимо найти аффинность
        :return: список значения аффинности для каждого антитела заданной популяции
        """
        return [
            self.find_antibody_affinity(antibody)
            for antibody in antibodies
        ]

    def run_iteration(self) -> Tuple[int, float, List[int]]:
        if self.iterations_passed == 0:
            self.initialize_population()
        self.make_clones_and_replace()
        self.update_state()
        return self.iterations_passed, self.best_value, self.best_antibody.genes

    def find_antibody_affinity(self, antibody) -> float:
        """
        :param antibody: антитело, для которого необходимо аффинность
        :return: значение аффинности заданного антитела
        """
        max_survival = self.max_survival
        survival = self.find_survival(antibody)
        return (max_survival - survival) / max_survival

    def find_survival(self, antibody: Antibody) -> float:
        """
        :param antibody: антитело, для которого ищется значение выживаемости.
        :return: значение выживаемости целей
        """
        return find_survival(
            targets_total=len(self.targets),
            targets_values=self.targets_values,
            weapon_types_amount=self.weapon_types_amount,
            weapon_types_survival_probabilities=self.weapon_types_survival_probabilities,
            solution=antibody.genes
        )

    def make_clones_and_replace(self):
        for i, (antibody, affinity) in enumerate(zip(self.population, self.population_affinity)):
            clones: List[Antibody] = antibody.clones(self.np)

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
