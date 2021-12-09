import traceback
from typing import List, Callable

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics
from PyQt5.QtWidgets import \
    QTableWidgetItem, QTableWidget, QStyleFactory, QApplication, QPushButton

from algorithms import \
    Algorithm, GADarwin, GADeVries, ImmuneAlgorithm, \
    weapons, solution_matrix, \
    int_or_float, parse_int_param, parse_float_param
from ui import Ui_MainWindow, GenerationWindow


class MainWindow(QtWidgets.QMainWindow):
    DEFAULT_TARGET_NAME = "Цель"
    DEFAULT_TARGET_VALUE = 1
    DEFAULT_WEAPON_TYPE = "Испол."
    DEFAULT_WEAPON_AMOUNT = 1
    DEFAULT_WEAPON_POSSIBILITY = 0.5
    FM = QFontMetrics(QFont("Ubuntu", 11))

    def __init__(self, app_context: QApplication):
        super(MainWindow, self).__init__()
        self.app_context = app_context
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.targets = ["Цель 1", "Цель 2", "Цель 3"]
        self.targets_values = [5, 10, 20]
        self.weapon_types = ["Танк", "Самолет", "Судно"]
        self.weapon_types_amount = [5, 2, 1]
        self.weapons = weapons(self.weapon_types, self.weapon_types_amount)
        self.weapon_types_success_probabilities = [[0.3, 0.2, 0.5],
                                                   [0.1, 0.6, 0.5],
                                                   [0.4, 0.5, 0.4]]
        self.solution = [0] * len(self.weapons)

        self.is_closing = False
        self.is_running = False

        self.ui.immuneButton.clicked.connect(self.start_immune)
        self.ui.gaButton.clicked.connect(self.start_ga)

        self.ui.addTargetButton.clicked.connect(self.add_target)
        self.ui.deleteTargetButton.clicked.connect(self.delete_target)
        self.ui.addWeaponButton.clicked.connect(self.add_weapon_type)
        self.ui.deleteWeaponButton.clicked.connect(self.delete_weapon_type)

        self.ui.generateButton.clicked.connect(self.show_generation_window)

        self.update_task()

    def show_generation_window(self):
        self.disable_buttons()
        s = self

        def handle_generated_task(task):
            (
                s.targets,
                s.targets_values,
                s.weapon_types,
                s.weapon_types_amount,
                s.weapon_types_success_probabilities
            ) = task
            s.weapons = weapons(s.weapon_types, s.weapon_types_amount)
            s.update_task()

        def handle_close(_):
            self.enable_buttons()

        GenerationWindow(self, handle_generated_task, handle_close).show()

    def add_target(self):
        """Добавляет новую цель."""
        self.targets.append(f"{self.DEFAULT_TARGET_NAME} {len(self.targets) + 1}")
        self.targets_values.append(self.DEFAULT_TARGET_VALUE)
        for row in self.weapon_types_success_probabilities:
            row.append(self.DEFAULT_WEAPON_POSSIBILITY)
        self.update_task()

    def delete_target(self):
        """Удаляет последнюю цель."""
        if len(self.targets) == 0:
            raise Exception("Нельзя удалить, т.к. нет целей")
        else:
            self.targets.pop()
            self.targets_values.pop()
            for row in self.weapon_types_success_probabilities:
                row.pop()
            self.update_task()

    def add_weapon_type(self):
        """Добавляет новый тип оружия."""
        self.weapon_types.append(f"{self.DEFAULT_WEAPON_TYPE} {len(self.weapon_types) + 1}")
        self.weapon_types_amount.append(self.DEFAULT_WEAPON_AMOUNT)
        self.weapons = weapons(self.weapon_types, self.weapon_types_amount)
        self.weapon_types_success_probabilities.append(
            [self.DEFAULT_WEAPON_POSSIBILITY for _ in range(len(self.targets))]
        )
        self.update_task()

    def delete_weapon_type(self):
        """Удаляет последний тип оружия."""
        if len(self.weapon_types) == 0:
            raise Exception("Нельзя удалить, т.к. нет оружий")
        else:
            self.weapon_types.pop()
            self.weapon_types_amount.pop()
            self.weapons = weapons(self.weapon_types, self.weapon_types_amount)
            self.weapon_types_success_probabilities.pop()
            self.update_task()

    def start_immune(self):
        """Запускает иммунный алгоритм."""
        try:
            np = parse_int_param("np", self.ui.immuneNp.text())
            ci = parse_float_param("ci", self.ui.immuneCi.text())
            ni = parse_int_param("ni", self.ui.immuneNi.text())

            immune_alg = ImmuneAlgorithm(
                targets=self.targets,
                targets_values=self.targets_values,
                weapon_types=self.weapon_types,
                weapon_types_amount=self.weapon_types_amount,
                weapon_types_success_probabilities=self.weapon_types_success_probabilities,
                np=np,
                ni=ni,
                ci=ci
            )
            self.run_algorithm(immune_alg)
        except BaseException as e:
            self.show_error(e)
            return

    def start_ga(self):
        """Запускает генетический алгоритм."""
        try:
            np = parse_int_param("np", self.ui.gaNp.text())
            mp = parse_float_param("mp", self.ui.gaMp.text())
            ni = parse_int_param("ni", self.ui.gaNi.text())
            evolution = self.ui.evolutionBox.currentText()
            if evolution == "Эволюция Дарвина":
                ga_class = GADarwin
            elif evolution == "Эволюция Де Фриза":
                ga_class = GADeVries
            else:
                raise Exception()

            ga = ga_class(
                targets=self.targets,
                targets_values=self.targets_values,
                weapon_types=self.weapon_types,
                weapon_types_amount=self.weapon_types_amount,
                weapon_types_success_probabilities=self.weapon_types_success_probabilities,
                np=np,
                ni=ni,
                mp=mp
            )
            self.run_algorithm(ga)
        except BaseException as e:
            self.show_error(e)
            return

    def run_algorithm(self, alg: Algorithm):
        """Выполнение заданного алгоритма."""
        self.disable_buttons()

        try:
            last_value = 0
            for iteration, value, solution in alg.run():

                if last_value < value:
                    last_value = value
                    self.solution = solution
                    self.ui.graphWidget.update_solution(self.solution)
                    self.update_solution_table()

                self.ui.result.setText(f'Итерация: {iteration}\n\n'
                                       f'Лучшее решение:\n'
                                       f'{solution}\n\n'
                                       f'Значение ЦФ: {value:.4f}\n\n'
                                       f'{self.text}')

                self.update()
                self.app_context.processEvents()
                if self.is_closing:
                    break

        except BaseException as e:
            self.enable_buttons()
            raise e

        self.enable_buttons()

    @property
    def text(self):
        return "\n".join([
            f'{weapon}: {self.targets[target_index - 1]}'
            for weapon, target_index in zip(self.individual_weapons, self.solution)
        ])

    @property
    def individual_weapons(self):
        rows = []

        weapon_type = self.weapons[0]
        weapon_index = 0
        for i, target_index in enumerate(self.solution):
            if weapon_type == self.weapons[i]:
                weapon_index += 1
            else:
                weapon_index = 1
                weapon_type = self.weapons[i]

            rows.append(f'"{weapon_type}" №{weapon_index}')

        return rows

    def update_solution_table(self):
        """Обновляет содержимое таблицы решения задачи."""
        if len(self.solution) != 0:
            MainWindow.fill_table(
                table=self.ui.solutionTable,
                row_headers=self.individual_weapons,
                col_headers=self.targets,
                data=solution_matrix(self.solution, len(self.targets)),
                highlight_non_zero=True
            )

    def show_error(self, e: BaseException):
        self.ui.result.setText(f"Ошибка:\n\n"
                               f"{e}")
        traceback.print_exc()

    def handle_targets_change(self, row: int, col: int, new_value: str):
        print(f"targets_change: {row} {col}")
        if row == 0:
            if new_value == "":
                del self.targets[col]
                del self.targets_values[col]
                for row in self.weapon_types_success_probabilities:
                    del row[col]
            else:
                self.targets[col] = new_value
        elif row == 1:
            try:
                value = int_or_float(new_value)
                if value >= 0:
                    self.targets_values[col] = value
            except ValueError:
                ...
        else:
            raise Exception
        self.update_task()

    def handle_weapons_change(self, row: int, col: int, new_value: str):
        print(f"weapons_change: {row} {col}")
        if row == 0:
            self.weapon_types[col] = new_value
        elif row == 1:
            try:
                value = int(new_value)
                if value < 0:
                    ...
                elif value == 0:
                    del self.weapon_types_amount[col]
                    del self.weapon_types[col]
                    del self.weapon_types_success_probabilities[col]
                else:
                    self.weapon_types_amount[col] = value
            except ValueError:
                ...
        else:
            raise Exception
        self.weapons = weapons(self.weapon_types, self.weapon_types_amount)
        self.update_task()

    def handle_probabilities_change(self, row: int, col: int, new_value: str):
        print(f"probabilities_change: {row} {col}")
        try:
            value = float(new_value)
            if value > 1:
                self.weapon_types_success_probabilities[row][col] = 1.0
            elif value < 0:
                self.weapon_types_success_probabilities[row][col] = 0.
            else:
                self.weapon_types_success_probabilities[row][col] = value
        except ValueError:
            ...
        self.update_task()

    def update_task(self):
        """Обновляет содержимое таблиц и графа для условий задачи."""
        try:
            self.ui.targetsTable.itemChanged.disconnect()
            self.ui.weaponsTable.itemChanged.disconnect()
            self.ui.possibilitiesTable.itemChanged.disconnect()
        except TypeError:
            ...

        self.solution = [0] * len(self.weapons)
        MainWindow.fill_interactive_table(
            table=self.ui.targetsTable,
            row_headers=["Цель", "Значимость"],
            col_headers=[str(i + 1) for i in range(len(self.targets))],
            data=[
                self.targets,
                [str(i) for i in self.targets_values]
            ],
            on_data_change=self.handle_targets_change
        )
        MainWindow.fill_interactive_table(
            table=self.ui.weaponsTable,
            row_headers=["Тип исполнителя", "Количество"],
            col_headers=[str(i + 1) for i in range(len(self.weapon_types))],
            data=[
                self.weapon_types,
                [str(amount) for amount in self.weapon_types_amount]
            ],
            on_data_change=self.handle_weapons_change
        )
        MainWindow.fill_interactive_table(
            table=self.ui.possibilitiesTable,
            row_headers=self.weapon_types,
            col_headers=self.targets,
            data=self.weapon_types_success_probabilities,
            on_data_change=self.handle_probabilities_change
        )
        self.update_solution_table()
        self.ui.graphWidget.update_task(
            targets=self.targets,
            weapon_types=self.weapon_types,
            weapon_types_amount=self.weapon_types_amount,
            weapon_types_success_probabilities=self.weapon_types_success_probabilities
        )

    @staticmethod
    def fill_interactive_table(table: QTableWidget,
                               row_headers: List[str],
                               col_headers: List[str],
                               data: List[List[str]],
                               on_data_change: Callable[[int, int, str], None]):
        """Заполняет заданную таблицу данными"""
        MainWindow.fill_table(table, row_headers, col_headers, data)

        def wrapper(c: QTableWidgetItem):
            new_value = c.text()
            on_data_change(c.row(), c.column(), new_value)

        table.itemChanged.connect(wrapper)

        max_header_width = max(MainWindow.FM.width(header) for header in row_headers) + 24
        MainWindow.set_minimal_size(table, header_width=max_header_width)

    @staticmethod
    def fill_table(table: QTableWidget,
                   row_headers: List[str],
                   col_headers: List[str],
                   data: List[List[str]],
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
    @staticmethod
    def set_minimal_size(table: QTableWidget, header_width: int):
        """Изменяет размер таблицы таким образом, чтобы она занимала минимальное место."""
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.resizeColumnsToContents()

        width = header_width
        for i in range(table.columnCount()):
            width += table.columnWidth(i)

        height = table.verticalHeader().length() + table.horizontalHeader().height() + 2

        table.setFixedSize(width, height)

    @property
    def ui_buttons(self) -> List[QPushButton]:
        return [
            self.ui.gaButton,
            self.ui.immuneButton,
            self.ui.addTargetButton,
            self.ui.deleteTargetButton,
            self.ui.addWeaponButton,
            self.ui.deleteWeaponButton,
            self.ui.saveIntoFileButton,
            self.ui.generateButton
        ]

    def disable_buttons(self):
        for button in self.ui_buttons:
            button.setEnabled(False)

    def enable_buttons(self):
        for button in self.ui_buttons:
            button.setEnabled(True)

    def closeEvent(self, a0):
        self.is_closing = True


app = QApplication([])
app.setStyle(QStyleFactory.create('Fusion'))
application = MainWindow(app_context=app)
application.show()

sys.exit(app.exec())
