import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
import matplotlib as mpl

# Increase default font size for better visibility
mpl.rcParams.update({
    'font.size':         18,    # Basis‐Schriftgröße
    'axes.titlesize':    18,    # Achsentitel
    'axes.labelsize':    20,    # Achsenbeschriftung
    'xtick.labelsize':   18,    # X‐Ticks
    'ytick.labelsize':   18,    # Y‐Ticks
    'legend.fontsize':   18,    # Legende
    'figure.titlesize':  20,    # Figure‐Titel (falls verwendet)
})

# Enable GDAL exceptions (FutureWarning fix)
gdal.UseExceptions()

def correlate_lst_with_indices():
    """
    Computes R² and scatter plots with colored regression lines for:
    - NDVI vs LST per season
    - NDMI vs LST per season
    Outputs saved in ../images/
    """
    gdal.UseExceptions()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    seasonal_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means')
    indices_dir = os.path.join(script_dir, '..', 'data', 'sentinel-2', 'ndvi-ndmi')
    plots_dir = os.path.join(script_dir, '..', 'images')
    os.makedirs(plots_dir, exist_ok=True)

    # find the single NDVI and NDMI files
    ndvi_file = next((f for f in os.listdir(indices_dir)
                      if f.lower().endswith('.tif') and 'ndvi' in f.lower()), None)
    ndmi_file = next((f for f in os.listdir(indices_dir)
                      if f.lower().endswith('.tif') and 'ndmi' in f.lower()), None)
    if not ndvi_file or not ndmi_file:
        raise FileNotFoundError("NDVI or NDMI file not found in indices directory.")

    # Loop through each seasonal LST mean file
    for fname in os.listdir(seasonal_dir):
        if not fname.lower().endswith('.tif'):
            continue
        season = os.path.splitext(fname)[0]  # e.g., 'Spring' or 'Summer'
        lst_path = os.path.join(seasonal_dir, fname)
        lst_ds = gdal.Open(lst_path)
        gt = lst_ds.GetGeoTransform()
        proj = lst_ds.GetProjection()
        xsize, ysize = lst_ds.RasterXSize, lst_ds.RasterYSize
        lst_arr = lst_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
        lst_nodv = lst_ds.GetRasterBand(1).GetNoDataValue()

        # compute spatial bounds
        minx, maxy = gt[0], gt[3]
        maxx = minx + gt[1] * xsize
        miny = maxy + gt[5] * ysize
        bounds = (minx, miny, maxx, maxy)

        # compare both indices
        for index_name, index_file in [
            ('NDVI', ndvi_file),
            ('NDMI', ndmi_file)
        ]:
            index_path = os.path.join(indices_dir, index_file)
            # resample index to LST grid
            res = gdal.Warp(
                '', index_path,
                format='MEM',
                outputBounds=bounds,
                width=xsize,
                height=ysize,
                dstSRS=proj,
                resampleAlg='bilinear'
            )
            idx_arr = res.GetRasterBand(1).ReadAsArray().astype(np.float32)
            idx_nodv = res.GetRasterBand(1).GetNoDataValue()
            res = None

            # mask valid pixels
            mask = (lst_arr != lst_nodv) & (idx_arr != idx_nodv)
            x = idx_arr[mask].ravel()
            y = lst_arr[mask].ravel()

            # linear regression and R²
            a, b = np.polyfit(x, y, 1)
            r2 = np.corrcoef(x, y)[0,1]**2

            # plot
            plt.figure(figsize=(6, 6))
            plt.scatter(x, y, s=1, alpha=0.5)

            # Regression line
            xs = np.linspace(x.min(), x.max(), 100)
            plt.plot(xs, a * xs + b, color='red')

            # Text box with equation and R²
            eq_text = (f"y = {a:.2f}·x + {b:.2f}\n"
                       f"R² = {r2:.3f}")
            plt.text(
                0.05, 0.95, eq_text,
                transform=plt.gca().transAxes,
                va='top',
                bbox=dict(boxstyle='round,pad=0.6',
                          facecolor='white',
                          edgecolor='gray', alpha=0.85))

            plt.xlabel(index_name)
            plt.ylabel('LST (°C)')
            plt.title(f'{index_name} vs LST ({season})')
            plt.grid(True)
            plt.tight_layout()

            # save
            out_fname = f"{index_name.lower()}_vs_{season.lower()}_a,b,r2.png"
            plt.savefig(os.path.join(plots_dir, out_fname), dpi=600, transparent=True)
            plt.close()

        lst_ds = None

if __name__ == '__main__':
    correlate_lst_with_indices()
