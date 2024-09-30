import ee


# Função para acessar a API do Google Earth Engine
def download_landsat(project_name, id, area_of_interest, output_folder):
    '''
    Baixa imagens Landsat 8 a partir de um ID e área de interesse.

    :param project_name: Nome do projeto no Google Earth Engine.
    :param id: ID da imagem Landsat 8.
    :param area_of_interest: Área de interesse no formato (min_lon, min_lat, max_lon, max_lat).
    :param output_folder: Pasta onde a imagem será salva.
    '''

    # Autenticar a sessão do Earth Engine
    ee.Authenticate()
    ee.Initialize(project=project_name)

     # Definir a área de interesse
    list_of_coordinates = []
    for i in area_of_interest:
        list_of_coordinates += i.split(' ')

    list_of_coordinates = list(filter(None, list_of_coordinates))
    area_de_interesse = ee.Geometry.Rectangle([float(list_of_coordinates[0]), float(list_of_coordinates[1]), float(list_of_coordinates[2]), float(list_of_coordinates[3])])

    satellite_name = 'LANDSAT/LC08/C02/T1/LC08_' + id

    # Acessar a imagem Landsat diretamente pelo ID
    imagem = ee.Image(satellite_name).select('B1', 'B2', 'B3', 'B4')  # Imagem multiespectral

    # Recortar a imagem para a área de interesse
    imagem_recortada = imagem.clip(area_de_interesse)

    # Descrição da imagem
    description = satellite_name + '_multiespectral'

    # Exportar a imagem para o Google Drive
    task = ee.batch.Export.image.toDrive(
        image=imagem_recortada,
        description=description.replace('/', '-'),
        folder=output_folder,
        scale=30,
        region=area_de_interesse,
        fileFormat='GeoTIFF'
    )
    task.start()

    # Acessar e exportar a imagem pancromática
    imagem_pancro = ee.Image(satellite_name).select('B8')  # Imagem pancromática
    imagem_pancro_recortada = imagem_pancro.clip(area_de_interesse)
    description_pancro = satellite_name + '_pancromatica'

    # Exportar a imagem pancromática
    task_pancro = ee.batch.Export.image.toDrive(
        image=imagem_pancro_recortada,
        description=description_pancro.replace('/', '-'),
        folder=output_folder,
        scale=15,
        region=area_de_interesse,
        fileFormat='GeoTIFF'
    )
    task_pancro.start()

    return True

