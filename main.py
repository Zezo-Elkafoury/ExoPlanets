import pandas as pd
import streamlit as st

# Load the dataset
df = pd.read_csv('planets.csv')

def search_planet(stars=None, moons=None, disc_year=None, orbital_period=None, 
                  radius=None, mass=None, equilibrium_temp=None, 
                  solar_radius=None, solar_mass=None, rotational_velocity=None, 
                  distance=None, gaia_magnitude=None):
    
    # Fixed tolerances for approximate search
    orbital_period_tol = 20
    radius_tol = 1
    mass_tol = 500
    solar_radius_tol = 1
    solar_mass_tol = 0.1
    rotational_velocity_tol = 0.5
    distance_tol = 10
    gaia_magnitude_tol = 0.5
    
    conditions = []
    
    # Exact match for categorical fields (stars, moons, disc_year)
    if stars is not None and stars >= 0:
        conditions.append(df['stars'] == stars)
    if moons is not None and moons >= 0:
        conditions.append(df['moons'] == moons)
    if disc_year is not None and disc_year >= 1990:
        conditions.append(df['disc_year'] == disc_year)

    # Approximate matches for numerical fields with fixed tolerances
    if orbital_period is not None and orbital_period >= 0:
        conditions.append((df['orbital period'] >= orbital_period - orbital_period_tol) & 
                          (df['orbital period'] <= orbital_period + orbital_period_tol))
    if radius is not None and radius >= 0:
        conditions.append((df['radius'] >= radius - radius_tol) & 
                          (df['radius'] <= radius + radius_tol))
    if mass is not None and mass >= 0:
        conditions.append((df['mass'] >= mass - mass_tol) & 
                          (df['mass'] <= mass + mass_tol))
    if equilibrium_temp is not None and equilibrium_temp >= 0:
        conditions.append(df['equilibrium temp'] == equilibrium_temp)  # Exact match for now
    if solar_radius is not None and solar_radius >= 0:
        conditions.append((df['solar radius'] >= solar_radius - solar_radius_tol) & 
                          (df['solar radius'] <= solar_radius + solar_radius_tol))
    if solar_mass is not None and solar_mass >= 0:
        conditions.append((df['solar mass'] >= solar_mass - solar_mass_tol) & 
                          (df['solar mass'] <= solar_mass + solar_mass_tol))
    if rotational_velocity is not None and rotational_velocity >= 0:
        conditions.append((df['rotational velocity'] >= rotational_velocity - rotational_velocity_tol) & 
                          (df['rotational velocity'] <= rotational_velocity + rotational_velocity_tol))
    if distance is not None and distance >= 0:
        conditions.append((df['distance'] >= distance - distance_tol) & 
                          (df['distance'] <= distance + distance_tol))
    if gaia_magnitude is not None and gaia_magnitude >= 0:
        conditions.append((df['gaia magnitude'] >= gaia_magnitude - gaia_magnitude_tol) & 
                          (df['gaia magnitude'] <= gaia_magnitude + gaia_magnitude_tol))

    # Combine all conditions
    if conditions:
        combined_conditions = conditions[0]
        for condition in conditions[1:]:
            combined_conditions &= condition
        filtered_df = df[combined_conditions]
    else:
        filtered_df = df

    # Return results
    if not filtered_df.empty:
        return filtered_df['pl_name'].values
    else:
        return "No matching planets found"

# Streamlit app
st.title('Planet Search Engine')

# Input fields with default values
stars = st.number_input('Stars', min_value=0, max_value=10, value=0)
moons = st.number_input('Moons', min_value=0, value=0)
disc_year = st.number_input('Discovery Year', min_value=1990, max_value=2024, value=1990)
orbital_period = st.number_input('Orbital Period', min_value=0.0, value=0.0, format="%.2f")
radius = st.number_input('Radius', min_value=0.0, value=0.0, format="%.2f")
mass = st.number_input('Mass', min_value=0.0, value=0.0, format="%.2f")
equilibrium_temp = st.number_input('Equilibrium Temperature', min_value=0.0, value=0.0, format="%.2f")
solar_radius = st.number_input('Solar Radius', min_value=0.0, value=0.0, format="%.2f")
solar_mass = st.number_input('Solar Mass', min_value=0.0, value=0.0, format="%.2f")
rotational_velocity = st.number_input('Rotational Velocity', min_value=0.0, value=0.0, format="%.2f")
distance = st.number_input('Distance', min_value=0.0, value=0.0, format="%.2f")
gaia_magnitude = st.number_input('Gaia Magnitude', min_value=0.0, value=0.0, format="%.2f")

# Search button
if st.button('Search'):
    results = search_planet(stars=None if stars == 0 else stars, 
                            moons=None if moons == 0 else moons, 
                            disc_year=None if disc_year == 0 else disc_year, 
                            orbital_period=None if orbital_period == 0.0 else orbital_period, 
                            radius=None if radius == 0.0 else radius, 
                            mass=None if mass == 0.0 else mass, 
                            equilibrium_temp=None if equilibrium_temp == 0.0 else equilibrium_temp, 
                            solar_radius=None if solar_radius == 0.0 else solar_radius, 
                            solar_mass=None if solar_mass == 0.0 else solar_mass, 
                            rotational_velocity=None if rotational_velocity == 0.0 else rotational_velocity, 
                            distance=None if distance == 0.0 else distance, 
                            gaia_magnitude=None if gaia_magnitude == 0.0 else gaia_magnitude)
    if isinstance(results, str):
        st.write(results)
    else:
        st.write('Matching planets:')
        st.write(results)
