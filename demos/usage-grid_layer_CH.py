"""
Visualizing the Real Estate Carbon Landscape 2023 with a Grid Layer of Pydeck
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

"""# visualizing with grid layer (pydeck)"""

df = re_cash_columns_random_CH

# Define a layer to display on a map

layer = pdk.Layer(
    "GridLayer", df, pickable=True, extruded=True, cell_size=200, elevation_scale=4, get_position=['Longitude', 'Latitude'],
)

# view_state = pdk.ViewState(latitude=46.7, longitude=8.1355, zoom=8, min_zoom=2)
# Set height and width variables
# view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)

view_state = pdk.ViewState(latitude=46.7, longitude=8.1355, zoom=8, bearing=0, pitch=45)

# Render
# r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{position}\nCount: {count}"},)

tooltip={"text": "{position}\nCount: {count}"}

# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer], 
             initial_view_state=view_state,
             tooltip=tooltip,
             api_keys={"mapbox":mapbox_api_token},
             map_provider="mapbox",
             map_style=pdk.map_styles.MAPBOX_DARK, 
    )

# Combined all of it and render a viewport
r.to_html('grid.html')

app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(), id="deck-gl", mapboxKey=r.mapbox_key
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)