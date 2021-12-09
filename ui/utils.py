from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QWidget

DEFAULT_DPI = 75


def dpi(elem: QApplication | QWidget | QObject) -> int:
    """
    :param elem: объект PyQT, для которого нужно найти оптимальный dpi
    :return: оптимальный dpi
    """
    global DEFAULT_DPI
    if isinstance(elem, QApplication):
        res = app_dpi(elem)
        DEFAULT_DPI = res
        return res

    elif isinstance(elem, (QWidget, QObject)):
        if hasattr(elem, "app_context"):
            app = elem.app_context
            res = app_dpi(app)
            DEFAULT_DPI = res
            return res
        else:
            try:
                parent_elem = elem.parent()
                res = app_dpi(parent_elem)
                DEFAULT_DPI = res
                return res
            except ValueError:
                return DEFAULT_DPI
    else:
        raise ValueError(f"Для элемента \"{elem}\" нельзя найти dpi")


def app_dpi(app: QApplication) -> int:
    """
    :param app: приложение, для которого нужно найти оптимальный dpi
    :return: оптимальный dpi
    """
    screen = app.screens()[0]
    dpi_float = screen.physicalDotsPerInch()
    dpi_int = int(dpi_float)
    return dpi_int


def parse_int_param(param_name: str, s: str) -> int:
    try:
        n = int(s)
    except ValueError:
        raise ValueError(f"Параметр {param_name} должен быть "
                         f"целым числом! (задано значение {s})")
    return n


def parse_float_param(param_name: str, s: str) -> float:
    try:
        n = float(s)
    except ValueError:
        raise ValueError(f"Параметр {param_name} должен быть "
                         f"вещественным числом! (задано значение {s})")
    return n


def parse_int(s: str, min_value: int, max_value: int) -> int:
    value = parse_int_param("", s)
    if min_value <= value <= max_value:
        return value
    else:
        raise ValueError(f"{value}")


def parse_float(s: str, min_value: float, max_value: float) -> float:
    value = parse_float_param("", s)
    if min_value <= value <= max_value:
        return value
    else:
        raise ValueError(f"{value}")
