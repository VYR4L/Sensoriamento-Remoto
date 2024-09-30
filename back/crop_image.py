from osgeo import gdal, osr
import tempfile
import os

def convert_to_wgs84(input_path, output_path_reprojetado):
    """
    Reprojeta a imagem para o sistema de coordenadas WGS84 (EPSG:4326).
    
    :param input_path: Caminho da imagem original.
    :param output_path_reprojetado: Caminho onde a imagem reprojetada será salva.
    """

    dataset = gdal.Open(input_path)
    if dataset is None:
        raise Exception("Erro ao abrir a imagem para reprojeção.")

    # Definir a referência de destino (WGS84)
    target_srs = osr.SpatialReference()
    target_srs.ImportFromEPSG(4326)  # WGS84 EPSG code

    # Reprojetar a imagem para WGS84 e fechar o dataset após a operação
    gdal.Warp(output_path_reprojetado, dataset, dstSRS=target_srs.ExportToWkt())

    # Certifique-se de liberar o dataset
    dataset = None

def crop_image(input_path, output_path, image_name, min_lon, min_lat, max_lon, max_lat):
    """
    Recorta um arquivo TIFF usando coordenadas geográficas (lon/lat) após reprojeção.
    
    :param input_path: Caminho para o arquivo TIFF de entrada.
    :param output_path: Caminho para salvar o arquivo TIFF recortado.
    :param image_name: Nome do arquivo de saída.
    :param min_lon: Longitude mínima.
    :param min_lat: Latitude mínima.
    :param max_lon: Longitude máxima.
    :param max_lat: Latitude máxima.
    """

    # Criar um arquivo temporário com delete=False
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as temp_file:
        output_path_reprojetado = temp_file.name
    
    try:
        # Reprojetar a imagem para WGS84
        convert_to_wgs84(input_path, output_path_reprojetado)    

        # Agora recortar a imagem reprojetada
        dataset = gdal.Open(output_path_reprojetado)
        if dataset is None:
            raise Exception("Erro ao abrir a imagem reprojetada para recorte.")

        # Definir a extensão de corte (em coordenadas geográficas)
        bbox = [min_lon, min_lat, max_lon, max_lat]

        # Checar se a área de corte é válida
        if min_lon >= max_lon or min_lat >= max_lat:
            raise Exception("Coordenadas de recorte inválidas: a longitude ou latitude mínima é maior ou igual à máxima.")

        # Recortar a imagem
        result = gdal.Warp(f'{output_path}/{image_name}.tif', dataset, outputBounds=bbox, format="GTiff")

        if result is None:
            raise Exception("Erro durante o recorte. Verifique as coordenadas fornecidas.")
        
        # Fechar o dataset após o corte
        dataset = None
    
    finally:
        # Remover o arquivo temporário após a operação
        if os.path.exists(output_path_reprojetado):
            os.remove(output_path_reprojetado)
