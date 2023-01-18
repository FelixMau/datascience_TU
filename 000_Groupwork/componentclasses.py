from pprint import pprint

import pandas as pd
import pypsa

from input_dataclasses import dataclass, field
from mapper import ATTRIBUTEMAPPER
import dataclasses



@dataclass(frozen=True, order=True)
class BUS:
    name: str = "BUS"
    x: str = field(init=False)
    y: str = field(init=False)

    def __post_init__(self):
        #Todo Get x and y values from geodataclass -> write function in inputdataclasses/gadm

    def add_to_network(self, network: pypsa.Network, **kwargs):
        keywords = {ATTRIBUTEMAPPER[name]: value for name, value in dataclasses.asdict(self).items()}
        network.add(class_name="Bus", name=getattr(self, "name"))

    def calc_crow_distance(self, another_x, another_y):
        # For line length between busses
        #Todo:

@dataclass(frozen=True, order=True)
class DISPATCHABLE:
    name: str
    bus: str
    p_nom: float
    marginal_costs: float = field(init = False)
    lifetime: int = field(init = False)
    capital_cost: float = field(init = False)
    type: str = "n/a"
    carrier: str = "n/a"
    p_unit: str = "MW"

    def __post_init__(self, **kwargs):
        # Todo: How (and from where!) are we going to construct the components?
        # Construct necesary values:


        # Construct from **kwargs:
        for param_name , param_value in kwargs.items():
            object.__setattr__(self, param_name, param_value)


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

some_dispatchable = DISPATCHABLE(name="DSP", bus="bus0", p_nom=100, marginal_costs=10, lifetime=20,
                                 capital_cost=5)
some_bus = BUS(name="bus0")

some_bus.add_to_network(network=n)
some_dispatchable.add_to_network(network=n)

pprint(n.generators)
