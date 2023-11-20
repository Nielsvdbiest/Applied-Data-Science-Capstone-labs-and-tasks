import dash
from dash import dcc, html

# Sample launch site names
launch_site_names = ['CCAFS LC-40', 'CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E']

# Create a Dash app
app = dash.Dash(__name__)

# Define layout with a dropdown for launch sites
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site_name in launch_site_names:
    dropdown_options.append({'label': site_name, 'value': site_name})

app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    )
])

# Callback function to render the pie chart based on selected launch site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, values='class', names='class', title=f'Success/Failure at {entered_site}')
        return fig

# Sample min and max payload values
min_payload = 0
max_payload = 10000

# Define layout with a range slider for payload selection
app.layout = html.Div([
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    html.Div(id='output-container-range-slider')
])

# Callback function to render the scatter plot based on selected launch site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, selected_payload):
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['PayloadMass'] >= selected_payload[0]) & (spacex_df['PayloadMass'] <= selected_payload[1])]
        fig = px.scatter(filtered_df, x='PayloadMass', y='class', color='BoosterVersion', title='Payload vs. Mission Outcome (All Sites)')
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['LaunchSite'] == selected_site) & (spacex_df['PayloadMass'] >= selected_payload[0]) & (spacex_df['PayloadMass'] <= selected_payload[1])]
        fig = px.scatter(filtered_df, x='PayloadMass', y='class', color='BoosterVersion', title=f'Payload vs. Mission Outcome at {selected_site}')
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)