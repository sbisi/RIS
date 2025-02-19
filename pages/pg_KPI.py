import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from dash import dash_table
import dash_bootstrap_components as dbc

# dash.register_page(__name__, name='Data Base & Quality - KPI', icon='bar-chart',order=3)

import dash


dash.register_page(__name__, name="Data Base & Quality - KPI", path="/kpi", order=3)

# Manuelle Registrierung des Icons
if __name__ in dash.page_registry:
    dash.page_registry[__name__]["icon"] = "fas fa-chart-bar"

# dash.register_page(__name__, path='/', name='Data Base & Quality - KPI', icon='bar-chart', title='Data Base & Quality - KPI', order=3)


explanation_texts = {
    'MunicipalityExists': 'Dieser Parameter zeigt an ob eine Gemeinde aus der RIS-Liste existiert',
    'Link_Dok_Present': 'Dieser Parameter zeigt an, ob es zu einer bestimmten Gemeinde einen Link in der RIS-Liste gibt',
    'LinkValid': 'Dieser Parameter zeigt an, ob der Link aus der RIS-Liste noch gültig ist.',
    'downloadedPdfDocumentValid': 'Dieser Parameter zeigt an, ein lesbares Dokument einer Gemeinde heruntergeladen werden konnte',
    'MetaDataOriginal': 'Dieser Parameter zeigt die Metadaten der Dokumente in der RIS-Liste',
    'MetaDataDownloadedFile': 'Dieser Parameter zeigt die Meta-Daten der heruntergeladenen Dokumente',
    'MetaDataDateEqual': 'Dieser Parameter zeigt an, ob die Metadaten aus der RIS-Liste mit den aktuellen Metadaten übereinstimmen. So kann man feststellen, ob neue Dokumente im Web vorhanden sind',
    'HashEqual': 'Dieser Parameter zeigt an, ob die Hash-Werte aus den vorhandenen RIS-Dokumenten mit den heruntergeladenen Dokumenten gleich sind oder nicht.',
    'CrawledLinkSameAsRISLink': 'Dieser Parameter zeigt an, ob der gecrawlte Link mit dem Link aus der RIS-Liste übereinstimmt oder nicht.'
}

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
canton_distribution_fig1 = px.bar(canton_distribution, labels={'index': 'Kanton', 'value': 'Anzahl der Gemeinden'}, color_discrete_sequence=['#636EFA'], title='Verteilung der Gemeinden pro Kanton')
canton_distribution_fig2 = px.bar(canton_distribution, labels={'index': 'Kanton', 'value': 'Anzahl der Gemeinden'}, color_discrete_sequence=['#636EFA'], title='Verteilung der Gemeinden pro Kanton')

canton_distribution_fig2.update_layout(
    paper_bgcolor='white',          # Hintergrundfarbe des gesamten Diagramms
    plot_bgcolor='rgba(0,0,0,0)',            # Hintergrundfarbe des Plot-Bereichs
    legend=dict(
        title_text="Legende",  # Setze den Titel der Legende
        x=1.05,
        y=1.0,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0, 0, 0, 0.0)',               # Rahmenfarbe der Legende
        borderwidth=2
    ),
    # title_text=" ",                      # Titel der Grafik
    title_font=dict(size=12),             # Schriftgröße des Titels
    xaxis_title=" ",
    # xaxis_title_font=dict(size=10),       # Schriftgröße des X-Achsen-Titels
    yaxis_title="",
    # yaxis_title_font=dict(size=10),        # Schriftgröße des Y-Achsen-Titels
    font=dict(
        # family="Courier New, monospace",      # Schriftart für alle Texte
        size=10,                            # Allgemeine Schriftgröße
        color="black"                       # Farbe des Textes
    ),
    margin=dict(l=10, r=10, t=50, b=10)  # Setzt alle Ränder auf 10 Pixel
)


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


# Pfad zur CSV-Datei
file_path = 'results.csv'
data = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')
data.columns = [col.strip() for col in data.columns]


# Datenbereinigung und Typumwandlung für Boolesche Spalten

# Umwandlung und Berechnung
boolean_columns = ['LINKDOC_PRESENT', 'DOWNLOADED_PDF_VALID', 'MUNICIPALITY_EXISTS', 'LINK_VALID', 'METADATA_EQUAL', 'HASH_EQUAL', 'CRAWLED_LINK_SAME']
for col in boolean_columns:
    data[col] = data[col].replace({'True': True, 'False': False, 'true': True, 'false': False}).astype(bool)
kpi_values = {col: (data[col].sum() / data[col].count() * 100 if data[col].count() > 0 else 0) for col in boolean_columns}

for col in boolean_columns:
    data[col] = data[col].astype(str)

def create_pie_chart(value, title, color='#636EFA', other_color='lightgrey'):
    # Berechne den Prozentsatz für den Kreisdiagramm-Sektor
    labels = ['True', 'False']
    values = [value, 100 - value]
    colors = [color, other_color]

    # Erstelle das Kreisdiagramm
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors, hole=.3)])

    fig.update_layout(
        title_text=title,
        title_font=dict(size=12, family='Verdana, sans-serif', color='black'),  # Setze Schriftart, Größe und Farbe des Titels
        showlegend=True,
        margin=dict(l=10, r=10, t=50, b=10),
        height=250,
        legend_title_font=dict(family='Verdana, sans-serif', size=10, color='blue'),  # Setze Schriftart für die Legende
        font=dict(family='Verdana, sans-serif', size=10, color='black')  # Standard-Schriftart für alle Textelemente
    )
    return fig

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
    style_cell={'textAlign': 'left', 'padding': '10px', 'font-size': '12px', 'color': 'black'},
    style_header={'backgroundColor': '#0074D9', 'fontWeight': 'bold', 'color': 'white', 'fontSize': '12px'},
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
    html.Div("Document Alerting Master - Übersicht BZO Gemeinden", style={'font-size': '16px',"margin-top": "10px","margin-bottom": "10px"}),
    # html.H1("Document Alerting Master", 
    #        style={'font-family': 'Verdana, sans-serif', 'font-size': '16px', "margin-top": "50px"}),
    html.Hr(style={'margin-bottom': '10px', 'margin-top': '0px'}),  # Setzt den oberen Rand 0 und den unteren Rand auf 10px
        dbc.Row([
        dbc.Col(dcc.Graph(figure=canton_distribution_fig1), xs=12, sm=6, md=6),
        # dbc.Col(dcc.Graph(figure=canton_distribution_fig1), xs=12, sm=6, md=6),
        dbc.Col([
            html.Div([
                html.H2("Erklärung der Parameter:", style={'font-family': 'Verdana, sans-serif', 'font-size': '16px'}),
                html.Ul([html.Li(f"{key}: {value}") for key, value in explanation_texts.items()], 
                style={'padding-left': '20px', 'margin-top': '5px','font-size': '14px', 'line-height': '30px'})  # Verstärken Sie die Listendarstellung
            ])
        ], xs=12, sm=6, md=6),
        ], justify="around"),
        html.Br(),
        html.Hr(style={'margin-bottom': '10px', 'margin-top': '1px'}),
    html.Div("Document Alerting Master - KPI BZO Gemeinden", style={'font-size': '16px',"margin-top": "10px","margin-bottom": "10px"}),
        html.Hr(style={'margin-bottom': '10px', 'margin-top': '0px'}),
        dbc.Row([
        dbc.Col(dcc.Graph(id='pie-1', figure=create_pie_chart(kpi_values['LINKDOC_PRESENT'], 'LINKDOC_PRESENT')), xs=12, sm=6, md=3),
        dbc.Col(dcc.Graph(id='pie-2', figure=create_pie_chart(kpi_values['DOWNLOADED_PDF_VALID'], 'DOWNLOADED_PDF_VALID')), xs=12, sm=6, md=3),
        dbc.Col(dcc.Graph(id='pie-3', figure=create_pie_chart(kpi_values['MUNICIPALITY_EXISTS'], 'MUNICIPALITY_EXISTS')), xs=12, sm=6, md=3),
        dbc.Col(dcc.Graph(id='pie-4', figure=create_pie_chart(kpi_values['LINK_VALID'], 'LINK_VALID')), xs=12, sm=6, md=3)
    ], justify="around"),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id='pie-5', figure=create_pie_chart(kpi_values['METADATA_EQUAL'], 'METADATA_EQUAL'))),
        dbc.Col(dcc.Graph(id='pie-6', figure=create_pie_chart(kpi_values['HASH_EQUAL'], 'HASH_EQUAL'))),
        dbc.Col(dcc.Graph(id='pie-7', figure=create_pie_chart(kpi_values['CRAWLED_LINK_SAME'], 'CRAWLED_LINK_SAME'))),
        dbc.Col(html.Div())  # Leer, um das Layout konsistent zu halten
    ], justify="around"),
    html.Br(),
#    html.H2('Numerische Werte', style={'font-family': 'Verdana, sans-serif', 'font-size': '16px'}),
#    html.Br(),
#    dbc.Row(dbc.Col(summary_table)),
    html.Br()
], fluid=True)
