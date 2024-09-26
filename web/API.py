import ee
import subprocess


# Função para acessar a API do Google Earth Engine
def api(project_name, satellite, id, area_of_interest, output_folder):
    satellite_name = ''

    # Autenticar a sessão do Earth Engine
    ee.Authenticate()
    ee.Initialize(project=project_name)

     # Definir a área de interesse
    list_of_coordinates = []
    for i in area_of_interest:
        list_of_coordinates += i.split(' ')

    list_of_coordinates = list(filter(None, list_of_coordinates))
    area_de_interesse = ee.Geometry.Rectangle([float(list_of_coordinates[0]), float(list_of_coordinates[1]), float(list_of_coordinates[2]), float(list_of_coordinates[3])])

    # Definir o nome do satélite e da coleção
    if satellite == 'Landsat 08':
        satellite_name = 'LANDSAT/LC08/C02/T1/LC08_'

    if satellite == 'CBERS 04A':
        satellite_name = 'CBERS/C4/AWFI/'

    if id:
        satellite_name += id

    # Para imagens Landsat
    if 'LANDSAT/LC' in satellite_name:
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
            scale=10,
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
            scale=10,
            region=area_de_interesse,
            fileFormat='GeoTIFF'
        )
        task_pancro.start()

        return True

    # Para imagens CBERS
    if 'CBERS' in satellite_name:
        # Acessar a imagem CBERS diretamente pelo ID
        imagem = ee.Image(satellite_name).select('BAND13', 'BAND14', 'BAND15', 'BAND16')  # Imagem multiespectral
        imagem_recortada = imagem.clip(area_de_interesse)
        description = satellite_name + '_multiespectral'

        # Exportar a imagem multiespectral
        task = ee.batch.Export.image.toDrive(
            image=imagem_recortada,
            description=description.replace('/', '-'),
            folder=output_folder,
            scale=10,
            region=area_de_interesse,
            fileFormat='GeoTIFF'
        )
        task.start()

        # Exportar a imagem pancromática
        imagem_pancro = ee.Image(satellite_name).select('BAND20')
        imagem_pancro_recortada = imagem_pancro.clip(area_de_interesse)
        description_pancro = satellite_name + '_pancromatica'

        task_pancro = ee.batch.Export.image.toDrive(
            image=imagem_pancro_recortada,
            description=description_pancro.replace('/', '-'),
            folder=output_folder,
            scale=10,
            region=area_de_interesse,
            fileFormat='GeoTIFF'
        )
        task_pancro.start()

        return True
