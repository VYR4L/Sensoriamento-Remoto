import sys
import markdown
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QBrush, QPalette, QIcon

ROOT_DIR = Path(__file__).resolve().parent.parent
STYLESHEET_PATH = ROOT_DIR / "front" / "static" / "css" / "style.css"
TUTORIAL_PATH = ROOT_DIR / "front" / "static" / "md" / "tutorial.md"
BACKGROUND_IMAGE_PATH = ROOT_DIR / "front" / "static" / "img" / "Background2.png"
ICON_IMAGE_PATH = ROOT_DIR / "front" / "static" / "img" / "imported.png"


class MainWindow(QMainWindow):
    def __init__(self, api_function, colorimetric_method, pca_method):
        super().__init__()
        self.pca_fucntion = pca_method
        self.colorimetric_function = colorimetric_method
        self.api_function = api_function
        self.setWindowTitle("Janela Principal")

        # Dimensões da janela
        self.setMaximumSize(400, 400)
        self.resize(400, 400)

        # Carregando a imagem de fundo
        background_image = QPixmap(str(BACKGROUND_IMAGE_PATH))

        # Ajustando o tamanho da imagem de fundo para o tamanho da janela
        scaled_background_image = background_image.scaled(self.size())

        # Configurando a paleta de cores para incluir transparência
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_background_image))
        self.setPalette(palette)

        # Configurando os botões principais
        self.open_tutorial_button = QPushButton("Abrir Tutorial")
        self.open_tutorial_button.setObjectName("OpenTutorialButton")
        self.open_tutorial_button.clicked.connect(self.open_tutorial)
        self.open_tutorial_button.setFixedSize(150, 50)

        self.open_api_setup_button = QPushButton("Configurar API")
        self.open_api_setup_button.setObjectName("ApiSetupButton")
        self.open_api_setup_button.clicked.connect(self.open_api_setup)
        self.open_api_setup_button.setFixedSize(150, 50)

        # Configurando os botões de importação
        self.import_multispectral_button = QPushButton("Importar MultiS")
        self.import_multispectral_button.setObjectName("MultiSpectralButton")
        self.import_multispectral_button.clicked.connect(self.import_multispectral)
        self.import_multispectral_button.setFixedSize(150, 50)
        self.import_multispectral_button.setIcon(QIcon(str(ICON_IMAGE_PATH)))

        self.import_panc_button = QPushButton("Importar PanC")
        self.import_panc_button.setObjectName("PanCButton")
        self.import_panc_button.clicked.connect(self.import_panc)
        self.import_panc_button.setFixedSize(150, 50)
        self.import_panc_button.setIcon(QIcon(str(ICON_IMAGE_PATH)))

        # Configurando os botões de métodos de fusão
        self.pca_method_button = QPushButton("Fusão PCA")
        self.pca_method_button.setObjectName("PCAFusionButton")
        self.pca_method_button.clicked.connect(self.open_pca_method)

        self.colorimetric_method_button = QPushButton("Fusão Colorimétrica")
        self.colorimetric_method_button.setObjectName("ColorimetricFusionButton")
        self.colorimetric_method_button.clicked.connect(self.open_colorimetric_method)    

        # Configurando o layout principal
        self.layout = QVBoxLayout()

        # Criando um layout vertical para os botões principais
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.open_tutorial_button, alignment=Qt.AlignmentFlag.AlignCenter)
        buttons_layout.addWidget(self.open_api_setup_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Criando um layout horizontal para os botões de importação
        import_buttons_layout = QHBoxLayout()
        import_buttons_layout.addWidget(self.import_multispectral_button)
        import_buttons_layout.addWidget(self.import_panc_button)

        # Adicionando os layouts ao layout principal
        self.layout.addLayout(buttons_layout)
        self.layout.addLayout(import_buttons_layout)

        # Criando layout horizontal para os botões de métodos de fusão
        methods_layout = QHBoxLayout()
        methods_layout.addWidget(self.pca_method_button)
        methods_layout.addWidget(self.colorimetric_method_button)
        self.layout.addLayout(methods_layout)

        # Configurando o widget central
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_tutorial(self):
        with open(TUTORIAL_PATH, "r", encoding='utf-8') as file:
            tutorial_content = file.read()

        html_content = markdown.markdown(tutorial_content)

        self.tutorial_dialog = TutorialDialog(html_content)
        self.tutorial_dialog.show()

    def open_api_setup(self):
        self.api_setup_window = SetUpAPIWindow(self.api_function)
        self.api_setup_window.show()

    def import_multispectral(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione o arquivo multiespectral:", "", "Tif files (*.tif)")
        if file_path:
            self.multiespectral_path = file_path

    def import_panc(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione o arquivo pancromático:", "", "Tif files (*.tif)")
        if file_path:
            self.panchromatic_path = file_path

    def open_pca_method(self):
        self.pca_fucntion(
            self.multiespectral_path,
            self.panchromatic_path,
            self.output_path
        )

    def open_colorimetric_method(self):
        self.colorimetric_function(
            self.multiespectral_path,
            self.panchromatic_path,
            self.output_path
        )


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
        self.close_button = QPushButton("Fechar")
        self.close_button.setObjectName("CloseButton")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        # Configurando o layout do widget
        self.setLayout(self.layout)

        self.setMinimumSize(500, 300)

    def import_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select a file:", "", "Tif files (*.tif)")

        if file_path:
            self.file_label.setText(f"File imported: {file_path}")
        else:
            self.file_label.setText("None file imported")


class SetUpAPIWindow(QWidget):
    def __init__(self, funcao):
        super().__init__()
        self.funcao = funcao
        self.setWindowTitle("Configuração de API")

        # Configurando o layout principal
        self.layout = QVBoxLayout()

        # Criando os campos de entrada
        self.account_field = QLineEdit()
        self.account_field.setPlaceholderText("Conta")
        self.layout.addWidget(self.account_field)

        self.api_file_button = QPushButton("Selecione o arquivo de API")
        self.api_file_button.setObjectName("ApiFileButton")
        self.api_file_button.clicked.connect(self.select_api_file)
        self.api_file_label = QLabel("Nenhum arquivo selecionado")
        self.layout.addWidget(self.api_file_button)
        self.layout.addWidget(self.api_file_label)

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
        self.area_of_interest_field.setPlaceholderText("Área de interesse")
        self.layout.addWidget(self.area_of_interest_field)

        self.output_folder_button = QPushButton("Selecione o diretório de saída")
        self.output_folder_button.setObjectName("OutputFolderButton")
        self.output_folder_button.clicked.connect(self.select_output_folder)
        self.output_folder_label = QLabel("Nenhum diretório selecionado")
        self.layout.addWidget(self.output_folder_button)
        self.layout.addWidget(self.output_folder_label)

        # Criando o botão de execução
        self.execute_button = QPushButton("Confirmar")
        self.execute_button.setObjectName("ExecuteButton")
        self.execute_button.clicked.connect(self.execute)
        self.layout.addWidget(self.execute_button)

        # Configurando o layout do widget
        self.setLayout(self.layout)

        self.setMinimumSize(500, 300)

    def select_api_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione o arquivo da API:", "", "JSON files (*.json)")

        if file_path:
            self.api_file_label.setText(f"Arquivo selecionado: {file_path}")
        else:
            self.api_file_label.setText("Nenhum arquivo selecionado")

    def select_output_folder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, "Selecione o diretório de saída")

        if folder_path:
            self.output_folder_label.setText(f"Diretório selecionado: {folder_path}")
        else:
            self.output_folder_label.setText("Nenhum diretório selecionado")

    def execute(self):
        # Chamando a função de API com os parâmetros necessários
        self.funcao(
            self.account_field.text(),
            self.api_file_label.text().replace("Arquivo selecionado: ", ""),
            self.satellite_field.currentText(),
            self.collection_field.currentText(),
            self.id_field.text(),
            self.area_of_interest_field.text(),
            self.output_folder_label.text().replace("Diretório selecionado: ", "")
        )
