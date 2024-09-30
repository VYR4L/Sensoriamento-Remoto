from osgeo import gdal
import numpy as np
import os
import tempfile

def rgb_to_hsv(r, g, b):
    # Converte RGB para HSV manualmente
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    maxc = np.maximum(r, np.maximum(g, b))
    minc = np.minimum(r, np.minimum(g, b))
    v = maxc

    # Inicializando a matriz para o canal de saturação
    s = np.zeros_like(maxc)

    # Evitando divisão por zero para saturação e tom
    delta = maxc - minc
    non_zero_mask = maxc != 0  # Evitar divisão por zero onde maxc é zero
    s[non_zero_mask] = delta[non_zero_mask] / maxc[non_zero_mask]

    # Inicializando a matriz para o canal de matiz (hue)
    h = np.zeros_like(maxc)

    # Apenas calcular o tom (hue) onde a diferença não é zero
    non_zero_delta_mask = delta != 0
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)

    rc[non_zero_delta_mask] = (maxc[non_zero_delta_mask] - r[non_zero_delta_mask]) / delta[non_zero_delta_mask]
    gc[non_zero_delta_mask] = (maxc[non_zero_delta_mask] - g[non_zero_delta_mask]) / delta[non_zero_delta_mask]
    bc[non_zero_delta_mask] = (maxc[non_zero_delta_mask] - b[non_zero_delta_mask]) / delta[non_zero_delta_mask]

    h[non_zero_delta_mask & (maxc == r)] = (bc[non_zero_delta_mask & (maxc == r)] - gc[non_zero_delta_mask & (maxc == r)]) % 6
    h[non_zero_delta_mask & (maxc == g)] = 2.0 + rc[non_zero_delta_mask & (maxc == g)] - bc[non_zero_delta_mask & (maxc == g)]
    h[non_zero_delta_mask & (maxc == b)] = 4.0 + gc[non_zero_delta_mask & (maxc == b)] - rc[non_zero_delta_mask & (maxc == b)]

    h = (h / 6.0) % 1.0

    # Onde não há diferença de cores, o tom (hue) pode ser definido como 0
    h[maxc == minc] = 0.0

    return h * 255.0, s * 255.0, v * 255.0


def hsv_to_rgb(h, s, v):
    # Converte HSV para RGB manualmente
    h = h / 255.0
    s = s / 255.0
    v = v / 255.0
    i = np.floor(h * 6.0).astype(int)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)

    i = i % 6
    r = np.zeros_like(h)
    g = np.zeros_like(h)
    b = np.zeros_like(h)

    r[i == 0] = v[i == 0]
    g[i == 0] = t[i == 0]
    b[i == 0] = p[i == 0]
    r[i == 1] = q[i == 1]
    g[i == 1] = v[i == 1]
    b[i == 1] = p[i == 1]
    r[i == 2] = p[i == 2]
    g[i == 2] = v[i == 2]
    b[i == 2] = t[i == 2]
    r[i == 3] = p[i == 3]
    g[i == 3] = q[i == 3]
    b[i == 3] = v[i == 3]
    r[i == 4] = t[i == 4]
    g[i == 4] = p[i == 4]
    b[i == 4] = v[i == 4]
    r[i == 5] = v[i == 5]
    g[i == 5] = p[i == 5]
    b[i == 5] = q[i == 5]

    return r * 255, g * 255, b * 255


def resize_to_match(reference_ds, target_ds):
    # Redimensiona a imagem 'target_ds' para ter as mesmas dimensões que 'reference_ds'.
    # Salva a imagem redimensionada em um arquivo temporário.
    target_path_resized = tempfile.NamedTemporaryFile(suffix='.tif', delete=True).name
    
    gdal.Warp(
        target_path_resized,
        target_ds,
        width=reference_ds.RasterXSize,
        height=reference_ds.RasterYSize,
        resampleAlg=gdal.GRA_Bilinear  # Algoritmo de reamostragem bilinear
    )
    
    return gdal.Open(target_path_resized)


def colorimetric_fusion_landsat(multispectral_path, panchromatic_path, output_path):
    '''
    Método para realizar a fusão colorimétrica de uma imagem Landsat 8.

    :param multispectral_path: Caminho da imagem multiespectral.
    :param panchromatic_path: Caminho da imagem pancromática.
    :param output_path: Caminho onde a imagem resultante será salva.
    '''

    # Abrir as imagens multiespectral e pancromática
    multispectral_ds = gdal.Open(multispectral_path)
    panchromatic_ds = gdal.Open(panchromatic_path)

    # Redimensionar as bandas multiespectrais para corresponder à pancromática
    multispectral_ds = resize_to_match(panchromatic_ds, multispectral_ds)

    # Ler as três bandas multiespectrais para RGB
    r = multispectral_ds.GetRasterBand(4).ReadAsArray()  # Banda Vermelha
    g = multispectral_ds.GetRasterBand(3).ReadAsArray()  # Banda Verde
    b = multispectral_ds.GetRasterBand(2).ReadAsArray()  # Banda Azul

    # Ler a banda pancromática
    pan = panchromatic_ds.GetRasterBand(1).ReadAsArray()

    # Normalizar a banda pancromática
    pan = (pan - pan.min()) / (pan.max() - pan.min()) * 255

    # Converter RGB para HSV
    h, s, v = rgb_to_hsv(r, g, b)

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


def colorimetric_fusion_cbers(band_1_path, band_2_path, band_3_path, panchromatic_path, output_path):
    '''
    Método para realizar a fusão colorimétrica de uma imagem CBERS4.

    :param band_1_path: Caminho da banda 1 (Azul).
    :param band_2_path: Caminho da banda 2 (Verde).
    :param band_3_path: Caminho da banda 3 (Vermelha).
    :param panchromatic_path: Caminho da imagem pancromática.
    :param output_path: Caminho onde a imagem resultante será salva.
    '''

    blue_ds = gdal.Open(band_1_path)
    green_ds = gdal.Open(band_2_path)
    red_ds = gdal.Open(band_3_path)
    panchromatic_ds = gdal.Open(panchromatic_path)

    blue_ds = resize_to_match(panchromatic_ds, blue_ds)
    green_ds = resize_to_match(panchromatic_ds, green_ds)
    red_ds = resize_to_match(panchromatic_ds, red_ds)

    blue = blue_ds.GetRasterBand(1).ReadAsArray()
    green = green_ds.GetRasterBand(1).ReadAsArray()
    red = red_ds.GetRasterBand(1).ReadAsArray()

    pan = panchromatic_ds.GetRasterBand(1).ReadAsArray()
    
    # Normalize o pano
    pan_min = pan.min()
    pan_max = pan.max()

    if pan_max - pan_min == 0:
        # Isso significa que todos os valores de 'pan' são iguais
        pan[:] = 0  # Ou use outro valor padrão como 255 ou um valor médio
    else:
        pan = (pan - pan_min) / (pan_max - pan_min) * 255

    h, s, v = rgb_to_hsv(red, green, blue)
    v = pan
    red, green, blue = hsv_to_rgb(h, s, v)

    driver = gdal.GetDriverByName('GTiff')
    fused_ds = driver.Create(output_path, blue_ds.RasterXSize, blue_ds.RasterYSize, 3, gdal.GDT_Byte)
    fused_ds.SetProjection(blue_ds.GetProjection())
    fused_ds.SetGeoTransform(blue_ds.GetGeoTransform())
    fused_ds.GetRasterBand(1).WriteArray(red)
    fused_ds.GetRasterBand(2).WriteArray(green)
    fused_ds.GetRasterBand(3).WriteArray(blue)

