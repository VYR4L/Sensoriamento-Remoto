from osgeo import gdal

#Abrir arquivo no gdal
ds = gdal.Open(file)

#Abrir a matriz de valores
array = gdal.Open(file).ReadAsArray()# Pode ser forçado para um tipo de dado com o '.astype(np.'tipo')'

#Criar um novo arquivo com base em outro
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

#Função WARP: https://gdal.org/programs/gdalwarp.html
#Para realizar o merge de imagens (necessário dar um dstSRS, para caso as entradas tenham SRS diferentes)
gdal.Warp(out_file,
          list_files,
          resampleAlg=gdal.GRA_Average,
          dstSRS="EPSG:4326",
          dstNodata=np.nan)

#Resize, reproject e clip
gdal.Warp(out_file,
          ds,
          format='GTiff',
          outputBounds=shape, #para recorte
          dstSRS="EPSG:5880", #para reprojetar
          width= ds.RasterXSize, height= ds.RasterYSize , resampleAlg=gdal.GRA_NearestNeighbour, #Para resample, definir o numero de colunas e linhas da nova matriz, pode ser pego de outra imagem de referência.
          dstNodata=np.nan)

#para obter o shape do recorte podemos usar o seguinte:
import geopandas
shp = geopandas.read_file(tile)
shape = shp.total_bounds
#Exemplo caso precise realizar a troca de SRS
shape_4326 = shp.to_crs('epsg:4326').total_bounds

#Relação das bands L8 e CBERS 4A:
#L8 - Banda PAN      - B8 - CBERS(WPM) - B0
#     Banda Azul     - B2 -            - B1
#     Banda verde    - B3 -            - B2
#     Banda vermelho - B4 -            - B3
#     Banda NIR      - B5 -            - B4
