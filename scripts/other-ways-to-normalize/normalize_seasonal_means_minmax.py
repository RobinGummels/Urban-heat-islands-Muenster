import os
from osgeo import gdal
import numpy as np

def normalize_seasonal_means_minmax():
    """
    Normalizes the seasonal mean LST rasters (spring & summer) using Min-Max transformation
    (T_norm = (T - T_min) / (T_max - T_min)) per raster, and saves outputs under
    ../data/landsat-imagery/seasonal-means-normalized-minmax.
    """
    gdal.UseExceptions()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means')
    output_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means-normalized-minmax')
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if not fname.lower().endswith('.tif'):
            continue

        in_path = os.path.join(input_dir, fname)
        ds = gdal.Open(in_path)
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray().astype(np.float32)
        nodv = band.GetNoDataValue()

        # Mask for valid data
        mask = (arr != nodv)
        valid = arr[mask]

        # Min-Max statistics
        t_min = valid.min()
        t_max = valid.max()

        # Min-Max-transformation
        norm = np.full(arr.shape, nodv, dtype=np.float32)
        # Not dividing by zero if t_max == t_min
        denominator = t_max - t_min if t_max != t_min else 1.0
        norm[mask] = (arr[mask] - t_min) / denominator

        # Output
        out_path = os.path.join(output_dir, f"MinMax-transformed_{fname}")
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.Create(
            out_path,
            ds.RasterXSize,
            ds.RasterYSize,
            1,
            gdal.GDT_Float32
        )
        out_ds.SetGeoTransform(ds.GetGeoTransform())
        out_ds.SetProjection(ds.GetProjection())
        out_band = out_ds.GetRasterBand(1)
        out_band.WriteArray(norm)
        out_band.SetNoDataValue(nodv)
        out_band.FlushCache()
        out_ds = None
        ds = None
        print(f"Normalized {fname} with Min-Max-Transformation: min={t_min:.2f}, max={t_max:.2f} -> {out_path}")


if __name__ == '__main__':
    normalize_seasonal_means_minmax()
