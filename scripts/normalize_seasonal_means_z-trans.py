import os
from osgeo import gdal
import numpy as np

# Enable GDAL exceptions (FutureWarning fix)
gdal.UseExceptions()

def normalize_seasonal_means():
    """
    Normalizes the seasonal mean LST rasters using Z-transformation
    (T_norm = (T - mu) / sigma) per raster, and saves outputs under
    ../data/landsat-imagery/seasonal-means-normalized.
    """
    gdal.UseExceptions()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means')
    output_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means-normalized-Z-transformed')
    os.makedirs(output_dir, exist_ok=True)

    # Process each seasonal mean TIFF
    for fname in os.listdir(input_dir):
        if not fname.lower().endswith('.tif'):
            continue
        in_path = os.path.join(input_dir, fname)
        out_path = os.path.join(output_dir, f"Z-transformed_{fname}")

        ds = gdal.Open(in_path)
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray().astype(np.float32)
        nodv = band.GetNoDataValue()

        # Mask NoData
        mask = (arr == nodv)
        valid = arr[~mask]

        # Compute mean and std for valid pixels
        mu = valid.mean()
        sigma = valid.std()

        # Z-transformation
        norm = (arr - mu) / sigma
        norm[mask] = nodv

        # Create output
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

        print(f"Normalized {fname} with Z-Transformation: mu={mu:.2f}, sigma={sigma:.2f} -> {out_path}")

if __name__ == '__main__':
    normalize_seasonal_means()
