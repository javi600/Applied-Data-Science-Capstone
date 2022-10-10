# Import required libraries
import pandas as pd
import dash
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
df_total=spacex_df


sites=spacex_df["Launch Site"].unique().tolist()
sites.insert(0, "All Sites")
labels=[]
for i,pos in enumerate(sites):
    if pos=="All Sites":
        labels.append({'label': pos, 'value': "ALL"})
    else:
        labels.append({'label': pos, 'value': pos})


min_value=spacex_df["Payload Mass (kg)"].min()
max_value=spacex_df["Payload Mass (kg)"].max()

  

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                    options=labels,
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                value=[min_value, max_value]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
# Add computation to callback function and return graph
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        
        filtered_df = spacex_df
        dx=filtered_df.groupby('Launch Site')['class'].sum()
        dx1=dx.nlargest(len(dx)).reset_index(name='Count')
        fig = px.pie(dx1, values="Count", names='Launch Site', title='Total succes rate by sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        # return the outcomes piechart for a selected site
        dx = filtered_df.groupby(["class"]).size().reset_index(name='Count')
        fig = px.pie(dx, values="Count", names='class', title='Total succes launches for site '+entered_site)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    

# TASK 4:
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
# Add computation to callback function and return graph
def get_scatter_chart(entered_site,entered_payload):
    
    if entered_site == 'ALL':
        
        filtered_df = spacex_df
        # return the outcomes piechart for a selected site
        l=entered_payload
        filtered_df=filtered_df[(filtered_df['Payload Mass (kg)']>=l[0]) & (filtered_df['Payload Mass (kg)']<=l[1])]
        
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y="class", color='Booster Version Category')#,width=1450, height=605
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        # return the outcomes piechart for a selected site
        l=entered_payload
        filtered_df=filtered_df[(filtered_df['Payload Mass (kg)']>=l[0]) & (filtered_df['Payload Mass (kg)']<=l[1])]
        
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y="class", color='Booster Version Category')#,width=1450, height=605
        return fig

# Run the app
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8056)
