from importlib import import_module
import inspect
from textwrap import dedent
import os
import pandas as pd
import plotly.express as px

import dash
import dash_bootstrap_components as dbc
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash import callback

import dash
from dash import dcc, html, callback, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

from dash.dependencies import Input, Output

from tqdm import tqdm

from pathlib import Path


# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='KPI DAM',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='Real Estate Platform'
)



#dash.register_page(__name__, name='KPI DAM')

data = pd.read_csv('Results_Document-Alerting-Master_01_E03.csv', delimiter=';')

# Datenbereinigung und Typumwandlung für Boolesche Spalten
boolean_columns = ['Link_Dok_Present', 'downloadedPdfDocumentValid', 'MunicipalityExists', 'LinkValid', 'MetaDataDateEqual', 'HashEqual', 'CrawledLinkSameAsRISLink']
for col in boolean_columns:
    data[col] = data[col].astype(str)  # Konvertiere alle Booleschen Spalten zu Strings

# Verteilung nach Kantonen als Balkendiagramm
canton_distribution = data['GDEKT'].value_counts()
canton_distribution_fig = px.bar(canton_distribution, labels={'index': 'Kanton', 'value': 'Anzahl der Gemeinden'}, title='Verteilung der Gemeinden pro Kanton')

# KPI Tabelle erstellen für jede Spalte
kpi_data = []
for col in boolean_columns:
    true_count = (data[col] == 'True').sum()
    false_count = (data[col] == 'False').sum()
    total_count = true_count + false_count
    if total_count > 0:  # Vermeidung der Division durch Null
        kpi_data.extend([
            {'KPI': col, 'Wert': 'True', 'Absolute': true_count, 'Prozent (%)': round(true_count / total_count * 100, 2)},
            {'KPI': col, 'Wert': 'False', 'Absolute': false_count, 'Prozent (%)': round(false_count / total_count * 100, 2)},
            {'KPI': '', 'Wert': '', 'Absolute': '', 'Prozent (%)': ''}  # Leerzeile
        ])

columns = [{'name': 'KPI', 'id': 'KPI'}, {'name': 'Wert', 'id': 'Wert'}, {'name': 'Absolute', 'id': 'Absolute'}, {'name': 'Prozent (%)', 'id': 'Prozent (%)'}]

summary_table = dash_table.DataTable(
    columns=columns,
    data=kpi_data,
    style_cell={
        'textAlign': 'left', 
        'padding': '10px', 
        'font-size': '16px', 
        'color': 'black'  # Setzt die Textfarbe auf Schwarz für alle Zellen
    },
    style_header={
        'backgroundColor': '#0074D9',
        'fontWeight': 'bold',
        'color': 'white',
        'fontSize': '18px'
    },
    style_data_conditional=[
        {
            'if': {'column_id': 'Absolute', 'filter_query': '{Wert} eq "True"'},
            'color': 'green'
        },
        {
            'if': {'column_id': 'Absolute', 'filter_query': '{Wert} eq "False"'},
            'color': 'red'
        },
        {
            'if': {'column_id': 'Prozent (%)', 'filter_query': '{Wert} eq "True"'},
            'color': 'green'
        },
        {
            'if': {'column_id': 'Prozent (%)', 'filter_query': '{Wert} eq "False"'},
            'color': 'red'
        },
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f9f9f9'
        }
    ],
    style_table={'overflowX': 'auto'}
)


app_selection = html.Div(
    [
        dbc.Label("Visualizing Model", width=4),
        dbc.Col(
            
#            width=9,
#            style={ 'border':'2px solid white', 'width':'200px', 'margin':'0 auto'},
        ),
    ],
#    row=True,
)

tab_style = {"height": "calc(100vh - 330px)", "padding": "15px", "color": "black"}
# tab_style = {'max-height': 'calc(100vh - 210px)'}
tabs = dbc.Tabs(
    [
        dbc.Tab(dcc.Markdown(id="description", style=tab_style), label="Description"),
        dbc.Tab(dcc.Markdown(id="source-code", style=tab_style), label="Parameters"),
    ]
)

Variable1= "KPI Document Alerting Master"

textareas = html.Div(
    [
        dbc.Textarea(className="mb-3", placeholder="A Textarea"),
        dbc.Textarea(
            valid=True,
            size="sm",
            className="mb-1",
            style={'align':'center', 'font-size':12,'background-color':'grey'},
            placeholder="A small, valid Textarea",
#        ),
#        dbc.Textarea(
#            invalid=True, size="lg", placeholder="A large, invalid Textarea",style={'align':'center', 'font-size':30,'background-color':'red'},
        ),
    ],
)

layout = dbc.Container([
    html.H1("KPI Document Alerting Master", style={'font-family': 'Verdana, sans-serif', 'font-size': '24px'}),
    html.Hr(),
 #   dbc.Row(dbc.Col(html.H2('Gesamtzahl der erfassten Gemeinden: {}'.format(data['GDENAME'].nunique()))), style={'font-family': 'Verdana, sans-serif', 'font-size': '12px'}),
    dbc.Row(dbc.Col(dcc.Graph(figure=canton_distribution_fig))),
    html.Br(),
    html.H2('Analyse der Werte pro Spalte', style={'font-family': 'Verdana, sans-serif', 'font-size': '24px'}),
    dbc.Row(dbc.Col(summary_table))
], fluid=True)