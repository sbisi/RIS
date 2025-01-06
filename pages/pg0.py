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


# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='KPI',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='Real Estate Platform'
)



#dash.register_page(__name__, name='BZO Kantone')


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

tab_style = {"height": "calc(100vh - 330px)", "padding": "15px"}
# tab_style = {'max-height': 'calc(100vh - 210px)'}
tabs = dbc.Tabs(
    [
        dbc.Tab(dcc.Markdown(id="description", style=tab_style), label="Description"),
        dbc.Tab(dcc.Markdown(id="source-code", style=tab_style), label="Parameters"),
    ]
)

Variable1= "Analyse der BZO"

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

layout = [
    html.H1("Quality Check BZO-Data", style={'font-family': 'Verdana, sans-serif', 'font-size': '24px'}),
    html.Br(),
    dcc.Location(id="url", refresh=False),
    dbc.Row(
        [
            dbc.Col(
                [dbc.Card(
                    id="deck-card", 
#                    style={"height": "calc(100vh - 110px)"},    #calc 100vh means 100% of the screen until 110% of the picture
                    style={"height": "calc(100vh)"},    #calc 100vh means 100% of the screen until 110% of the picture
                    body=True,
                ),
                html.I("(c) Dr. Peter Staub, pom+Group AG, peter.staub@pom.ch", style={'align':'center', 'font-size':12})],
                md=8,
            ),      
            # dbc.Col([app_selection, tabs,html.I("(c) Peter Staub)", style={'align':'center', 'font-size':12})], md=4),
            
#            dbc.Col([
#                app_selection, 
#                tabs,
#                (html.B("Analyse der BZO der Schweiz", 
#                style={"color":"white","height": "50px", "width": "600px",'align':'center', 'font-size':20,"padding": "0px"})),
#                (html.Br()),
#                (html.B("pom+HSLU", 
#                style={"color":"black",'background-color':'white',"height": "50px", "width": "600px",'align':'center', 'font-size':40, "padding": "0px"})),
#             ], 
#             md=4),
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
    desc = module.__doc__
#    code = f"```\n{inspect.getsource(module)}\n```"
    code = "Parameter Setting Coming soon"

    end = dedent(
        
        f"""
    -----
    
    Application to show, simulate & optimize CO2 pollution from buildings in Switzerland.
    """)

    return deck_component, desc+end, code
