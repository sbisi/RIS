import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Suche', icon='fa-search', title='Suche', order=1)

layout = html.Div(
    style={"display": "flex", "flexDirection": "column", "alignItems": "center", "height": "100vh", "paddingTop": "200px"},
    children=[
        html.H3("RIS - Regulatory Information System", style={"fontSize": "18px", "fontWeight": "bold", "color": "white"}),

        dcc.Input(
            id="search-input",
            type="text",
            placeholder="Gemeinde, Adresse oder Parzellennummer eingeben",
            style={"width": "50%", "padding": "15px", "fontSize": "16px", "borderRadius": "5px", "textAlign": "center", "marginTop": "20px"},
            debounce=True,  # Verhindert überflüssige Updates während der Eingabe
        ),

        html.Button("Suchen", id="search-button", style={"marginTop": "30px", "width": "100px", "height": "40px", "backgroundColor": "#555555", "color": "white"}),

        dcc.Store(id="search-store"),  # Speichert die Suchanfrage
        dcc.Location(id="url", refresh=True),  # URL-Steuerung
        html.Div(id="output", style={"marginTop": "30px", "color": "white"})
    ]
)

@callback(
    [Output("search-store", "data"), Output("output", "children"), Output("url", "href")],
    [Input("search-button", "n_clicks"), Input("search-input", "n_submit")],  # 🔹 Auch Enter-Taste wird getriggert
    State("search-input", "value"),
    prevent_initial_call=True
)
def update_output(n_clicks, n_submit, search_value):
    if search_value:
        return search_value, f"Du hast gesucht nach: {search_value}", f"/Parzellen?query={search_value}"
    return no_update, "Keine Eingabe erkannt.", no_update
