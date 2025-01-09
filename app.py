import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import logging


def Header(name, app):
    title = html.H1(name, style={"margin-top": 30, 'fontSize': '30px'})
    logo = html.Img(
        #src=app.get_asset_url('dash-logo.png'),


        src=app.get_asset_url('dash-logo.png'), style={"float": "right", "height": 40, "marginTop": 30, "marginRight": 20}

        #style={'float': 'right', 'height': 60,"marginTop": 20, "marginRight": 40}
    )
    link = html.A(logo, href="https://www.pom.ch/")

    return dbc.Row([dbc.Col(title, md=8), dbc.Col(link, md=4)])

# Setze das Logging-Level
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "red",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H6("Content", style={'fontSize':20, 'textAlign':'left'}),
        html.Hr(),
        #html.P(
        #    "A simple sidebar layout with navigation links", className="lead"
        #),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                    html.Div(page["name"], className="ms-2"),
                    #html.Div(page["name"], style={"background-color": "red", "textAlign":"left"}),
                    ],
                    href=page["path"],
                    active="exact",
                    # style={"background-color": "red", "textAlign":"left"},
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={'fontSize':15, 'textAlign':'left'}
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = dbc.Container([
    dbc.Row([
        Header("RIS - Regulatory Information System", app)
        #dbc.Col(html.Div("Python Multipage App with Dash",
        #                 style={'fontSize':50, 'textAlign':'left'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                sidebar
                ], xs=4,sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Standardport auf 8050 setzen, falls keine PORT Umgebungsvariable gesetzt ist
    app.run(host='0.0.0.0', port=port, debug=False)
