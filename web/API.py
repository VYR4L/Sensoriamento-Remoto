import ee
import subprocess

# Função para acessar a API do Google Earth Engine
def api(account, api_file, satellite, collection, id, area_of_interest, output_folder):
    satellite_name = ''
    conta = account
    caminho_da_api = api_file

    # Autenticar a sessão do Earth Engine
    ee.Authenticate()
    credenciais = ee.ServiceAccountCredentials(conta, caminho_da_api)
    ee.Initialize(credenciais)

    # Definir a área de interesse
    area_de_interesse = ee.Geometry.Rectangle(area_of_interest)

    if satellite == 'Landsat LC08':
        if collection == 'C01':
            satellite_name = 'LANDSAT/LC08/C01/T1_L2/'
        elif collection == 'C02':
            satellite_name = 'LANDSAT/LC08/C02/T1_L2/'
    elif satellite == 'Landsat LC09':
        if collection == 'C01':
            satellite_name = 'LANDSAT/LC09/C01/T1_L2/'
        elif collection == 'C02':
            satellite_name = 'LANDSAT/LC09/C02/T1_L2/'

    if id is not None:
        satellite_name = satellite_name + id

    if satellite_name.find('LANDSAT/LC') == True:
    # Acessar a imagem Landsat diretamente pelo ID
        imagem = ee.Image(satellite_name)

        # Recortar a imagem para a área de interesse
        imagem_recortada = imagem.clip(area_de_interesse)

        # Baixar a imagem
        exportation = f"earthengine --output={output_folder} export image {imagem_recortada.getDownloadURL()}"
        subprocess.call(exportation, shell=True)