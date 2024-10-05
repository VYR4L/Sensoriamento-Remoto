import numpy as np
from PIL import Image
from osgeo import gdal

def save_raster(stacked_array, dataset, out_file):
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(out_file, dataset.RasterXSize, dataset.RasterYSize, 3, gdal.GDT_Byte)
    out_ds.SetProjection(dataset.GetProjection())
    out_ds.SetGeoTransform(dataset.GetGeoTransform())
    out_ds.GetRasterBand(1).WriteArray(stacked_array[0])
    out_ds.GetRasterBand(2).WriteArray(stacked_array[1])
    out_ds.GetRasterBand(3).WriteArray(stacked_array[2])
    out_ds.FlushCache()
    out_ds = None

def normalization(array):
    return (array - array.min()) / (array.max() - array.min()) * 255
     

class Colorimetry:

    def __init__(self):
        pass
    
    def hsv(self, pan, multi, output_path):
        def rgb_to_hsv(r, g, b):
            rgb = np.stack([r, g, b], axis=-1)
            img = Image.fromarray((rgb).astype(np.uint8), 'RGB').convert('HSV')
            hsv = np.array(img)
            h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
            return v, h, s

        def hsv_to_rgb(h, s, v):
            hsv = np.stack([h, s, v], axis=-1).astype(np.uint8)
            img = Image.fromarray(hsv, 'HSV').convert('RGB')
            rgb = np.array(img)
            return rgb[..., 0], rgb[..., 1] , rgb[..., 2]

        # Ler as três bandas multiespectrais para RGB
        r = normalization(multi.GetRasterBand(3).ReadAsArray())
        g = normalization(multi.GetRasterBand(2).ReadAsArray())
        b = normalization(multi.GetRasterBand(1).ReadAsArray())

        # Normalizar a banda pancromática
        pan = normalization(pan.GetRasterBand(1).ReadAsArray())

        # Converter RGB para HSV
        _, h, s = rgb_to_hsv(r, g, b)

        # Converter HSV de volta para RGB
        r, g, b = hsv_to_rgb(h, s, pan)

        # Salvar a imagem resultante
        stacked_array = np.stack((r, g, b), axis=0)
        save_raster(stacked_array, multi, output_path)

    def ihs():
        pass