"""
Visualizing the Real Estate Carbon Landscape 2023 with a Usage Map Layer of Pydeck
"""

import os

import dash
import dash_deck
import pydeck as pdk
import pandas as pd

from dash import dcc
from dash import html

# mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")
mapbox_api_token = "pk.eyJ1IjoicGV0ZXJzdGF1YjYxIiwiYSI6ImNsYnhjenFyejE1d3Q0MG55NjBjZDJ6aWoifQ.xgY2YrkCbL2pq0CletAT5g"

# NUR REDUZIERTES FILE EINLESEN WEGEN GITHUB-LIMITIERUNG AUF 25 GB !
re_cash_columns_random_CH = pd.read_csv("co2_landscape_random_CH.csv")

import plotly.express as px

fig = px.scatter_mapbox(re_cash_columns_random_CH, lat="Latitude", lon="Longitude", hover_name="GDENAME", hover_data=["co2_m2"],
                        color_discrete_sequence=["fuchsia"], zoom=7, height=2000)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

# Combined all of it and render a viewport

app = dash.Dash(__name__)



# Create the dash layout and overall div
app.layout = html.Div(children=[
    html.Div(dcc.Graph(id='fig', figure=fig))
    ])



# Create the dash layout and overall div
# app.layout = html.Div(children=[html.Div(dcc.Graph(id=fig))],)

if __name__ == "__main__":
    app.run_server(debug=True)

