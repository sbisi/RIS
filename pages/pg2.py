import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objects as go

dash.register_page(__name__, name='BZO Kantone')

# Pfad zur CSV-Datei
file_path = 'results.csv'

# Daten einlesen, dabei schlechte Zeilen überspringen und Spaltennamen bereinigen
data = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')
data.columns = [col.strip() for col in data.columns]  # Entferne Leerzeichen von Spaltennamen

# Definition der Variablen und ihrer Labels
variables = {
    'DOWNLOADED_PDF_VALID': ('Valid', 'Invalid'),
    'LINKDOC_PRESENT': ('Present', 'Not Present'),
    'MUNICIPALITY_EXISTS': ('Exists', 'Does Not Exist'),
    'LINK_VALID': ('Valid', 'Invalid'),
    'METADATA_EQUAL': ('Equal', 'Not Equal'),
    'METADATA_ORIGINAL': ('Original', 'Modified'),
    'METADATA_DOWNLOADEDFILE': ('Matches', 'Does Not Match'),
    'HASH_EQUAL': ('Equal', 'Not Equal'),
    'CRAWLED_LINK_SAME': ('Same', 'Different')
}

# Farbschema für die Variablen definieren
color_scheme = {
    'DOWNLOADED_PDF_VALID': ['green', 'red', 'grey'],
    'LINKDOC_PRESENT': ['green', 'red', 'grey'],
    'MUNICIPALITY_EXISTS': ['green', 'red', 'grey'],
    'LINK_VALID': ['red', 'green', 'grey'],
    'METADATA_EQUAL': ['red', 'green', 'grey'],
    'METADATA_ORIGINAL': ['green', 'red', 'grey'],
    'METADATA_DOWNLOADEDFILE': ['red', 'green', 'grey'],
    'HASH_EQUAL': ['red', 'green', 'grey'],
    'CRAWLED_LINK_SAME': ['red', 'green', 'grey']
}

# Umwandlung und Aggregation der Daten
data_frames = {}
for var, labels in variables.items():
    data[var] = data[var].fillna('Data Not Available').replace({'True': labels[0], 'False': labels[1]})
    grouped = data.groupby(['GDEKT', var]).size()
    unstacked = grouped.unstack(fill_value=0)
    data_frames[var] = unstacked


# Erstelle den Gauge-Indikator
gauge = go.Indicator(
    mode="gauge+number",
    value=3.2,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Bewertung"},
    gauge={
        'axis': {'range': [0, 5]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 4], 'color': 'lightgrey'},
            {'range': [4, 5], 'color': 'green'}
        ]
    }
)

# Layout der App
layout = html.Div([
    html.H1("Quality Check BZO-Data", style={'font-family': 'Verdana, sans-serif', 'font-size': '24px'}),
    dcc.Dropdown(
        id='kanton-dropdown',
        options=[{'label': kanton, 'value': kanton} for kanton in data['GDEKT'].unique()],
        multi=True,
        placeholder='Wähle einen oder mehrere Kantone',
        style={'color': 'black'}
    ),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(id=f'graph-{var}', style={'width': '70%'}),
            html.Div([
                html.P(variables[var][0]),  # Anzeige der Label-Texte für jede Graph
            ], style={'width': '30%', 'padding': '10px', 'border': 'none', 'margin-left': '20px'})
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
            legend=dict(font=dict(size=10)),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        figures.append(fig)
    return figures
