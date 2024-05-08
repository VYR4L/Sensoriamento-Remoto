import numpy as np
from osgeo import gdal
from sklearn.decomposition import PCA


# TODO: Englobar numa função e receber por parametros no pyqt

# Caminho para as imagens multiespectral e pancromática
multispectral_path = "caminho_para_a_imagem_multiespectral.tif"
panchromatic_path = "caminho_para_a_imagem_pancromatica.tif"

# Abrindo as imagens com GDAL
multispectral_dataset = gdal.Open(multispectral_path)
panchromatic_dataset = gdal.Open(panchromatic_path)

# Lendo os dados das imagens
multispectral_data = multispectral_dataset.ReadAsArray()
panchromatic_data = panchromatic_dataset.ReadAsArray()

# Obtendo as dimensões das imagens
rows, cols = multispectral_data.shape

# Redimensionando a imagem pancromática para a mesma resolução espacial da imagem multiespectral
panchromatic_data_resized = np.zeros((rows, cols))
gdal.ReprojectImage(
    panchromatic_dataset,
    np.zeros((rows, cols)),
    multispectral_dataset.GetProjection(),
    np.zeros((rows, cols)),
    multispectral_dataset.GetProjection(),
    gdal.GRA_Bilinear, 0, 0,
    callback=None,
    callback_data=None)

# Reformulando os dados para a entrada do PCA
panchromatic_flat = panchromatic_data_resized.flatten()
multispectral_flat = multispectral_data.reshape(multispectral_data.shape[0], -1).T

# Aplicando o PCA
pca = PCA(n_components=1)
panchromatic_pca = pca.fit_transform(panchromatic_flat.reshape(-1, 1))
fused_data = multispectral_flat + panchromatic_pca @ pca.components_

# Reshape dos dados fundidos
fused_data_reshaped = fused_data.T.reshape(multispectral_data.shape)

# Salvando a imagem resultante
output_path = "caminho_para_a_imagem_fundida.tif"
driver = gdal.GetDriverByName("GTiff")
output_dataset = driver.Create(output_path, cols, rows, multispectral_dataset.RasterCount, multispectral_dataset.GetRasterBand(1).DataType)

# Escrevendo os dados na banda
for i in range(multispectral_dataset.RasterCount):
    output_band = output_dataset.GetRasterBand(i + 1)
    output_band.WriteArray(fused_data_reshaped[i, :, :])

# Copiando informações de georreferenciamento e projeção da imagem multiespectral
output_dataset.SetGeoTransform(multispectral_dataset.GetGeoTransform())
output_dataset.SetProjection(multispectral_dataset.GetProjection())

# Fechando os datasets
multispectral_dataset = None
panchromatic_dataset = None
output_dataset = None

print("Fusão espacial concluída. Imagem resultante salva em:", output_path)
