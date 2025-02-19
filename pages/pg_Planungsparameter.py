import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objects as go

#dash.register_page(__name__, name='Planungsparameter & Vorschriften',
#                    order=6)

dash.register_page(__name__, name="Planungsparameter & Vorschriften", path="/Parameter", order=6)

if __name__ in dash.page_registry:
    dash.page_registry[__name__]["icon"] = "/assets/parameter.svg"

# Layout der App definieren
layout = html.Div([
    html.Div("Funktionen", style={'font-size': '16px', "margin-top": "10px", "margin-bottom": "10px"}),
    html.Hr(style={'margin-bottom': '10px', 'margin-top': '0px'}),
    html.Div(
        [
            html.H5("Geo-Navigator"),
            html.Ul(children=[
                html.Li("Suche und Filteroptionen: Benutzer können nach Parzelle, Gemeinde, Kanton, Bauzone oder Parameter filtern und geografisch suchen über eine Map oder Suchbegriffe."),
            ]),
            html.H5("Darstellung Parameter pro Parzelle"),
            html.Ul(children=[
                html.Li("Darstellung der eindeutigen zonenspezifischen Parameter (Regelbauweisen)."),
                html.Li("Spezifikation der Abweichungen für Zonen mit Abweichungen zur Regelbauweise (z.B. Arealüberbauung mit Gestaltungsplanverfahren, Ortsbild- oder Denkmalschutz, besondere Industrie- und Arbeitszonen, Zonen des öffentlichen Interesses, Naturschutz, Verdichtungs- und Altstadtgebiete)."),
                html.Li("Darstellung des Bezugs zu anderen Sonderregeln (auch externe Dokumente)."),
                html.Li("Kartenvisualisierung mit Filteroptionen für Bauzonen, Komplexitätsniveau der Baugesetze und Nachhaltigkeitsindex."),
                html.Li("Parameter-Viewer: Zugriff auf detaillierte Bauparameter (z.B. Ausnützungsziffern, Grenzabstände) und spezifische Zonendaten für eine schnelle und genaue Projektplanung."),
            ]),
            html.H5("Parametervergleich"),
            html.Ul(children=[
                html.Li("Vergleich von Parametern zwischen verschiedenen Gemeinden und Zonen, um Bauprojekte optimal anzupassen."),
                html.Li("Erkennung von und Extraktion von Text in Bilddateien mittels OCR-Erkennung."),
            ]),
            html.H5("Alert Manager"),
            html.Ul(children=[
                html.Li("Warnsystem Aktualität Baugesetze."),
                html.Li("Benachrichtigungen zu Änderungen in den Baugesetzen und deren potenziellen Auswirkungen auf laufende und geplante Projekte."),
            ]),
        ],
        style={
            'margin-left': '20px',
            'margin-right': '20px',
        }
    ),
])
