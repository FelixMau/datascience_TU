"""
Takes Data, mapping and expansion to build pypsa model
"""
import pandas as pd
import pypsa
import json
import input_dataclasses
import componentclasses


def expansion_limit(component_type):
    # Todo: Get Component limits either from geographical limits or yaml
    #   Shall also be added to country class?!
    return None



def build_components(config_dir: str, power_plant_data: input_dataclasses.global_power_plants, expansion_limits: pd.DataFrame,
                     country: str = "RWANDA"):
    # config contains all information necesary to build components:
    n = pypsa.Network()
    with open(config_dir, "r") as f:
        config = json.loads(f)
    POWER_PLANTS = input_dataclasses.global_power_plants(country_name=country)
    RWANDA = input_dataclasses.gadm(country_name=country)
    for component_type in POWER_PLANTS:
        for region in RWANDA.gadm_gdf.index:
            componentclasses.BUS(name=region).add_to_network(n)


        # This loop iterates though every forseen component type
        # Todo: global_power_plants class needs a function to filter for the Data.
        #   Config.yaml neeeds to contain information on filter data for every component type
        comps = power_plant_data.filter(component_type["filter"])
        for region in config["regions"]:
            for comp_number, comp in enumerate(comps):
                # Iterate over every component of the component type above
                # Todo: Config.yaml needs to contain information about parameters/attributes and the value
                #  for this parameters for each component type
                keyword_args = {}
                for keyword, value in component_type["keywords"].items():
                    # keyword dict is filled with Data by using config and inputdata
                    # Todo: The class contains information on how to construct itself (post init) and the config would
                    #   only know what class it should use now and pass the information to the class constructor
                    #   Or using a dictionary to map to the classes? Maybe more straight forward
                    #
                    keyword_args[keyword] = get_value(keyword, value, component_type)
                n.add(class_name=component_type["class_name"], name=component_type["class_name"]+str(comp_number),
                kwargs = keyword_args)

def build_model(busses, dispatchables, volatiles, storages, lines):
    network = pypsa.Network
    #for i in components:
     #   i.add_to_network(network=network)

