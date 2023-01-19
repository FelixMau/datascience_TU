"""
Contains mapping functions to map energysystem data to pypsa classes
"""

ATTRIBUTEMAPPER = {
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