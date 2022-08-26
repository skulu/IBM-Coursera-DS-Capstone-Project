# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r'G:\My Drive\Courses\2022.05 Coursera - IBM Data Science Professional Certificate\10. Applied Data Science Capstone\spacex_launch_dash.csv')
    #r'D:\Skyler\Google Drive\Courses\2022.05 Coursera - IBM Data Science Professional Certificate\10. Applied Data Science Capstone\spacex_launch_dash.csv')
    #r'G:\My Drive\Courses\2022.05 Coursera - IBM Data Science Professional Certificate\10. Applied Data Science Capstone\spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options = [
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],
                                    value='ALL',
                                    placeholder='Select a launch site',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'), 
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        filtered_df = filtered_df.loc[filtered_df['Launch Site'] == entered_site]
        filtered_df['counter'] = 1
        filtered_df.sort_values(by='class', ascending=False, inplace=True)
        # fig = px.pie(filtered_df, values='counter', names='class', title=f'Total Success Launches for site {entered_site}')
        fig = go.Figure(data=[go.Pie(labels=filtered_df['class'], values=filtered_df['counter'], sort=False, title=f'Total Success Launches for site {entered_site}')])
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id='payload-slider', component_property='value')
)
def get_scatter_chart(site, payloadmass):
    filtered_df = spacex_df
    if site == 'ALL':
        filtered_df = filtered_df.loc[(filtered_df['Payload Mass (kg)'] <= payloadmass[1]) & (filtered_df['Payload Mass (kg)'] >= payloadmass[0])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title = 'Correlation between Payload and Success for all sites')
    else:
        filtered_df = filtered_df.loc[(filtered_df['Launch Site'] == site) & (filtered_df['Payload Mass (kg)'] <= payloadmass[1]) & (filtered_df['Payload Mass (kg)'] >= payloadmass[0])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title = f'Correlation between Payload and Success for site {site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
