from osgeo import gdal
import numpy as np
from sklearn.preprocessing import StandardScaler
import tempfile
import os


def read_band(file_path, band_number):
    '''
    Método para ler uma banda de um arquivo raster.

    :param file_path: Caminho do arquivo raster.
    :param band_number: Número da banda a ser lida.
    '''

    ds = gdal.Open(file_path)
    band = ds.GetRasterBand(band_number)
    array = band.ReadAsArray()
    return array, ds.GetGeoTransform(), ds.GetProjection()


def write_geotiff(output_path, data, geo_transform, projection):
    '''
    Método para salvar um array numpy como um arquivo GeoTIFF.

    :param output_path: Caminho do arquivo de saída.
    :param data: Array numpy a ser salvo.
    :param geo_transform: Transformação geométrica.
    :param projection: Projeção.
    '''

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(output_path, data.shape[2], data.shape[1], data.shape[0], gdal.GDT_Float32)
    out_raster.SetGeoTransform(geo_transform)
    out_raster.SetProjection(projection)
    for i in range(data.shape[0]):
        out_raster.GetRasterBand(i + 1).WriteArray(data[i])
    out_raster.FlushCache()
    out_raster = None


def resize_to_match(reference_ds, target_ds):
    '''
    Método para redimensionar uma imagem para ter as mesmas dimensões de outra imagem.

    :param reference_ds: Dataset de referência.
    :param target_ds: Dataset a ser redimensionado.
    '''

    # Redimensiona a imagem 'target_ds' para ter as mesmas dimensões que 'reference_ds'.
    # Salva a imagem redimensionada em um arquivo temporário.
    target_path_resized = tempfile.NamedTemporaryFile(suffix='.tif').name
    
    gdal.Warp(
        target_path_resized,
        target_ds,
        width=reference_ds.RasterXSize,
        height=reference_ds.RasterYSize,
        resampleAlg=gdal.GRA_Bilinear  # Algoritmo de reamostragem bilinear
    )
        
    return gdal.Open(target_path_resized)


def pca_fusion_landsat(multispectral_path, panchromatic_path, output_path):
    '''
    Fusão de imagens multiespectrais e pancromáticas usando Análise de Componentes Principais (PCA).

    :param multispectral_path: Caminho do arquivo multiespectral.
    :param panchromatic_path: Caminho do arquivo pancromático.
    :param output_path: Caminho do arquivo de saída.
    '''

    # Ler as bandas multiespectrais
    X1, geo_transform, projection = read_band(multispectral_path, 1)
    X2, _, _ = read_band(multispectral_path, 2)
    X3, _, _ = read_band(multispectral_path, 3)
    X4, _, _ = read_band(multispectral_path, 4)
    
    # Empilhar as bandas multiespectrais em uma matriz
    X = np.stack((X1, X2, X3, X4), axis=0)
    n_bands, n_rows, n_cols = X.shape
    x_flat = X.reshape(n_bands, -1).T

    # Ler a banda pancromática
    panchromatic_ds = gdal.Open(panchromatic_path)
    
    # Redimensionar a banda pancromática para corresponder à resolução multiespectral
    panchromatic_ds = resize_to_match(gdal.Open(multispectral_path), panchromatic_ds)
    pan = panchromatic_ds.GetRasterBand(1).ReadAsArray()

    # Normalizar a banda pancromática com base na banda a ser substituída
    pan = (pan - pan.min()) / (pan.max() - pan.min()) * (X.max() - X.min())
    
    # Centralizar os dados
    scaler = StandardScaler()
    x_flat = scaler.fit_transform(x_flat)

    # Calcular a matriz de covariância e obter os autovalores e autovetores
    cov_matrix = np.cov(x_flat, rowvar=False)
    eigvals, eigvecs = np.linalg.eig(cov_matrix)

    # Transformar os dados para o espaço dos componentes principais
    Y = np.dot(x_flat, eigvecs)

    # Substituir o primeiro componente principal pela banda pancromática
    pan_flat = pan.flatten()
    if pan_flat.shape[0] == Y[:, 0].shape[0]:  # Garantir que os tamanhos são iguais
        Y[:, 0] = pan_flat

    # Transformar de volta para o espaço original
    x_fused_flat = np.dot(Y, np.linalg.inv(eigvecs))
    x_fused_flat = scaler.inverse_transform(x_fused_flat)

    # Reshape para a forma original
    x_fused = x_fused_flat.T.reshape(n_bands, n_rows, n_cols)

    # Salvar a imagem resultante
    write_geotiff(output_path, x_fused, geo_transform, projection)


def pca_fusion_cbers(band_1_path, band_2_path, band_3_path, band_4_path, panchromatic_path, output_path):
    '''
    Fusão de imagens multiespectrais e pancromáticas usando Análise de Componentes Principais (PCA).

    :param band_1_path: Caminho da banda 1 (Red).
    :param band_2_path: Caminho da banda 2 (Green).
    :param band_3_path: Caminho da banda 3 (Blue).
    :param band_4_path: Caminho da banda 4 (NIR).
    :param panchromatic_path: Caminho da banda pancromática.
    '''

    # Ler as bandas multiespectrais
    X1, geo_transform, projection = read_band(band_1_path, 1)
    X2, _, _ = read_band(band_2_path, 1)
    X3, _, _ = read_band(band_3_path, 1)
    X4, _, _ = read_band(band_4_path, 1)


    # Empilhar as bandas multiespectrais em uma matriz
    X = np.stack((X1, X2, X3, X4), axis=0)
    n_bands, n_rows, n_cols = X.shape
    x_flat = X.reshape(n_bands, -1).T

    # Ler a banda pancromática
    panchromatic_ds = gdal.Open(panchromatic_path)

    # Redimensionar a banda pancromática para corresponder à resolução multiespectral
    panchromatic_ds = resize_to_match(gdal.Open(band_1_path), panchromatic_ds)
    pan = panchromatic_ds.GetRasterBand(1).ReadAsArray()

    # Normalizar a banda pancromática com base na banda a ser substituída
    pan = (pan - pan.min()) / (pan.max() - pan.min()) * (X.max() - X.min())

    # Centralizar os dados
    scaler = StandardScaler()

    x_flat = scaler.fit_transform(x_flat)

    # Calcular a matriz de covariância e obter os autovalores e autovetores
    cov_matrix = np.cov(x_flat, rowvar=False)
    eigvals, eigvecs = np.linalg.eig(cov_matrix)

    # Transformar os dados para o espaço dos componentes principais
    Y = np.dot(x_flat, eigvecs)

    # Substituir o primeiro componente principal pela banda pancromática
    pan_flat = pan.flatten()
    if pan_flat.shape[0] == Y[:, 0].shape[0]:  # Garantir que os tamanhos são iguais
        Y[:, 0] = pan_flat

    # Transformar de volta para o espaço original
    x_fused_flat = np.dot(Y, np.linalg.inv(eigvecs))
    x_fused_flat = scaler.inverse_transform(x_fused_flat)

    # Reshape para a forma original
    x_fused = x_fused_flat.T.reshape(n_bands, n_rows, n_cols)

    # Salvar a imagem resultante
    write_geotiff(output_path, x_fused, geo_transform, projection)