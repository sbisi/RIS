"""
Visualizing the Real Estate Carbon Landscape 2023 with a Hexagon Layer of Pydeck
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


# Daten laden
path_geojson = "tlm_kantonsgebiet.geojson"
geo_df = gpd.read_file(path_geojson)
file_path = 'results.csv'
data_df = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')

# Umwandlung und Bereinigung für Boolesche Spalten
boolean_columns = [
    'LINKDOC_PRESENT', 'DOWNLOADED_PDF_VALID', 'MUNICIPALITY_EXISTS', 
    'LINK_VALID', 'METADATA_EQUAL', 'HASH_EQUAL', 'CRAWLED_LINK_SAME'
]
data_df[boolean_columns] = data_df[boolean_columns].replace(
    {'True': True, 'False': False, 'true': True, 'false': False}
).astype(bool)

# Zuordnungstabelle erstellen und Namen standardisieren
kanton_mapping = {
    'ZH': 'Zürich', 'BE': 'Bern', 'LU': 'Luzern', 'UR': 'Uri', 
    'SZ': 'Schwyz', 'OW': 'Obwalden', 'NW': 'Nidwalden', 
    'GL': 'Glarus', 'ZG': 'Zug', 'FR': 'Fribourg', 'SO': 'Solothurn', 
    'BS': 'Basel-Stadt', 'BL': 'Basel-Landschaft', 'SH': 'Schaffhausen', 
    'AR': 'Appenzell Ausserrhoden', 'AI': 'Appenzell Innerrhoden', 
    'SG': 'St. Gallen', 'GR': 'Graubünden', 'AG': 'Aargau', 
    'TG': 'Thurgau', 'TI': 'Tessin', 'VD': 'Vaud', 'VS': 'Valais', 
    'NE': 'Neuchâtel', 'GE': 'Genève', 'JU': 'Jura', 'FL': 'Liechtenstein'
}

data_df['GDEKT'] = data_df['GDEKT'].map(kanton_mapping)

# Daten nach Kanton aggregieren
aggregated_data = data_df.groupby('GDEKT').agg({'LINKDOC_PRESENT': 'sum'}).reset_index()

# Merge der aggregierten Daten ins GeoDataFrame
geo_df = geo_df.merge(aggregated_data, how='left', left_on='name', right_on='GDEKT')
geo_df['LINKDOC_PRESENT'].fillna(0, inplace=True)  # Fehlende Werte mit 0 auffüllen

# GeoJSON-Datei mit aktualisierten Daten speichern
geo_df.to_file('output.geojson', driver='GeoJSON')

print("FINALER CHECK !!:",geo_df[['name', 'LINKDOC_PRESENT']])

# Pydeck Visualisierung vorbereiten
INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=46.7, longitude=8.1355, zoom=6, max_zoom=15, pitch=40.5, bearing=20.36
)

import geopandas as gpd
from shapely.geometry import shape

# Angenommen, deine Daten beinhalten eine Spalte 'geometry' mit GeoJSON-Strukturen
if 'geometry' in geo_df.columns:
    # Konvertiere die JSON-Strings in Geometrien
    geo_df['geometry'] = geo_df['geometry'].apply(shape)
    # Konvertiere DataFrame zu GeoDataFrame
    geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry')

polygon = pdk.Layer(
    "PolygonLayer",
    data=geo_df,
    get_polygon="geometry.coordinates",  # Zugriff auf Koordinaten im GeoJSON
    get_fill_color=[0, 0, 0, 20],  # Semi-transparent Schwarz
    stroked=False
    )

layer = pdk.Layer(
    "GeoJsonLayer",
    data=geo_df,  # Stelle sicher, dass dies ein korrekter Pfad zum GeoJSON ist, oder verwende geo_df.__geo_interface__ wenn geo_df ein GeoDataFrame ist.
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="LINKDOC_PRESENT*100",  # Korrekte Referenz auf die Elevationseigenschaft
    # get_fill_color=[255, 140, 0, 150],  # Konstante Farbe, semi-transparent
    get_fill_color=[255, 255, 255],
    # get_fill_color="primary" 
    get_line_color=[255, 255, 255],
)

r = pdk.Deck(layers=[polygon, layer], initial_view_state=INITIAL_VIEW_STATE)
r.to_html("SAMSTAG.html")

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_deck.DeckGL(
        r.to_json(),
        id="deck-gl",
        mapboxKey=mapbox_api_token,
        style={"height": "100vh"}
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)