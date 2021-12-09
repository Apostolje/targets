import os

import platform

# автоматически конвертирует из .ui в .py при запуске main
if platform.system() == "Linux":
    os.system("./ui/convert.sh")

from ui.utils import dpi, parse_int_param, parse_float_param, parse_int, parse_float
from ui.tables import fill_table, fill_interactive_table

from ui.converted.application_window import Ui_ApplicationWindow as ApplicationWindowUI
from ui.converted.generation_window import Ui_GenerationWindow as GenerationWindowUI
from ui.src.generation_window import GenerationWindow
from ui.src.application_window import ApplicationWindow
from ui.run import run
