import dataclasses
from dataclasses import dataclass, field

import pandas as pd
import pypsa
import shapely.geometry.point

import input_dataclasses
from mapper import ATTRIBUTES


@dataclass(frozen=True, order=True)
class Bus:
    """
    Contains Bus information:
        Name of the Bus (Must be Region GID 1)
        GID_1 location of BUS
        country location of BUS (extract from GID 1?

        Function:
            calc_crow_distance, takes another BUS class instance to return the distance between both busses

    """
    name: str  # Name can be freely chosen
    GID_1: str  # GID_1 region where Bus is located
    AdministrativeRegion: input_dataclasses.AdministrativeRegion  # gadm class of country containing more information
    # on administrative regions
    representative_point: shapely.geometry.point.Point = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "representative_point", self.AdministrativeRegion.coordinates(self.GID_1))

    def add_to_network(self, network: pypsa.Network, **kwargs):
        network.add(class_name="Bus", name=getattr(self, "name"))

    def calc_crow_distance(self, bus_region):
        return self.AdministrativeRegion.coordinates(bus_region).distance(self.representative_point) / 1e3


@dataclass(frozen=True, order=True)
class ElectricComponent:
    """
    Parent class for electric components (not Busses)  that are already existing


    """
    name: str  # Instance of global_power_plants.dta.index

    country: input_dataclasses.AdministrativeRegion  # country class from input_dataclasses to search for Values and to
    # locate Powerplants to country and regions

    power_plants: input_dataclasses.GlobalPowerPlants  # global_power_plant class from input_dataclasses to get
    # information for this electric component


    # ToDo: To allow Investment: need for possibility to add components that are NOT within the
    #  already existing global power plants class. -> implement check if searched Index is within index
    #   -> then do investment stuff!

    marginal_costs: float
    lifetime: int
    capital_cost: float
    bus: str = field(init=False)
    p_nom: float = field(init=False)
    investment: bool = False # True if this component is non-existing in the powerplant database and Investment
    # for this component shall be evaluated
    carrier: str = "n/a"
    p_unit: str = "MW"

    def __post_init__(self):
        if self.investment is False:
            # Get the Bus where the powerplant is connected to (GID_1 takes point and returns GID_1 region containing point)
            print(self.name)
            object.__setattr__(self, "bus", self.country.GID_1(self.power_plants.dta.loc[self.name, "geometry"]))
            object.__setattr__(self, "p_nom", self.power_plants.dta.loc[self.name, "capacity_mw"])

            # Todo: allocate source for marginal costs and add to powerplants dta GeoDataFrame
            #  (within global_power_plants  __post_init__)
            # object.__setattr__(self, "marginal_costs", self.power_plants.dta.loc[self.name, "marginal_costs"])
        elif self.investment is True:
            # ToDo: How is investment done in Pypsa? -> Implement!
            pass

    def add_to_network(self, network: pypsa.Network, **kwargs):
        keywords = {ATTRIBUTES[name]: value for name, value in dataclasses.asdict(self).items()}
        keywords.pop("name")
        # network.generators.loc[getattr(self, "name") + str(1), :] = keywords
        network.add(class_name=self.type, name=getattr(self, "name"), kwargs=keywords)

@dataclass(frozen=True, order=True)
class Dispatchable(ElectricComponent):
    type: str = "Generator"

    pass


class Volatile(ElectricComponent):
    type: str = "Generator"
    p_max_pu: pd.Series(float)


class StorageUnit(ElectricComponent):
    type: str = "Storage"
    max_hours: float

#
# n = pypsa.Network()
#
# CHOSEN_COUNTRY_NAME = "Rwanda"
#
# RWANDA = input_dataclasses.gadm(country_name=CHOSEN_COUNTRY_NAME)
# POWER_PLANTS = input_dataclasses.GlobalPowerPlant(country_name=CHOSEN_COUNTRY_NAME)
#
# dispo = Dispatchable(name="WRI1061143", power_plants=POWER_PLANTS, country=RWANDA)

