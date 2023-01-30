import streamlit as st
import pypsa

network = pypsa.Network()

network.add("Bus", "bus1", v_nom=20)
network.add("Bus", "bus2", v_nom=30)

network.add("Line", "line1", bus0="bus1", bus1="bus2", s_nom=10, length=100)

network.add("Generator", "gen1", bus="bus1", p_nom=10)
network.add("Generator", "gen2", bus="bus1", p_nom=15)
network.add("Generator", "gen3", bus="bus2", p_nom=10)
network.add("Generator", "gen4", bus="bus2", p_nom=15)

network.add("Load", "load_1", bus="bus1", p_set=15)
network.add("Load", "load_2", bus="bus2", p_set=20)

st.header("PyPSA Energy System Network")

bus_options = ["bus1", "bus2"]
bus = st.selectbox("Choose bus", bus_options)

st.write("Buses:")
st.write(network.buses)

st.write("Lines:")
st.write(network.lines)

st.write("Generators:")
if bus == "bus1":
    st.write(network.generators.loc[["gen1", "gen2"]])
else:
    st.write(network.generators.loc[["gen3", "gen4"]])

if bus == "bus1":
    bus1_gen1_cost = st.slider("Bus 1 Generator 1 Cost", 0, 100, 10)
    bus1_gen2_cost = st.slider("Bus 1 Generator 2 Cost", 0, 100, 15)
    network.generators.loc["gen1", "marginal_cost"] = bus1_gen1_cost
    network.generators.loc["gen2", "marginal_cost"] = bus1_gen2_cost
else:
    bus2_gen3_cost = st.slider("Bus 2 Generator 3 Cost", 0, 100, 10)
    bus2_gen4_cost = st.slider("Bus 2 Generator 4 Cost", 0, 100, 15)
    network.generators.loc["gen3", "marginal_cost"] = bus2_gen3_cost
    network.generators.loc["gen4", "marginal_cost"] = bus2_gen4_cost

bus_load = st.slider("Bus Load", 0, 100, 50)
@st.cache
def update_results():
    if bus == "bus1":
        network.generators.loc["gen1", "marginal_cost"] = bus1_gen1_cost
        network.generators.loc["gen2", "marginal_cost"] = bus1_gen2_cost
    else:
        network.generators.loc["gen3", "marginal_cost"] = bus2_gen3_cost
        network.generators.loc["gen4", "marginal_cost"] = bus2_gen4_cost


    network.lopf(solver_name="cbc")

    return network

network = update_results()
st.write("Optimal Generation:")
if bus == "bus1":
    st.write(network.generators_t.p.loc[:, ["gen1", "gen2"]])
else:
    st.write(network.generators_t.p.loc[:, ["gen3", "gen4"]])

st.write("Total Cost:")
st.write(network.objective / 1e6, "EUR million")
import streamlit as st
import pypsa
#
# network = pypsa.Network()
#
# # create buses
# network.add("Bus", "bus1", v_nom=20)
# network.add("Bus", "bus2", v_nom=30)
#
# # create lines
# network.add("Line", "line1", bus0="bus1", bus1="bus2", s_nom=10, length=100)
#
# # create generators
# network.add("Generator", "gen1", bus="bus1", p_nom=10)
# network.add("Generator", "gen2", bus="bus2", p_nom=15)
#
# network.add("Load", "load1", bus="bus1", p_set=10)
#
# network.lopf()
#
# st.write("Optimized total costs: ", network.objective)
# st.write("Generation per bus: ")
# st.write(network.generators_t.p.sum(axis=0))
# st.write("Load per bus: ")
# st.write(network.loads_t.p.sum(axis=0))
