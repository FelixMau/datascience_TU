"""
Takes Data, mapping and expansion to build pypsa model
"""
import pandas as pd
import pypsa
import json
import input_dataclasses
import componentclasses
import mapper
import geopandas as gpd
from pprint import pprint

# Todo: finish component mapper. Write all possible kinds of electical components (also non defined ones)
# COMPONENTS = {
#     {"column_name": "column_value", "....": "::::"}: componentclasses.Bus, ## allgemein
#     {"primary_fuel": ["Gas, Coal...."]}: componentclasses.Dispatchable  #Beispiel
# }

def expansion_limit(component_type):
    # Todo: Get Component limits either from geographical limits or yaml
    #   I think it would be best to implement a method within the AdministrativeRegion class that takes a
    #   component_type and returns m^2
    return None


# def add_component_classes_to_power_plants_gdf(GlobalPowerPlants: input_dataclasses.GlobalPowerPlants)->gpd.GeoDataFrame:
#     gdf = GlobalPowerPlants.dta
#
#     gdf = gdf.apply(lambda x: print(x), axis=1)

    #object.__setattr__(GlobalPowerPlants, "dta", gdf)

def build_components(config_dir: str = None, expansion_limits: pd.DataFrame = None, country: str = "RWANDA"):
    # config contains all information necessary to build components:
    n = pypsa.Network()
    power_plants = input_dataclasses.GlobalPowerPlants(country_name=country)
    rwanda = input_dataclasses.AdministrativeRegion(country_name=country)
    #add_component_classes_to_power_plants_gdf(power_plants)
    for region in rwanda.gadm_gdf.index:
        print(region)
        componentclasses.Bus(name=region, GID_1=region, AdministrativeRegion=rwanda).add_to_network(n)



build_components()
