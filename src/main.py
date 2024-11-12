from orbit import get_time_steps, get_planet_positions, plot_orbits
from dash import Dash, dcc, html, Input, Output
from distance import calculate_distances


# Initialize the Dash app
app = Dash(__name__)

# Define layout with only the orbit plot and click data output (no interval for updates)
app.layout = html.Div([
    dcc.Graph(id='orbit-plot'),
    html.Div(id='output-click')
])

# Update the figure when the app starts (without periodic updates)
@app.callback(
    Output('orbit-plot', 'figure'),
    Input('orbit-plot', 'relayoutData')
)
def update_orbit_plot(_):
    times = get_time_steps()
    planets = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
    planet_positions = {planet: get_planet_positions(planet, times) for planet in planets}
    fig = plot_orbits(planet_positions, times)
    return fig

# Callback to display data on click
@app.callback(
    Output('output-click', 'children'),
    Input('orbit-plot', 'clickData')
)
def display_click_data(clickData):
    if clickData and "points" in clickData and clickData['points']:
        point = clickData['points'][0]
        if 'customdata' in point and len(point['customdata']) >= 5:
            planet, distance, x, y, z = point['customdata']
            return f"Planet: {planet.capitalize()}, Distance: {distance:.2f} AU, Position: ({x:.2f}, {y:.2f}, {z:.2f})"
    return "Click on a planet to see details."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
