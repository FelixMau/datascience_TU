import geopandas as gpd
import pandas as pd
import country_converter as coco

import rasterio


"""
Data-adapters to read and partially preprocess Data for PyPsa, Geopandas and other necesary operations

refactors figures to match units
refactors map projections to unify

classes: 
    - marine_regions: 
    - world_protected_areas

"""

cc = coco.CountryConverter()

def marine_regions(country_name: str,
                   marine_data_file_index: str = "assignment-4-data/marineregions/World_EEZ_v11_20191118_gpkg/eez_boundaries_v11.gpkg",
                   projection: int = 4326):
    country_name = cc.convert(names=country_name, to="ISO3")
    marine_gdf = gpd.read_file(marine_data_file_index, geometry="geometry", crs=projection)
    return marine_gdf


def world_protected_areas(country_name: str = "Germany", wdpa_dir: str = "assignment-4-data/wdpa/",
                          projection: int = 4326):
    country_name = cc.convert(names=country_name, to="ISO3")
    wdpa_file_name = wdpa_dir + "WDPA_Oct2022_Public_shp-" + country_name + ".tif"
    wdpa_clc = rasterio.open(wdpa_file_name)
    return wdpa_clc


def load_series(country_name: str = "Germany", gegis_dir: str = "assignment-4-data/gegis/load.csv"):
    country_name = cc.convert(names=country_name, to="ISO2")
    load_series_df = pd.read_csv(filepath_or_buffer=gegis_dir, index_col="time")[country_name]
    return load_series_df


def gadm(country_name: str = "Germany", gadm_dir: str = "assignment-4-data/gadm/",
         gadm_file_start: str = "gadm_410-levels-ADM_1-"):
    country_name = cc.convert(names=country_name, to="ISO3")
    gadm_file_name = gadm_dir + gadm_file_start + country_name+ ".shp"
    gadm_gdf = gpd.read_file(gadm_file_name)
    return gadm_gdf
