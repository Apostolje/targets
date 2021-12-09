from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontMetrics, QFont
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

FM = QFontMetrics(QFont("Ubuntu", 11))


def fill_interactive_table(
        table: QTableWidget,
        row_headers: list[str] | tuple[str, ...],
        col_headers: list[str] | tuple[str, ...],
        data: list[list[str | float]] | tuple[tuple[str | float, ...], ...],
        on_data_change: Callable[[int, int, str], None]):
    """Заполняет заданную таблицу данными"""
    fill_table(table, row_headers, col_headers, data)

    def wrapper(c: QTableWidgetItem):
        new_value = c.text()
        on_data_change(c.row(), c.column(), new_value)

    table.itemChanged.connect(wrapper)

    max_header_width = max(FM.width(header) for header in row_headers) + 24
    set_minimal_size(table, header_width=max_header_width)


def fill_table(
        table: QTableWidget,
        row_headers: list[str] | tuple[str, ...],
        col_headers: list[str] | tuple[str, ...],
        data: list[list[str | float]] | tuple[tuple[str | float, ...], ...],
        highlight_non_zero: bool = False):
    """Заполняет заданную таблицу данными"""
    n_rows = len(row_headers)
    n_cols = len(col_headers)
    assert len(data) == n_rows, f"len({data}) != {n_rows}"
    for row in data:
        assert len(row) == n_cols, f"len({row}) != {n_cols}"

    table.setRowCount(n_rows)
    table.setColumnCount(n_cols)
    table.setHorizontalHeaderLabels(col_headers)
    table.setVerticalHeaderLabels(row_headers)
    for i in range(n_cols):
        table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
    for i in range(n_rows):
        table.verticalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            item = QTableWidgetItem()
            if isinstance(data[i][j], float):
                item.setText(str(data[i][j]))
            else:
                item.setText(data[i][j])
            item.setTextAlignment(Qt.AlignCenter)

            if highlight_non_zero:
                if value != "" and value != "0":
                    item.setBackground(QColor(30, 144, 255))

            table.setItem(i, j, item)


# TODO пофиксить ресайз
def set_minimal_size(table: QTableWidget, header_width: int):
    """Изменяет размер таблицы таким образом, чтобы она занимала минимальное место."""
    table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    table.resizeColumnsToContents()

    width = header_width
    for i in range(table.columnCount()):
        width += table.columnWidth(i)

    height = table.verticalHeader().length() + table.horizontalHeader().height() + 2

    table.setFixedSize(width, height)
