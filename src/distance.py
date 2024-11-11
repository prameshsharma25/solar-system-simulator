import numpy as np

from typing import Dict

def calculate_distances(planet_positions: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    distances = {}
    for planet, positions in planet_positions.items():
        distances[planet] = np.linalg.norm(positions, axis=1)
    return distances