from typing import List, Tuple

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget


class GraphWidget(QWidget):
    TOP_BOTTOM_MARGIN = 40
    POINT_MAX_SIZE = 25
    TYPE_RECT_PADDING = 5
    TARGET_COLOR = QColor(71, 104, 214)
    WEAPON_COLOR = QColor(235, 177, 36)
    TITLE_FONT = QFont('Decorative', 14)
    TITLE_FONT_METRICS = QFontMetrics(TITLE_FONT)
    MIN_LINE_THICKNESS = 1
    MAX_LINE_THICKNESS = 6

    SHORTEST_COLOR = (255, 252, 0)
    LONGEST_COLOR = (237, 110, 26)

    def __init__(self, parent):
        super().__init__(parent)

        self.targets: List[str] = []
        self.weapon_types: List[str] = []
        self.weapon_types_amount: List[int] = []
        self.weapon_types_success_probabilities: List[List[float]] = []
        self.solution = []

    def update_task(self,
                    targets: List[str],
                    weapon_types: List[str],
                    weapon_types_amount: List[int],
                    weapon_types_success_probabilities: List[List[float]]):
        """Обновление условий задачи для правильной отрисовки."""
        self.targets = targets
        self.weapon_types = weapon_types
        self.weapon_types_amount = weapon_types_amount
        self.weapon_types_success_probabilities = weapon_types_success_probabilities
        print(self.targets, self.weapon_types, self.weapon_types_amount)

    def update_solution(self, solution: List[int]):
        """Обновляет виджет новыми данными."""
        self.solution = solution
        for v1, v2 in zip(self.solution, solution):
            if v1 != v2:
                self.update()
                break

    def paintEvent(self, e):
        """Вызывается каждый раз при обновлении update()"""
        targets = self.target_points
        weapons = self.weapon_points
        lines = self.solution_lines(targets, weapons, self.weapon_types_success_probabilities)
        rects = self.rects_around_weapon_points(weapons, self.weapon_types_amount)

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.draw_rects(qp, rects)
        self.draw_lines(qp, lines)
        self.draw_points(qp, targets)
        self.draw_points(qp, weapons)
        self.draw_target_titles(qp, self.targets, targets)
        self.draw_weapon_type_titles(qp, self.weapon_types, rects)
        qp.end()

    def rects_around_weapon_points(self,
                                   weapon_points: List[Tuple[int, int, int, QColor]],
                                   weapon_types_amount: List[int]
                                   ) -> List[Tuple[int, int, int, int, QColor]]:
        rects = []
        shift = 0
        for amount in weapon_types_amount:
            if amount == 0:
                continue

            x1, y1, size1, _ = weapon_points[shift]
            x2, y2, size2, _ = weapon_points[shift + amount - 1]
            rect = (
                x1 - self.TYPE_RECT_PADDING,
                y1 - self.TYPE_RECT_PADDING,
                x2 - x1 + size2 + self.TYPE_RECT_PADDING * 2,
                y2 - y1 + size2 + self.TYPE_RECT_PADDING * 2,
                QColor(160, 160, 160)
            )
            rects.append(rect)
            shift += amount

        return rects

    def solution_lines(self,
                       target_points: List[Tuple[int, int, int, QColor]],
                       weapon_points: List[Tuple[int, int, int, QColor]],
                       probabilities: List[List[float]]
                       ) -> List[Tuple[int, int, int, int, QColor, int]]:
        max_probability = max(max(row) for row in probabilities)
        min_probability = min(min(row) for row in probabilities)

        def line_thickness(prob: float) -> int:
            coefficient = (max_probability - min_probability) \
                          / (self.MAX_LINE_THICKNESS - self.MIN_LINE_THICKNESS)
            return int((prob - min_probability) // coefficient)

        lines = []
        weapon_type = 0
        weapon_type_i = 0
        for i, target_selected in enumerate(self.solution):
            if target_selected == 0:
                break

            if self.weapon_types_amount[weapon_type] == 0:
                continue

            probability = probabilities[weapon_type][target_selected - 1]
            thickness = line_thickness(probability)

            x1, y1, size1, _ = weapon_points[i]
            x2, y2, size2, _ = target_points[target_selected - 1]

            x1, y1 = x1 + size1 // 2, y1 + size1 // 2
            x2, y2 = x2 + size2 // 2, y2 + size2 // 2

            lines.append((x1, y1, x2, y2, QColor(128, 128, 128), thickness))

            weapon_type_i += 1
            if self.weapon_types_amount[weapon_type] == weapon_type_i:
                weapon_type_i = 0
                weapon_type += 1

        return lines

    @property
    def target_points(self) -> List[Tuple[int, int, int, QColor]]:
        w, h = self.size().width(), self.size().height()
        n_targets = len(self.targets)

        space = w // n_targets  # занимаемое с отступами место
        if space > self.POINT_MAX_SIZE:
            gap = space - self.POINT_MAX_SIZE
            size = self.POINT_MAX_SIZE
        else:
            gap = 0
            size = space

        return [
            (i * gap + gap // 2 + i * size,
             self.TOP_BOTTOM_MARGIN,
             size,
             self.TARGET_COLOR
             )
            for i in range(n_targets)
        ]

    @property
    def weapon_points(self) -> List[Tuple[int, int, int, QColor]]:
        w, h = self.size().width(), self.size().height()
        n_weapons = sum(self.weapon_types_amount)

        space = w // n_weapons  # занимаемое с отступами место
        if space > self.POINT_MAX_SIZE:
            gap = space - self.POINT_MAX_SIZE
            size = self.POINT_MAX_SIZE
        else:
            gap = 0
            size = space

        return [
            (i * gap + gap // 2 + i * size,
             h - self.TOP_BOTTOM_MARGIN - size,
             size,
             self.WEAPON_COLOR
             )
            for i in range(n_weapons)
        ]

    @staticmethod
    def draw_points(qp: QPainter,
                    points: List[Tuple[int, int, int, QColor]]):
        for x, y, size, color in points:
            qp.setBrush(color)
            qp.setPen(size)
            qp.drawEllipse(x, y, size, size)

    @staticmethod
    def draw_lines(qp: QPainter, lines: List[Tuple[int, int, int, int, QColor, int]]):
        for x1, y1, x2, y2, color, thickness in lines:
            qp.setPen(QPen(color, thickness, Qt.SolidLine))
            qp.drawLine(x1, y1, x2, y2)

    def draw_target_titles(self,
                           qp: QPainter,
                           target_titles: List[str],
                           targets: List[Tuple[int, int, int, QColor]]):
        for title, (x, _, size, _) in zip(target_titles, targets):
            w = self.TITLE_FONT_METRICS.width(title)
            h = self.TITLE_FONT_METRICS.height()
            x = x - w // 2.34 + size // 2
            y = self.TOP_BOTTOM_MARGIN / 2 + h / 2
            qp.drawText(x, y, title)

    def draw_weapon_type_titles(self,
                                qp: QPainter,
                                weapon_type_titles: List[str],
                                rects: List[Tuple[int, int, int, int, QColor]]):
        for title, (x, _, rect_w, rect_h, _) in zip(weapon_type_titles, rects):
            title = f'Тип "{title}"'
            w = self.TITLE_FONT_METRICS.width(title)
            h = self.TITLE_FONT_METRICS.height()
            x = x - w // 2.5 + rect_w // 2
            y = self.height() - self.TOP_BOTTOM_MARGIN / 2 + h / 2
            qp.drawText(x, y, title)

    @staticmethod
    def draw_rects(qp: QPainter,
                   rects: List[Tuple[int, int, int, int, QColor]]):
        for rect in rects:
            x, y, w, h, color = rect
            qp.setBrush(color)
            qp.drawRect(x, y, w, h)

    def color_by_value(self, value, min_value, max_value):
        return self.convert_to_rgb(min_value, max_value, value)

    def convert_to_rgb(self, min_value, max_value, val):
        colors = [self.SHORTEST_COLOR, self.LONGEST_COLOR]
        fi = float(val - min_value) / float(max_value - min_value) * (len(colors) - 1)
        i = int(fi)
        f = fi - i
        if f < sys.float_info.epsilon:
            return colors[i]
        else:
            (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i + 1]
            return (
                int(r1 + f * (r2 - r1)),
                int(g1 + f * (g2 - g1)),
                int(b1 + f * (b2 - b1))
            )
