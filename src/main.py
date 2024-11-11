from orbit import get_time_steps, get_planet_positions, plot_orbits


def main():
    times = get_time_steps()

    planets = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
    planet_positions = {planet: get_planet_positions(planet, times) for planet in planets}
    plot_orbits(planet_positions, times)


if __name__ == "__main__":
    main()