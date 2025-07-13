import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
import matplotlib as mpl

# Increase default font size for better visibility
mpl.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 18,
    'axes.labelsize': 20,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'legend.fontsize': 18,
    'figure.titlesize': 20
})

# Enable GDAL exceptions (FutureWarning fix)
gdal.UseExceptions()

def boxplot_lst_by_class():
    """
    Loads seasonal mean LST rasters (Spring, Summer) and a classification raster,
    resamples LST rasters to classification grid (10m resolution), then for each
    land-use class (1-4) plots side-by-side boxplots of LST values in Spring vs Summer.
    Saves figure to ../images/lst_boxplots_by_class.png
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Paths
    class_path = os.path.join(script_dir, '..', 'data', 'sentinel-2', 'classification', 'classification.tif')
    seasonal_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'seasonal-means')
    plots_dir = os.path.join(script_dir, '..', 'images')
    os.makedirs(plots_dir, exist_ok=True)

    # Seasonal files
    spring_file = next(f for f in os.listdir(seasonal_dir) if 'spring' in f.lower() and f.lower().endswith('.tif'))
    summer_file = next(f for f in os.listdir(seasonal_dir) if 'summer' in f.lower() and f.lower().endswith('.tif'))
    spring_path = os.path.join(seasonal_dir, spring_file)
    summer_path = os.path.join(seasonal_dir, summer_file)

    # Open classification raster
    cls_ds = gdal.Open(class_path)
    cls_band = cls_ds.GetRasterBand(1)
    cls_arr = cls_band.ReadAsArray().astype(np.int32)
    cls_nodv = cls_band.GetNoDataValue()
    gt = cls_ds.GetGeoTransform()
    proj = cls_ds.GetProjection()
    xsize, ysize = cls_ds.RasterXSize, cls_ds.RasterYSize
    bounds = (
        gt[0],
        gt[3] + gt[5] * ysize,
        gt[0] + gt[1] * xsize,
        gt[3]
    )
    cls_ds = None

    # Function to resample a raster to classification grid
    def resample_to_cls(path):
        mem = gdal.Warp(
            '', path,
            format='MEM',
            outputBounds=bounds,
            width=xsize,
            height=ysize,
            dstSRS=proj,
            resampleAlg='bilinear'
        )
        arr = mem.GetRasterBand(1).ReadAsArray().astype(np.float32)
        nodv = mem.GetRasterBand(1).GetNoDataValue()
        mem = None
        return arr, nodv

    spring_arr, spring_nodv = resample_to_cls(spring_path)
    summer_arr, summer_nodv = resample_to_cls(summer_path)

    # Prepare data per class
    classes = [1, 4, 2, 3]
    spring_vals = []
    summer_vals = []
    for cls in classes:
        mask = (cls_arr == cls)
        # exclude nodata
        mask &= (spring_arr != spring_nodv) & (summer_arr != summer_nodv)
        spring_vals.append(spring_arr[mask].ravel())
        summer_vals.append(summer_arr[mask].ravel())

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    positions = []
    data = []
    labels = []
    offset = 0.2
    for i, cls in enumerate(classes):
        pos_center = i + 1
        # Spring box
        positions.append(pos_center - offset)
        data.append(spring_vals[i])
        labels.append('')  # no individual labels
        # Summer box
        positions.append(pos_center + offset)
        data.append(summer_vals[i])
        labels.append('')
    # Colors: Spring = light green/yellow, Summer = red/orange
    box_colors = ['#A1D99B' if idx % 2 == 0 else '#FC9272' for idx in range(len(data))]

    bp = ax.boxplot(
        data,
        positions=positions,
        widths=0.35,
        patch_artist=True,
        showfliers=False,
        medianprops={'color': 'red', 'linewidth': 2}
    )
    for patch, color in zip(bp['boxes'], box_colors):
        patch.set_facecolor(color)

    # X-axis
    ax.set_xticks([i + 1 for i in range(len(classes))])
    ax.set_xticklabels(['Infrastructure', 'Field/Meadow', 'Water', 'Forest' ])
    ax.set_xlabel('Class')
    ax.set_ylabel('LST (°C)')
    ax.set_title('LST Distribution by Class and Season')

    # Legend
    summer_patch = plt.Line2D([0], [0], color="#FC9272", lw=10)
    spring_patch = plt.Line2D([0], [0], color='#A1D99B', lw=10)
    ax.legend([spring_patch, summer_patch], ['Spring', 'Summer'], loc='upper right')

    plt.tight_layout()
    out_path = os.path.join(plots_dir, 'lst_boxplots_by_class.png')
    plt.savefig(out_path, dpi=600, transparent=True)
    plt.show()

if __name__ == '__main__':
    boxplot_lst_by_class()
