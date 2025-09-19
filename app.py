import dash
import pandas as pd
from dash import Dash, Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc
import dash_auth

# only for development
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'password',
    'peppe': 'peppe',
}

# css file for dash components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
# LOAD DATA #############################################################################################################

# DASH APP ##############################################################################################################
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, dbc_css]) #suppress_callback_exceptions=True

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

def create_app_layout():
    return dbc.Container(
        [
            dbc.NavbarSimple(
                id = "navbar",
                children=[
                    dbc.NavItem(dbc.NavLink("HOME", href="/", style={'font-size': '15px'})),
                    dbc.NavItem(dbc.NavLink("Guide", href="/guide", style={'font-size': '15px'})),
                    #dropdown menu with links
                    dbc.DropdownMenu(
                        nav=True,
                        in_navbar=True,
                        label="Pages",
                        children=[
                        ],
                    ),
                    html.Div(style={'display': 'inline-block', 'width': '35px'}),
                ],
                brand="Dynamic Order Simulation",
                brand_href="/",
                color="#1E1E1E",
                dark=True,
            ),
            html.Hr(),
    	    dash.page_container,
            # add a footer
            html.Br(),
            html.Hr(),
        ],
        fluid=True,
    )

app.layout = create_app_layout

# RUN THE APP ###########################################################################################################
if __name__ == "__main__":
    # shut down any running dash processes if necessary
    #import os
    #os.system("taskkill /f /im python.exe")
    
    # start the dash app
    #app.run_server(host='0.0.0.0', port=8080, debug=False, use_reloader=False) # for production
    app.run(debug=True, use_reloader=True, port=8080) # for development
    

# if Python [Errno 98] Address already in use: "kill -9 $(ps -A | grep python | awk '{print $1}')"