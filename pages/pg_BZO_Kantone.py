import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import matplotlib.pyplot as plt
from dash import callback
from dash import html, dcc, Input, Output
import plotly.express as px

# Stelle sicher, dass die Seite im Dash-Framework registriert ist
# dash.register_page(__name__, name='BZO Kantone', order=4)

dash.register_page(__name__, name="BZO Kantone", path="/BZO_Kantone", order=4)

# Manuelle Registrierung des Icons mit dem relativen Pfad zur SVG-Datei
if __name__ in dash.page_registry:
    dash.page_registry[__name__]["icon"] = "/assets/book-section-regular.svg"
    
# Daten laden
df = pd.read_csv('Results_Document-Alerting-Master_01_E03.csv', delimiter=';')

# Definition der Variablen und ihrer Labels
variables = {
    'downloadedPdfDocumentValid': ('Valid', 'Invalid'),
    'Link_Dok_Present': ('Present', 'Not Present'),
    'MunicipalityExists': ('Exists', 'Does Not Exist'),
    'LinkValid': ('Valid', 'Invalid'),
    'MetaDataDateEqual': ('Equal', 'Not Equal'),
    'MetaDataOriginal': ('Original', 'Modified'),
    'MetaDataDownloadedFile': ('Matches', 'Does Not Match'),
    'HashEqual': ('Equal', 'Not Equal'),
    'CrawledLinkSameAsRISLink': ('Same', 'Different')
}

# Farbschema für die Variablen definieren
color_scheme = {
    'downloadedPdfDocumentValid': ['green', 'red', 'grey'],
    'Link_Dok_Present': ['green', 'red', 'grey'],
    'MunicipalityExists': ['green', 'red', 'grey'],
    'LinkValid': ['red', 'green', 'grey'],
    'MetaDataDateEqual': ['red', 'green', 'grey'],
    'MetaDataOriginal': ['green', 'red', 'grey'],
    'MetaDataDownloadedFile': ['red', 'green', 'grey'],
    'HashEqual': ['red', 'green', 'grey'],
    'CrawledLinkSameAsRISLink': ['red', 'green', 'grey']
}

# Erklärungstexte für jede Grafik
explanation_texts = {
    'MunicipalityExists': 'Dieser Parameter zeigt an, ob eine Gemeinde aus der RIS-Liste existiert',
    'Link_Dok_Present': 'Dieser Parameter zeigt an, ob es zu einer bestimmten Gemeinde einen Link in der RIS-Liste gibt',
    'LinkValid': 'Dieser Parameter zeigt an, ob der Link aus der RIS-Liste noch gültig ist.',
    'downloadedPdfDocumentValid': 'Dieser Parameter zeigt an, ob ein lesbares Dokument einer Gemeinde heruntergeladen werden konnte',
    'MetaDataOriginal': 'Dieser Parameter zeigt die Metadaten der Dokumente in der RIS-Liste',
    'MetaDataDownloadedFile': 'Dieser Parameter zeigt die Meta-Daten der heruntergeladenen Dokumente',
    'MetaDataDateEqual': 'Dieser Parameter zeigt an, ob die Metadaten aus der RIS-Liste mit den aktuellen Metadaten übereinstimmen. So kann man feststellen, ob neue Dokumente im Web vorhanden sind',
    'HashEqual': 'Dieser Parameter zeigt an, ob die Hash-Werte aus den vorhandenen RIS-Dokumenten mit den heruntergeladenen Dokumenten gleich sind oder nicht.',
    'CrawledLinkSameAsRISLink': 'Dieser Parameter zeigt an, ob der gecrawlte Link mit dem Link aus der RIS-Liste übereinstimmt oder nicht.'
}

# Umwandlung und Aggregation der Daten
data_frames = {}
for var, labels in variables.items():
    df[var] = df[var].fillna('Data Not Available')
    df[var] = df[var].replace({'True': labels[0], 'False': labels[1], 'None': 'Data Not Available'})
    grouped = df.groupby(['GDEKT', var]).size()
    unstacked = grouped.unstack(fill_value=0)
    unstacked = unstacked[[labels[0], labels[1]]] if labels[0] in unstacked.columns and labels[1] in unstacked.columns else unstacked
    data_frames[var] = unstacked

# Dashboard Layout
layout = html.Div([
    html.Div("Document Alerting Master - Übersicht BZO Gemeinden", style={'font-size': '16px',"margin-top": "10px","margin-bottom": "10px"}),
    html.Hr(style={'margin-bottom': '10px', 'margin-top': '0px'}),  # Setzt den oberen Rand 0 und den unteren Rand auf 10px
     dcc.Dropdown(
        id='kanton-dropdown',
        options=[{'label': kanton, 'value': kanton} for kanton in df['GDEKT'].unique()],
        multi=True,
        placeholder='Wähle einen oder mehrere Kantone',
        value=[],
        style={'font-size': '14px','color': 'black'}
    ),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(id=f'graph-{var}', style={'width': '70%'}),
            html.Div([
                html.P(explanation_texts[var])  # Individuelle Texte für jede Textbox
            ], style={'width': '30%', 'padding': '10px','margin-left': '20px'})
        ], style={'display': 'flex', 'align-items': 'flex-start', 'justify-content': 'space-between', 'margin-bottom': '20px'})
        for var in variables
    ])
])

@callback(
    [Output(f'graph-{var}', 'figure') for var in variables],
    [Input('kanton-dropdown', 'value')]
)
def update_graphs(selected_kantone):
    figures = []
    for var in variables:
        filtered_data = data_frames[var].loc[selected_kantone] if selected_kantone else data_frames[var]
        fig = px.bar(
            filtered_data,
            x=filtered_data.index,
            y=filtered_data.columns.tolist(),
            barmode='group',
            title=f'{var.replace("_", " ")} pro Kanton',
            color_discrete_sequence=color_scheme[var],
            template='plotly_white'
        )
        fig.update_layout(
            legend=dict(
                font=dict(
                    size=10  # Reducing font size of the legend
                )
            ),
            margin=dict(l=20, r=20, t=40, b=20)  # Adjusting margins to use space more effectively
        )
        figures.append(fig)
    return figures