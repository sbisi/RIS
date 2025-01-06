import dash
from dash import html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Daten laden
df = pd.read_csv('Results_Document-Alerting-Master_01_E03.csv', delimiter=';')

# Umwandlung der Wahrheitswerte
df['downloadedPdfDocumentValid'] = df['downloadedPdfDocumentValid'].replace({'True': 'Valid', 'False': 'Invalid'})

# Daten aggregieren
grouped = df.groupby(['GDEKT', 'downloadedPdfDocumentValid']).size()
pdf_validity = grouped.unstack(fill_value=0)

# print("Hallo: ", pdf_validity)
pdf_validity.head()
pdf_validity.info()