import rasterio

with rasterio.open('L8_ldna_20200504.tif') as sourceset:
    band_1 = sourceset.read(5)

    profile = sourceset.profile

    profile['count'] = 1

    band_1 = band_1.reshape(1, band_1.shape[0], band_1.shape[1])

    with rasterio.open('new_tif_file.tif', 'w', **profile) as dataset:
        dataset.write(band_1)

with rasterio.open('new_tif_file.tif') as source_set2:
    band_created = source_set2.read(1)
    print(band_created)
