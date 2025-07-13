import os
from osgeo import gdal
import numpy as np

def compute_seasonal_anomalies():
    """
    For each seasonal mean raster in ../data/landsat-imagery/seasonal-means,
    computes an anomaly map where T_anomaly = T - global_mean_temperature.
    Outputs are saved as Float32 with NoData = -9999 in
    ../data/landsat-imagery/seasonal-means-anomaly/.
    """
    gdal.UseExceptions()
    
    # Determine script and data directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means')
    output_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means-anomaly')
    os.makedirs(output_dir, exist_ok=True)

    # Loop through each seasonal mean file
    for fname in os.listdir(input_dir):
        if not fname.lower().endswith('.tif'):
            continue

        in_path = os.path.join(input_dir, fname)
        out_path = os.path.join(output_dir, f"Anomaly_{fname}")

        # Open the input raster
        ds = gdal.Open(in_path)
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray().astype(np.float32)
        nodata = band.GetNoDataValue()

        # Create mask for valid data pixels
        valid_mask = (arr != nodata)
        # Calculate the global mean temperature for valid pixels
        if np.any(valid_mask):
            global_mean = arr[valid_mask].mean()
        else:
            global_mean = 0.0

        # Initialize anomaly array with NoData values
        anomaly = np.full(arr.shape, nodata, dtype=np.float32)
        # Compute anomaly: difference from global mean (in °C)
        anomaly[valid_mask] = arr[valid_mask] - global_mean

        # Create output raster
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.Create(
            out_path,
            ds.RasterXSize,
            ds.RasterYSize,
            1,
            gdal.GDT_Float32
        )
        # Copy georeferencing
        out_ds.SetGeoTransform(ds.GetGeoTransform())
        out_ds.SetProjection(ds.GetProjection())

        # Write anomaly band
        out_band = out_ds.GetRasterBand(1)
        out_band.WriteArray(anomaly)
        out_band.SetNoDataValue(nodata)
        out_band.FlushCache()

        # Close datasets
        out_ds = None
        ds = None

if __name__ == '__main__':
    compute_seasonal_anomalies()
