from osgeo import gdal
import os

from back.stats import Stats
from back.colorimetryN import Colorimetry

class Processor:

    def __init__(self):
        pass

    def run(self, multispectral_path, panchromatic_path, output_path, process):
        
        temp_files = []

        #Abrir pan e pegar as informações de resolução
        pan = gdal.Open(panchromatic_path)
        res_pan = pan.GetGeoTransform()

        #Abrir multi e pegar as informações de resolução
        if type(multispectral_path) == type([]):
            
            file = r'./multi_uni_temp.tif'
            temp_files.append(file)
            ds = gdal.Open(multispectral_path[0])
            if ds is None:
                raise FileNotFoundError(f"Não foi possível abrir o arquivo {multispectral_path[0]}")
            multi = gdal.GetDriverByName('GTiff').Create(file, ds.RasterXSize, ds.RasterYSize, len(multispectral_path), ds.GetRasterBand(1).DataType)
            multi.SetProjection(ds.GetProjection())
            multi.SetGeoTransform(ds.GetGeoTransform())
            # Ler e escrever cada banda no dataset em memória
            for idx, band_file in enumerate(multispectral_path):
                ds_band = gdal.Open(band_file)
                if ds_band is None:
                    raise FileNotFoundError(f"Não foi possível abrir o arquivo {band_file}")
                band_data = ds_band.GetRasterBand(1).ReadAsArray()
                in_memory_band = multi.GetRasterBand(idx + 1)
                in_memory_band.WriteArray(band_data)
                ds_band = in_memory_band = band_data = None
            ds = multi = None
            multispectral_path = file
        
        multi = gdal.Open(multispectral_path)
        res_multi = multi.GetGeoTransform()

        bands_multi = multi.RasterCount
        if process.__module__ == 'back.colorimetry' and bands_multi != 3:
            raise RuntimeError('Os metodos colorimetricos necessitam de exatamente 3 bandas espectrais')

        #Verificar se necessário converter a multi para a resolução da pan
        if res_multi != res_pan:
            file = r'./multi_temp.tif'
            temp_files.append(file)
            xmin = res_pan[0]
            ymax = res_pan[3]
            xmax = xmin + res_pan[1] * pan.RasterXSize
            ymin = ymax + res_pan[5] * pan.RasterYSize
            warp_options = gdal.WarpOptions(format='GTiff',
                                            outputBounds=(xmin, ymin, xmax,
                                                          ymax),
                                            xRes=res_pan[1],
                                            yRes=abs(res_pan[5]),
                                            dstSRS=pan.GetProjection(),
                                            resampleAlg='bilinear')
            multi = gdal.Warp(file, multi, options=warp_options)
            multispectral_path = file

        #processamento
        if process in [Stats.pansharp]:
            process(self, panchromatic_path, multispectral_path, output_path)
        else:
            process(self, pan, multi, output_path)

        del pan
        del multi
        
        for f in temp_files:
            os.remove(f)
        