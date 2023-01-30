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


# Todo: finish component mapper. Write all possible kinds of electrical components (also non defined ones)
def component_object(primary_fuel, name, power_plants: input_dataclasses.GlobalPowerPlants.country_name,
                     administrative_region: input_dataclasses.AdministrativeRegion, config_yaml_dir: str = None,
                     ) -> componentclasses.ElectricComponent:

    # ToDo: Diese test_kwargs sollten aus einer config datei kommen um Code und Daten/Config besser zu trennen!
    #   -Auch eine Quelle für die Daten (lifetime und kosten) fehlt noch, diese hier sind ausgedacht^^
    #   -Runtimeoptimierung könnte man auch anstreben, zuerst soll es aber mal laufen? (Ist extrem langsam durch
    #   die ganzen klassen)
    test_kwargs = {"name": name,
                   "power_plants": power_plants,
                   "country": administrative_region,
                   "marginal_costs": 10,
                   "lifetime": 20,
                   "capital_cost": 10}

    COMPONENTS = {
        "Gas": componentclasses.Dispatchable(**test_kwargs),
        "Hydro": componentclasses.Dispatchable(**test_kwargs),
        "Coal": componentclasses.Dispatchable(**test_kwargs),
        "Lignite": componentclasses.Dispatchable(**test_kwargs),
        "Waste": componentclasses.Dispatchable(**test_kwargs),
        "Oil": componentclasses.Dispatchable(**test_kwargs),
        "Wind": componentclasses.Volatile(**test_kwargs),
        "Solar": componentclasses.Volatile(**test_kwargs),
        "electricity": componentclasses.StorageUnit(**test_kwargs),
    }

    return COMPONENTS[primary_fuel]


def expansion_limit(component_type):
    # Todo: Get Component limits either from geographical limits or yaml
    #   I think it would be best to implement a method within the AdministrativeRegion class that takes a
    #   component_type and returns m^2 (maybe? :))
    return None


def build_components(config_dir: str = None, expansion_limits: pd.DataFrame = None, country: str = "RWANDA"):
    # Building components from input_dataclasses, componentclasses and config
    n = pypsa.Network()
    power_plants = input_dataclasses.GlobalPowerPlants(country_name=country)
    rwanda = input_dataclasses.AdministrativeRegion(country_name=country)
    # Adding a Bus for each region (one for each region since we only have one carrier (electricity)
    # (could be more for monitoring comodities as well)
    for region in rwanda.gadm_gdf.index:
        componentclasses.Bus(name=region, GID_1=region, AdministrativeRegion=rwanda).add_to_network(n)
    # Add existing PowerPlants
    plant_df = power_plants.dta
    plant_df["class"] = plant_df.apply(lambda x: component_object(primary_fuel=x["primary_fuel"],
                                                                  power_plants=power_plants,
                                                                  administrative_region=rwanda,
                                                                  name=x.name), axis=1)


build_components()
