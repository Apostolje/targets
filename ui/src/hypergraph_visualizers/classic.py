from typing import Literal

import networkx as nx
import hypernetx as hnx
from hypernetx.drawing.rubber_band import layout_node_link

from algorithms import Solution
from ui.src.hypergraph_visualizers import Axes, HypergraphVisualizer
from ui.src.hypergraph_visualizers.utils import node_color


class Classic(HypergraphVisualizer):
    """
    Классическое представление гиперграфа
    """

    DEFAULT_NODE_COLOR: Literal["black"] = "black"

    def __init__(self):
        super().__init__()
        self.hypergraph = hnx.Hypergraph()

        self.edgecolors = []
        self.facecolors = []
        self.pos = {}

    def _draw(self, axes: Axes, solution: Solution):
        hnx.draw(
            self.hypergraph,
            pos=self.pos,
            ax=axes,
            edges_kwargs={
                "edgecolors": self.edgecolors,
            },
            nodes_kwargs={
                "facecolors": self.facecolors,
            },
            node_labels={
                "fontsize": 10,
            }
        )

    def _calculate_task_layout(self, solution: Solution):
        task = solution.task

        color = node_color(task)
        self.edgecolors = color[-task.targets_amount:]
        self.facecolors = color[:task.weapons_total_amount]

    def _calculate_solution_layout(self, solution: Solution):
        individual_weapons = solution.task.individual_weapons
        targets = solution.task.targets
        assignment = solution.assignment

        hypergraph = hnx.Hypergraph()
        for target in targets:
            hypergraph.add_edge(target)

        for weapon, target_index in zip(individual_weapons, assignment):
            hypergraph.add_node_to_edge(weapon, targets[target_index - 1])

        self.hypergraph = hypergraph
        self.pos = layout_node_link(self.hypergraph, layout=nx.spring_layout)

    @property
    def description(self) -> str:
        return "обычное представление графа"
