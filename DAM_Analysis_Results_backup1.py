import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Daten laden
df = pd.read_csv('Results_Document-Alerting-Master_01_E03.csv', delimiter=';')

# Korrekte Umwandlung der Wahrheitswerte
df['downloadedPdfDocumentValid'] = df['downloadedPdfDocumentValid'].replace({'True': 'Valid', 'False': 'Invalid'})

# Daten aggregieren
grouped = df.groupby(['GDEKT', 'downloadedPdfDocumentValid']).size()
pdf_validity = grouped.unstack(fill_value=0)

# Überprüfen, ob die Spalten 'Valid' und 'Invalid' korrekt benannt sind
pdf_validity.columns = ['Invalid' if col == False else 'Valid' if col == True else col for col in pdf_validity.columns]

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
    dcc.Graph(id='pdf-validity-per-kanton')
])

@app.callback(
    Output('pdf-validity-per-kanton', 'figure'),
    Input('kanton-dropdown', 'value')
)
def update_pdf_validity_per_kanton(selected_kantone):
    if not selected_kantone:
        filtered_df = pdf_validity
    else:
        # Sicherstellen, dass der Index korrekt gesetzt ist
        if pdf_validity.index.name != 'GDEKT':
            pdf_validity.set_index('GDEKT', inplace=True)
        filtered_df = pdf_validity.loc[selected_kantone]

    fig = px.bar(
        filtered_df,
        x=filtered_df.index,
        y=['Valid', 'Invalid'],
        barmode='group',
        title='PDF-Validität pro Kanton'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
