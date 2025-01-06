import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

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
    'downloadedPdfDocumentValid': 'Dieser Parameter zeigt an, ob die heruntergeladenen BZO gültig sind oder nicht.',
    'Link_Dok_Present': 'Dieser Parameter zeigt an, ob der Link in der RIS-Liste zu einer BZO aktuell ist oder nicht.',
    'MunicipalityExists': 'Dieser Parameter zeigt an ob eine Gemeinde aus der RIS-Liste existiert .',
    'LinkValid': 'Dieser Parameter zeigt an, ob der Link aus der RIS-Liste noch gültig ist.',
    'MetaDataDateEqual': 'Dieser Parameter zeigt an, ob die Metadaten aus der RIS-Liste übereinstmmer mit den aktuellen Metadaten.',
    'MetaDataOriginal': 'Dieser Parameter zeigt an wie die originalen Metadaten sind.',
    'MetaDataDownloadedFile': 'Dieser Parameter zeigt an, ob die Meta-Daten der heruntergeladenen BZO übereinstimmen oder nicht.',
    'HashEqual': 'Dieser Parameter zeigt an, ob die Hash-Werte gleich sind oder nicht.',
    'CrawledLinkSameAsRISLink': 'Dieser Parameter zeigt an, ob der gecrawlte Link mit dem Link aus dem RIS-Dokument übereinstimmt oder nicht.'
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
app.layout = html.Div([
    html.H1("RIS-Dashboard", style={'font-family': 'Verdana, sans-serif'}),
    dcc.Dropdown(
        id='kanton-dropdown',
        options=[{'label': kanton, 'value': kanton} for kanton in df['GDEKT'].unique()],
        multi=True,
        placeholder='Wähle einen oder mehrere Kantone',
        value=[]
    ),
    html.Div([
        html.Div([
            dcc.Graph(id=f'graph-{var}', style={'width': '70%'}),
            html.Div([
                html.P(explanation_texts[var])  # Individuelle Texte für jede Textbox
            ], style={'width': '30%', 'padding': '10px', 'border': '1px solid #ddd', 'margin-left': '20px'})
        ], style={'display': 'flex', 'align-items': 'flex-start', 'justify-content': 'space-between', 'margin-bottom': '20px'})
        for var in variables
    ])
])

@app.callback(
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

if __name__ == '__main__':
    app.run_server(debug=True)
