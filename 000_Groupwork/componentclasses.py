import country_converter as coco
import geopandas as gpd
import pandas as pd
import rasterio
import pypsa
from pprint import pprint

from dataclasses import dataclass, field
import dataclasses

from mapper import ATTRIBUTEMAPPER

@dataclass(frozen = True,  order=True)
class BUS:
    name: str = "BUS"
    def add_to_network(self, network: pypsa.Network, **kwargs):
        keywords = {ATTRIBUTEMAPPER[name] : value for name, value in dataclasses.asdict(self).items()}
        network.add(class_name="Bus", name=getattr(self, "name"))


@dataclass(frozen=True, order=True)
class DISPATCHABLE:
    name: str
    bus: str
    p_nom: float
    marginal_costs: float
    lifetime: int
    capital_cost: float
    type: str = "n/a"
    carrier: str = "n/a"
    p_unit: str = "MW"

    def add_to_network(self, network: pypsa.Network, **kwargs):
        keywords = {ATTRIBUTEMAPPER[name] : value for name, value in dataclasses.asdict(self).items()}
        keywords.pop("name")
        network.generators.loc[getattr(self, "name")+str(1),:] = keywords

@dataclass(frozen = True, order=True)
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
    capital_cost: float = field(init = False)
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
