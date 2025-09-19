# IMPORT LIBRARIES #####################################################################################################
import dash
from dash import dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/guide',
    )

layout = dbc.Container(
    [
        # markdown
        dcc.Markdown('''
            ## Dashboard Functionality Guide
            
            Welcome to our dashboard! This guide is designed to help you navigate and utilize the various functionalities of our dashboard effectively. Whether you're a newcomer or a seasoned user, this guide will walk you through the key features and tools available to make the most out of your dashboard experience.
            
            ### 1. Overview
               - **Purpose**: Briefly explain the purpose and objectives of the dashboard.
               - **Audience**: Identify the target audience for the dashboard and their primary needs.
               - **Key Metrics**: Highlight the main metrics and data points tracked on the dashboard.
            
            ### 2. Navigation
               - **Layout**: Provide an overview of the dashboard layout and organization.
               - **Sections**: Explain the different sections or tabs available and what each contains.
               - **Menus and Buttons**: Familiarize users with navigation menus and buttons for seamless exploration.
            
            ### 3. Interactivity
               - **Filters**: Explain how to use filters to customize the data displayed based on specific criteria.
               - **Drill-Down**: Describe how users can drill down into more detailed information by clicking on data points.
               - **Hover-over Information**: Highlight any interactive features that provide additional information when hovered over.
            
            ### Conclusion
            Thank you for using our dashboard functionality guide. We hope this resource enhances your experience and enables you to derive valuable insights from our data. If you have any questions or feedback, please don't hesitate to reach out to our support team.
            
                    
                    
        '''),
    ],
)

# Pagina della guida in markdown