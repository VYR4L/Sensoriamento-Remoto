import ee
import subprocess


# TODO arrumar o landsat
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

    # Definir o nome do satélite e da coleção
    if satellite == 'Landsat LC08':
        if collection == 'C01':
            satellite_name = 'LANDSAT/LC08/C01/T1/'
        elif collection == 'C02':
            satellite_name = 'LANDSAT/LC08/C02/T1/'
    elif satellite == 'Landsat LC09':
        if collection == 'C01':
            satellite_name = 'LANDSAT/LC09/C01/T1/'
        elif collection == 'C02':
            satellite_name = 'LANDSAT/LC09/C02/T1/'

    if satellite == 'CBERS':
        satellite_name = 'CBERS/C4/AWFI/'

    if id is not None:
        satellite_name = satellite_name + id

    if satellite_name.find('LANDSAT/LC') == True:
    # Acessar a imagem Landsat diretamente pelo ID
        imagem = ee.Image(satellite_name).select('B1','B2','B3','B4') # Imagem multiespectral

        # Recortar a imagem para a área de interesse
        imagem_recortada = imagem.clip(area_de_interesse)

        # Baixar a imagem
        exportation = f"earthengine --output={output_folder} export image {imagem_recortada.getDownloadURL()}"
        subprocess.call(exportation, shell=True)

        imagem = ee.Image(satellite_name).select('B8') # Imagem pancromática

        # Recortar a imagem para a área de interesse
        imagem_recortada = imagem.clip(area_de_interesse)

        # Baixar a imagem
        exportation = f"earthengine --output={output_folder} export image {imagem_recortada.getDownloadURL()}"
        subprocess.call(exportation, shell=True)

    if satellite_name.find('CBERS') == True:
        # Acessar a imagem CBERS diretamente pelo ID
        imagem = ee.Image(satellite_name).select('BAND13','BAND14','BAND15','BAND16') # Imagem multiespectral

        # Recortar a imagem para a área de interesse
        imagem_recortada = imagem.clip(area_de_interesse)

        # Baixar a imagem
        exportation = f"earthengine --output={output_folder} export image {imagem_recortada.getDownloadURL()}"
        subprocess.call(exportation, shell=False)

        imagem = ee.Image(satellite_name).select('BAND20') # Imagem pancromática

        # Recortar a imagem para a área de interesse
        imagem_recortada = imagem.clip(area_de_interesse)

        # Baixar a imagem
        exportation = f"earthengine --output={output_folder} export image {imagem_recortada.getDownloadURL()}"
        subprocess.call(exportation, shell=False)


