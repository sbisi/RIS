"""
Visualizing the Real Estate Carbon Landscape of the Community of Windisch 2023 with a Columns Layer of Pydeck
"""

import dash
from dash import dcc, html, Input, Output, callback, State
import requests
from geopy.geocoders import Nominatim
import json
import socket
from pyproj import Transformer
from urllib.parse import parse_qs, unquote
import dash_bootstrap_components as dbc
from shapely.geometry import shape

# ✅ Importiere icons
from components import search_button, bullet_point, create_icon_text_row 

# ✅ FIXED: `get_coordinates()` muss vor den Callbacks definiert sein

# Manuelle Registrierung des Icons mit dem relativen Pfad zur SVG-Datei
dash.register_page(__name__, name="Parzellen", path="/Parzellen", order=2)

if __name__ in dash.page_registry:
    dash.page_registry[__name__]["icon"] = "/assets/maps.svg"

# ✅ FIXED: `dcc.Store` zur Speicherung von Klick-Koordinaten hinzugefügt
clicked_coordinates_store = dcc.Store(id="clicked_coordinates", data={})

def convert_coordinates(x, y, from_epsg="EPSG:4326", to_epsg="EPSG:2056"):
    transformer = Transformer.from_crs(from_epsg, to_epsg, always_xy=True)
    return transformer.transform(x, y)


def get_coordinates(address):
    r = requests.get(
        "https://api3.geo.admin.ch/rest/services/api/SearchServer",
        params={"searchText": address, "type": "locations"},
        timeout=10
    )
    r.raise_for_status()
    data = r.json()

    results = data.get("results", [])
    if not results:
        return None

    # GeoAdmin liefert i.d.R. WGS84 (lat/lon) unter attrs, je nach result type
    attrs = results[0].get("attrs", {})
    lon = attrs.get("lon")
    lat = attrs.get("lat")
    if lon is None or lat is None:
        return None

    return float(lon), float(lat)


from shapely.geometry import shape, Polygon

def get_parcel_data(lon, lat):
    e, n = convert_coordinates(lon, lat, "EPSG:4326", "EPSG:2056")
    url = f"https://api3.geo.admin.ch/rest/services/ech/MapServer/identify?"
    url += f"geometryType=esriGeometryPoint&geometry={e},{n}"
    url += "&sr=2056&layers=all:ch.swisstopo-vd.amtliche-vermessung"
    url += "&tolerance=0&returnGeometry=true&geometryFormat=geojson&f=json"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            feature = data["results"][0]
            parcel_id = feature["featureId"]
            parcel_name = feature["properties"].get("label", "Unbekannte Parzelle")  # ✅ Name der Parzelle hinzufügen
            geom = feature.get("geometry")
            area = None
            
            if geom and "coordinates" in geom:
                try:
                    polygon = shape(geom)
                    area = polygon.area  # **Fläche berechnen**
                    print(f"📏 Berechnete Fläche: {area} m²")
                except Exception as e:
                    print(f"Fehler bei der Flächenberechnung: {e}")

            return parcel_id, parcel_name, e, n, area  # ✅ Jetzt werden 5 Werte zurückgegeben

    except requests.exceptions.RequestException as e:
        print(f"API Fehler: {e}")

    return None, None, None, None, None  # ✅ Rückgabe auf 5 Werte erweitern


tab_style = {"height": "calc(100vh - 330px)", "padding": "15px", "font-size": "12px", "margin-top": "100px"}
parcel_data_store = dcc.Store(id="parcel_data_store", data={})  # 🆕 Speichert die Daten

layout = html.Div([
    dcc.Store(id="parcel_data_store", data={}),
    html.Div(id="parcel_area", style={"display": "none"}),
    html.Div(
        "Informationen Parzellen",
        style={'font-size': '16px', "margin-top": "10px", "margin-bottom": "10px", "margin-left": "15px"}
    ),
    
    html.Hr(style={'margin-bottom': '10px', 'margin-top': '0px'}),
    
    dcc.Location(id="url", refresh=False),  # ✅ URL-Tracking für automatische Adressübernahme

    dbc.Row([
        # **Kartenansicht**
        dbc.Col(
            html.Div([
                html.Iframe(id='map', src="", width="100%", height="700px", 
                            style={'marginTop': '0px', 'marginLeft': '15px', 'marginRight': '20px', 'border': 'none'})
            ]),
            md=8,
        ),

        # **Seitliches Panel**
        dbc.Col([
            # **Eingabefeld & Suchbutton**
            dcc.Input(
                id='address_input', type='text', placeholder='Adresse eingeben', value='', 
                style={'font-size': '14px', 'width': '85%', 'height': '30px', 'padding': '10px', 
                       'borderRadius': '5px', 'border': '1px solid #ccc'}
            ),
            search_button,
            dcc.Store(id="clicked_coordinates", data={}),  # ✅ Speichert Klick-Daten

            # **Tabs für Datenanzeige**
            dbc.Col([
                dbc.Tabs(
                    [
                        dbc.Tab(label="Stammdaten", tab_id="tab-1", 
                                style={"padding": "2px", "min-height": "20px"}),
                        dbc.Tab(label="Parameter", tab_id="tab-2", 
                                style={"padding": "2px", "min-height": "20px"}),
                    ],
                    id="tabs",
                    active_tab="tab-1",
                    className="mb-0",
                    style={
                        "display": "flex",
                        "justify-content": "flex-start",
                        "flex-wrap": "nowrap",
                        "width": "100%",
                        "margin-top": "10px",
                        "font-size": "14px",  
                        "border-bottom": "1px solid #555",  
                        "border-bottom": "1px",  # ❌ Entferne die border-bottom hier
                        "padding-bottom": "0px",
                        "height": "25px",  
                    }
                ),
              
                html.Hr(style={"width": "100%", "border": "1px solid white", "margin-top": "0px"}),  # ✅ Zusätzliche Linie

                # html.Hr(style={"width": "85%", "border": "1px solid white", "margin-top": "10px"}),

                # **Tab-Inhalte**
                html.Div(
                    id="tab-content",
                    style={
                        "padding": "0px",
                        "background-color": "#222",
                        "height": "calc(100vh - 110px)",
                        "padding-left": "20px",
                        "padding-top": "0px",
                    }
                )
            ], width=4, style={"width": "100%"})
        ]),
    ]),
])


@callback(
    [Output('address_input', 'value'), Output('search_button', 'n_clicks')],
    Input("url", "search")
)
def fill_address_from_search(search_query):
    if search_query:
        query_params = parse_qs(search_query.lstrip("?"))
        address = query_params.get("query", [""])[0]  # Holen des Suchparameters
        address = unquote(address)  # ✅ Dekodiert "%20" in Leerzeichen usw.
        print(f"🔍 URL-Parameter empfangen: {address}")  # Debugging
        return address, 1  # 1 simulierter Klick auf den Such-Button
    return dash.no_update, dash.no_update

@callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    [State("parcel_data_store", "data")]  # ✅ Holen der gespeicherten Daten!
)

def update_tab_content(active_tab, parcel_data):
    if active_tab == "tab-1":
        area_text = "bitte Parzelle wählen"
        if parcel_data and 'area' in parcel_data:
            area_text = f"{parcel_data['area']:.2f} m²"

        return html.Div([
            # Erste Zeile: Parzellenfläche
            dbc.Row([
                dbc.Col(create_icon_text_row('bullseye-pointer-regular', 'Parzellenfläche'), width=4, style={'padding': '0px'}),
                dbc.Col(html.Div(id='parcel_area', children="bitte Parzelle wählen", 
                                 style={'margin': '0px', 'height': 'auto', 'fontSize': '14px', 
                                        'color': 'white', 'fontStyle': 'italic',
                                        'display': 'flex', 'align-items': 'center',
                                        'width': 'fit-content',
                                        'position': 'relative', 'left': '100px'}), 
                        width=8, style={'padding': '0px'})
            ], align="center", style={'margin-bottom': '0px', 'padding-bottom': '0px'}),  
            
            # Zweite Zeile: Kleiner Grenzabstand
            dbc.Row([
                dbc.Col(create_icon_text_row('bullseye-pointer-regular', 'Zonenplan'), width=4, style={'padding': '0px'}),
                dbc.Col(html.Div(id='valentine_info', children="[Info folgt]", 
                                 style={'margin': '0px', 'height': 'auto', 'fontSize': '14px', 
                                        'color': 'white', 'fontStyle': 'italic',
                                        'display': 'flex', 'align-items': 'center',
                                        'width': 'fit-content',
                                        'position': 'relative', 'left': '100px'}), 
                        width=8, style={'padding': '0px'})
            ], align="center", style={'margin-bottom': '0px', 'padding-bottom': '0px'}),
        ])

    elif active_tab == "tab-2":
        return html.Div([
            dbc.Row([
                dbc.Col(create_icon_text_row('bullseye-pointer-regular', 'Grosser Grenzabstand'), width=4, style={'padding': '0px'}),
                dbc.Col(html.Div(id='Grosser_Grenzabstand', children="8m", 
                                style={'margin': '0px', 'height': 'auto', 'fontSize': '14px', 
                                        'color': 'white', 'fontStyle': 'italic',
                                        'display': 'flex', 'align-items': 'center',
                                        'width': 'fit-content',
                                        'position': 'relative', 'left': '100px'}), 
                        width=8, style={'padding': '0px'})
            ], align="center", style={'margin-bottom': '0px', 'padding-bottom': '0px'}),  
            # Zweite Zeile: Zonenplan
            dbc.Row([
                dbc.Col(create_icon_text_row('bullseye-pointer-regular', 'Kleiner Grenzabstand'), width=4, style={'padding': '0px'}),
                dbc.Col(html.Div(id='Kleiner_Grenzabstand', children="4m", 
                                 style={'margin': '0px', 'height': 'auto', 'fontSize': '14px', 
                                        'color': 'white', 'fontStyle': 'italic',
                                        'display': 'flex', 'align-items': 'center',
                                        'width': 'fit-content',
                                        'position': 'relative', 'left': '100px'}), 
                        width=8, style={'padding': '0px'})
            ], align="center", style={'margin-bottom': '0px', 'padding-bottom': '0px'}),
        ])
        # Falls ein unbekannter Tab aktiv ist, gibt die Funktion None zurück
        return None


@callback(
    Output("parcel_area", "children"),
    Input("parcel_data_store", "data")
)
def update_parcel_area(parcel_data):
    if parcel_data and parcel_data.get("area") is not None:
        return f"{parcel_data['area']:.2f} m²"
    return "Keine Parzelle ausgewählt."


@callback(
    Output("parcel_data_store", "data"),
    [Input("search_button", "n_clicks"),
     Input("address_input", "n_submit"),
     Input("clicked_coordinates", "data")],
    [State("address_input", "value")]
)
def store_parcel_data(n_clicks, n_submit, clicked_coordinates, address):
    if not address:
        return dash.no_update  # Falls keine Adresse eingegeben wurde

    coords = get_coordinates(address)
    if not coords:
        return dash.no_update  # Falls keine Koordinaten gefunden wurden

    lon, lat = coords
    parcel_id, parcel_name, e, n, area = get_parcel_data(lon, lat)
    
    if not parcel_id:
        return dash.no_update  # Falls keine Parzelle gefunden wurde

    return {"parcel_id": parcel_id, "parcel_name": parcel_name, "area": area}


def update_parcel_area(n_clicks, n_submit, clicked_coordinates, address):
    print(f"📢 Callback getriggert! n_clicks: {n_clicks}, n_submit: {n_submit}")

    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "none"
    print(f"🔥 Trigger: {triggered_id}")

    if triggered_id == "none":
        return "Kein Event erkannt"

    if triggered_id == "search_button" or triggered_id == "address_input":
        if address:
            coords = get_coordinates(address)
            if coords:
                lon, lat = coords
                print(f"🏠 Adresse-Koordinaten: {lon}, {lat}")
                parcel_id, parcel_name, e, n, area = get_parcel_data(lon, lat)
                return f"{area:.2f} m²" if area else "Keine Parzelle gefunden"

    return "Keine Parzelle ausgewählt."


@callback(
    Output('map', 'src'),
    [Input('search_button', 'n_clicks'),
     Input("address_input", "n_submit")],  # 🆕 Jetzt wird Enter berücksichtigt
    State('address_input', 'value')
)
def update_map(n_clicks, n_submit, address):
    print(f"🔄 Callback update_map() wurde getriggert! n_clicks: {n_clicks}, n_submit: {n_submit}")

    ctx = dash.callback_context
    if not ctx.triggered:
        print("⚠️ Kein Trigger erkannt (ctx.triggered ist leer!)")
        return dash.no_update

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(f"🔥 Trigger: {triggered_id}")

    # Falls weder Button noch Enter genutzt wurde, nichts tun
    if triggered_id not in ["search_button", "address_input"]:
        return dash.no_update

    if address:
        coords = get_coordinates(address)
        if not coords:
            print("❌ Keine Koordinaten gefunden!")
            return ""

        lon, lat = coords
        print(f"📍 Gefundene Koordinaten: {lon}, {lat}")

        parcel_id, parcel_name, e, n, _ = get_parcel_data(lon, lat)

        if not parcel_id:
            print("❌ Keine Parzelle gefunden!")
            return ""

        print(f"✅ Parzelle gefunden: {parcel_id}, Zentrum: {e}, {n}")

        return f"https://map.geo.admin.ch/embed.html?showMap=true&lang=de&bgLayer=void&layers=ch.kantone.cadastralwebmap-farbe@features={parcel_id}&layers_opacity=1&center={e},{n}&zoom=12.4"

    return ""
