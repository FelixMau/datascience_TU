import country_converter as coco
import geopandas as gpd
import pandas as pd
import rasterio

from input_dataclasses import dataclass, field

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
class marine_regions:
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
class world_protected_areas:
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
    country_name: str = "Germany"
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
class load_series:
    """
    Load series dataclass

    functions:
        sort and filter:
            returns pd.Series load for country
    """
    country_name: str = "Germany"
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
class gadm:
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
    country_name: str = "Germany"
    gadm_dir: str = \
        "assignment-4-data/gadm/"
    projection: int = 4326
    gadm_gdf: rasterio.default_gtiff_profile = field(init=False)
    gadm_file_name: str = field(init=False)
    gadm_file_start: str = "gadm_410-levels-ADM_1-"

    def __post_init__(self):
        self.country_name = cc.convert(names=self.country_name, to="ISO3")
        self.gadm_file_name = self.gadm_dir + self.gadm_file_start + self.country_name + ".gpkg"
        self.gadm_gdf = gpd.read_file(self.gadm_file_name, geometry="geometry", index_col = "GID_1")


@dataclass()
class glc:
    name: str


@dataclass(frozen=True)
class global_power_plants:
    """
    Dataclass for global powerplants
    *Attributes:
        -country_name = Name of country
        -dta = Pandas Dataframe with country specific Data

    *functions:
        -filter = takes filter dictionary {"columname":"keyword to search for"} and returns filtered Dataframe
    """
    country_name:str = "Germany"
    data_path: str = "assignment-4-data/global-power-plant-database/global_power_plant_database_v_1_3/global_power_plant_database.csv"
    dta: pd.DataFrame = field(init=False)

    def __post_init__(self)-> None:
        # Rewriting country-name to match columns
        object.__setattr__(self, "country_name", cc.convert(names=self.country_name, to="ISO3"))
        # Setting dta to country Dataframe
        object.__setattr__(self, "dta",
                       pd.read_csv(self.data_path, index_col="gppd_idnr").query(f"country == '{self.country_name}'"),
                       index_col="gppd_idnr")

    def filter(self, filter: dict = None)->list[pd.DataFrame]:
        filtered = []
        for col, filter_kw in filter.items():
            filtered = filtered.append(self.dta.query(f"{col} == '{filter_kw}'"))
        return filtered

@dataclass(frozen=True)
class roads_and_airports:
    country_name: str = "Germany"
    data_path: str = "assignment-4-data/ne_10m_roads.gpkg"
    dta: gpd.GeoDataFrame = field(init=False)

    def __post_init__(self) -> None:
        # Rewriting country-name to match columns
        object.__setattr__(self, "country_name", cc.convert(names=self.country_name, to="ISO3"))
        # Setting dta to country Dataframe
        object.__setattr__(self, "dta",
                           gpd.read_file(self.data_path, geometry="geometry"))


def main():
    pass

if __name__ == "__main__":
    main()


