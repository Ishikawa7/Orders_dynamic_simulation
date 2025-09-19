import dash
import plotly.express as px
import pandas as pd
from dash import Dash, Input, Output, State, callback, html, dcc, dash_table
import dash_bootstrap_components as dbc
from system import Storage

storage = Storage()

dash.register_page(
    __name__,
    path='/',
    )
def create_app_layout():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H4("Demand stats"),
                                            # add line chart with demand over time
                                            dcc.Graph(id='demand-line', figure={}),
                                            # add bar chart with current demand
                                            dcc.Graph(id='current-demand-bar', figure={}),
                                            html.Hr(),
                                            html.H4("Log"),
                                            html.Div(id='log-container'),
                                        ]
                                    ),
                                ]
                            ),
                        ], width=6),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H4("Storage stats"),
                                            # add line chart with storage over time
                                            dcc.Graph(id='storage-line', figure={}),
                                            # add bar chart with current storage
                                            dcc.Graph(id='current-storage-bar', figure={}),
                                            # add bar chart with time to stockout
                                            dcc.Graph(id='time-to-stockout-bar', figure={}),
                                        ]
                                    ),
                                ]
                            ),
                        ], width=6),
                ]
            ),
            dcc.Interval(
                id='interval-component',
                interval=1*10000,  # in milliseconds
                n_intervals=0
            ),
        ],
        fluid=True,
    )

layout = create_app_layout

# create a callback to update the log
@callback(
    [
        Output('log-container', 'children'),
        Output('demand-line', 'figure'),
        Output('current-demand-bar', 'figure'),
        Output('storage-line', 'figure'),
        Output('current-storage-bar', 'figure'),
        Output('time-to-stockout-bar', 'figure'),
    ],
    Input('interval-component', 'n_intervals')
)
def update_log(n):
    global storage
    if 'storage' not in globals():
        storage = Storage()
    storage.run_simulation_step()
    
    # update log
    log_children = [html.P(entry) for entry in storage.log[-10:][::-1]]  # show last 10 log entries

    # update demand line chart
    demand_df = pd.DataFrame(storage.demand)
    demand_fig = px.line(demand_df, title='Demand Over Time', template='plotly_dark', line_shape='spline')

    # update current demand bar chart (use only the last value of each material)
    current_demand_fig = px.bar(demand_df.iloc[-1:], title='Current Demand', barmode='group', template='plotly_dark', text_auto=True)

    # update storage count line chart
    storage_count_df = pd.DataFrame(storage.storage_count)
    storage_fig = px.line(storage_count_df, title='Storage Over Time', template='plotly_dark')

    # update current storage bar chart (use only the last value of each material)
    current_storage_fig = px.bar(storage_count_df.iloc[-1:], title='Current Storage', barmode='group', template='plotly_dark', text_auto=True)

    # update time to stockout bar chart
    avg_m1 = sum(storage.storage['M1']) / len(storage.storage['M1']) if len(storage.storage['M1']) > 0 else 0
    avg_m2 = sum(storage.storage['M2']) / len(storage.storage['M2']) if len(storage.storage['M2']) > 0 else 0
    avg_m3 = sum(storage.storage['M3']) / len(storage.storage['M3']) if len(storage.storage['M3']) > 0 else 0
    storage_df = pd.DataFrame({
        'Material': ['M1', 'M2', 'M3'],
        'Hours to Stockout': [avg_m1, avg_m2, avg_m3]
    })
    storage_df.set_index('Material', inplace=True)
    storage_df = storage_df.rename(columns={'Hours to Stockout': 'AVG Hours to Stockout'})
    stockout_fig = px.bar(storage_df,
        title='Time to Stockout (in hours)',
        labels={'x': 'Material', 'y': 'AVG Hours to Stockout'}, template='plotly_dark', text_auto=True
    )

    return log_children, demand_fig, current_demand_fig, storage_fig, current_storage_fig, stockout_fig