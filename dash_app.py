import dash
from dash import html, dcc, Output, Input
import pandas as pd
import plotly.express as px
import os

def load_sales_data():
    files = ['daily_sales_data_0.csv', 'daily_sales_data_1.csv', 'daily_sales_data_2.csv']
    dataframes = []

    for file in files:
        if os.path.exists(file):
            df = pd.read_csv(file, parse_dates=['date'])
            dataframes.append(df)
        else:
            print(f"File not found: {file}")

    combined = pd.concat(dataframes)

    pink_df = combined[combined['product'].str.lower() == 'pink morsel'].copy()

    pink_df['price'] = pink_df['price'].replace('[\$,]', '', regex=True).astype(float)

    pink_df['revenue'] = pink_df['price'] * pink_df['quantity']

    return pink_df

sales_df = load_sales_data()

app = dash.Dash(__name__)
app.title = "Soul Foods Sales Visualizer"

app.layout = html.Div([
    html.H1("Soul Foods Sales Visualizer", style={
        'textAlign': 'center',
        'color': '#ffffff',
        'backgroundColor': '#5D3FD3',
        'padding': '20px',
        'borderRadius': '10px'
    }),

    html.Div([
        html.P("Visualizing the impact of the Pink Morsel price increase on January 15, 2021.",
               style={'fontSize': '16px'}),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            labelStyle={'display': 'inline-block', 'margin': '10px', 'fontWeight': 'bold'}
        ),
        dcc.Graph(id='sales-graph', config={'displayModeBar': False})
    ], style={
        'backgroundColor': '#f8f9fa',
        'padding': '20px',
        'margin': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    })
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#eef2f7', 'minHeight': '100vh'})


@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-filter', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = sales_df
    else:
        filtered_df = sales_df[sales_df['region'].str.lower() == selected_region]

    daily_revenue = filtered_df.groupby('date')['revenue'].sum().reset_index()

    fig = px.line(daily_revenue, x='date', y='revenue',
                  title=f'Pink Morsel Sales Over Time - {selected_region.capitalize()} Region' if selected_region != 'all' else 'Pink Morsel Sales Over Time',
                  labels={'date': 'Date', 'revenue': 'Total Revenue ($)'},
                  template='plotly_white')

    fig.add_vline(x='2021-01-15', line_dash='dash', line_color='red',
                  annotation_text='Price Increase', annotation_position='top right')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
