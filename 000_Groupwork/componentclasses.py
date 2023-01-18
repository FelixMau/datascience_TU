import country_converter as coco
import geopandas as gpd
import pandas as pd
import rasterio

from dataclasses import dataclass, field

@dataclass(frozen = True,  ordered=True)
class BUS:
    name: str = "BUS"


@dataclass(frozen=True, ordered=True)
class DISPATCHABLE:
    name: str
    bus: str
    p_nom: float
    marginal_costs: float
    lifetime: int
    capital_cost: float = field(init=False)
    type: str = "n/a"
    carrier: str = "n/a"
    p_unit: str = "MW"

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
