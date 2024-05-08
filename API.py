import ee
import datetime

# Insersão das credenciais
conta = "api-geo-processamento@ee-fkzzanatt.iam.gserviceaccount.com"
caminho_da_api = "ee-fkzzanatt-ac9270b29327.json"

# Autenticar a sessão do Earth Engine
ee.Authenticate()
credenciais = ee.ServiceAccountCredentials(conta, caminho_da_api)
ee.Initialize(credenciais)

# Definir a área de interesse
area_de_interesse = ee.Geometry.Rectangle([-96.5682, 39.1816, -96.5616, 39.1847])


# Acessar a imagem Landsat diretamente pelo ID
imagem = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_028033_20240414')

# Recortar a imagem para a área de interesse
imagem_recortada = imagem.clip(area_de_interesse)

# Baixar a imagem
ee.batch.Export.image.toDrive(image=imagem_recortada,
                              description='landsat_image',
                              folder='landsat_images',
                              scale=30).start()
