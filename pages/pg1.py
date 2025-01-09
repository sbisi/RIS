import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='KPI')

# Pfad zur CSV-Datei
file_path = 'results.csv'
data = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')
data.columns = [col.strip() for col in data.columns]

# Umwandlung und Berechnung
boolean_columns = ['LINKDOC_PRESENT', 'DOWNLOADED_PDF_VALID', 'MUNICIPALITY_EXISTS', 'LINK_VALID', 'METADATA_EQUAL', 'HASH_EQUAL', 'CRAWLED_LINK_SAME']
for col in boolean_columns:
    data[col] = data[col].replace({'True': True, 'False': False, 'true': True, 'false': False}).astype(bool)
kpi_values = {col: (data[col].sum() / data[col].count() * 100 if data[col].count() > 0 else 0) for col in boolean_columns}

# Erstelle den Gauge-Indikator
def create_gauge(value, title, min_value=0, max_value=100, color='#636EFA', step_color='lightgrey', number_font_size=16):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16}},
        gauge={
            'axis': {'range': [min_value, max_value]},
            'bar': {'color': color},
            'steps': [{'range': [min_value, value], 'color': step_color}, {'range': [value, max_value], 'color': step_color}],
            'threshold': {'line': {'color': "#636EFA", 'width': 4}, 'thickness': 0.75, 'value': value}
        },
        number={'font': {'size': number_font_size, 'color': 'black'}}  # Komma ist jetzt korrekt eingefügt
    ))
    fig.update_layout(margin={"l": 10, "r": 10, "t": 10, "b": 10}, height=250, autosize=True)
    return fig


# Layout der Anwendung mit dbc
layout = dbc.Container([
    html.H1("KPI Data Quality", style={'font-family': 'Verdana, sans-serif', 'font-size': '24px'}),
    html.Hr(),
        dbc.Row([
        dbc.Col(dcc.Graph(id='gauge-1', figure=create_gauge(kpi_values['LINKDOC_PRESENT'], 'LINKDOC_PRESENT')), xs=12, sm=6, md=3),
        dbc.Col(dcc.Graph(id='gauge-2', figure=create_gauge(kpi_values['DOWNLOADED_PDF_VALID'], 'DOWNLOADED_PDF_VALID')), xs=12, sm=6, md=3),
        dbc.Col(dcc.Graph(id='gauge-3', figure=create_gauge(kpi_values['MUNICIPALITY_EXISTS'], 'MUNICIPALITY_EXISTS')), xs=12, sm=6, md=3),
        dbc.Col(dcc.Graph(id='gauge-4', figure=create_gauge(kpi_values['LINK_VALID'], 'LINK_VALID')), xs=12, sm=6, md=3)
    ], justify="around"),

    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id='gauge-5', figure=create_gauge(kpi_values['METADATA_EQUAL'], 'METADATA_EQUAL'))),
        dbc.Col(dcc.Graph(id='gauge-6', figure=create_gauge(kpi_values['HASH_EQUAL'], 'HASH_EQUAL'))),
        dbc.Col(dcc.Graph(id='gauge-7', figure=create_gauge(kpi_values['CRAWLED_LINK_SAME'], 'CRAWLED_LINK_SAME'))),
        dbc.Col(html.Div())
    ], justify="around"),
    html.Br()
], fluid=True)
