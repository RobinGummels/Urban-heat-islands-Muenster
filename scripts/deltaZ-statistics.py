import os
import numpy as np
from osgeo import gdal

# Enable GDAL exceptions (FutureWarning fix)
gdal.UseExceptions()

# determine script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# paths
landcov_path = os.path.join(
    script_dir, '..', 'data', 'sentinel-2', 'classification', 'classification.tif'
)
deltaz_path = os.path.join(
    script_dir, '..', 'data', 'landsat-imagery', 'delta-z', 'delta_z.tif'
)

# -------------------------------------------------------------------
# 1) Open landcover raster to get geotransform, projection and size
# -------------------------------------------------------------------
lc_ds = gdal.Open(landcov_path)
gt      = lc_ds.GetGeoTransform()
proj    = lc_ds.GetProjection()
xsize   = lc_ds.RasterXSize
ysize   = lc_ds.RasterYSize
landarr = lc_ds.GetRasterBand(1).ReadAsArray().astype(np.int32)
lc_ds   = None

# -------------------------------------------------------------------
# 2) Resample delta-z (30 m) on-the-fly to exactly match the landcover grid (10 m)
# -------------------------------------------------------------------
# compute outputBounds: (minX, minY, maxX, maxY)
minx = gt[0]
maxy = gt[3]
maxx = minx + gt[1] * xsize
miny = maxy + gt[5] * ysize

delta_ds = gdal.Warp(
    '', deltaz_path,
    format='MEM',
    outputBounds=(minx, miny, maxx, maxy),
    width=xsize,
    height=ysize,
    dstSRS=proj,
    resampleAlg='bilinear'   # smooth interpolation
)
dz      = delta_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
nodv    = delta_ds.GetRasterBand(1).GetNoDataValue()
delta_ds = None

# -------------------------------------------------------------------
# 3) Mask valid pixels
# -------------------------------------------------------------------
valid  = (dz != nodv)
dz_val = dz[valid]

# -------------------------------------------------------------------
# 4) Compute dynamic thresholds based on standard deviation
# -------------------------------------------------------------------
sigma = dz_val.std()
thr1  = 0.5 * sigma
thr2  = sigma

pct_gt_thr1 = (dz_val >  thr1).sum() / dz_val.size * 100
pct_gt_thr2 = (dz_val >  thr2).sum() / dz_val.size * 100
pct_lt_mthr1 = (dz_val < -thr1).sum() / dz_val.size * 100

p95   = np.percentile(dz_val, 95)
dz_min, dz_max = dz_val.min(), dz_val.max()

print(f"Overall   >0.5σ: {pct_gt_thr1:.1f}%   >1σ: {pct_gt_thr2:.1f}%   <-0.5σ: {pct_lt_mthr1:.1f}%")
print(f"Overall   σ = {sigma:.2f},  P95 = {p95:.2f},  Min = {dz_min:.2f},  Max = {dz_max:.2f}\n")

# -------------------------------------------------------------------
# 5) Per-class statistics
# -------------------------------------------------------------------
class_map = {
    1: "Infrastructure",
    2: "Water",
    3: "Forest",
    4: "Field/Meadow"
}

stats = {}
for code, name in class_map.items():
    mask = valid & (landarr == code)
    arr  = dz[mask]
    if arr.size == 0:
        continue
    stats[name] = {
        "count":     int(arr.size),
        "mean":      float(arr.mean()),
        "p95":       float(np.percentile(arr, 95)),
        "pct_gt1σ":  float((arr >  thr1).mean() * 100),
        "pct_gt2σ":  float((arr >  thr2).mean() * 100),
        "pct_lt1σ":  float((arr < -thr1).mean() * 100)
    }

for name, s in stats.items():
    print(
        f"{name:14s}  n={s['count']:7d}  μ={s['mean']:+.2f}  "
        f"P95={s['p95']:+.2f}  >0.5σ={s['pct_gt1σ']:.1f}%  >1σ={s['pct_gt2σ']:.1f}%  <-0.5σ={s['pct_lt1σ']:.1f}%"
    )
