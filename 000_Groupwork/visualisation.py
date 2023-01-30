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

st.header("PyPSA Energy System Network")

st.write("Buses:")
st.write(network.buses)

st.write("Lines:")
st.write(network.lines)

st.write("Generators:")
st.write(network.generators)

bus1_gen1_cost = st.slider("Bus 1 Generator 1 Cost", 0, 100, 10)
bus1_gen2_cost = st.slider("Bus 1 Generator 2 Cost", 0, 100, 15)
bus2_gen3_cost = st.slider("Bus 2 Generator 3 Cost", 0, 100, 10)
bus2_gen4_cost = st.slider("Bus 2 Generator 4 Cost", 0, 100, 15)

network.generators.loc["gen1", "marginal_cost"] = bus1_gen1_cost
network.generators.loc["gen2", "marginal_cost"] = bus1_gen2_cost
network.generators.loc["gen3", "marginal_cost"] = bus2_gen3_cost
network.generators.loc["gen4", "marginal_cost"] = bus2_gen4_cost

network.lopf(solver_name="cbc")

st.write("Optimal Generation:")
st.write(network.generators_t.p)

st.write("Total Cost:")
st.write(network.objective / 1e6, "EUR million")

# import plotly.express as px
# import plotly.graph_objects as go
# import pypsa
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
# # Import dash components
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
#
# # Initialize app
# app = dash.Dash()
# app.layout = html.Div([
#     html.H1("PyPSA Energy System"),
#     html.Div([
#         dcc.Dropdown(
#             id="bus-select",
#             options=[
#                 {"label": "Bus 1", "value": "bus1"},
#                 {"label": "Bus 2", "value": "bus2"},
#             ],
#             value="bus1",
#         ),
#         dcc.Slider(
#             id="gen-slider",
#             min=0,
#             max=25,
#             step=1,
#             value=10,
#         ),
#         dcc.Slider(
#             id="load-slider",
#             min=0,
#             max=25,
#             step=1,
#             value=0,
#         ),
#     ]),
#     dcc.Graph(id="network-graph"),
# ])
#
#
# # Callback to update graph based on selected bus
# @app.callback(
#     dash.dependencies.Output("network-graph", "figure"),
#     [dash.dependencies.Input("bus-select", "value"),
#      dash.dependencies.Input("gen-slider", "value"),
#      dash.dependencies.Input("load-slider", "value")]
# )
# def update_graph(selected_bus, gen_value, load_value):
#     network.generators.loc[network.generators.bus == selected_bus, "p_set"] = gen_value
#     network.buses.loc[network.buses.index == selected_bus, "p_set"] = -load_value
#     network.lopf(solver_name="cbc")
#
#     bus_data = network.buses_t.p.T
#     line_data = network.lines_t.p0.T
#
#     fig = px.line(bus_data, title="Buses Power Profile")
#     fig.add_trace(go.Scatter(x=line_data.index, y=line_data[selected_bus], name="Selected Bus Line Power"))
#
#     return fig
#
#
# if __name__ == "__main__":
#     app.run_server(debug=True)
