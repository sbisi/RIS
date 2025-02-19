"""
Visualizing the Real Estate Carbon Landscape of the Community of Windisch 2023 with a Columns Layer of Pydeck
"""


from importlib import import_module
import inspect
from textwrap import dedent
import os

import dash
import dash_bootstrap_components as dbc
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash import callback

from dash.dependencies import Input, Output

from tqdm import tqdm

from pathlib import Path

# dash.register_page(__name__, name='Geomaps BZO', order=5)
#
# dash.register_page(__name__, name="BZO Kantone", path="/BZO_Kantone", order=4)

# Manuelle Registrierung des Icons mit dem relativen Pfad zur SVG-Datei
dash.register_page(__name__, name="Geomaps BZO", path="/geomaps", order=4)

if __name__ in dash.page_registry:
    dash.page_registry[__name__]["icon"] = "/assets/maps.svg"

def Header(name, app):
    title = html.H1(name, style={"margin-top": 15})
    logo = html.Img(
        #src=app.get_asset_url('dash-logo.png'),


        src=app.get_asset_url('dash-logo.png'), style={"float": "right", "height": 40, "marginTop": 30, "marginRight": 20}

        #style={'float': 'right', 'height': 60,"marginTop": 20, "marginRight": 40}
    )
    link = html.A(logo, href="https://www.pom.ch/")

    return dbc.Row([dbc.Col(title, md=8), dbc.Col(link, md=4)])


def format_demo_name(demo):
    return demo.replace("usage-", "").replace("-", " ").title()


ignored_demos = ["usage-events.py", "usage-style-prop.py", "usage-geopandas.py"]

path = Path(__file__).parent.absolute()
path = f"{path}/demos"
print(path)
print()

deck_demos = [
    n.replace(".py", "").replace("usage-", "")
    for n in sorted(os.listdir(path))
    if ".py" in n and n not in ignored_demos
]

#deck_demos = [
#    n.replace(".py", "").replace("usage-", "")
#    for n in sorted(os.listdir("./demos"))
#    if ".py" in n and n not in ignored_demos
#]

print(sorted(os.listdir("./demos")))

# deck_demos=['columns_layer_CH']

print(os.getcwd())
# deck_modules = {demo: import_module(f"demos.usage-{demo}") for demo in tqdm(deck_demos)}

print("Loaded demos:", deck_demos)

app_selection = html.Div(
    [
        dbc.Label("Visualizing Model", width=4),
        dbc.Col(
            dbc.Select(
                id="demo-selection",
                options=[
                    {"label": demo.replace("-", " ").title(), "value": demo}
                    for demo in deck_demos
                ],
                style={'background-color':'white'},
                className="form-control-plaintext",
                value=deck_demos[0],
            ),
#            width=9,
#            style={ 'border':'2px solid white', 'width':'200px', 'margin':'0 auto'},
        ),
    ],
#    row=True,
)

tab_style = {"height": "calc(100vh - 330px)", "padding": "15px", "font-size": "16px"}

# tab_style = {'max-height': 'calc(100vh - 210px)'}
tabs = dbc.Tabs(
    [
        dbc.Tab(dcc.Markdown(id="description", style=tab_style), label="Description"),
        dbc.Tab(dcc.Markdown(id="source-code", style=tab_style), label="Parameters"),
    ]
)

Variable1= "1000 Tonnen co2/m2"

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

deck_modules = {demo: import_module(f"demos.usage-{demo}") for demo in tqdm(deck_demos)}

layout = [
    html.Div("Geodaten basierte Visualisierungen", style={'font-size': '16px',"margin-top": "10px","margin-bottom": "10px"}),
    html.Hr(style={'margin-bottom': '10px', 'margin-top': '0px'}),  # Setzt den oberen Rand 0 und den unteren Rand auf 10px
    dcc.Location(id="url", refresh=False),
    dbc.Row(
        [
            dbc.Col(
                [dbc.Card(
                    id="deck-card", 
                    style={"height": "calc(100vh - 110px)"},    #calc 100vh means 100% of the screen until 110% of the picture
                    body=True,
                ),
                html.I("(c) Dr. Peter Staub, pom+Group AG, peter.staub@pom.ch", style={'align':'center', 'font-size':12})],
                md=8,
            ),      
            # dbc.Col([app_selection, tabs,html.I("(c) Peter Staub)", style={'align':'center', 'font-size':12})], md=4),
            dbc.Col([
                app_selection, 
                tabs,
#                (html.B("Total Building CO2-Emmissions Switzerland", 
#                style={"color":"white","height": "50px", "width": "600px",'align':'center', 'font-size':20,"padding": "0px"})),
                (html.Br())
#               (html.Br()),
#               (html.B("1’062’919 t CO2", 
#               style={"color":"black",'background-color':'white',"height": "50px", "width": "600px",'align':'center', 'font-size':40, "padding": "0px"})),
             ], 
             md=4),
        ],
        style={"height": "calc(100vh - 110px)"},
    ),
]


@callback(Output("url", "pathname"), Input("demo-selection", "value"))
def update_url(name):
    return "/deck-explorer/" + name

@callback(
    [
        Output("deck-card", "children"),
        Output("description", "children"),
        Output("source-code", "children"),
    ],
    Input("url", "pathname"),
)
def update_demo(pathname):
    if pathname in ["/deck-explorer/", None, "/"]:
        return dash.no_update

    name = pathname.split("/")[-1]

    module = deck_modules[name]
    deck_component = module.app.layout
#    desc = " "
    desc = module.__doc__
    code = f"```\n{inspect.getsource(module)}\n```"
    code = "Parameter Setting Coming soon"

    end = dedent(
        
        f"""
    -----
    
    Application to show the Quality, Chances & Risks of the BZO's in Switzerland
    """)

    return deck_component, desc+end, code
