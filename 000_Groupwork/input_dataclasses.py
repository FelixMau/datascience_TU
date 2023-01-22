import country_converter as coco
import geopandas as gpd
import pandas as pd
import rasterio
import shapely

from dataclasses import dataclass, field

"""
Data-adapters to read and partially preprocess Data for PyPsa, Geopandas and other necesary operations

refactors figures to match units
refactors map projections to unify

classes: 
    - marine_regions: 
    - world_protected_areas
"""

cc = coco.CountryConverter()

@dataclass()
class MarineRegion:
    """
    Dataclass for marine regions
    contains Marine region information for the whole world.
        functions:
            sort_and_filter: returns Geodataframe
        Attributes:
            country name
            optional file dir
            optional projection (default is 4326)

        Possible functions:
            interact with restrictions together with Protected areas, airports and roads
    """
    country_name: str
    marine_data_file_index: str = \
        "assignment-4-data/marineregions/World_EEZ_v11_20191118_gpkg/eez_boundaries_v11.gpkg"
    marine_gdf: gpd.GeoDataFrame = field(init=False)
    projection: int = 4326

    def __post_init__(self):
        self.country_name = cc.convert(names=self.country_name, to="ISO3")
        self.marine_gdf = gpd.read_file(self.marine_data_file_index, geometry="geometry", crs=self.projection)

    def sort_and_filter(self, sorting_by: str = None, filter_by: str = None):
        return self.marine_gdf


@dataclass()
class WorldProtectedAreas:
    """
    Dataclass for World protected areas

    functions:
        :return rasterio open object to assert to excluder
    Attributes:
        country_name: adds together with wdpa_file_name and wdpa_file_start to search for tif file.
            converts automativally to ISO3
        projection: currently unused attribute

    possible functionality:
        interact with restrictions together with Protected areas, airports and roads
    """
    country_name: str = "Rwanda"
    wdpa_dir: str = \
        "assignment-4-data/wdpa/"
    projection: int = 4326
    wdpa_clc: rasterio.default_gtiff_profile = field(init=False)
    wdpa_file_name: str = field(init=False)
    wdpa_file_start: str = "WDPA_Oct2022_Public_shp-"

    def __post_init__(self):
        self.country_name = cc.convert(names=self.country_name, to="ISO3")
        self.wdpa_file_name = self.wdpa_dir + self.wdpa_file_start + self.country_name + ".tif"
        self.wdpa_clc = rasterio.open(self.wdpa_file_name)


@dataclass()
class LoadSeries:
    """
    Load series dataclass

    functions:
        sort and filter:
            returns pd.Series load for country
    """
    country_name: str = "Rwanda"
    gegis_dir: str = "assignment-4-data/gegis/load.csv"
    columns: list = field(init=False)
    load_series_df: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.country_name = cc.convert(names = self.country_name, to="ISO2")
        self.load_series_df = pd.read_csv(filepath_or_buffer=self.gegis_dir, index_col="time")[self.country_name]

    def sort_and_filter(self, filterer: str = None, sorter: str = None, **kwargs)->pd.Series:
        """
        filterer takes dictionary and filters for values in key columns
            i.e. {column: value_to_filter_for}
        sorter takes one string corresponding to columns

        kwargs for later use

        :return: filtered (and sorted) pd.Dataframe
        """
        return self.load_series_df

@dataclass()
class AdministrativeRegion:
    """
        Dataclass for administrative regions

        functions:
            -
        Attributes:
            country_name: adds together with gadm_file_name and gadm_file_start to search for tif file.
                converts automativally to ISO3
            gadm_gdf: geopandas dataframe with level 1 region as index. For country.

        possible functionality:

        """
    country_name: str = "Rwanda"
    gadm_dir: str = \
        "assignment-4-data/gadm/"
    projection: str = 4326
    gadm_gdf: gpd.GeoDataFrame = field(init=False)
    gadm_file_name: str = field(init=False)
    gadm_file_start: str = "gadm_410-levels-ADM_1-"

    def __post_init__(self):
        self.country_name = cc.convert(names=self.country_name, to="ISO3")
        self.gadm_file_name = self.gadm_dir + self.gadm_file_start + self.country_name + ".gpkg"
        self.gadm_gdf = gpd.read_file(self.gadm_file_name, geometry="geometry", crs ="ESRI:54009").set_index("GID_1")

    def coordinates(self, subregion) ->shapely.geometry.point.Point:
        projection = "ESRI:54009"
        return self.gadm_gdf.to_crs(projection).representative_point().loc[subregion]
    def GID_1(self, point: shapely.geometry.point.Point)->str:
        return self.gadm_gdf.contains(point)[self.gadm_gdf.contains(point)].index[0]



@dataclass()
class LandCover:
    country_name: str = "Rwanda"
    data_path: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "country_name", cc.convert(self.country_name, to="ISO2"))
        object.__setattr__(self, "data_path", f"assignment-4-data/copernicus-glc/PROBAV_LC100_global_v3.0.1_2019-nrt_Discrete-Classification-map_EPSG-4326-{self.country_name}.tif")
        object.__setattr__(self, "land_cover", rasterio.open(self.data_path))

@dataclass(frozen=True)
class GlobalPowerPlants:
    """
    Dataclass for global powerplants
    *Attributes:
        -country_name = Name of country
        -dta = Pandas Dataframe with country specific Data

    *functions:
        -filter = takes filter dictionary {"columname":"keyword to search for"} and returns filtered Dataframe
    """
    country_name:str = "Rwanda"
    data_path: str = "assignment-4-data/global-power-plant-database/global_power_plant_database_v_1_3/global_power_plant_database.csv"
    dta: pd.DataFrame = field(init=False)

    def __post_init__(self)-> None:
        # You may ignore strings, they look complicated but that's just due to the folder structure(:
        # Rewriting country-name to match columns
        object.__setattr__(self, "country_name", cc.convert(names=self.country_name, to="ISO3"))
        # Setting dta to country Dataframe
        df = pd.read_csv(self.data_path, index_col="gppd_idnr", low_memory=False).query(f"country == '{self.country_name}'")
        geometry = gpd.points_from_xy(df.longitude, df.latitude)
        object.__setattr__(self, "dta", gpd.GeoDataFrame(df, geometry=geometry, crs="ESRI:54009"))



    def filter(self, filter: dict = None)->list[pd.DataFrame]:
        filtered = []
        for col, filter_kw in filter.items():
            filtered = filtered.append(self.dta.query(f"{col} == '{filter_kw}'"))
        return filtered

    def get_value(self, index, column):
        return




@dataclass(frozen=True)
class RoadAndAirport:
    country_name: str = "Rwanda"
    data_path: str = "assignment-4-data/ne_10m_roads.gpkg"
    dta: gpd.GeoDataFrame = field(init=False)

    def __post_init__(self) -> None:
        # Rewriting country-name to match columns
        object.__setattr__(self, "country_name", cc.convert(names=self.country_name, to="ISO3"))
        # Setting dta to country Dataframe
        object.__setattr__(self, "dta",
                           gpd.read_file(self.data_path, geometry="geometry"), index_col="GID_1" )


@dataclass()
class AdministrativeRegion:
    """
        Dataclass for administrative regions

        functions:
            -
        Attributes:
            country_name: adds together with gadm_file_name and gadm_file_start to search for tif file.
                converts automativally to ISO3
            gadm_gdf: geopandas dataframe with level 1 region as index. For country.

        possible functionality:

        """
    country_name: str = "Rwanda"
    gadm_dir: str = \
        "assignment-4-data/gadm/"
    projection: str = 4326
    gadm_gdf: gpd.GeoDataFrame = field(init=False)
    gadm_file_name: str = field(init=False)
    gadm_file_start: str = "gadm_410-levels-ADM_1-"

    def __post_init__(self):
        self.country_name = cc.convert(names=self.country_name, to="ISO3")
        self.gadm_file_name = self.gadm_dir + self.gadm_file_start + self.country_name + ".gpkg"
        self.gadm_gdf = gpd.read_file(self.gadm_file_name, geometry="geometry", crs="ESRI:54009").set_index("GID_1")

    def coordinates(self, subregion) ->shapely.geometry.point.Point:
        projection = "ESRI:54009"
        return self.gadm_gdf.to_crs(projection).representative_point().loc[subregion]
    def GID_1(self, point: shapely.geometry.point.Point)->str:
        try:
            return self.gadm_gdf.contains(point)[self.gadm_gdf.contains(point)].index[0]
        except IndexError:
            print(f"{self.country_name} does not contain {point}")



    def potential_m2(self, roads: RoadAndAirport, airports: RoadAndAirport,
                     protected_areas: WorldProtectedAreas, land_cover: LandCover, component_type: str,
                     ):
        pass





