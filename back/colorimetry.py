from osgeo import gdal
import numpy as np
import cv2


def rgb_to_ihs(r, g, b):
    # Converte RGB para IHS
    rgb = np.stack([r, g, b], axis=-1)
    ihs = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    return ihs[..., 2], ihs[..., 1], ihs[..., 0]  # IHS -> HSI com canais H, S, I


def ihs_to_rgb(h, s, i):
    # Converte IHS para RGB
    ihs = np.stack([h, s, i], axis=-1)
    rgb = cv2.cvtColor(ihs, cv2.COLOR_HSV2RGB)
    return rgb[..., 0], rgb[..., 1], rgb[..., 2]


def colorimetric_fusion(multispectral_path, panchromatic_path, output_path):
    # Abrir as imagens multiespectral e pancromática
    multispectral_ds = gdal.Open(multispectral_path)
    panchromatic_ds = gdal.Open(panchromatic_path)

    # Ler as três bandas multiespectrais para RGB (e.g., B2, B3, B4)
    r = multispectral_ds.GetRasterBand(3).ReadAsArray()  # Banda Vermelha
    g = multispectral_ds.GetRasterBand(2).ReadAsArray()  # Banda Verde
    b = multispectral_ds.GetRasterBand(1).ReadAsArray()  # Banda Azul

    # Ler a banda pancromática
    panchromatic_data = panchromatic_ds.GetRasterBand(1).ReadAsArray()

    # Converter RGB para IHS
    i, h, s = rgb_to_ihs(r, g, b)

    # Substituir o componente de Intensidade pela banda pancromática
    i = panchromatic_data

    # Converter IHS de volta para RGB
    r, g, b = ihs_to_rgb(h, s, i)

    # Salvar a imagem resultante
    driver = gdal.GetDriverByName('GTiff')
    fused_ds = driver.Create(output_path, multispectral_ds.RasterXSize, multispectral_ds.RasterYSize, 3, gdal.GDT_Byte)
    fused_ds.SetProjection(multispectral_ds.GetProjection())
    fused_ds.SetGeoTransform(multispectral_ds.GetGeoTransform())
    fused_ds.GetRasterBand(1).WriteArray(r)
    fused_ds.GetRasterBand(2).WriteArray(g)
    fused_ds.GetRasterBand(3).WriteArray(b)
    fused_ds = None
