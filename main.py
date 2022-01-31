import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_table
from dash.dependencies import Input, Output
import data_functions as functions

### DASHBOARD PAGES CREATION FUNCTIONS ###

def create_graph_line_home(data_society,graph_id):
    history = functions.min_max_history(data_society,coll_data)
    return  html.Div([dcc.Graph(id=data_society+graph_id,style={'width': '45vh', 'height': '45vh','display': 'inline-block'},
                         figure=px.line(title = data_society + " History",x=sorted(functions.graph_coordinates(data_society,coll_data)["x"]),
                         y=functions.graph_coordinates(data_society,coll_data)["y"],labels={"x":"Date","y":"Close/Last"})),
            html.Div([
                    dcc.Markdown('''
                    * Min_value : ''' + '''$''' +str(round(history["min"],2)) +  '''
                    * Average_value : ''' + '''$''' +str(round(history["avg"],2)) + '''
                    * Max_value : ''' + '''$''' +str(round(history["max"],2)))
                ])
            ],style={'width': '45vh', 'height': '45vh','display': 'inline-block'})

def create_page(data_society,article_society):
    article = functions.recup_article(article_society,coll_article)
    history = functions.min_max_history(data_society,coll_data)
    return [
                html.H1(data_society.replace("_"," "),
                        style={'textAlign':'center'}),
                dcc.Graph(id=data_society+'graph',
                         figure=px.line(x=sorted(functions.graph_coordinates(data_society,coll_data)["x"]),
                         y=functions.graph_coordinates(data_society,coll_data)["y"],labels={"x":"Date","y":"Close/Last"})),
                html.Div([
                    dcc.Markdown('''
                    * Min_value : ''' + '''$''' +str(round(history["min"],2)) +  '''
                    * Average_value : ''' + '''$''' +str(round(history["avg"],2)) + '''
                    * Max_value : ''' + '''$''' +str(round(history["max"],2)))
                ]),
                html.Div([
                    dash_table.DataTable(id="data_table",columns=[{"name":i,"id":i} for i in functions.mongo_to_df(coll_data.find({"Society":data_society}).sort([("Date",-1)])).columns],
                    data=functions.mongo_to_df(coll_data.find({"Society":data_society}).sort([("Date",1)])).to_dict('records'),page_size=10)
                ]),
                html.Div([
                    html.H1(article["title"]),
                    html.Div([
                    html.P(article['text']),
                    html.A(article['link'],href=article['link'])
                    ])
                ])
                ]



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "Projet Web scrapping e4 DSIA", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Apple", href="/page-1", active="exact"),
                dbc.NavLink("Activision_Blizzard", href="/page-2", active="exact"),
                dbc.NavLink("Amazon", href="/page-3", active="exact"),
                dbc.NavLink("Intel", href="/page-4", active="exact"),
                dbc.NavLink("Microsoft", href="/page-5", active="exact"),
                dbc.NavLink("Netflix", href="/page-6", active="exact"),
                dbc.NavLink("NVIDIA", href="/page-7", active="exact"),
                dbc.NavLink("Sanofi", href="/page-8", active="exact"),
                dbc.NavLink("Tesla", href="/page-9", active="exact"),
                dbc.NavLink("Texas_Instruments", href="/page-10", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Home',
                        style={'textAlign':'center'}),
                create_graph_line_home("Apple","_graph_1"),
                create_graph_line_home("Activision_Blizzard","_graph_1"),
                create_graph_line_home("Amazon","_graph_1"),
                create_graph_line_home("Intel","_graph_1"),
                create_graph_line_home("Microsoft","_graph_1"),
                create_graph_line_home("Netflix","_graph_1"),
                create_graph_line_home("NVIDIA","_graph_1"),
                create_graph_line_home("Sanofi","_graph_1"),
                create_graph_line_home("Tesla","_graph_1"),
                create_graph_line_home("Texas_Instruments","_graph_1"),
                ]
    elif pathname == "/page-1":
        return create_page("Apple","Apple")
    elif pathname == "/page-2":
        return create_page("Activision_Blizzard","Blizzard")
    elif pathname == "/page-3":
        return create_page("Amazon","Amazon")
    elif pathname == "/page-4":
        return create_page("Intel","Intel")
    elif pathname == "/page-5":
        return create_page("Microsoft","Microsoft")
    elif pathname == "/page-6":
        return create_page("Netflix","Netflix")
    elif pathname == "/page-7":
        return create_page("NVIDIA","Nvidia")
    elif pathname == "/page-8":
        return create_page("Sanofi","Sanofi")
    elif pathname == "/page-9":
        return create_page("Tesla","Tesla")
    elif pathname == "/page-10":
        return create_page("Texas_Instruments","Texas_instruments")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



if __name__=='__main__':
      
    functions.scrap()
    client = functions.new_mongoClient()
    db = client["nasdaq"]
    coll_data = db["history"]
    coll_article = db["article"]

    functions.data_traitments()
    functions.csv_to_mongodb(coll_data,"Datas/data.csv")
    functions.article_traitments(coll_article)
    
    app.run_server(debug=True, port=3000)
