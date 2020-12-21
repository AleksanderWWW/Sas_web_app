from flask import Flask, redirect, render_template

external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']
server = Flask(__name__)


@server.route('/')
def go_home():
    return redirect('/home/')


@server.route('/home/')
def index():
    return render_template('index.html')

########################################################################################################################


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import os

filename = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'data.csv')
df = pd.read_csv(filename, sep=',', encoding='UTF-8')

app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/', external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.Div(children=[html.A("Home", href="/home/")], style={'float': 'right', 'margin-right': '10%'}),
    html.Div(children=[
        html.H2(children='''
            Enter variable to graph:
        '''),
        html.Br(),
        dcc.Input(id='input', value='', type='text'),
        html.Button('Graph', id='submit-val', n_clicks=0),
        html.Br(),
        html.Div(id='output-graph'),
        html.Div(children=[
            html.H3("Available columns:"),
            html.P(",\n".join(df.columns),
                   className='container')])
], className='container')])


@app.callback(
    Output('output-graph', 'children'),
    [Input('submit-val', 'n_clicks'),
     State('input', 'value')]
    )
def update_value(n_clicks, input_data):
    try:
        s = df[input_data].describe().to_frame()
        s["stats"] = s.index
        s.rename(columns={input_data: "value"}, inplace=True)

        return html.Div(id="output-ok", children=[dcc.Graph(id="graph", figure=px.histogram(df,
                                                            x=input_data,
                                                            title=f"Histogram of variable '{input_data}'",
                                                            height=700,
                                                            width=1200)),
                                                  dash_table.DataTable(
                                                      id='table',
                                                      columns=[{"name": "stats", "id": "stats"},
                                                               {"name": "value", "id": "value"}],
                                                      data=s.to_dict("records")
                                                  ),
                                                  html.Br()
                                                  ]
                         )
    except (ValueError, KeyError):
        return html.Div(children=[
            html.Br(),
            html.P(id="error", children="Insert proper column name!", style={'color': 'red'})], className='container')


if __name__ == '__main__':
    app.run_server(debug=True)

