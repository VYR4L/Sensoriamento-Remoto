from osgeo import gdal
import numpy as np
from PIL import Image


def rgb_to_hsv(r, g, b):
    # Converte RGB para HSV
    rgb = np.stack([r, g, b], axis=-1).astype(np.float32) / 255.0
    img = Image.fromarray((rgb * 255).astype(np.uint8), 'RGB').convert('HSV')
    hsv = np.array(img)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    return v, h, s

def hsv_to_rgb(h, s, v):
    # Converte HSV para RGB
    hsv = np.stack([h, s, v], axis=-1).astype(np.uint8)
    img = Image.fromarray(hsv, 'HSV').convert('RGB')
    rgb = np.array(img) / 255.0
    return rgb[..., 0] * 255, rgb[..., 1] * 255, rgb[..., 2] * 255

def colorimetric_fusion(multispectral_path, panchromatic_path, output_path):
    # Abrir as imagens multiespectral e pancromática
    multispectral_ds = gdal.Open(multispectral_path)
    panchromatic_ds = gdal.Open(panchromatic_path)

    # Ler as três bandas multiespectrais para RGB
    r = multispectral_ds.GetRasterBand(3).ReadAsArray()  # Banda Vermelha
    g = multispectral_ds.GetRasterBand(2).ReadAsArray()  # Banda Verde
    b = multispectral_ds.GetRasterBand(1).ReadAsArray()  # Banda Azul

    # Ler a banda pancromática
    pan = panchromatic_ds.GetRasterBand(1).ReadAsArray()

    # Normalizar a banda pancromática
    pan = (pan - pan.min()) / (pan.max() - pan.min()) * 255

    # Converter RGB para HSV
    v, h, s = rgb_to_hsv(r, g, b)

    # Substituir o componente de Intensidade pela banda pancromática
    v = pan

    # Converter HSV de volta para RGB
    r, g, b = hsv_to_rgb(h, s, v)

    # Salvar a imagem resultante
    driver = gdal.GetDriverByName('GTiff')
    fused_ds = driver.Create(output_path, multispectral_ds.RasterXSize, multispectral_ds.RasterYSize, 3, gdal.GDT_Byte)
    fused_ds.SetProjection(multispectral_ds.GetProjection())
    fused_ds.SetGeoTransform(multispectral_ds.GetGeoTransform())
    fused_ds.GetRasterBand(1).WriteArray(r)
    fused_ds.GetRasterBand(2).WriteArray(g)
    fused_ds.GetRasterBand(3).WriteArray(b)
    fused_ds = None
