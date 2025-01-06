"""
Visualizing the Real Estate Carbon Landscape of the Community of Windisch 2023 with a Columns Layer of Pydeck
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
re_cash_columns_community_Windisch = pd.read_csv("co2_landscape_community_Windisch.csv")

"""# visualizing with hexagon layer (pydeck)"""

tooltip = {
   "html": "<b>Elevation Value:</b> {elevationValue}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}

view_state = pdk.ViewState(
    longitude=8.21907,
    latitude=47.4747,
    zoom=10,
    min_zoom=6,
    max_zoom=25,
    pitch=40.5,
    bearing=-20.36)

layer = pdk.Layer(
    'HexagonLayer',  # `type` positional argument is here
    re_cash_columns_community_Windisch, 
    get_position=['Longitude', 'Latitude'],
    auto_highlight=True,
    elevation_scale=20,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1)

# special view state for Windisch
view_state = pdk.ViewState(
    longitude=8.21907,
    latitude=47.4747,
    zoom=10,
    min_zoom=6,
    max_zoom=25,
    pitch=40.5,
    bearing=-20.36)


# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer], 
             initial_view_state=view_state,
             tooltip=tooltip,
             api_keys={"mapbox":mapbox_api_token},
             map_provider="mapbox",
             map_style=pdk.map_styles.MAPBOX_DARK, 
    )

# Combined all of it and render a viewport
r.to_html('peter_staub.html')

app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(), id="deck-gl", mapboxKey=r.mapbox_key
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)