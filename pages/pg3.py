import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objects as go

dash.register_page(__name__, name='Planungsparameter & Vorschriften')

# Layout der App definieren
layout = html.Div(
    style={
        'margin-left': '20px',   # Rand links für bessere Lesbarkeit
        'margin-right': '20px',  # Rand rechts für bessere Lesbarkeit
    },
    children=[
        html.H4("Output-Funktionen"),
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
    ]
)
