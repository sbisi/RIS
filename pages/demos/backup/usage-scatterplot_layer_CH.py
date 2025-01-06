"""
Visualizing the Real Estate Carbon Landscape 2023 with a Scatterplot Layer of Pydeck
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

"""# visualizing with hexagon layer (pydeck)"""

tooltip = {
   "html": "<b>Elevation Value:</b> {elevationValue}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}

layer = pdk.Layer(
    'ScatterplotLayer',     # Change the `type` positional argument here
    re_cash_columns_random_CH,
    get_position=['Longitude', 'Latitude'],
    auto_highlight=True,
    get_radius=1000,          # Radius is given in meters
    get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
    pickable=True)


view_state = pdk.ViewState(
    longitude=8.1355,
    latitude=46.7,
    zoom=7,
    min_zoom=6,
    max_zoom=15,
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