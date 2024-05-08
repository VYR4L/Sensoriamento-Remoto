from osgeo import gdal
import numpy as np
import geopandas
import pathlib

file = f'{pathlib.Path(__file__).parent.absolute()}\L8_ldna_20200504.tif'
print(file)

# Abrir arquivo no gdal
ds = gdal.Open(file)

# Abrir a matriz de valores
array = ds.ReadAsArray()  # Alterado para usar a variável 'ds' já aberta

# Criar um novo arquivo com base em outro
def create_file(array, input_file, out_file):
    ds = gdal.Open(input_file)
    drive = gdal.GetDriverByName("GTiff")
    outdata = drive.Create(out_file,
                           ds.RasterXSize, ds.RasterYSize, 1,
                           gdal.GDT_Float32, options=["COMPRESS=LZW"])
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjectionRef())
    outdata.GetRasterBand(1).WriteArray(array)
    outdata.GetRasterBand(1).SetNoDataValue(np.nan)
    outdata.FlushCache()
    outdata = None

# para obter o shape do recorte podemos usar o seguinte:
shp = geopandas.read_file(file)
shape = shp.total_bounds
# Exemplo caso precise realizar a troca de SRS
shape_4326 = shp.to_crs('epsg:4326').total_bounds

# Função WARP: https://gdal.org/programs/gdalwarp.html
# Para realizar o merge de imagens (necessário dar um dstSRS, para caso as entradas tenham SRS diferentes)
gdal.Warp('out.tif',
          [file, 'out.tif'],
          format='GTiff',
          resampleAlg=gdal.GRA_Average,
          dstSRS="EPSG:4326",
          dstNodata=np.nan)

# Resize, reproject e clip
gdal.Warp('out.tif',
          ds,
          format='GTiff',
          outputBounds=shape,  # para recorte
          dstSRS="EPSG:5880",  # para reprojetar
          width=ds.RasterXSize, height=ds.RasterYSize, resampleAlg=gdal.GRA_NearestNeighbour,
          dstNodata=np.nan)

# Relação das bands L8 e CBERS 4A:
# L8 - Banda PAN      - B8 - CBERS(WPM) - B0
#     Banda Azul     - B2 -            - B1
#     Banda verde    - B3 -            - B2
#     Banda vermelho - B4 -            - B3
#     Banda NIR      - B5 -            - B4
