import ui
from algorithms import *

import traceback
from functools import cached_property

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton


class ApplicationWindow(QMainWindow):

    def __init__(self, app_context: QApplication):
        super(ApplicationWindow, self).__init__()
        self.app_context = app_context
        self.ui = ui.ApplicationWindowUI()
        self.ui.setupUi(self)

        self.task, self.solution = self.change_task(Task.create_default())

        self.is_closing = False
        self.is_running = False

        self.ui.immuneButton.clicked.connect(self.start_immune)
        self.ui.gaButton.clicked.connect(self.start_ga)

        self.ui.addTargetButton.clicked.connect(self.add_target)
        self.ui.deleteTargetButton.clicked.connect(self.delete_last_target)
        self.ui.addWeaponButton.clicked.connect(self.add_weapon_type)
        self.ui.deleteWeaponButton.clicked.connect(self.delete_last_weapon_type)

        self.ui.saveIntoFileButton.clicked.connect(self.save_task_into_file)
        self.ui.loadFromFileButton.clicked.connect(self.load_task_from_file)
        self.ui.generateButton.clicked.connect(self.show_generation_window)

    def change_task(self, new_task: Task):
        self.task = new_task
        self.solution = Solution.generate_random_solution(self.task)
        self.update_all()
        self.ui.result.setText(
            f'Случайное решение:\n'
            f'{self.solution.assignment}\n\n'
            f'Значение ЦФ: {self.solution.value:.4f}\n\n'
            f'{self.solution.text}'
        )
        return self.task, self.solution

    def show_generation_window(self):
        self.disable_buttons()
        ui.GenerationWindow(self, self.change_task, self.enable_buttons).show()

    def add_target(self):
        """Добавляет новую цель."""
        self.change_task(self.task.add_target())

    def delete_last_target(self):
        """Удаляет последнюю цель."""
        if self.task.targets_amount <= 1:
            return
        self.change_task(self.task.delete_last_target())

    def add_weapon_type(self):
        """Добавляет новый тип оружия."""
        self.change_task(self.task.add_weapon_type())

    def delete_last_weapon_type(self):
        """Удаляет последний тип оружия."""
        if len(self.task.weapon_types) <= 1:
            return
        self.change_task(self.task.delete_last_weapon_type())

    def start_immune(self):
        """Запускает иммунный алгоритм."""
        try:
            np = ui.parse_int_param("np", self.ui.immuneNp.text())
            ci = ui.parse_float_param("ci", self.ui.immuneCi.text())
            ni = ui.parse_int_param("ni", self.ui.immuneNi.text())

            immune_alg = ImmuneAlgorithm(task=self.task, np=np, ni=ni, ci=ci)
            self.run_algorithm(immune_alg)
        except BaseException as e:
            self.show_error(e)
            return

    def start_ga(self):
        """Запускает генетический алгоритм."""
        try:
            np = ui.parse_int_param("np", self.ui.gaNp.text())
            mp = ui.parse_float_param("mp", self.ui.gaMp.text())
            ni = ui.parse_int_param("ni", self.ui.gaNi.text())
            evolution = self.ui.evolutionBox.currentText()
            if evolution == "Эволюция Дарвина":
                ga_class = GADarwin
            elif evolution == "Эволюция Де Фриза":
                ga_class = GADeVries
            else:
                raise Exception

            ga = ga_class(task=self.task, np=np, ni=ni, mp=mp)
            self.run_algorithm(ga)
        except BaseException as e:
            self.show_error(e)
            return

    def run_algorithm(self, alg: Algorithm):
        """Выполнение заданного алгоритма."""
        self.disable_buttons()
        try:
            algorithm_solutions = alg.run()
            self.solution = next(algorithm_solutions)

            for new_solution in algorithm_solutions:

                if self.solution.value < new_solution.value:
                    self.solution = new_solution
                    self.update_hypergraph()
                    self.update_solution_table()

                self.ui.result.setText(
                    f'Итерация: {new_solution.iterations_passed}\n\n'
                    f'Лучшее решение:\n'
                    f'{self.solution.assignment}\n\n'
                    f'Значение ЦФ: {self.solution.value:.4f}\n\n'
                    f'{self.solution.text}'
                )

                self.update()
                self.app_context.processEvents()
                if self.is_closing:
                    break

        except BaseException as e:
            self.enable_buttons()
            raise e
        self.enable_buttons()

    def show_error(self, e: BaseException):
        self.ui.result.setText(f"Ошибка:\n\n{e}")
        traceback.print_exc()

    def handle_targets_change(self, row: int, col: int, new_value: str):
        if row == 0:
            if new_value == "":
                self.change_task(self.task.remove_nth_target(col))
            else:
                self.change_task(self.task.change_nth_target(col, new_value))
        elif row == 1:
            try:
                value = int(float(new_value))
                if value >= 0:
                    self.change_task(self.task.change_nth_target_value(col, value))
            except ValueError:
                self.update_all()
        else:
            raise Exception

    def handle_weapons_change(self, row: int, col: int, new_value: str):
        if row == 0:
            self.change_task(self.task.change_nth_weapon_type(col, new_value))
        elif row == 1:
            try:
                value = int(new_value)
                if value < 0:
                    pass
                elif value == 0:
                    if len(self.task.weapon_types) > 1:
                        self.change_task(self.task.remove_nth_weapon_type(col))
                    else:
                        self.update_all()
                else:
                    self.change_task(self.task.change_nth_weapon_type_amount(col, value))
            except ValueError:
                self.update_all()
        else:
            raise Exception

    def handle_probabilities_change(self, row: int, col: int, new_value: str):
        try:
            value = float(new_value)
            if value > 1:
                value = 1.0
            if value < 0:
                value = 0.0
            self.change_task(self.task.change_weapon_types_success_probabilities(row, col, value))
        except ValueError:
            self.update_all()

    def update_all(self):
        self.update_task_tables()
        self.update_solution_table()
        self.update_hypergraph()

    def update_hypergraph(self):
        self.ui.graphWidget.draw_solution(self.solution)

    def update_solution_table(self):
        """Обновляет содержимое таблицы решения задачи."""
        if len(self.solution.assignment) != 0:
            ui.fill_table(
                table=self.ui.solutionTable,
                row_headers=self.task.individual_weapons,
                col_headers=self.task.targets,
                data=self.solution.solution_matrix,
                highlight_non_zero=True
            )

    def update_task_tables(self):
        """Обновляет содержимое таблиц для условий задачи"""
        try:
            self.ui.targetsTable.itemChanged.disconnect()
            self.ui.weaponsTable.itemChanged.disconnect()
            self.ui.possibilitiesTable.itemChanged.disconnect()
        except TypeError:
            pass

        ui.fill_interactive_table(
            table=self.ui.targetsTable,
            row_headers=["Цель", "Значимость"],
            col_headers=[str(i + 1) for i in range(len(self.task.targets))],
            data=[
                self.task.targets,
                [str(i) for i in self.task.targets_values]
            ],
            on_data_change=self.handle_targets_change
        )
        ui.fill_interactive_table(
            table=self.ui.weaponsTable,
            row_headers=["Тип исполнителя", "Количество"],
            col_headers=[str(i + 1) for i in range(len(self.task.weapon_types))],
            data=[
                self.task.weapon_types,
                [str(amount) for amount in self.task.weapon_types_amount]
            ],
            on_data_change=self.handle_weapons_change
        )
        ui.fill_interactive_table(
            table=self.ui.possibilitiesTable,
            row_headers=self.task.weapon_types,
            col_headers=self.task.targets,
            data=self.task.weapon_types_success_probabilities,
            on_data_change=self.handle_probabilities_change
        )

    def save_task_into_file(self):
        """Сохраняет условия задачи в файл."""
        file_name = QFileDialog.getSaveFileName(
            self,
            'Сохранить условие в...',
            '',
            filter="Task file extension - *.json (*.json)"
        )[0]
        if file_name[len(file_name) - 4:] != "json":
            file_name = f"{file_name}.json"
        try:
            print(file_name)
            self.task.save_task(file_name)
        except Exception as e:
            print(e)

    def load_task_from_file(self):
        """Загрузает условия задачи из файла."""
        file_name = QFileDialog.getOpenFileName(
            self,
            'Загрузить условия из...',
            '',
            filter="Task file - *.json (*.json)"
        )[0]
        try:
            print(file_name)
            self.change_task(Task.load_task(file_name))
        except Exception as e:
            print(e)

    @cached_property
    def ui_buttons(self) -> tuple[QPushButton, ...]:
        return (
            self.ui.gaButton,
            self.ui.immuneButton,
            self.ui.addTargetButton,
            self.ui.deleteTargetButton,
            self.ui.addWeaponButton,
            self.ui.deleteWeaponButton,
            self.ui.saveIntoFileButton,
            self.ui.loadFromFileButton,
            self.ui.generateButton
        )

    def disable_buttons(self):
        for button in self.ui_buttons:
            button.setEnabled(False)

    def enable_buttons(self, _=None):
        for button in self.ui_buttons:
            button.setEnabled(True)

    def closeEvent(self, a0):
        self.is_closing = True
