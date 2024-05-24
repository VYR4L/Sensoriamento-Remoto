import sys
import markdown
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt


ROOT_DIR = Path(__file__).resolve().parent.parent
STYLESHEET_PATH = ROOT_DIR / "front" / "static" / "css" / "style.css"
TUTORIAL_PATH = ROOT_DIR / "front" / "static" / "md" / "tutorial.md"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela Principal")

        # Dimensões da janela
        self.resize(500, 300)

        # Configurando o botão para abrir o tutorial
        self.open_tutorial_button = QPushButton("Abrir Tutorial")
        self.open_tutorial_button.clicked.connect(self.open_tutorial)
        
        # Configurando o botão para abrir a janela de configuração da API
        self.open_api_setup_button = QPushButton("Configurar API")
        self.open_api_setup_button.clicked.connect(self.open_api_setup)

        # Configurando o botão para abrir a janela secundária
        self.open_import_window_button = QPushButton("Abrir Janela de Importação")
        self.open_import_window_button.clicked.connect(self.open_import_window)

        # Configurando o layout e widget central
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.open_tutorial_button)
        self.layout.addWidget(self.open_api_setup_button)
        self.layout.addWidget(self.open_import_window_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_tutorial(self):
        with open(TUTORIAL_PATH, "r") as file:
            tutorial_content = file.read()

        html_content = markdown.markdown(tutorial_content)

        self.tutorial_dialog = TutorialDialog(html_content)
        self.tutorial_dialog.show()

    def open_api_setup(self):
        self.api_setup_window = SetUpAPIWindow()
        self.api_setup_window.show()

    def open_import_window(self):
        self.import_window = FileImportWindow()
        self.import_window.show()


class TutorialDialog(QDialog):
    def __init__(self, content):
        super().__init__()
        self.setWindowTitle("Tutorial de Uso")

        # Configurando o layout principal
        self.layout = QVBoxLayout()

        # Adicionando um QTextEdit para exibir o conteúdo do tutorial
        self.text_edit = QTextEdit()
        self.text_edit.setHtml(content)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        # Adicionando o botão de fechar
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        # Configurando o layout do widget
        self.setLayout(self.layout)


class FileImportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import files")

        # Configurando o layout principal
        self.layout = QVBoxLayout()

        # Criando o botão de importação
        self.import_button = QPushButton("Import file")
        self.import_button.clicked.connect(self.import_file)
        self.layout.addWidget(self.import_button)

        # Criando o label para exibir o nome do arquivo
        self.file_label = QLabel("None file imported")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.file_label)

        # Configurando o layout do widget
        self.setLayout(self.layout)

    def import_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select a file:", "", "Tif files (*.tif)")

        if file_path:
            self.file_label.setText(f"File imported: {file_path}")
        else:
            self.file_label.setText("None file imported")


class SetUpAPIWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set up API")

        # Configurando o layout principal
        self.layout = QVBoxLayout()

        # Criando os campos de entrada
        self.account_field = QLineEdit()
        self.account_field.setPlaceholderText("Account")
        self.layout.addWidget(self.account_field)

        self.api_file_field = QLineEdit()
        self.api_file_field.setPlaceholderText("API file")
        self.layout.addWidget(self.api_file_field)

        self.satellite_field = QComboBox()
        self.satellite_field.addItems(["Landsat", "CBERS"])
        self.layout.addWidget(self.satellite_field)

        self.collection_field = QComboBox()
        self.collection_field.addItems(["C01", "C02"])
        self.layout.addWidget(self.collection_field)

        self.id_field = QLineEdit()
        self.id_field.setPlaceholderText("ID")
        self.layout.addWidget(self.id_field)

        self.area_of_interest_field = QLineEdit()
        self.area_of_interest_field.setPlaceholderText("Area of interest")
        self.layout.addWidget(self.area_of_interest_field)

        self.output_folder_field = QLineEdit()
        self.output_folder_field.setPlaceholderText("Output folder")
        self.layout.addWidget(self.output_folder_field)

        # Criando o botão de execução
        self.execute_button = QPushButton("Set up")
        self.execute_button.clicked.connect(self.execute)
        self.layout.addWidget(self.execute_button)

        # Configurando o layout do widget
        self.setLayout(self.layout)

    def execute(self):
        # Chamando a função de API
        # api(self.account_field.text(), self.api_file_field.text(), self.satellite_field.currentText(), self.collection_field.currentText(), self.id_field.text(), self.area_of_interest_field.text(), self.output_folder_field.text())
        pass


        
        

def main():
    app = QApplication(sys.argv)

    with open(STYLESHEET_PATH, "r") as file:
        app.setStyleSheet(file.read())

    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
