from functools import cached_property
from itertools import chain
from typing import Literal

import networkx as nx
import numpy as np

from networkx.drawing.layout import rescale_layout

from ui.src.hypergraph_visualizers import Axes, \
    HypergraphVisualizer, Solution
from ui.src.hypergraph_visualizers.utils import node_color


class Koenig(HypergraphVisualizer):
    """
    Кенигово представление гиперграфа

    Гиперграф представляется в виде двудольного графа, в котором
    первая доля вершин состоит из исходных вершин гиперграфа, а
    вторая - из гиперребер гиперграфа.

    Особенности реализации:
        1) Верхний ряд представляет собой ребра гиперграфа
        2) Нижний ряд - исходные вершины гиперграфа
    """

    DEFAULT_NODE_COLOR: Literal["black"] = "black"

    def __init__(self):
        super().__init__()

        # noinspection PyMethodMayBeStatic
        class FakeGraph:

            def is_directed(self):
                return False

            def is_multigraph(self):
                return False

            @cached_property
            def adj(self):
                return {}

        self.graph = FakeGraph()

        self.nodelist: list[str] = []
        self.edgelist: list[tuple[str, str]] = []

        self.edge_nodes_set: set[str] = set()
        self.edge_nodes: list[str] = []
        self.node_color = []
        self.node_size = []
        self.edge_labels = []
        self.pos = {}

    def _draw(self, axes: Axes, solution: Solution):
        axes.set_axis_off()
        generic_kwargs = dict(
            G=self.graph,
            pos=self.pos,
            ax=axes
        )
        nx.draw_networkx_nodes(
            nodelist=self.nodelist,
            node_color=self.node_color,
            node_size=self.node_size,
            **generic_kwargs
        )
        nx.draw_networkx_edges(
            nodelist=self.nodelist,
            edgelist=self.edgelist,
            label="kek",
            **generic_kwargs
        )
        nx.draw_networkx_edge_labels(
            edge_labels=self.edge_labels,
            label_pos=0.93,
            **generic_kwargs
        )
        self.draw_labels(axes, self.pos)

    # TODO улучшить скейлинг шрифта
    def draw_labels(self, axes: Axes, pos: dict):
        for node, (x, y) in pos.items():
            axes.text(
                x,
                y + (0.1 if node in self.edge_nodes_set else -0.1),
                node,
                size=10,
                color="k",
                family="sans-serif",
                weight="normal",
                alpha=None,
                horizontalalignment="center",
                verticalalignment="center",
                transform=axes.transData,
                bbox=None,
                clip_on=True,
            )

    def _calculate_task_layout(self, solution: Solution):
        task = solution.task

        self.pos = Koenig.bipartite_layout(
            top=task.targets,
            bottom=task.individual_weapons,
        )
        self.nodelist = list(self.pos.keys())
        self.node_color = node_color(task)
        self.edge_nodes_set = set(task.targets)

    def _calculate_solution_layout(self, solution: Solution):
        individual_weapons = solution.task.individual_weapons
        targets = solution.task.targets
        assignment = solution.assignment
        probabilities = solution.task.individual_weapons_success_probabilities

        self.edgelist = [
            (weapon, targets[target_index - 1])
            for weapon, target_index in zip(individual_weapons, assignment)
        ]
        self.node_size = 300
        self.edge_labels = {
            (weapon, target): probabilities[weapon][target]
            for (weapon, target) in self.edgelist
        }

    @staticmethod
    def bipartite_layout(top, bottom, scale=1, aspect_ratio=4 / 3):
        top, bottom = bottom, top
        height = 1
        width = aspect_ratio * height
        offset = (width / 2, height / 2)

        left_xs = np.repeat(0, len(top))
        right_xs = np.repeat(width, len(bottom))
        left_ys = np.linspace(0, height, len(top))
        right_ys = np.linspace(0, height, len(bottom))

        top_pos = np.column_stack([left_xs, left_ys]) - offset
        bottom_pos = np.column_stack([right_xs, right_ys]) - offset

        pos = np.concatenate([top_pos, bottom_pos])
        pos = rescale_layout(pos, scale=scale) + np.zeros(2)
        pos = np.flip(pos, 1)
        pos = dict(zip(chain(top, bottom), pos))
        return pos

    @property
    def description(self) -> str:
        return "Кёнигово представление гиперграфа"
