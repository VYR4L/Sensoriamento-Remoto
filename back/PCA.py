from osgeo import gdal
import numpy as np
from sklearn.preprocessing import StandardScaler


def read_band(file_path, band_number):
    ds = gdal.Open(file_path)
    band = ds.GetRasterBand(band_number)
    array = band.ReadAsArray()
    return array


def write_geotiff(output_path, data, geo_transform, projection):
    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(output_path, data.shape[2], data.shape[1], data.shape[0], gdal.GDT_Float32)
    out_raster.SetGeoTransform(geo_transform)
    out_raster.SetProjection(projection)
    for i in range(data.shape[0]):
        out_raster.GetRasterBand(i + 1).WriteArray(data[i])
    out_raster.FlushCache()
    out_raster = None


def pca_fusion(multispectral_path, panchromatic_path, output_path):
    # Ler as bandas multiespectrais
    X1 = read_band(multispectral_path, 1)
    X2 = read_band(multispectral_path, 2)
    X3 = read_band(multispectral_path, 3)
    X4 = read_band(multispectral_path, 4)
    
    # Empilhar as bandas multiespectrais em uma matriz
    X = np.stack((X1, X2, X3, X4), axis=0)
    n_bands, n_rows, n_cols = X.shape
    X_flat = X.reshape(n_bands, -1).T

    # Ler a banda pancromática e normalizá-la com base na banda a ser substituída
    pan = read_band(panchromatic_path, 1)
    pan = (pan - pan.min()) / (pan.max() - pan.min()) * (X.max() - X.min())
    # Centralizar os dados
    scaler = StandardScaler()
    X_flat = scaler.fit_transform(X_flat)

    # Calcular a matriz de covariância e obter os autovalores e autovetores
    cov_matrix = np.cov(X_flat, rowvar=False)
    eigvals, eigvecs = np.linalg.eig(cov_matrix)

    # Transformar os dados para o espaço dos componentes principais
    Y = np.dot(X_flat, eigvecs)

    # Substituir o primeiro componente principal pela banda pancromática
    pan_flat = pan.flatten()
    Y[:, 0] = pan_flat

    # Transformar de volta para o espaço original
    X_fused_flat = np.dot(Y, np.linalg.inv(eigvecs))
    X_fused_flat = scaler.inverse_transform(X_fused_flat)

    # Reshape para a forma original
    X_fused = X_fused_flat.T.reshape(n_bands, n_rows, n_cols)

    # Salvar a imagem resultante
    multispectral_ds = gdal.Open(multispectral_path)
    geo_transform = multispectral_ds.GetGeoTransform()
    projection = multispectral_ds.GetProjection()
    
    write_geotiff(output_path, X_fused, geo_transform, projection)
