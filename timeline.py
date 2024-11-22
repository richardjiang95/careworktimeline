import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the processed dataset
data_path = 'top_topics_per_year.csv'  
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
    [Input('timeline', 'hoverData')]
)
def update_timeline(hover_data):
    # Create a bar chart for timeline visualization
    fig = px.bar(
        top_topics_per_year,
        x='Year',
        y='Count',
        color='Topics (L)',
        title='Top 5 Topics Per Year',
        labels={'Count': 'Occurrences', 'Year': 'Year'}
    )
    fig.update_layout(barmode='stack', hovermode='x unified')

    # Handle hover data to show top topics for a specific year
    if hover_data:
        year = hover_data['points'][0]['x']
        topics_for_year = top_topics_per_year[top_topics_per_year['Year'] == int(year)]
        hover_content = [
            html.H3(f"Top Topics for {int(year)}:"),
            html.Ul([html.Li(f"{row['Topics (L)']}: {row['Count']} occurrences") for _, row in topics_for_year.iterrows()])
        ]
    else:
        hover_content = html.Div("Hover over a year to see the top 5 topics.")

    return fig, hover_content

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
