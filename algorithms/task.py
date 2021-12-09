import json
from dataclasses import dataclass
from functools import cached_property
from itertools import repeat
from random import randint, uniform


@dataclass(frozen=True)
class Task:
    targets: tuple[str, ...]  # названия_целей
    targets_values: tuple[int, ...]  # значимости_целей
    weapon_types: tuple[str, ...]  # типы_исполнителей
    weapon_types_amount: tuple[int, ...]  # количество_исполнителей_каждого_типа
    weapon_types_success_probabilities: tuple[tuple[float, ...], ...]  # вероятности_выполнения

    DEFAULT_TARGET_NAME = "Цель"
    DEFAULT_TARGET_VALUE = 1
    DEFAULT_WEAPON_TYPE = "Испол."
    DEFAULT_WEAPON_AMOUNT = 1
    DEFAULT_WEAPON_POSSIBILITY = 0.5

    def __post_init__(self):
        self.assert_if_correct()

    def __eq__(self, other):
        return \
            other is not None and \
            self.targets == other.targets and \
            self.targets_values == other.targets_values and \
            self.weapon_types == other.weapon_types and \
            self.weapon_types_amount == other.weapon_types_amount and \
            self.weapon_types_success_probabilities == other.weapon_types_success_probabilities

    @cached_property
    def weapons(self) -> tuple[str]:
        res = []
        for weapon_type, amount in zip(self.weapon_types, self.weapon_types_amount):
            res.extend(repeat(weapon_type, amount))
        return tuple(res)

    @cached_property
    def weapon_types_survival_probabilities(self) -> tuple[tuple[float]]:
        return tuple(
            tuple(1 - success_probability for success_probability in row)
            for row in self.weapon_types_success_probabilities
        )

    @cached_property
    def weapons_total_amount(self) -> int:
        """:return: общее число оружий всех типов"""
        return sum(self.weapon_types_amount)

    @cached_property
    def targets_amount(self) -> int:
        """:return: общее число целей"""
        return len(self.targets)

    @cached_property
    def values_sum(self) -> int:
        """:return: сумма значимостей всех целей"""
        return sum(self.targets_values)

    @cached_property
    def individual_weapons(self) -> tuple[str]:
        res = []

        weapon_type = self.weapons[0]
        weapon_index = 0
        for i in range(self.weapons_total_amount):
            if weapon_type == self.weapons[i]:
                weapon_index += 1
            else:
                weapon_index = 1
                weapon_type = self.weapons[i]

            res.append(f'"{weapon_type}" №{weapon_index}')

        return tuple(res)

    @cached_property
    def individual_weapons_success_probabilities(self) -> dict[str, dict[str, float]]:
        res = {
            weapon: {}
            for weapon in self.individual_weapons
        }

        i = 0  # weapon_of_the_type index
        j = 0  # weapon_type index
        for weapon in res.keys():
            for k, target in enumerate(self.targets):
                res[weapon][target] = self.weapon_types_success_probabilities[j][k]
            if i == self.weapon_types_amount[j] - 1:
                j += 1
                i = 0
            else:
                i += 1

        return res

    @staticmethod
    def generate_random_task(min_n_targets: int,
                             max_n_targets: int,
                             min_target_value: int,
                             max_target_value: int,
                             min_n_weapon_type: int,
                             max_n_weapon_type: int,
                             min_n_weapon_amount: int,
                             max_n_weapon_amount: int,
                             min_success_probability: float,
                             max_success_probability: float
                             ):
        n_targets = randint(min_n_targets, max_n_targets)
        n_weapon_types = randint(min_n_weapon_type, max_n_weapon_type)

        targets = tuple(
            f"{Task.DEFAULT_TARGET_NAME} {i + 1}"
            for i in range(n_targets)
        )
        targets_values = tuple(
            randint(min_target_value, max_target_value)
            for _ in range(n_targets)
        )
        weapon_types = tuple(
            f"{Task.DEFAULT_WEAPON_TYPE} {i + 1}"
            for i in range(n_weapon_types)
        )
        weapon_types_amount = tuple(
            randint(min_n_weapon_amount, max_n_weapon_amount)
            for _ in range(n_weapon_types)
        )
        weapon_types_success_probabilities = tuple(
            tuple(
                round(uniform(min_success_probability, max_success_probability), 3)
                for _ in range(n_targets)
            )
            for _ in range(n_weapon_types)
        )

        return Task(
            targets,
            targets_values,
            weapon_types,
            weapon_types_amount,
            weapon_types_success_probabilities
        )

    def find_survival(self, assignment: tuple[int, ...] | list[int]) -> float:
        """
        Поиск значения выживаемости для заданной задачи и решения.

        :param assignment: решение задачи
        :return: значение выживаемости целей
        """
        targets_total = self.targets_amount
        targets_values = self.targets_values
        weapon_types_amount = self.weapon_types_amount
        weapon_types_survival_probabilities = self.weapon_types_survival_probabilities

        survival = 0.

        # TODO ускорить
        for target_index, target_value in zip(range(1, targets_total + 1),
                                              targets_values):
            target_survival: float = target_value
            shift = 0
            for type_amount, type_probabilities in zip(weapon_types_amount,
                                                       weapon_types_survival_probabilities):
                # вероятность выживания от оружия этого типа
                probability = type_probabilities[target_index - 1]

                # количество оружий этого типа, нацеленных на эту цель
                aimed = 0
                for selected_target_index in assignment[shift:shift + type_amount]:
                    if selected_target_index == target_index:
                        aimed += 1

                if probability == 0:
                    if aimed > 0:
                        target_survival = 0
                else:
                    target_survival *= probability ** aimed

                shift += type_amount

            survival += target_survival

        return survival

    def objective_function(self, assignment: tuple[int, ...] | list[int]) -> float:
        """
        Целевая функция
        """
        if self.values_sum == 0:
            return 1
        else:
            return (self.values_sum - self.find_survival(assignment)) / self.values_sum

    def assert_if_correct(self):
        """
        Проверяет эту задачу на корректность.
       """
        assert len(self.targets) != 0, "Не указаны цели!"
        assert len(self.weapon_types) != 0, "Не указаны типы оружий!"
        assert len(self.targets) == len(self.targets_values), \
            f"Каждой цели {self.targets} должно соответствовать ее значимость {self.targets_values}"
        assert len(self.weapon_types) == len(self.weapon_types_amount), \
            f"Каждому типу оружий {self.weapon_types} должно соответствовать его количество {self.weapon_types_amount}"
        assert len(self.weapon_types_success_probabilities) == len(self.weapon_types), \
            f"Вероятности поражения целей {self.weapon_types_success_probabilities} " \
            f"не соответсвуют количеству оружий {len(self.weapon_types)}"
        for type_probabilities, type_name in zip(self.weapon_types_success_probabilities, self.weapon_types):
            assert len(type_probabilities) == len(self.targets), \
                f"Вероятности поражения {type_probabilities} для типа \"{type_name}\" не соответсвуют количеству целей"

    def save_task(self, file_path: str):
        """
        Сохраняет задачу в заданный файл.

        :param file_path: путь к файлу.
        """
        with open(file_path, "w") as file:
            json.dump(
                dict(
                    targets=self.targets,
                    targets_values=self.targets_values,
                    weapon_types=self.weapon_types,
                    weapon_types_amount=self.weapon_types_amount,
                    weapon_types_success_probabilities=self.weapon_types_success_probabilities
                ),
                file
            )

    @staticmethod
    def load_task(file_path: str):
        """Загружает задачу из заданного файла."""
        with open(file_path, "r") as file:
            data = json.load(file)
            try:
                targets = data['targets']
                targets_values = data['targets_values']
                weapon_types = data['weapon_types']
                weapon_types_amount = data['weapon_types_amount']
                weapon_types_success_probabilities = data['weapon_types_success_probabilities']
                task = Task(
                    targets,
                    targets_values,
                    weapon_types,
                    weapon_types_amount,
                    weapon_types_success_probabilities
                )
                return task

            except BaseException:
                raise Exception("Wrong format")

    def add_target(self):
        """Добавляет одну новую цель"""
        return Task(
            (*self.targets, f"{self.DEFAULT_TARGET_NAME} {len(self.targets) + 1}"),
            (*self.targets_values, Task.DEFAULT_TARGET_VALUE),
            self.weapon_types,
            self.weapon_types_amount,
            tuple(
                (*row, self.DEFAULT_WEAPON_POSSIBILITY)
                for row in self.weapon_types_success_probabilities
            )
        )

    def delete_last_target(self):
        """Удаляет последнюю цель"""
        if len(self.targets) == 0:
            raise Exception("Нельзя удалить, т.к. нет целей")

        return Task(
            self.targets[0:-1],
            self.targets_values[0:-1],
            self.weapon_types,
            self.weapon_types_amount,
            tuple(
                row[0:-1]
                for row in self.weapon_types_success_probabilities
            )
        )

    def add_weapon_type(self):
        """Добавляет новый тип оружия"""
        return Task(
            self.targets,
            self.targets_values,
            (*self.weapon_types, f"{self.DEFAULT_WEAPON_TYPE} {len(self.weapon_types) + 1}"),
            (*self.weapon_types_amount, self.DEFAULT_WEAPON_AMOUNT),
            (
                *self.weapon_types_success_probabilities,
                tuple(repeat(self.DEFAULT_WEAPON_POSSIBILITY, len(self.targets)))
            )
        )

    def delete_last_weapon_type(self):
        """Удаляет последний тип оружия"""
        if len(self.weapon_types) == 0:
            raise Exception("Нельзя удалить, т.к. нет оружий")

        return Task(
            self.targets,
            self.targets_values,
            self.weapon_types[0:-1],
            self.weapon_types_amount[0:-1],
            self.weapon_types_success_probabilities[0:-1]
        )

    def remove_nth_target(self, n: int):
        return Task(
            (*self.targets[:n], *self.targets[n + 1:]),
            (*self.targets_values[:n], *self.targets_values[n + 1:]),
            self.weapon_types,
            self.weapon_types_amount,
            tuple(
                (*row[:n], *row[n + 1:])
                for row in self.weapon_types_success_probabilities
            )
        )

    def change_nth_target(self, n: int, new_value: str):
        return Task(
            (*self.targets[:n], new_value, *self.targets[n + 1:]),
            self.targets_values,
            self.weapon_types,
            self.weapon_types_amount,
            self.weapon_types_success_probabilities
        )

    def change_nth_target_value(self, n: int, new_value: int):
        return Task(
            self.targets,
            (*self.targets_values[:n], new_value, *self.targets_values[n + 1:]),
            self.weapon_types,
            self.weapon_types_amount,
            self.weapon_types_success_probabilities
        )

    def remove_nth_weapon_type(self, n: int):
        return Task(
            self.targets,
            self.targets_values,
            (*self.weapon_types[:n], *self.weapon_types[n + 1:]),
            (*self.weapon_types_amount[:n], *self.weapon_types_amount[n + 1:]),
            (*self.weapon_types_success_probabilities[:n], *self.weapon_types_success_probabilities[n + 1:]),
        )

    def change_nth_weapon_type_amount(self, n: int, new_value: int):
        return Task(
            self.targets,
            self.targets_values,
            self.weapon_types,
            (*self.weapon_types_amount[:n], new_value, *self.weapon_types_amount[n + 1:]),
            self.weapon_types_success_probabilities
        )

    def change_nth_weapon_type(self, n: int, new_value: str):
        return Task(
            self.targets,
            self.targets_values,
            (*self.weapon_types[:n], new_value, *self.weapon_types[n + 1:]),
            self.weapon_types_amount,
            self.weapon_types_success_probabilities
        )

    def change_weapon_types_success_probabilities(self, i: int, j: int, new_value: float):
        return Task(
            self.targets,
            self.targets_values,
            self.weapon_types,
            self.weapon_types_amount,
            tuple(
                row if i != row_i else (*row[:j], new_value, *row[j + 1:])
                for row_i, row in enumerate(self.weapon_types_success_probabilities)
            )
        )

    @staticmethod
    def create_default():
        return Task(
            ("Цель 1", "Цель 2", "Цель 3"),
            (5, 10, 20),
            ("Танк", "Самолет", "Судно"),
            (5, 2, 1),
            (
                (0.3, 0.2, 0.5),
                (0.1, 0.6, 0.5),
                (0.4, 0.5, 0.4)
            )
        )
