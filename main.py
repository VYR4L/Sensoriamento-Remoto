import rasterio
import rasterio.features
import rasterio.warp
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

ROOT_DIR = Path(__file__).parent.parent
IMAGES_DIR = f'{ROOT_DIR}/images'

with rasterio.open('CBERS_Teste.tif') as dataset:
    mask = dataset.dataset_mask()

    band = dataset.read(1)
    print(band.shape)
    # print(band[dataset.height // 2, dataset.width // 2])
    # plt.imshow(band)
    # plt.colorbar()
    # plt.title(f'Banda')
    # plt.show()

    # SPATIAL INDEXING
    # x, y = (dataset.bounds.left + 100, dataset.bounds.top - 50)
    # row, col = dataset.index(x, y)
    # print(row, col)
    # print(band[row, col])
    # print(dataset.xy(dataset.height//2, dataset.width//2))

    # CREATING DATA
    # x = np.linspace(-4.0, 4.0, 240)
    # y = np.linspace(-3.0, 3.0, 180)
    # X, Y = np.meshgrid(x, y)
    # Z1 = np.exp(-2 * np.log(2) * ((X - 0.5) ** 2 + (Y - 0.5) ** 2) / 1 ** 2)
    # Z2 = np.exp(-3 * np.log(2) * ((X + 0.5) ** 2 + (Y + 0.5) ** 2) / 2.5 ** 2)
    # Z = 10 * (Z2 - Z1)
    # contour = plt.contour(X*1000, Y*1000, Z*1000, colors=['blue', 'green', 'red'])
    # plt.clabel(contour, inline=True, fontsize=8)
    # plt.show()

    # for geom, val in rasterio.features.shapes(
    #         mask, transform=dataset.transform):
    #     geom = rasterio.warp.transform_geom(
    #         dataset.crs, 'EPSG:32622', geom, precision=6)
    #     print(geom)

    # print(dataset.name)  #nome do arquivo
    # print(dataset.mode)  # modo de leitura
    # print(dataset.height)  # altura
    # print(dataset.width)  # largura
    # for i, dtype in zip(dataset.indexes, dataset.dtypes):
    #     print(i, dtype)
    #
    # print(dataset.bounds)
    # X2, Y2 = dataset.transform * (0, 0)  # coordenadas espaciais (x, y)
    # Z2 = 10 * (Y2 - Y2)
    # contour = plt.contour(X2, Y2, Z2, colors=['blue', 'green', 'red'])
    # plt.clabel(contour, inline=True, fontsize=8)
    # plt.show()
    # print(dataset.transform * (dataset.width, dataset.height))  # coordinate reference system (CRS)
    # print(dataset.crs)  #
