import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objects as go

dash.register_page(__name__, name='Chancen & Risiken')

# Layout der App definieren
layout = html.Div(
    style={
        'margin-left': '20px',   # Rand links für bessere Lesbarkeit
        'margin-right': '20px',  # Rand rechts für bessere Lesbarkeit
    },
    children=[
        html.H4("Output-Funktionen"),
        html.H5("Prognose Bewilligungsrisiken"),
        html.Ul(children=[
            html.Li("Detaillierte Ansicht zu jedem Projekt, inklusive Prognose der Bewilligungsdauer und Risikoscores, die Investoren helfen, fundierte Entscheidungen zu treffen."),
            html.Li("Ein interaktives Dashboard, das die Bewilligungsrisiken und Chancen eines geplanten Bauprojekts anzeigt. Basierend auf den spezifischen Bauzonen und den kommunalen Bauvorschriften erhält der Benutzer Risikoscores und Chancenanalysen."),
            html.Li("Darstellung des Scores für zonenspezifische Chancen und Risiken der baulichen Investition."),
            html.Li("Quantifizierung des kausalen Effekts der Bauparameter und der Komplexität auf Bautätigkeit, Bewilligungsrisiken und Verdichtung."),
            html.Li("Chancen-Risiko-Schätzung für die Entwicklung: Prognosetool für Bewilligungsrisiken/-chancen."),
            html.Li("Durchschnittliches Projektrisiko: Visualisiert das aktuelle Risikoniveau der Projekte."),
            html.Li("Prognose von Bewilligungsrisiken spezifisch für nachhaltige Aspekte von Bauprojekten (Energieträger, Heizung/Warmwasser, Baumaterialien, PV-Anlagen, Geothermie, etc.).")
        ]),
        html.H5("Regel-Monitor"),
        html.Ul(children=[
            html.Li("Spezifikation des Ausmaßes der interpretierbaren Regeln (z.B. «Architektonisch gute Bebauung», «gute Integration ins Ortsbild»; Relativierungen und qualitative Aussagen mit großem Interpretationsspielraum)."),
            html.Li("Querverweis-Visualisierung: Darstellung der Verlinkungen und Abhängigkeiten zwischen Regeln, Ausnahmen und Querverweisen, um die Regeldichte besser verstehen und navigieren zu können.")
        ]),
        html.H5("Darstellung Komplexität"),
        html.Ul(children=[
            html.Li("Berechnung der Baugesetzkomplexität."),
            html.Li("Darstellung des Scores der Komplexität in Prozessen, inhaltliche Komplexität sowie sprachliche und strukturelle Komplexität."),
            html.Li("Komplexitätsübersicht: Eine Analyse der textlichen und prozessualen Komplexität der Baugesetze in jeder Gemeinde mit Scores und Indikatoren (z.B. Prozesskomplexität, Lesbarkeit, Regelabweichungen)."),
            html.Li("Textkomplexität-Highlighting: Aufbereitung der komplexen Textpassagen, die detaillierte Erklärungen oder Vorschläge für mögliche Vereinfachungen bieten.")
        ]),
        html.H5("Weitere Sektionen wie 3.3.4 Unterstützung Bauprozesse usw. können analog hinzugefügt werden.")
    ]
)
