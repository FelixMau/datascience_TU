"""
Takes Data, mapping and expansion to build pypsa model
"""
import pandas as pd
import pypsa
import json
import input_dataclasses

def get_value():
    pass

def build_components(config_dir: str, power_plant_data: input_dataclasses.global_power_plants, expansion_limits: pd.DataFrame):
    # config contains all information necesary to build components:
    n = pypsa.Network()
    with open(config_dir, "r") as f:
        config = json.loads(f)
    for component_type in config["components"]:
        # This loop iterates though every forseen component type
        # Todo: global_power_plants needs a function to filter for the Data.
        #   Config.yaml neeeds to contain information on filter data for every component type
        comps = power_plant_data.filter(component_type["filter"])
        for comp_number, comp in enumerate(comps):
            # Iterate over every component of the component type above
            # Todo: Config.yaml needs to contain information about parameters/attributes and the value
            #  for this parameters for each component type
            keyword_args = {}
            for keyword, value in component_type["keywords"].items():
                # keyword dict is filled with Data by using config and inputdata
                # Todo: get_value takes the value (and more inputs) to get the value. The Value might be stored
                #   somewhere in the inputdata or in the config file. Config file should contain information where
                #   Data is stored
                keyword_args[keyword] = get_value(value)
            n.add(class_name=component_type["class_name"], name=component_type["class_name"]+str(comp_number)),
            kwargs =

def build_model(busses, dispatchables, volatiles, storages, lines):
    network = pypsa.Network
    for i in components:
        i.add_to_network(network=network)

