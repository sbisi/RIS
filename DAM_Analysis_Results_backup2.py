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

# Umwandlung und Aggregation der Daten
data_frames = {}
for var, labels in variables.items():
    # Behandlung von NaN-Werten und Umwandlung von True/False
    df[var] = df[var].fillna('Data Not Available')
    df[var] = df[var].replace({'True': labels[0], 'False': labels[1], 'None': 'Data Not Available'})
    grouped = df.groupby(['GDEKT', var]).size()
    unstacked = grouped.unstack(fill_value=0)
    unstacked = unstacked[[labels[0], labels[1]]] if labels[0] in unstacked.columns and labels[1] in unstacked.columns else unstacked
    data_frames[var] = unstacked

# Dashboard Layout
app.layout = html.Div([
    html.H1("RIS-Dashboard"),
    dcc.Dropdown(
        id='kanton-dropdown',
        options=[{'label': kanton, 'value': kanton} for kanton in df['GDEKT'].unique()],
        multi=True,
        placeholder='Wähle einen oder mehrere Kantone',
        value=[]
    ),
    *[dcc.Graph(id=f'graph-{var}') for var in variables]
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
            title=f'{var.replace("_", " ")} pro Kanton'
        )
        figures.append(fig)
    return figures

if __name__ == '__main__':
    app.run_server(debug=True)
