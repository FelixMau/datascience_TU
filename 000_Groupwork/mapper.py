"""
Contains mapping functions to map energysystem data to pypsa classes
"""

#import componentclasses

ATTRIBUTES = {
    "name":"name",
    "bus": "bus",
    "p_nom": "p_nom",
    "marginal_costs": "marginal_costs",
    "lifetime": "lifetime",
    "capital_cost": "capital_cost",
    "type":"type",
    "carrier":"type",
    "p_unit":"p_unit",
          }

VALUE_CALCULATOR = {
    "CROW_FLY_DISTANCE": " Bus.calc_crow_distance('second bus') ",

}

# ToDo: Alle (wahrscheinlich) vorkommenden Komponenten abdecken (auch komponentden die noch nicht in componentclasses
#  implementiert sind.

# Vorschlag ersmal so:

COMPONENTS_DEFINING_COLUMNS = ["primary_fuel", "other_fuel1", "...."]


