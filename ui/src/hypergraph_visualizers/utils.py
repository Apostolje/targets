from typing import Iterable

from matplotlib import colors, cm

from algorithms import Task


def create_color_mapping(a: Iterable[int], cmap):
    """
    :param a: последовательность целых чисел
    :return: список цветов
    """
    low, *_, high = sorted(a)
    norm = colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap(cmap))
    return [
        mapper.to_rgba(n)
        for n in a
    ]


def node_color(task: Task):
    res = []
    i = task.targets_amount + len(task.weapon_types) - 1
    for amount in task.weapon_types_amount:
        for _ in range(amount):
            res.append(i)
        i -= 1
    for _ in task.targets:
        res.append(i)
        i -= 1
    return create_color_mapping([
        *res[:task.weapons_total_amount],
        *res[-task.targets_amount:][::-1]
    ], "jet")
