from osgeo import gdal
import numpy as np

def colorimetric_fusion(multispectral_path, panchromatic_path, output_path):
    # Abrir as imagens multiespectral e pancromática
    multispectral_ds = gdal.Open(multispectral_path)
    panchromatic_ds = gdal.Open(panchromatic_path)

    # Ler os dados das imagens
    multispectral_data = []
    for i in range(1, multispectral_ds.RasterCount + 1):
        band_data = multispectral_ds.GetRasterBand(i).ReadAsArray()
        multispectral_data.append(band_data)

    multispectral_data = np.array(multispectral_data)
    panchromatic_data = panchromatic_ds.GetRasterBand(1).ReadAsArray()

    # Realizar a fusão colorimétrica
    fused_data = np.zeros_like(multispectral_data[0], dtype=np.uint8)
    for i in range(fused_data.shape[0]):
        for j in range(fused_data.shape[1]):
            pixel_values = multispectral_data[:, i, j]
            fused_data[i,j] = int(np.mean(pixel_values) * (panchromatic_data[i,j] / 255.0))

    # Salvar a imagem resultante
    driver = gdal.GetDriverByName('GTiff')
    fused_ds = driver.Create(output_path, multispectral_ds.RasterXSize, multispectral_ds.RasterYSize, 1, gdal.GDT_Byte)
    fused_ds.SetProjection(multispectral_ds.GetProjection())
    fused_ds.SetGeoTransform(multispectral_ds.GetGeoTransform())
    fused_ds.GetRasterBand(1).WriteArray(fused_data)
    fused_ds = None

    print("Fusão colorimétrica concluída. Imagem salva em:", output_path)

# Exemplo de uso
multispectral_path = 'multiespectral.tif'
panchromatic_path = 'pancromatica.tif'
output_path = 'fusao_colorimetrica.tif'
colorimetric_fusion(multispectral_path, panchromatic_path, output_path)
