from front.interface import MainWindow, STYLESHEET_PATH
from PyQt6.QtWidgets import QApplication
import sys
from web.API import api


def main():
    app = QApplication(sys.argv)

    with open(STYLESHEET_PATH, "r") as file:
        app.setStyleSheet(file.read())

    main_window = MainWindow(api)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
