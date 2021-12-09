from algorithms import Solution

from abc import ABC, abstractmethod

from matplotlib.axes import Axes


class HypergraphVisualizer(ABC):
    """
    Базовый для всех способов отрисовки гиперграфа класс
    """

    def __init__(self):
        self.solution: Solution | None = None  # последнее отрисованное решение

    def draw(self, axes: Axes, solution: Solution):
        """
        Отрисовывает задачу с заданным решением
        """
        self._prepare_to_draw(solution)
        self._draw(axes, solution)
        self.solution = solution

    def draw_ignore_previously_drawn(self, axes: Axes, solution: Solution):
        self._calculate_task_layout(solution)
        self._calculate_solution_layout(solution)
        self._draw(axes, solution)

        self.solution = solution

    def _prepare_to_draw(self, solution: Solution):
        """
        Подготовка к отрисовке: вычисление разметки.

        Разметка не будет заново вычислена, если рисуется одна и та же задача и
        одно и то же решение.
        """
        if self.solution is None or solution.task != self.solution.task:
            self._calculate_task_layout(solution)
            self._calculate_solution_layout(solution)

        elif solution != self.solution:
            self._calculate_solution_layout(solution)

    @abstractmethod
    def _calculate_task_layout(self, solution: Solution):
        """Вычисление разметки гиперграфа с учетом условий задачи"""
        ...

    @abstractmethod
    def _calculate_solution_layout(self, solution: Solution):
        """Вычисление разметки гиперграфа с учетом решения для задачи"""
        ...

    @abstractmethod
    def _draw(self, axes: Axes, solution: Solution):
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """:return: краткое описание этого способа отрисовки"""
        ...
