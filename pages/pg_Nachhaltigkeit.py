import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objects as go

dash.register_page(__name__, name="Nachhaltigkeitsmonitor", path="/Nachhaltigkeit", order=8)

if __name__ in dash.page_registry:
    dash.page_registry[__name__]["icon"] = "/assets/leaf.svg"

# Layout der App definieren
layout = html.Div([
    html.Div("Funktionen", style={'font-size': '16px', "margin-top": "10px", "margin-bottom": "10px"}),
    html.Hr(style={'margin-bottom': '10px', 'margin-top': '0px'}),
    html.Div(
        [
            html.H5("Nachhaltigkeitsindex"),
            html.Ul(children=[
                html.Li("Quantifizierung kausaler Effekte der Ausgestaltung von Bauordnungen auf nachhaltige Bauweise."),
                html.Li("Quantifizierung des kausalen Effekts von Bauregulierung und Komplexität auf nachhaltige Bauweise (Auswirkung bestimmter Formulierungen/Regeln (fördernd bzw. hemmend) auf z.B. PV-Dachaufbauten oder Erdsonden)."),
                html.Li("Nachhaltigkeitsindex: Übersicht über Nachhaltigkeitskriterien in den Bauvorschriften je Gemeinde und deren Einfluss auf Projektplanungen. Ein Index zeigt auf, welche Gemeinden besonders fördernde oder hemmende Regeln haben."),
            ]),
            html.H5("Nachhaltigkeits-Optimizer"),
            html.Ul(children=[
                html.Li("Empfehlungen und Best Practices: Vorschläge zur Optimierung nachhaltiger Projekte und Compliance mit lokalen Regeln, basierend auf den kausalen Analysen."),
            ]),
            html.H5("Nachhaltigkeitsmonitor"),
            html.Ul(children=[
                html.Li("Ermittlung der Regulierungen welche nachhaltige Bauweise (Dämmung/Heizsysteme) etc. am stärksten fördern."),
                html.Li("Darstellung der optimalen Gemeinde-spezifischen Kriterien zur Nachhaltigkeitsförderung (ohne den Denkmalschutz zu vernachlässigen)."),
                html.Li("Darstellung von Nachhaltigkeitsaspekte, welche ein besonderes Bewilligungsrisiko bieten."),
                html.Li("Kausale Effekte von Bauvorgaben bzw. Komplexität auf nachhaltige Immobilienlandschaft."),
                html.Li("Nachhaltigkeitsindex für Gemeinden."),
                html.Li("Nachhaltigkeitsindex Projekte."),
            ]),
        ],
        style={
            'margin-left': '20px',
            'margin-right': '20px',
        }
    ),
])
