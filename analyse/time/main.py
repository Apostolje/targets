import json
from time import time

from algorithms import generate_random_task, ImmuneAlgorithm, GADarwin, GADeVries, Algorithm

FILE = "results.json"
RUNS_PER_TASK = 10
BCA_NP = 10
GA_NP = 150
CI = 2.7
MP = 0.20
NI = 1000


def run_fixed_iterations(algorithm: Algorithm, iterations: int) -> float:
    """
    Запускает алгоритм на выполнение заданного числа итерации.

    :param algorithm: алгоритм
    :param iterations: количество итераций
    :return: время работы алгоритма в секундах
    """
    start = time()
    for i, _ in enumerate(algorithm.run()):
        if i == iterations - 1:
            break
    stop = time()
    return stop - start


tasks = [
    generate_random_task(min_n_targets=n,
                         max_n_targets=n,
                         min_n_weapon_amount=1,
                         max_n_weapon_amount=1,
                         min_n_weapon_type=n,
                         max_n_weapon_type=n,
                         min_target_value=10,
                         max_target_value=100,
                         min_success_probability=0.1,
                         max_success_probability=1.0)
    for n in range(10, 100 + 1, 10)
]

# ПРОГРЕВ
print("ПРОГРЕВ...")
run_fixed_iterations(ImmuneAlgorithm(*tasks[-1], np=BCA_NP, ni=NI, ci=CI), NI)
run_fixed_iterations(GADarwin(*tasks[-1], np=GA_NP, ni=NI, mp=MP), NI)
run_fixed_iterations(GADeVries(*tasks[-1], np=GA_NP, ni=NI, mp=MP), NI)
print("ПРОГРЕВ ЗАКОНЧЕН")


bca = []
for task in tasks:
    for i in range(RUNS_PER_TASK):
        alg = ImmuneAlgorithm(*task, np=BCA_NP, ni=NI, ci=CI)
        sec = run_fixed_iterations(alg, NI)
        size = len(task[0])
        print(f"{i + 1}) {size} [bca] {sec:.2f} sec")
        bca.append({"size": size, "time": sec})

gaDarwin = []
for task in tasks:
    for i in range(RUNS_PER_TASK):
        alg = GADarwin(*task, np=GA_NP, ni=NI, mp=MP)
        sec = run_fixed_iterations(alg, NI)
        size = len(task[0])
        print(f"{i + 1}) {size} [gaDarwin] {sec:.2f} sec")
        gaDarwin.append({"size": size, "time": sec})

gaDeVries = []
for task in tasks:
    for i in range(RUNS_PER_TASK):
        alg = GADeVries(*task, np=GA_NP, ni=NI, mp=MP)
        sec = run_fixed_iterations(alg, NI)
        size = len(task[0])
        print(f"{i + 1}) {size} [gaDeVries] {sec:.2f} sec")
        gaDeVries.append({"size": size, "time": sec})

with open(FILE, "w") as file:
    json.dump({"bca": bca, "gaDarwin": gaDarwin, "gaDeVries": gaDeVries}, file)
