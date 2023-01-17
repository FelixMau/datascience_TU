import streamlit as st
import pypsa

network = pypsa.Network()

# create buses
network.add("Bus", "bus1", v_nom=20)
network.add("Bus", "bus2", v_nom=30)

# create lines
network.add("Line", "line1", bus0="bus1", bus1="bus2", s_nom=10, length=100)

# create generators
network.add("Generator", "gen1", bus="bus1", p_nom=10)
network.add("Generator", "gen2", bus="bus2", p_nom=15)

st.title("PyPSA Dashboard")

if st.checkbox("Show buses"):
    st.write(network.buses)

if st.checkbox("Show lines"):
    st.write(network.lines)

if st.checkbox("Show generators"):
    st.write(network.generators)
