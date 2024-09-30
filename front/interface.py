import markdown
from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QLabel, QTextEdit, QDialog, QLineEdit, QComboBox, QMessageBox, QListWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QBrush, QPalette, QIcon
from back.colorimetry import colorimetric_fusion_landsat, colorimetric_fusion_cbers
from back.PCA import pca_fusion_landsat, pca_fusion_cbers
from back.crop_image import crop_image
from web.api_landsat import download_landsat
from web.api_cbers import get_images, download_cbers
from cbers4asat import Cbers4aAPI
from deep_translator import GoogleTranslator


ROOT_DIR = Path(__file__).resolve().parent.parent
STYLESHEET_PATH = ROOT_DIR / "front" / "static" / "css" / "style.css"
TUTORIAL_PATH = ROOT_DIR / "front" / "static" / "md" / "tutorial.md"
BACKGROUND_IMAGE_PATH = ROOT_DIR / "front" / "static" / "img" / "Background2.png"
ICON_IMAGE_PATH = ROOT_DIR / "front" / "static" / "img" / "imported.png"
error_string = 'Ocorreu um erro!'
translator = GoogleTranslator(source='en', target='pt')


class MainWindow(QMainWindow):
    '''
    Janela principal da aplicação.

    Esta janela contém os botões principais para abrir o tutorial, configurar a API,
    recortar imagens e realizar a fusão de imagens.
    '''

    def __init__(self):
        super().__init__()
        self.output_path = ''
        self.setWindowTitle("Janela Principal")

        # Dimensões da janela
        self.setMaximumSize(400, 400)
        self.resize(400, 400)

        # Carregando a imagem de fundo
        background_image = QPixmap(str(BACKGROUND_IMAGE_PATH))
        scaled_background_image = background_image.scaled(self.size())
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_background_image))
        self.setPalette(palette)

        # Botões principais
        self.open_tutorial_button = QPushButton("Abrir Tutorial")
        self.open_tutorial_button.setObjectName("Button")
        self.open_tutorial_button.setFixedSize(150, 50)
        self.open_tutorial_button.clicked.connect(self.open_tutorial)

        self.open_api_setup_button_landsat = QPushButton("Baixar Landsat")
        self.open_api_setup_button_landsat.setObjectName("Button")
        self.open_api_setup_button_landsat.setFixedSize(150, 50)
        self.open_api_setup_button_landsat.clicked.connect(self.open_api_setup_landsat)

        self.open_api_setup_button_cbers = QPushButton("Baixar CBERS")
        self.open_api_setup_button_cbers.setObjectName("Button")
        self.open_api_setup_button_cbers.setFixedSize(150, 50)
        self.open_api_setup_button_cbers.clicked.connect(self.open_api_setup_cbers)

        self.crop_image_button = QPushButton("Recortar Imagem")
        self.crop_image_button.setObjectName("Button")
        self.crop_image_button.setFixedSize(150, 50)
        self.crop_image_button.clicked.connect(self.crop_image)

        self.satellite_field = QComboBox()
        self.satellite_field.setObjectName("SatelliteField")
        self.satellite_field.addItems(["CBERS 04A", "Landsat 08"])
        self.satellite_field.setFixedSize(150, 50)
        self.satellite_field.currentTextChanged.connect(self.update_import_buttons)

        # Botão de saída de imagem
        self.output_folder_button = QPushButton("Selecione o diretório de saída")
        self.output_folder_button.setObjectName("Button")
        self.output_folder_button.clicked.connect(self.select_output_folder)

        # Botões de importação
        self.import_band1_button = QPushButton("Banda azul")
        self.import_band1_button.setObjectName("Button")
        self.import_band1_button.setFixedSize(150, 50)
        self.import_band1_button.setIcon(QIcon(str(ICON_IMAGE_PATH)))

        self.import_band2_button = QPushButton("Banda verde")
        self.import_band2_button.setObjectName("Button")
        self.import_band2_button.setFixedSize(150, 50)
        self.import_band2_button.setIcon(QIcon(str(ICON_IMAGE_PATH)))

        self.import_band3_button = QPushButton("Banda vermelha")
        self.import_band3_button.setObjectName("Button")
        self.import_band3_button.setFixedSize(150, 50)
        self.import_band3_button.setIcon(QIcon(str(ICON_IMAGE_PATH)))

        self.import_band4_button = QPushButton("Banda infra-prox")
        self.import_band4_button.setObjectName("Button")
        self.import_band4_button.setFixedSize(150, 50)
        self.import_band4_button.setIcon(QIcon(str(ICON_IMAGE_PATH)))

        self.import_multispectral_button = QPushButton("Banda MultEspec")
        self.import_multispectral_button.setObjectName("Button")
        self.import_multispectral_button.setFixedSize(150, 50)
        self.import_multispectral_button.setIcon(QIcon(str(ICON_IMAGE_PATH)))

        self.import_panc_button = QPushButton("Banda Pan")
        self.import_panc_button.setObjectName("Button")
        self.import_panc_button.setFixedSize(150, 50)
        self.import_panc_button.setIcon(QIcon(str(ICON_IMAGE_PATH)))

        # Conectar os botões de importação às funções correspondentes
        self.import_band1_button.clicked.connect(self.import_band1)
        self.import_band2_button.clicked.connect(self.import_band2)
        self.import_band3_button.clicked.connect(self.import_band3)
        self.import_band4_button.clicked.connect(self.import_band4)
        self.import_multispectral_button.clicked.connect(self.import_multispectral)
        self.import_panc_button.clicked.connect(self.import_panc)

        # Configurando os botões de métodos de fusão
        self.pca_method_button = QPushButton("Fusão PCA")
        self.pca_method_button.setObjectName("Button")
        self.pca_method_button.clicked.connect(self.open_pca_method)

        self.colorimetric_method_button = QPushButton("Fusão Colorimétrica")
        self.colorimetric_method_button.setObjectName("Button")
        self.colorimetric_method_button.clicked.connect(self.open_colorimetric_method)

        # Layout principal
        self.layout = QVBoxLayout()

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.open_tutorial_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(buttons_layout)

        config_layout = QHBoxLayout()
        config_layout.addWidget(self.open_api_setup_button_landsat)
        config_layout.addWidget(self.open_api_setup_button_cbers)
        config_layout.addWidget(self.crop_image_button)
        self.layout.addLayout(config_layout)

        # Adiciona o campo de seleção de satélite
        satellite_chose = QVBoxLayout()
        satellite_chose.addWidget(self.satellite_field, alignment=Qt.AlignmentFlag.AlignCenter) 
        self.layout.addLayout(satellite_chose)   

        # Adiciona o campo de saída de imagem
        output = QVBoxLayout()
        output.addWidget(self.output_folder_button, alignment=Qt.AlignmentFlag.AlignCenter)  
        self.layout.addLayout(output)

        # Layout para botões de importação
        self.import_buttons_layout = QVBoxLayout() 
        self.layout.addLayout(self.import_buttons_layout)

        # Inicializa os botões com o satélite selecionado no início
        self.update_import_buttons()

        # Layout para botões de métodos de fusão
        methods_layout = QHBoxLayout()
        methods_layout.addWidget(self.colorimetric_method_button)
        methods_layout.addWidget(self.pca_method_button)
        self.layout.addLayout(methods_layout)

        # Widget central
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def update_import_buttons(self):
        # Limpa o layout de botões de importação sem deletar os objetos
        for i in reversed(range(self.import_buttons_layout.count())):
            widget_to_remove = self.import_buttons_layout.itemAt(i).layout()  # Remove o layout inteiro (linha)
            if widget_to_remove:
                while widget_to_remove.count():
                    item = widget_to_remove.takeAt(0)
                    if item.widget():
                        item.widget().setParent(None)
                widget_to_remove.deleteLater()  # Deleta o layout vazio

        # Adiciona os botões correspondentes ao satélite selecionado
        if self.satellite_field.currentText() == 'CBERS 04A':
            # Primeira linha: Banda 1 e Banda 2
            row1 = QHBoxLayout()
            row1.addWidget(self.import_band1_button)
            row1.addWidget(self.import_band2_button)
            self.import_buttons_layout.addLayout(row1)

            # Segunda linha: Banda 3 e Banda 4
            row2 = QHBoxLayout()
            row2.addWidget(self.import_band3_button)
            row2.addWidget(self.import_band4_button)
            self.import_buttons_layout.addLayout(row2)

            # Terceira linha: Pan
            row3 = QHBoxLayout()
            row3.addWidget(self.import_panc_button)
            self.import_buttons_layout.addLayout(row3)

        else:
            # Para Landsat 08, mantém o layout padrão (MultiS + Pan)
            row1 = QHBoxLayout()
            row1.addWidget(self.import_multispectral_button)
            row1.addWidget(self.import_panc_button)
            self.import_buttons_layout.addLayout(row1)

    def open_tutorial(self):
        with open(TUTORIAL_PATH, "r", encoding='utf-8') as file:
            tutorial_content = file.read()

        html_content = markdown.markdown(tutorial_content)

        self.tutorial_dialog = TutorialDialog(html_content)
        self.tutorial_dialog.show()

    def open_api_setup_landsat(self):
        self.api_setup_window = SetUpApiLandsat()
        self.api_setup_window.show()

    def open_api_setup_cbers(self):
        self.api_setup_window = SetUpApiCBERS()
        self.api_setup_window.show()

    def crop_image(self):
        self.crop_image_window = CropImageWindow()
        self.crop_image_window.show()

    def import_band1(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione a banda azul:", "", "Tif files (*.tif)")
        if file_path:
            self.band1_path = file_path

    def import_band2(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione a banda verde:", "", "Tif files (*.tif)")
        if file_path:
            self.band2_path = file_path

    def import_band3(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione a banda vermelha:", "", "Tif files (*.tif)")
        if file_path:
            self.band3_path = file_path

    def import_band4(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione a banda infravermelha próxima:", "", "Tif files (*.tif)")
        if file_path:
            self.band4_path = file_path
    
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

    def select_output_folder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, "Selecione o diretório de saída")
        if folder_path:
            self.output_path = Path(folder_path) / "resultado_fusao.tif"

    def open_pca_method(self):
        if self.output_path != '':
            if self.satellite_field.currentText() == 'CBERS 04A':
                try:
                    band_1_path_str = str(self.band1_path)
                    band_2_path_str = str(self.band2_path)
                    band_3_path_str = str(self.band3_path)
                    band_4_path_str = str(self.band4_path)
                    panchromatic_path_str = str(self.panchromatic_path)
                    output_path_str = str(self.output_path)

                    pca_fusion_cbers(
                        band_1_path_str,
                        band_2_path_str,
                        band_3_path_str,
                        band_4_path_str,
                        panchromatic_path_str,
                        output_path_str
                    )

                    success_message = QMessageBox()
                    success_message.setIcon(QMessageBox.Icon.Information)
                    success_message.setWindowTitle("Sucesso")
                    success_message.setText("Fusão realizada com sucesso!")
                    success_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    success_message.exec()

                except Exception as e:
                    error_message = QMessageBox()
                    error_message.setIcon(QMessageBox.Icon.Critical)
                    error_message.setWindowTitle("Erro")
                    error_message.setText(error_string)
                    translated_error = translator.translate(str(e))
                    error_message.setInformativeText(translated_error)
                    error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    error_message.exec()

            else:
                try:
                    multispectral_path_str = str(self.multiespectral_path)
                    panchromatic_path_str = str(self.panchromatic_path)
                    output_path_str = str(self.output_path)

                    pca_fusion_landsat(
                    multispectral_path_str,
                    panchromatic_path_str,
                    output_path_str
                )
                    success_message = QMessageBox()
                    success_message.setIcon(QMessageBox.Icon.Information)
                    success_message.setWindowTitle("Sucesso")
                    success_message.setText("Fusão realizada com sucesso!")
                    success_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    success_message.exec()

                except Exception as e:
                    error_message = QMessageBox()
                    error_message.setIcon(QMessageBox.Icon.Critical)
                    error_message.setWindowTitle("Erro")
                    error_message.setText(error_string)
                    translated_error = translator.translate(str(e))
                    error_message.setInformativeText(translated_error)
                    error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    error_message.exec()

        else:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Icon.Critical)
            error_message.setWindowTitle("Erro")
            error_message.setText(error_string)
            error_message.setInformativeText("Por favor, insira um diretório de saída.")
            error_message.setStandardButtons(QMessageBox.StandardButton.Ok)  
            error_message.exec()
                

    def open_colorimetric_method(self):
        if self.output_path != '':
            if self.satellite_field.currentText() == 'CBERS 04A':
                try:
                    band_1_path_str = str(self.band1_path)
                    band_2_path_str = str(self.band2_path)
                    band_3_path_str = str(self.band3_path)
                    panchromatic_path_str = str(self.panchromatic_path)
                    output_path_str = str(self.output_path)

                    colorimetric_fusion_cbers(
                        band_1_path_str,
                        band_2_path_str,
                        band_3_path_str,
                        panchromatic_path_str,
                        output_path_str
                    )

                    success_message = QMessageBox()
                    success_message.setIcon(QMessageBox.Icon.Information)
                    success_message.setWindowTitle("Sucesso")
                    success_message.setText("Fusão realizada com sucesso!")
                    success_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    success_message.exec()

                except Exception as e:
                    error_message = QMessageBox()
                    error_message.setIcon(QMessageBox.Icon.Critical)
                    error_message.setWindowTitle("Erro")
                    error_message.setText(error_string)
                    translated_error = translator.translate(str(e))
                    error_message.setInformativeText(translated_error)
                    error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    error_message.exec()
            else:
                try:
                    multispectral_path_str = str(self.multiespectral_path)
                    panchromatic_path_str = str(self.panchromatic_path)
                    output_path_str = str(self.output_path)

                    colorimetric_fusion_landsat(
                    multispectral_path_str,
                    panchromatic_path_str,
                    output_path_str
                )
                    
                    success_message = QMessageBox()
                    success_message.setIcon(QMessageBox.Icon.Information)
                    success_message.setWindowTitle("Sucesso")
                    success_message.setText("Fusão realizada com sucesso!")
                    success_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    success_message.exec()

                except Exception as e:
                    error_message = QMessageBox()
                    error_message.setIcon(QMessageBox.Icon.Critical)
                    error_message.setWindowTitle("Erro")
                    error_message.setText(error_string)
                    translated_error = translator.translate(str(e))
                    error_message.setInformativeText(translated_error)
                    error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    error_message.exec()

        else:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Icon.Critical)
            error_message.setWindowTitle("Erro")
            error_message.setText(error_string)
            error_message.setInformativeText("Por favor, insira um diretório de saída.")
            error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_message.exec()
        

class TutorialDialog(QDialog):
    '''
    Janela de diálogo para exibir o tutorial de uso da aplicação.

    O conteúdo do tutorial é carregado a partir de um arquivo Markdown.
    '''

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
        self.close_button.setObjectName("Button")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        # Configurando o layout do widget
        self.setLayout(self.layout)

        self.setMinimumSize(500, 300)


class SetUpApiLandsat(QWidget):
    '''
    Janela de configuração da API para download de imagens Landsat.

    Nesta janela, o usuário deve inserir o nome do projeto GEE, o ID da imagem Landsat,
    a área de interesse e o diretório de saída das imagens.
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração de API")

        # Configurando o layout principal
        self.layout = QVBoxLayout()

        # Criando os campos de entrada
        self.account_field = QLineEdit()
        self.account_field.setPlaceholderText("Nome do Projeto GEE")
        self.layout.addWidget(self.account_field)

        # Diretório do drive de saída das imagens
        self.output_folder_field_images = QLineEdit()
        self.output_folder_field_images.setPlaceholderText("Diretório do Google Drive onde as imagens serão salvas")
        self.layout.addWidget(self.output_folder_field_images)

        # ID da imagem do satélite
        self.id_field = QLineEdit()
        self.id_field.setPlaceholderText("ID")
        self.layout.addWidget(self.id_field)

        # Área de recorte da imagem
        self.area_of_interest_field = QLineEdit()
        self.area_of_interest_field.setPlaceholderText("Área de interesse")
        self.layout.addWidget(self.area_of_interest_field)

        # Criando o botão de execução
        self.execute_button = QPushButton("Confirmar")
        self.execute_button.setObjectName("WButton")
        self.execute_button.clicked.connect(self.execute)
        self.layout.addWidget(self.execute_button)

        # Configurando o layout do widget
        self.setLayout(self.layout)

        self.setMinimumSize(500, 300)


    def execute(self):
        # Chamando a função de API com os parâmetros necessários
        try:
            download_landsat(
                self.account_field.text(),
                self.satellite_field.currentText(),
                self.id_field.text(),
                self.area_of_interest_field.text().split(","),
                self.output_folder_field_images.text()
            )

            if True:
                success_message = QMessageBox()
                success_message.setIcon(QMessageBox.Icon.Information)
                success_message.setWindowTitle("Sucesso")
                success_message.setText("Imagens baixadas com sucesso! Cheque seu Google Drive.")
                success_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                success_message.exec()

                self.close()

        except Exception as e:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Icon.Critical)
            error_message.setWindowTitle("Erro")
            error_message.setText(error_string)
            translated_error = translator.translate(str(e))
            error_message.setInformativeText(translated_error)
            error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_message.exec()


class SetUpApiCBERS(QWidget):
    '''
    Janela de configuração da API para download de imagens CBERS.

    Nesta janela, o usuário deve inserir o email, bbox, datas inicial e final, nuvem e limite.
    Depois, o usuário pode selecionar a imagem que deseja e a baixar.
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CBERS Image Viewer')

        # Layout principal
        layout = QVBoxLayout()

        # Campo para email
        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        # Campo para bbox
        self.bbox_label = QLabel('BBox:')
        self.bbox_input = QLineEdit()
        layout.addWidget(self.bbox_label)
        layout.addWidget(self.bbox_input)

        # Campo para data inicial
        self.initial_date_label = QLabel('Data Inicial: (AAAA, MM, DD)')
        self.initial_date_input = QLineEdit()
        layout.addWidget(self.initial_date_label)
        layout.addWidget(self.initial_date_input)

        # Campo para data final
        self.final_date_label = QLabel('Data Final: (AAAA, MM, DD)')
        self.final_date_input = QLineEdit()
        layout.addWidget(self.final_date_label)
        layout.addWidget(self.final_date_input)

        # Campo para nuvem
        self.cloud_label = QLabel('Nuvem:')
        self.cloud_input = QLineEdit()
        layout.addWidget(self.cloud_label)
        layout.addWidget(self.cloud_input)

        # Campo para limite
        self.limit_label = QLabel('Limite:')
        self.limit_input = QLineEdit()
        layout.addWidget(self.limit_label)
        layout.addWidget(self.limit_input)

        # Lista para mostrar os scene_id
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Botão para carregar imagens
        self.load_button = QPushButton('Carregar Imagens')
        self.load_button.setObjectName("WButton")
        layout.addWidget(self.load_button)

        # Conectar o botão à função de carregar imagens
        self.load_button.clicked.connect(self.load_images)

        # Obter caminho para salvar a imagem
        self.output_folder_field = QPushButton("Selecione o diretório de saída")
        self.output_folder_field.setObjectName("WButton")
        self.output_folder_field.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_folder_field)

        # Botão para baixar a imagem
        self.download_button = QPushButton('Baixar Imagem')
        self.download_button.setObjectName("WButton")
        self.download_button.clicked.connect(self.download_image)
        layout.addWidget(self.download_button)

        # Definir layout
        self.setLayout(layout)

        self.api_cbers = None
        self.output_path = None 

    # Função para carregar imagens ao clicar no botão
    def load_images(self):
        try:
            # Processando o bbox a partir do input de texto
            bbox_text = self.bbox_input.text()  # Recebe o texto do bbox
            bbox = [float(coord) for coord in bbox_text.split(',')]  # Converte em lista de floats

            # Convertendo datas para tuplas (AAAA, MM, DD)
            initial_date = tuple(map(int, self.initial_date_input.text().split(',')))
            final_date = tuple(map(int, self.final_date_input.text().split(',')))

            # Convertendo nuvem e limite
            cloud = int(self.cloud_input.text())
            limit = int(self.limit_input.text())

            # Chama a função para buscar os scene_id
            self.api_cbers = Cbers4aAPI(self.email_input.text())  
            scene_info = get_images(
                self.api_cbers,
                bbox,
                initial_date,
                final_date,
                cloud,
                limit
            )

            # Limpa a lista antes de exibir novos dados
            self.list_widget.clear()

            # Adiciona os scene_id e coleção na lista da interface
            for scene_id, collection in scene_info:
                if collection == 'CBERS4A_WPM_L2_DN':
                    collection = 'L2'
                elif collection == 'CBERS4A_WPM_L4_DN':
                    collection = 'L4'
                display_text = f"{scene_id} - {collection}"  # Formata a string
                self.list_widget.addItem(display_text)


        except Exception as e:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Icon.Critical)
            error_message.setWindowTitle("Erro")
            error_message.setText("Erro ao carregar imagens.")
            translated_error = translator.translate(str(e))
            error_message.setInformativeText(translated_error)
            error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_message.exec()

    def select_output_folder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, "Selecione o diretório de saída")
        if folder_path:
            self.output_path = folder_path  # Armazena o caminho selecionado

    def download_image(self):
        try:
            selected_item = self.list_widget.currentItem()  # Obtem o item selecionado
            if not self.output_path or not selected_item:
                raise Exception("Por favor, selecione um diretório e uma imagem.")

            download_cbers(
                self.api_cbers,
                selected_item.text(),
                self.output_path
            )

            success_message = QMessageBox()
            success_message.setIcon(QMessageBox.Icon.Information)
            success_message.setWindowTitle("Sucesso")
            success_message.setText("Imagens baixadas com sucesso! Cheque seu diretório de saída.")
            success_message.exec()
            self.close()

        except Exception as e:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Icon.Critical)
            error_message.setWindowTitle("Erro")
            error_message.setText("Erro ao baixar a imagem.")
            translated_error = translator.translate(str(e))
            error_message.setInformativeText(translated_error)
            error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_message.exec()


class CropImageWindow(QWidget):
    '''
    Janela de recorte de imagem.

    Nesta janela, o usuário deve selecionar a imagem que deseja recortar, o diretório de saída,
    o nome da imagem de saída e as coordenadas.
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recorte de Imagem")

        # Configurando o layout principal
        self.layout = QVBoxLayout()

        # Criação do botão de seleção de imagem:
        self.input_field = QPushButton("Selecione a imagem")
        self.input_field.setObjectName("WButton")
        self.input_field.clicked.connect(self.select_input_image)
        self.layout.addWidget(self.input_field)        

        # Diretório de saída
        self.output_folder_field = QPushButton("Selecione o diretório de saída")
        self.output_folder_field.setObjectName("WButton")
        self.output_folder_field.clicked.connect(self.select_output_folder)
        self.layout.addWidget(self.output_folder_field)   

        # Nome da imagem de saída
        self.output_folder_name = QLineEdit()
        self.output_folder_name.setPlaceholderText("Nome da imagem de saída")
        self.layout.addWidget(self.output_folder_name)

        # Coordenadas do canto superior esquerdo
        self.upper_left_x_field = QLineEdit()
        self.upper_left_x_field.setPlaceholderText("Longitude mínima")
        self.layout.addWidget(self.upper_left_x_field)

        self.upper_left_y_field = QLineEdit()
        self.upper_left_y_field.setPlaceholderText("Latitude mínima")
        self.layout.addWidget(self.upper_left_y_field)

        # Coordenadas do canto inferior direito
        self.lower_right_x_field = QLineEdit()
        self.lower_right_x_field.setPlaceholderText("Longitude máxima")
        self.layout.addWidget(self.lower_right_x_field)

        self.lower_right_y_field = QLineEdit()
        self.lower_right_y_field.setPlaceholderText("Latitude máxima")
        self.layout.addWidget(self.lower_right_y_field)

        # Criando o botão de execução
        self.execute_button = QPushButton("Recortar")
        self.execute_button.setObjectName("WButton")
        self.execute_button.clicked.connect(self.execute)
        self.layout.addWidget(self.execute_button)

        # Configurando o layout do widget
        self.setLayout(self.layout)

        self.setMinimumSize(500, 300)

        # Inicializando variáveis para caminhos
        self.input_path = ""
        self.output_path = ""

    def execute(self):
        # Chamando a função de recorte com os parâmetros necessários
        try:
            # Verifica se os caminhos estão corretos
            if not self.input_path or not self.output_path or not self.output_folder_name.text():
                raise Exception("Por favor, preencha todos os campos e selecione os diretórios.")

            crop_image(
                self.input_path,
                self.output_path,
                self.output_folder_name.text(),
                float(self.upper_left_x_field.text()),
                float(self.upper_left_y_field.text()),
                float(self.lower_right_x_field.text()),
                float(self.lower_right_y_field.text())
            )

            success_message = QMessageBox()
            success_message.setIcon(QMessageBox.Icon.Information)
            success_message.setWindowTitle("Sucesso")
            success_message.setText("Imagem recortada com sucesso!")
            success_message.exec()

            self.close()

        except Exception as e:
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Icon.Critical)
            error_message.setWindowTitle("Erro")
            error_message.setText("Erro ao processar a imagem.")
            translated_error = translator.translate(str(e))
            error_message.setInformativeText(translated_error)
            error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_message.exec()

    def select_input_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione a imagem:", "", "Tif files (*.tif)")
        if file_path:
            self.input_path = file_path

    def select_output_folder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, "Selecione o diretório de saída")
        if folder_path:
            self.output_path = folder_path
