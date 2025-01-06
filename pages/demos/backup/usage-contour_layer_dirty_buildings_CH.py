"""
Visualizing the Real Estate Carbon Landscape 2023 with a Contour Layer of Pydeck
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

df = re_cash_columns_random_CH

def is_not_ecological(co2_m2):
    """Return a green RGB value if a location produces to much co2"""
    if co2_m2 > 30.0:
        return [255, 0, 187]
    return[0, 187, 255]

df["color"] = df["co2_m2"].apply(is_not_ecological)

view_state = pdk.ViewState(latitude=46.7, longitude=8.1355, zoom=6, min_zoom=2)
# Set height and width variables
view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)

COUNTRIES = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_scale_rank.geojson"


tooltip = {
   "html": "<b>Elevation Value:</b> {elevationValue}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}


layers = [
    pdk.Layer(
        # "GeoJsonLayer",
        # "GridLayer", (COOL !)
        "ContourLayer",
        id="base-map",
        data=COUNTRIES,
        stroked=False,
        filled=True,
        get_fill_color=[200, 200, 200],
    ),
    pdk.Layer(
        "ColumnLayer",
        id="co2_m2",
        data=df,
        get_elevation="co2_m2",
        get_position=["Longitude", "Latitude"],
        elevation_scale=300,
        pickable=True,
        auto_highlight=True,
        radius=200,
        get_fill_color="color",
    ),
]

r = pdk.Deck(
    views=[view],
    initial_view_state=view_state,
    tooltip={"text": "{STRNAME}, {PLZNAME}, co2_m2: {co2_m2}"},
    layers=layers,
    # Note that this must be set for the globe to be opaque
    parameters={"cull": True},
)

r.to_html("globe_view.html", css_background_color="black")


# Combined all of it and render a viewport
r = pdk.Deck(layers=[layers], 
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