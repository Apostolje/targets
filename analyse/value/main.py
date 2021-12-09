# TODO пофиксить Task
# ЗАПУСКАТЬ ЧЕРЕЗ PYPY!


import json

from algorithms import Task, ImmuneAlgorithm, GADarwin, GADeVries

FILE = "results.json"
RUNS_PER_TASK = 10
BCA_NP = 13
GA_NP = 100
CI = 2.7
MP = 0.20
NI = 500

tasks = [
    Task.generate_random_task(
        min_n_targets=n,
        max_n_targets=n,
        min_n_weapon_amount=1,
        max_n_weapon_amount=1,
        min_n_weapon_type=n,
        max_n_weapon_type=n,
        min_target_value=10,
        max_target_value=100,
        min_success_probability=0.1,
        max_success_probability=1.0
    )
    for n in range(10, 100 + 1, 10)
]

bca = []
for task in tasks:
    for i in range(RUNS_PER_TASK):
        alg = ImmuneAlgorithm(*task, np=BCA_NP, ni=NI, ci=CI)
        for _, value, _ in alg.run():
            continue
        size = len(task[0])
        print(f"{i + 1}) {size} [bca] {value:.5f}")
        bca.append({"size": size, "value": value})

gaDarwin = []
for task in tasks:
    for i in range(RUNS_PER_TASK):
        alg = GADarwin(*task, np=GA_NP, ni=NI, mp=MP)
        for _, value, _ in alg.run():
            continue
        size = len(task[0])
        print(f"{i + 1}) {size} [gaDarwin] {value:.5f}")
        gaDarwin.append({"size": size, "value": value})

gaDeVries = []
for task in tasks:
    for i in range(RUNS_PER_TASK):
        alg = GADeVries(*task, np=GA_NP, ni=NI, mp=MP)
        for _, value, _ in alg.run():
            continue
        size = len(task[0])
        print(f"{i + 1}) {size} [gaDeVries] {value:.5f}")
        gaDeVries.append({"size": size, "value": value})

with open(FILE, "w") as file:
    json.dump({"bca": bca, "gaDarwin": gaDarwin, "gaDeVries": gaDeVries}, file)
