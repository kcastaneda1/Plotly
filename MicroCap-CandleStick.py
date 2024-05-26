#!/usr/bin/env python
# coding: utf-8


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import datetime
import plotly.express as px
from plotly.subplots import make_subplots


# load data and anlyze 
df = pd.read_csv('https://raw.githubusercontent.com/kcastaneda1/Plotly/main/MicroCapStockYrlyHistory.csv')

# convert date to date format
df['ref.date'] = pd.to_datetime(df['ref.date'])


# make copy
df2 = df.copy()


# create dashboard

app = Dash(__name__)
server = app.server


app.layout = html.Div([
    dcc.Dropdown(
        id = 'Stock_Dropdown',
        options = [{
            'label':i,
            'value':i
        } for i in df['ticker'].unique()
        ],style={'width': '40%'}),
    dcc.Graph(id = "Candle_Graph",style = {'height': '400'})
])



@app.callback(Output('Candle_Graph', 'figure'),
             [Input('Stock_Dropdown', 'value')])

def update_Ohlcgraph(selected_dropdown_value):
    dff = df[df['ticker'] == selected_dropdown_value]
    dff['MA20'] = dff['price.adjusted'].rolling(20).mean()
    dff['MA50'] = dff['price.adjusted'].rolling(50).mean()  

    OHLC = px.Candlestick(
        x = dff['ref.date'],
        open = dff['price.open'],
        high = dff['price.high'],
        low = dff['price.low'],
        close = dff['price.adjusted'],
        name = 'Candle Chart')
    
    MA20 = px.Scatter(
        x = dff['ref.date'],
        y = dff['MA20'],
        mode = 'lines',
        name = 'MA10',
        line=dict(color='purple', width=1))
    
    MA50 = px.Scatter(
        x = dff['ref.date'],
        y = dff['MA50'],
        mode = 'lines',
        name = 'EMA50',
        line=dict(color='orange', width=1))

    Volume = px.Bar(
        x = dff['ref.date'],
        y = dff['volume'],
        name = 'Volume')
        
    data = make_subplots(rows =2, cols =1, shared_xaxes = True, vertical_spacing = 0.1, row_width = [0.2,0.7])
        
    data.append_trace(OHLC,1,1)
    
    data.append_trace(MA20,1,1)
    data.append_trace(MA50,1,1)
    data.append_trace(Volume,2,1)
    
    data.update_layout(xaxis_rangeslider_visible = False)
    data.update_layout( height = 1200)

    
    return data


if __name__ == '__main__':
    app.run_server(debug = False)

