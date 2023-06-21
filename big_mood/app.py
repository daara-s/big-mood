import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc, Output, Input

df = pd.read_csv('data/daylio_cleaned.csv', parse_dates=["full_date"])

app = Dash(__name__)

YEAR = 2023

app.layout = html.Div([
    html.Div(children='Mood Data Dashboard'),
    html.P("Month:"),
    dcc.Dropdown(
        id='dropdown',
        options=sorted(df[df.full_date.dt.year == YEAR].full_date.dt.month.unique()),
        value=6,
        clearable=False,
    ),
    dcc.Graph(id='graph'),
])


@app.callback(
    Output("graph", "figure"),
    Input(component_id="dropdown", component_property="value")
)
def display_month(month: int) -> go.Figure:
    filtered_df = (df[
        (df['full_date'].dt.year == YEAR)
        & (df['full_date'].dt.month == month)])
    fig = px.line(filtered_df, x='full_date', y='mood_val_day_mean')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
