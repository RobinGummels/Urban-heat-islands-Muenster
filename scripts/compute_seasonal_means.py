import os
import numpy as np
from osgeo import gdal

def compute_seasonal_means():
    """
    Calculates the pixel-wise mean of all clipped LST rasters (_ST_B10.TIF) per season
    and writes one GeoTIFF per season under ../data/landsat-imagery/seasonal-means.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'clipped-lst')
    output_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means')
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each season subfolder
    for season in os.listdir(input_dir):
        season_dir = os.path.join(input_dir, season)
        if not os.path.isdir(season_dir):
            continue

        # Collect all thermal band files
        tif_files = [os.path.join(season_dir, f) for f in os.listdir(season_dir)
                     if f.upper().endswith('_ST_B10.TIF')]
        if not tif_files:
            continue

        # Use first file as template for georeference
        ds0 = gdal.Open(tif_files[0])
        geotrans = ds0.GetGeoTransform()
        proj = ds0.GetProjection()
        band0 = ds0.GetRasterBand(1)
        nodata = band0.GetNoDataValue()
        xsize = ds0.RasterXSize
        ysize = ds0.RasterYSize
        ds0 = None

        # Initialize sum and count arrays
        sum_arr = np.zeros((ysize, xsize), dtype=np.float64)
        count_arr = np.zeros((ysize, xsize), dtype=np.int32)

        # Accumulate
        for tif in tif_files:
            ds = gdal.Open(tif)
            arr = ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
            mask = (arr != nodata)
            sum_arr[mask] += arr[mask]
            count_arr[mask] += 1
            ds = None

        # Compute mean, set nodata where no valid pixels
        mean_arr = np.full((ysize, xsize), nodata, dtype=np.float32)
        valid = count_arr > 0
        mean_arr[valid] = (sum_arr[valid] / count_arr[valid]).astype(np.float32)

        # Write output GeoTIFF
        out_path = os.path.join(output_dir, f"{season}_mean_ST_B10.tif")
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.Create(out_path, xsize, ysize, 1, gdal.GDT_Float32)
        out_ds.SetGeoTransform(geotrans)
        out_ds.SetProjection(proj)
        out_band = out_ds.GetRasterBand(1)
        out_band.SetNoDataValue(nodata)
        out_band.WriteArray(mean_arr)
        out_band.FlushCache()
        out_ds = None

        print(f"Written seasonal mean for {season}: {out_path}")

if __name__ == '__main__':
    compute_seasonal_means()
