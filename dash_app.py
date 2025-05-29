import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import os

# Load and prepare the data
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

    # Filter only Pink Morsel
    pink_df = combined[combined['product'].str.lower() == 'pink morsel'].copy()

    # Clean and convert price
    pink_df['price'] = pink_df['price'].replace('[\$,]', '', regex=True).astype(float)

    # Compute revenue
    pink_df['revenue'] = pink_df['price'] * pink_df['quantity']

    # Group by date
    daily_revenue = pink_df.groupby('date')['revenue'].sum().reset_index()
    return daily_revenue.sort_values('date')

# Prepare data
sales_df = load_sales_data()

# Build the chart
fig = px.line(sales_df, x='date', y='revenue', title='Pink Morsel Sales Over Time',
              labels={'date': 'Date', 'revenue': 'Total Revenue ($)'})

# Add vertical line for Jan 15, 2021
fig.add_vline(x='2021-01-15', line_dash='dash', line_color='red',
              annotation_text='Price Increase', annotation_position='top right')

# Create the Dash app
app = dash.Dash(__name__)
app.title = "Soul Foods Sales Visualizer"

app.layout = html.Div([
    html.H1("Soul Foods Sales Visualizer", style={'textAlign': 'center'}),

    html.Div([
        html.P("Visualizing the impact of the Pink Morsel price increase on January 15, 2021."),
        dcc.Graph(figure=fig)
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
