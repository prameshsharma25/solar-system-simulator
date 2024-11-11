import os
import numpy as np
import plotly.graph_objs as go

from typing import List, Dict
from dotenv import load_dotenv
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric_posvel

from distance import calculate_distances


load_dotenv()

def get_time_steps() -> List[Time]:
    start_time = Time(os.getenv("START_TIME"))
    end_time = Time(os.getenv("END_TIME"))
    num_steps = int(os.getenv("NUM_STEPS"))
    times = start_time + (end_time - start_time) * np.linspace(0, 1, num_steps)
    return list(times)

def get_planet_positions(planet_name: str, times: List[Time]) -> np.ndarray:
    positions = []
    with solar_system_ephemeris.set('builtin'):
        for time in times:
            pos, _ = get_body_barycentric_posvel(planet_name, time)
            positions.append([pos.x.to('AU').value, pos.y.to('AU').value, pos.z.to('AU').value])
    return np.array(positions)

def plot_orbits(planet_positions: Dict[str, np.ndarray], times: List[Time]):
    traces = []
    frames = []
    distances = calculate_distances(planet_positions)

    # add each planet to the plot
    for planet, positions in planet_positions.items():
        hover_texts = [f"{planet.capitalize()}<br>Distance from Sun: {dist:.2f} AU" for dist in distances[planet]]

        trace = go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2],
            mode='lines',
            name=planet.capitalize(),
            line=dict(width=2),
            text=hover_texts,
            hoverinfo="text",
        )
        traces.append(trace)

    # define each frame for animation
    for step, time in enumerate(times):
        frame_data = []
        for planet, positions in planet_positions.items():
            frame_trace = go.Scatter3d(
                x=[positions[step, 0]],
                y=[positions[step, 1]],
                z=[positions[step, 2]],
                mode='markers',
                marker=dict(size=4),
                name=planet.capitalize()
            )
            frame_data.append(frame_trace)

        frames.append(go.Frame(data=frame_data, name=f"Frame{step}", traces=list(range(len(planet_positions)))))

    # add the sun to the center
    sun_trace = go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=10, color='yellow'),
        name="Sun"
    )
    traces.append(sun_trace)

    layout = go.Layout(
        title="Animated Planetary Orbits in the Solar System",
        scene=dict(
            xaxis_title='X (AU)',
            yaxis_title='Y (AU)',
            zaxis_title='Z (AU)',
            aspectmode="auto",
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None, dict(frame=dict(duration=100, redraw=True), 
                                           fromcurrent=True)]),
                     dict(label="Pause",
                          method="animate",
                          args=[[None], dict(frame=dict(duration=0, redraw=True), 
                                             mode="immediate",
                                             fromcurrent=True)])]
        )],
        sliders=[dict(
            active=0,
            yanchor="top",
            xanchor="left",
            currentvalue=dict(prefix="Time: "),
            pad=dict(b=10, t=50),
            len=0.9,
            steps=[dict(method="animate",
                        label=str(time.iso),
                        args=[[f"Frame{step}"],
                              dict(mode="immediate",
                                   frame=dict(duration=100, redraw=True),
                                   transition=dict(duration=0))])
                   for step, time in enumerate(times)]
        )]
    )

    fig = go.Figure(data=traces, layout=layout, frames=frames)
    fig.show()