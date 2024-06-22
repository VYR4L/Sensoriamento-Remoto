from front.interface import MainWindow, STYLESHEET_PATH
from PyQt6.QtWidgets import QApplication
import sys
from web.API import api
from back.colorimetry import colorimetric_fusion
from back.PCA import pca_fusion


def main():
    app = QApplication(sys.argv)

    with open(STYLESHEET_PATH, "r") as file:
        app.setStyleSheet(file.read())

    main_window = MainWindow(api, colorimetric_fusion, pca_fusion)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
