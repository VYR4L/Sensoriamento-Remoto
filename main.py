from front.interface import MainWindow, STYLESHEET_PATH
from PyQt6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)

    with open(STYLESHEET_PATH, "r") as file:
        app.setStyleSheet(file.read())

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
