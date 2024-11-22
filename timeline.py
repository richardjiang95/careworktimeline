import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Load the processed dataset
data_path = 'top_topics_per_year.csv'  # Ensure this file is in the same directory as this script
top_topics_per_year = pd.read_csv(data_path)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout for the Dash app
app.layout = html.Div([
    html.H1("Interactive Timeline of Presentation Topics"),
    dcc.Graph(
        id='timeline',
        config={'displayModeBar': False}
    ),
    html.Div(id='hover-data', style={'marginTop': '20px'})
])

# Callback to update the timeline and hover information
@app.callback(
    [Output('timeline', 'figure'),
     Output('hover-data', 'children')],
    [Input('timeline', 'hoverData'),
     Input('timeline', 'clickData')]
)
def update_timeline(hover_data, click_data):
    # Create a line chart for timeline visualization
    fig = px.line(
        top_topics_per_year,
        x='Year',
        y='Count',
        color='Topics (L)',
        markers=True,
        title='Top 5 Topics Per Year',
        labels={'Count': 'Occurrences', 'Year': 'Year', 'Topics (L)': 'Topic'}
    )
    fig.update_traces(mode="lines+markers")
    fig.update_layout(hovermode='x unified')

    # Handle hover or click data to show top topics for a specific year
    year = None
    if hover_data:
        year = hover_data['points'][0]['x']
    elif click_data:
        year = click_data['points'][0]['x']
    
    if year is not None:
        topics_for_year = top_topics_per_year[top_topics_per_year['Year'] == int(year)]
        hover_content = [
            html.H3(f"Top Topics for {int(year)}:"),
            html.Ul([html.Li(f"{row['Topics (L)']}: {row['Count']} occurrences") for _, row in topics_for_year.iterrows()])
        ]
    else:
        hover_content = html.Div("Hover or click on a year to see the top 5 topics.")

    return fig, hover_content

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))  # Get PORT from environment or default to 8050
    app.run_server(debug=True, host='0.0.0.0', port=port)



