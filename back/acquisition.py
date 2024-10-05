from osgeo import gdal
import numpy as np
from pystac_client import Client

def save_raster(array_data, dataset, file):
    drive = gdal.GetDriverByName('GTiff')
    num_bands = len(array_data)
    outdata = drive.Create(file,
                           dataset.RasterXSize,
                           dataset.RasterYSize,
                           num_bands, gdal.GDT_Float32)
    outdata.SetGeoTransform(dataset.GetGeoTransform())
    outdata.SetProjection(dataset.GetProjection())
    for i in range(num_bands):
        band = outdata.GetRasterBand(i + 1)
        band.WriteArray(array_data[i])
    outdata.FlushCache()
    outdata = None


def main():

    # shp = geopandas.read_file('shp_file')
    # bounds4326 = shp.to_crs('epsg:4326').total_bounds

    client = Client.open("https://landsatlook.usgs.gov/stac-server/")
    SentinelSearch = client.search(
        bbox=list([
            -53.556296596456406, -25.40353459796093, -53.45658187069899,
            -25.312934556934213
        ]),
        datetime='2024-09-01/2024-09-30',
        collections='landsat-c2l2-sr',
    )
    Sentinel_items = SentinelSearch.items_as_dicts()
    
    for item in Sentinel_items:
        print(item)

    # warp_options = gdal.WarpOptions(
    #         format='MEM',
    #         outputBounds=bounds,
    #         dstSRS="EPSG:5880",
    #         width=1000,
    #         height=1000,
    #         resampleAlg=gdal.GRA_NearestNeighbour,
    #         dstNodata=np.nan
    #     )
    # dataset_scl = gdal.Warp(
    #     '',
    #     f"/vsicurl/{['href']}",
    #     options=warp_options
    # )

if __name__ == "__main__":
    main()