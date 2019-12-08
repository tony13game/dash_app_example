
#!/usr/bin/env python
# coding: utf-8
# In[2]:
#Here's a quick example
#if you dont stop it it will keep running(?)

# scatter plot + Linear plot
#Final Homework
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df = pd.read_csv('nama_10_gdp_1_Data.csv')

available_indicators = df['NA_ITEM'].unique()
unit_item=df['UNIT'].unique()
country_indicators = df['GEO'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Imports of goods'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            dcc.RadioItems(
                id='value_format',
                options=[{'label': i, 'value': i} for i in unit_item],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),

 html.Hr(),
      html.Div([

        html.Div([
            dcc.Dropdown(
                id='country-value',
                options=[{'label': i, 'value': i} for i in country_indicators],
                value='European Union - 28 countries'
            ),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Imports of goods'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
             dcc.RadioItems(
                id='value_format',
                options=[{'label': i, 'value': i} for i in unit_item],
                value='Chain linked volumes, index 2010=100',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(id='lineplot_graphic')  

])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('value_format', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,value_format,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]  #filter the year
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
@app.callback(
    dash.dependencies.Output('lineplot_graphic', 'figure'),
    [dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('country-value', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('value_format', 'value')])
def update_graph1(yaxis_column_name, country_value, yaxis_type,
                 value_format):
    dff = df[(df['GEO'] == country_value) & (df['UNIT'] == value_format) & (df['NA_ITEM'] == yaxis_column_name)] #filter the year
    
    return {
        'data': [go.Scatter(
            x=dff.TIME,
            y=dff.Value,
            text=dff.GEO,
            mode='lines'
        )],
        'layout': go.Layout(
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
    
