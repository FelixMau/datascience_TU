from pprint import pprint

import pandas as pd
import pypsa
import shapely

import input_dataclasses
from dataclasses import dataclass, field
from mapper import ATTRIBUTEMAPPER
import dataclasses



@dataclass(frozen=True, order=True)
class BUS:
    """
    Contains Bus information:
        Name of the Bus (Must be Region GID 1)
        GID_1 location of BUS
        country location of BUS (extract from GID 1?

        Function:
            calc_crow_distance, takes another BUS class instance to return the distance between both busses

    """
    name: str # Name can be freely chosen
    GID_1: str # GID_1 region where Bus is located
    country: input_dataclasses.gadm # gadm class of country containing more information on administrative regions


    def __post_init__(self):
        object.__setattr__(self, "representative_point", self.country.coordinates(self.GID_1))

    def add_to_network(self, network: pypsa.Network, **kwargs):
        keywords = {ATTRIBUTEMAPPER[name]: value for name, value in dataclasses.asdict(self).items()}
        network.add(class_name="Bus", name=getattr(self, "name"))

    def calc_crow_distance(self, bus_region):
        return self.country.coordinates(bus_region).distance(self.representative_point)/1e3



@dataclass(frozen=True, order=True)
class DISPATCHABLE:
    name: str # Instance of global_power_plants.dta.index
    country: input_dataclasses.gadm
    power_plants: input_dataclasses.global_power_plants
    bus: str = field(init=False)
    p_nom: float = field(init=False)
    marginal_costs: float = field(init = False)
    lifetime: int = field(init = False)
    capital_cost: float = field(init = False)
    type: str = "n/a"
    carrier: str = "n/a"
    p_unit: str = "MW"

    def __post_init__(self):
        object.__setattr__(self, "bus", self.country.GID_1(self.power_plants.dta.loc[self.name, "geometry"]))
        object.__setattr__(self, "p_nom", self.power_plants.dta.loc[self.name, "capacity_mw"])

        # Todo allocate source for marginal costs
        object.__setattr__(self, "marginal_costs", self.power_plants.dta.loc[self.name, "marginal_costs"])

        # Todo: Write function in powerplants to return searched value
        # Construct necesary values:


        # Construct from **kwargs:


    def add_to_network(self, network: pypsa.Network, **kwargs):
        keywords = {ATTRIBUTEMAPPER[name]: value for name, value in dataclasses.asdict(self).items()}
        keywords.pop("name")
        #network.generators.loc[getattr(self, "name") + str(1), :] = keywords
        network.add(class_name="Generator", name=getattr(self, "name"), kwargs=keywords)


@dataclass(frozen=True, order=True)
class VOLATILE:
    name: str
    bus: str
    p_nom: float
    marginal_costs: float
    p_max_pu: pd.Series(float)
    lifetime: int
    capital_cost: float = field(init=False)
    type: str = "n/a"
    carrier: str = "n/a"
    p_unit: str = "MW"


@dataclass(frozen=True, order=True)
class STORAGE_UNIT:
    name: str
    bus: str
    p_nom: float
    marginal_costs: float
    p_max_pu: pd.Series(float)
    lifetime: int
    max_hours: float
    capital_cost: float = field(init=False)
    type: str = "n/a"
    carrier: str = "n/a"
    p_unit: str = "MW"


n = pypsa.Network()

RWANDA = input_dataclasses.gadm(country_name="Rwanda")
POWER_PLANTS = input_dataclasses.global_power_plants(country_name="Rwanda")

dispo = DISPATCHABLE(name="WRI1061143", power_plants=POWER_PLANTS, country=RWANDA)
print(dispo.GID_1)



# #some_dispatchable = DISPATCHABLE(name="DSP", bus="bus0", p_nom=100)
# rwanda = gadm(country_name="Rwanda")
# some_bus = BUS(name="bus0", GID_1="RWA.1_1", country=rwanda)
#
# print(some_bus.calc_crow_distance("RWA.2_1"))
#
# #some_bus.add_to_network(network=n)
# #some_dispatchable.add_to_network(network=n)
#
# pprint(n.generators)
