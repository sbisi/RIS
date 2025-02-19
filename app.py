import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import logging


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"])
server = app.server

def Header(name, app):
    title = html.H1(name, style={"margin-top": 18, 'fontSize': '20px'})
    logo = html.Img(
        src=app.get_asset_url('dash-logo.png'), 
        style={"float": "right", "height": '22px', "marginTop": '22px', "marginRight": 20}
    )
    link = html.A(logo, href="https://www.pom.ch/")
    return dbc.Row([dbc.Col(title, md=8), dbc.Col(link, md=4)])

logging.getLogger('werkzeug').setLevel(logging.ERROR)

# Button für Sidebar Toggle
toggle_button = dbc.Button(
    html.I(className="fas fa-arrow-left", id="toggle-icon"),
    id="sidebar-toggle",
    n_clicks=0,
    className="mb-3",
    color="primary",
    style={
        'position': 'absolute',
        'top': '12px',
        'right': '10px',
        # 'padding': '4px 8px',
        'fontSize': '12px',
        'transition': 'right 0.3s',
    }
)

# Sidebar-Header mit Navigationstext
INITIAL_SIDEBAR_HEADER_STYLE = {
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'left',  # Text links ausrichten
    'height': '25px',  # Mehr Höhe für eine echte Zentrierung
    'width': '100%',
    'padding': '5px 10px',  # Padding statt margin
    'transition': 'all 0.3s ease-in-out',
    'margin-top': '15px'
}

sidebar_header = html.Div(
    [
#        html.H6("Navigation", id="nav-text", 
#                style={'fontSize': 16, 'textAlign': 'left', 'margin-left': '0', 'margin-top': '5px'}),  # Text-Position beibehalten
         html.H6("Navigation", id="nav-text", 
                style={
                    'fontSize': 16, 
                    'textAlign': 
                    'left', 
                    'margin-left': '0', 
                    'margin-top': '5px',
                    'line-height': '24px',
                    'display': 'flex',
                    'align-items': 'center'}),  # Fixierte Höhe
         toggle_button  # Falls nötig, diesen Button separat positionieren
    ],
    id="sidebar-header",
    style=INITIAL_SIDEBAR_HEADER_STYLE
)

pages = list(dash.page_registry.values())

def get_icon(page):
    """Holt das Icon, entweder als FontAwesome oder als Bild."""
    if "icon" in page and isinstance(page["icon"], str):
        icon_path = page["icon"].lstrip("assets/")  # Entfernt doppeltes "assets/"
        if icon_path.endswith(".svg"):  # SVG-Icons als <img>
            return html.Img(
                src=app.get_asset_url(icon_path), 
                height="20px", width="20px", 
                style={
                    "margin-left": "5px",  # Kleiner Abstand vom linken Rand
                    "margin-right": "10px",  
                    "filter": "invert(1)",  
                    "opacity": "0.8"
                }
            )
        else:  # FontAwesome Icons
            return html.I(className=f"fa {page['icon']} me-2", 
                          style={"font-size": "20px", "color": "white", "margin-left": "5px"})  # Abstand reduzieren
    return html.I(className="fa fa-info-circle me-2", 
                  style={"font-size": "20px", "color": "white", "margin-left": "5px"})  # Standard-Icon


sidebar = html.Div(
    [
        sidebar_header,
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        get_icon(page),
                        html.Div(page["name"], className="ms-2", id=f"nav-text-{i}", 
                                 style={'textAlign': 'left', 'margin-left': '0px'})  # Text-Position beibehalten
                    ],
                    href=page["path"],
                    active="exact",
                    className="custom-hover-link",
                    style={
                        'display': 'flex', 
                        'align-items': 'center', 
                        'textAlign': 'left',
                        'padding-left': '15px'  # Reduziert den Abstand vom linken Rand
                    }
                ) for i, page in enumerate(pages)
            ] if pages else [],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style={
        'width': '16rem',
        'position': 'fixed',
        'height': 'calc(100vh - 50px)',
        'left': '0',
        'top': '65px',
        'backgroundColor': '#333',
        'overflowY': 'auto',
        'transition': 'width 0.3s'
    }
)


app.layout = dbc.Container([
    Header("RIS - Regulatory Information System", app),
    # html.Hr(),
    dbc.Row([
        html.Div(
            sidebar,
            id="sidebar-container-fixed"  # Umbenennung, um Duplikat zu vermeiden
        ),
        dbc.Col(
            dash.page_container,
            id="main-content",
            style={
                'padding': '0px',
                'margin-left': '16rem',
                'margin-top': '15px',
                'width': 'calc(100% - 16rem)',
                'overflowY': 'auto',
                'backgroundColor': 'black'
            }
        )
    ])
], fluid=True)

# Definiere den ursprünglichen Zustand der Sidebar inklusive Header

INITIAL_SIDEBAR_STATE = {
    "sidebar_style": {
        'width': '16rem',
        'position': 'fixed',
        'height': 'calc(100vh - 50px)',
        'left': '0',
        'top': '65px',
        'backgroundColor': '#333',
        'overflowY': 'auto',
        'transition': 'width 0.3s'
    },
    "sidebar_header_style": {
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'left',  # Text links ausrichten
        'height': '20px',  # Mehr Höhe für eine echte Zentrierung
        'width': '100%',
        'padding': '5px 10px',  # Padding statt margin
        'transition': 'all 0.3s ease-in-out',
        'margin-top': '20px' #HIER IST DIE KONTROLLE
    }
}

@app.callback(
    [
        Output("sidebar", "style"),
        Output("sidebar-header", "style"),  # Sidebar-Header bleibt unverändert beim Zuklappen
        Output("toggle-icon", "className"),
        Output("main-content", "style"),
        Output("nav-text", "style"),
        *[Output(f"nav-text-{i}", "style") for i in range(len(pages))],
        Output("sidebar-toggle", "style"),  # Button-Stil
    ],
    Input("sidebar-toggle", "n_clicks"),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks):
    collapsed = n_clicks % 2 == 1

    if collapsed:
        # Der zugeklappte Zustand bleibt exakt so, wie er vorher war!
        new_sidebar_style = {
            'width': '4rem',
            'position': 'fixed',
            'height': 'calc(100vh - 50px)',
            'left': '0',
            'top': '65px',
            'backgroundColor': '#333',
            'overflowY': 'auto',
            'transition': 'width 0.3s'
        }
        new_sidebar_header_style = INITIAL_SIDEBAR_STATE["sidebar_header_style"]  # Header bleibt sichtbar
    else:
        # Wiederherstellen des Originalzustands
        new_sidebar_style = INITIAL_SIDEBAR_STATE["sidebar_style"]
        new_sidebar_header_style = INITIAL_SIDEBAR_STATE["sidebar_header_style"]

    new_button_style = {  # Dynamischer Stil für den Button
        'position': 'absolute',
        'top': '12px',
        'right': '10px' if not collapsed else '20px',
        'padding': '4px 8px',
        'fontSize': '12px',
        'transition': 'right 0.3s'
    }

    return (
        new_sidebar_style,
        new_sidebar_header_style,  # Header bleibt sichtbar, außer wenn es vorher anders war
        "fas fa-arrow-right" if collapsed else "fas fa-arrow-left",
        {
            'padding': '15px',
            'margin-left': new_sidebar_style["width"],
            'margin-top': '12px',
            'width': f'calc(100% - {new_sidebar_style["width"]})',
            'overflowY': 'auto',
            'backgroundColor': 'black'
        },
        {'display': 'none' if collapsed else 'inline-block'},
        *[{'display': 'none' if collapsed else 'inline-block'} for _ in range(len(pages))],
        new_button_style
    )

# if __name__ == "__main__":
#    app.run_server(debug=False)

if __name__ == "__main__":
    app.config.suppress_callback_exceptions = True
    app.run_server(host="0.0.0.0", port=10000, debug=True)
