import inspect

import pandas as pd
import json
import csv
import numpy as np
from typing import Sequence, Union
from dataclasses import dataclass, field
import geopandas as gpd
from pprint import pprint
import inspect


@dataclass(order=True)
class marine_regions:
    name: str
    marine_data_file_index: str = \
        "assignment-4-data/marineregions/World_EEZ_v11_20191118_gpkg/eez_boundaries_v11.gpkg"
    marine_gdf: gpd.GeoDataFrame = field(init=False)

    def __post_init__(self):
        self.marine_gdf = gpd.read_file(self.marine_data_file_index)

    def sort_and_filter(self, sorting_by: str = None, filter_by: str = None):
        return self.marine_gdf


def main():
    abc = marine_regions(name="abd")
    print(abc.sort_and_filter())

if __name__ == "__main__":
    main()


