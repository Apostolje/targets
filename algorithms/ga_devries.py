import random

import math

from .chromosome import Chromosome
from .ga_darwin import GADarwin


class GADeVries(GADarwin):
    # вероятности возникновения катастрофы
    BEFORE_PROBABILITY = 0.019  # перед селекцией
    AFTER_PROBABILITY = 0.011  # после селекции

    # количество погибших в катастрофе (%)
    MIN_DEATHS = 0.3
    MAX_DEATHS = 0.7

    def run_selection(self):
        self.catastrophe(self.BEFORE_PROBABILITY)
        super(GADeVries, self).run_selection()
        self.catastrophe(self.AFTER_PROBABILITY)

    def catastrophe(self, probability: float):
        if random.random() <= probability:
            death_percent = random.uniform(self.MIN_DEATHS, self.MAX_DEATHS)
            n_deaths = math.ceil(self.np * death_percent)

            for _ in range(n_deaths):
                i = random.randrange(0, self.np)
                c = Chromosome(
                    targets_amount=self.targets_amount,
                    weapons_total_amount=self.weapons_total_amount
                )
                self.population[i] = c
                # если у хромосомы изначально было известно ЦФ, то оно пересчитывается
                if len(self.population_fitness) > i:
                    self.population_fitness[i] = self.find_chromosome_fitness(c)
