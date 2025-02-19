from dash import html
import dash_bootstrap_components as dbc

# 🔍 search_button
search_button = html.Button(
    html.Img(src="/assets/search.svg", width=20, height=20),
    id="search_button",
    style={
        "border": "none",
        "background": "none",
        "cursor": "pointer",
        "padding": "5px",
        "height": "30px",
        "width": "30px",
        "margin-left": "5px",
        "margin-right": "10px",
        "filter": "invert(1)",
        "opacity": "0.8"
    },
    n_clicks=0
)

# 🔍 buttet_point
bullet_point = html.Button(
    html.Img(src="/assets/bullseye-pointer-regular.svg", width=20, height=20),
    id="bullet_point",
    style={
        "border": "none",
        "background": "none",
        "cursor": "pointer",
        "padding": "0px",
        "height": "20px",
        "width": "20px",
        "margin-left": "10px",
        "margin-right": "0px",
        "filter": "invert(1)",
        "opacity": "0.8"
    },
    n_clicks=0
)

def create_icon_text_row(icon_name, text):
    return dbc.Row([
        # Icon-Spalte mit fester Breite
        dbc.Col(html.Img(src=f"/assets/{icon_name}.svg", width=14, height=14, 
                         style={'margin-right': '10px', "margin-left": "5px",
                                "border": "none", "background": "none",
                                "cursor": "pointer", "padding": "0px",
                                "filter": "invert(1)", "opacity": "0.8"}), 
                width=1),  # Fixierte Breite für das Icon
        
        # Label-Spalte mit fixierter Breite
        dbc.Col(html.Span(f"{text}:", 
                         style={'font-size': '14px', 'margin': '0px',
                                'padding-left': '10px', 'width': '160px', 
                                'text-align': 'left',
                                'display': 'inline-block', 'white-space': 'nowrap'}),  
                width=4),  # ❗ Mehr Platz für das Label reservieren
    ], align="center", justify="start", className="mb-0")
