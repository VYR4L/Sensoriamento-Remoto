from osgeo import gdal
from osgeo_utils import gdal_pansharpen
import numpy as np
from sklearn.preprocessing import StandardScaler

def save_raster(array_data, dataset, file):
        drive = gdal.GetDriverByName('GTiff')
        num_bands = len(array_data)
        outdata = drive.Create(file,
                               dataset.RasterXSize,
                               dataset.RasterYSize,
                               num_bands, gdal.GDT_Float32)
        outdata.SetGeoTransform(dataset.GetGeoTransform())
        outdata.SetProjection(dataset.GetProjection())
        for i in range(num_bands):
            band = outdata.GetRasterBand(i + 1)
            band.WriteArray(array_data[i])
        outdata.FlushCache()
        outdata = None

class Stats:

    def __init__(self):
        pass

    def pansharp(self, pan, multi, out):

        gdal_pansharpen.main(['gdal_pansharpen.py', pan, multi, out])

    def pca(self, pan, multi, output_path):
        
        # Ler as bandas multiespectrais
        Xs = []
        for x in range(multi.RasterCount):
            Xs.append(multi.GetRasterBand(x+1).ReadAsArray())
        
        # Empilhar as bandas multiespectrais em uma matriz
        X = np.stack(Xs, axis=0)
        n_bands, n_rows, n_cols = X.shape
        x_flat = X.reshape(n_bands, -1).T

        # Ler a banda pancromática e normalizá-la com base na banda a ser substituída
        pan = pan.GetRasterBand(1).ReadAsArray()
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
        Y[:, 0] = pan_flat

        # Transformar de volta para o espaço original
        x_fused_flat = np.dot(Y, np.linalg.inv(eigvecs))
        x_fused_flat = scaler.inverse_transform(x_fused_flat)

        # Reshape para a forma original
        x_fused = x_fused_flat.T.reshape(n_bands, n_rows, n_cols)
        print(x_fused)

        # Salvar a imagem resultante
        save_raster(x_fused, multi, output_path)

    def brovey():
        pass