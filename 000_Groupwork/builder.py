"""
Takes Data, mapping and expansion to build pypsa model
"""
import pypsa

def build_model(busses, dispatchables, volatiles, storages, lines):
    for i in list_of_busses:
