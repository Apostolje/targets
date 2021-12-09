import ui

from typing import Callable
from PyQt5.QtWidgets import QMainWindow

from algorithms import Task


class GenerationWindow(QMainWindow):

    def __init__(self, parent,
                 new_task_handler: Callable,
                 close_handler: Callable):
        super(GenerationWindow, self).__init__(parent)
        self.ui = ui.GenerationWindowUI()
        self.ui.setupUi(self)

        self.new_task_handler = new_task_handler
        self.closeEvent = close_handler
        self.ui.generateButton.clicked.connect(self.generate_task)

    def generate_task(self):
        try:
            min_n_targets: int = ui.parse_int(self.ui.minNTargets.text(), 1, 50)
            max_n_targets: int = ui.parse_int(self.ui.minNTargets.text(), 1, 50)
            if max_n_targets < min_n_targets:
                raise ValueError("max_n_targets < min_n_targets")

            min_target_value: int = ui.parse_int(self.ui.minTargetValue.text(), 0, 100_000_000)
            max_target_value: int = ui.parse_int(self.ui.maxTargetValue.text(), 0, 100_000_000)
            if max_target_value < min_target_value:
                raise ValueError("max_target_value < min_target_value")

            min_n_weapon_type: int = ui.parse_int(self.ui.minWeaponTypes.text(), 1, 1000)
            max_n_weapon_type: int = ui.parse_int(self.ui.maxWeaponTypes.text(), 1, 1000)
            if max_n_weapon_type < min_n_weapon_type:
                raise ValueError("max_n_weapon_type < min_n_weapon_type")

            min_n_weapon_amount: int = ui.parse_int(self.ui.minNWeaponAmount.text(), 1, 1000)
            max_n_weapon_amount: int = ui.parse_int(self.ui.maxNWeaponAmount.text(), 1, 1000)
            if max_n_weapon_amount < min_n_weapon_amount:
                raise ValueError("max_n_weapon_amount < min_n_weapon_amount")

            min_success_probability: float = ui.parse_float(self.ui.minSuccessProbability.text(), 0, 1)
            max_success_probability: float = ui.parse_float(self.ui.maxSuccessProbability.text(), 0, 1)
            if max_success_probability < min_success_probability:
                raise ValueError("max_success_probability < min_success_probability")

            task = Task.generate_random_task(
                min_n_targets,
                max_n_targets,
                min_target_value,
                max_target_value,
                min_n_weapon_type,
                max_n_weapon_type,
                min_n_weapon_amount,
                max_n_weapon_amount,
                min_success_probability,
                max_success_probability,
            )
            self.new_task_handler(task)
            self.close()

        except BaseException as e:
            print(e)
            self.close()
