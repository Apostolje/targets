import sys

import ui

from PyQt5.QtWidgets import QApplication, QStyleFactory


def run():
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    application = ui.ApplicationWindow(app_context=app)
    application.show()

    sys.exit(app.exec())
