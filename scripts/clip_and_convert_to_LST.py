import os
import xml.etree.ElementTree as ET
import numpy as np
from osgeo import gdal

def clip_and_convert_to_lst():
    """
    Clips only the Landsat thermal band rasters (ending with _ST_B10.TIF)
    using the specified shapefile, converts DN to °C using the
    LEVEL2_SURFACE_TEMPERATURE_PARAMETERS, and saves as Float32 with NoData=-9999.
    """
    # Determine paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'raw-data')
    shapefile = os.path.join(script_dir, '..', 'data', 'project-area', 'Project-Area Münster.shp')
    output_dir = os.path.join(script_dir, '..', 'data', 'landsat-imagery', 'clipped-lst')

    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.upper().endswith('_ST_B10.TIF'):
                # Get all paths and prepare output
                in_tif = os.path.join(root, filename)
                xml_file = filename.replace('_ST_B10.TIF', '_MTL.xml')
                xml_path = os.path.join(root, xml_file)
                rel_path = os.path.relpath(in_tif, input_dir)
                out_tif = os.path.join(output_dir, rel_path)
                os.makedirs(os.path.dirname(out_tif), exist_ok=True)

                # Parse XML for mult and add
                tree = ET.parse(xml_path)
                root_xml = tree.getroot()
                ns = ''  # no namespace
                params = root_xml.find('.//LEVEL2_SURFACE_TEMPERATURE_PARAMETERS')
                mult = float(params.find('TEMPERATURE_MULT_BAND_ST_B10').text)
                add = float(params.find('TEMPERATURE_ADD_BAND_ST_B10').text)

                # 1. Clip with Warp to Float32 (it's necessary to keep the NoData value on -9999)
                warp_drv = gdal.Warp(
                    out_tif,
                    in_tif,
                    format='GTiff',
                    outputType=gdal.GDT_Float32,
                    cutlineDSName=shapefile,
                    cropToCutline=True,
                    dstNodata=-9999
                )
                warp_drv = None  # close

                # 2. Open clipped file, convert DN->Kelvin->°C
                ds = gdal.Open(out_tif, gdal.GA_Update)
                band = ds.GetRasterBand(1)
                arr = band.ReadAsArray()

                # Apply conversion: DN * M + A gives Kelvin → subtract 273.15 for °C
                arr_c = (arr * mult + add) - 273.15
                # Preserve NoData
                nodv = band.GetNoDataValue()
                arr_c[arr == nodv] = nodv

                band.WriteArray(arr_c)
                band.SetNoDataValue(nodv)
                band.FlushCache()
                ds = None  # close

if __name__ == "__main__":
    clip_and_convert_to_lst()
