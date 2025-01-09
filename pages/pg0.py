import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Data Basis', title='Index',
                   image='pg1.png', description='Real Estate Platform')

# Daten einlesen
data = pd.read_csv('results.csv', delimiter=';', on_bad_lines='skip')

# Bereinigung der Spaltennamen
data.columns = [col.strip() for col in data.columns]

# Datenbereinigung und Typumwandlung für Boolesche Spalten
boolean_columns = [
    'LINKDOC_PRESENT', 'DOWNLOADED_PDF_VALID', 'MUNICIPALITY_EXISTS',
    'LINK_VALID', 'METADATA_EQUAL', 'HASH_EQUAL', 'CRAWLED_LINK_SAME'
]

for col in boolean_columns:
    data[col] = data[col].astype(str)

# Verteilung nach Kantonen als Balkendiagramm
canton_distribution = data['GDEKT'].value_counts()
canton_distribution_fig = px.bar(canton_distribution, labels={'index': 'Kanton', 'value': 'Anzahl der Gemeinden'}, color_discrete_sequence=['#636EFA'], title='Verteilung der Gemeinden pro Kanton')

# KPI Tabelle erstellen
kpi_data = []
for col in boolean_columns:
    true_count = (data[col] == 'True').sum()
    false_count = (data[col] == 'False').sum()
    total_count = true_count + false_count
    kpi_data.extend([
        {'KPI': col, 'Wert': 'True', 'Absolute': true_count, 'Prozent (%)': round(true_count / total_count * 100, 2)},
        {'KPI': col, 'Wert': 'False', 'Absolute': false_count, 'Prozent (%)': round(false_count / total_count * 100, 2)},
        {'KPI': '', 'Wert': '', 'Absolute': '', 'Prozent (%)': ''}  # Leerzeile für bessere Trennung
    ])

columns = [{'name': 'KPI', 'id': 'KPI'}, {'name': 'Wert', 'id': 'Wert'}, {'name': 'Absolute', 'id': 'Absolute'}, {'name': 'Prozent (%)', 'id': 'Prozent (%)'}]

summary_table = dash_table.DataTable(
    columns=columns,
    data=kpi_data,
    style_cell={'textAlign': 'left', 'padding': '10px', 'font-size': '16px', 'color': 'black'},
    style_header={'backgroundColor': '#0074D9', 'fontWeight': 'bold', 'color': 'white', 'fontSize': '18px'},
    style_data_conditional=[
        {'if': {'column_id': 'Absolute', 'filter_query': '{Wert} eq "True"'}, 'color': 'green'},
        {'if': {'column_id': 'Absolute', 'filter_query': '{Wert} eq "False"'}, 'color': 'red'},
        {'if': {'column_id': 'Prozent (%)', 'filter_query': '{Wert} eq "True"'}, 'color': 'green'},
        {'if': {'column_id': 'Prozent (%)', 'filter_query': '{Wert} eq "False"'}, 'color': 'red'},
        {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'}
    ],
    style_table={'overflowX': 'auto'}
)

layout = dbc.Container([
    html.H1("KPI Document Alerting Master", style={'font-family': 'Verdana, sans-serif', 'font-size': '24px'}),
    html.Hr(),
    dbc.Row(dbc.Col(dcc.Graph(figure=canton_distribution_fig))),
    html.Br(),
    html.H2('Analyse der Werte pro Spalte', style={'font-family': 'Verdana, sans-serif', 'font-size': '24px'}),
    dbc.Row(dbc.Col(summary_table))
], fluid=True)
