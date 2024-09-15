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

# Input fields with default inclusion
include_stars = st.checkbox('Include Stars', value=True)
stars = st.number_input('Stars', value=0) if include_stars else None

include_moons = st.checkbox('Include Moons', value=True)
moons = st.number_input('Moons', value=0) if include_moons else None

include_disc_year = st.checkbox('Include Discovery Year', value=True)
disc_year = st.number_input('Discovery Year', max_value=2024, value=1990) if include_disc_year else None

include_orbital_period = st.checkbox('Include Orbital Period', value=True)
orbital_period = st.number_input('Orbital Period', value=78052) if include_orbital_period else None

include_radius = st.checkbox('Include Radius', value=True)
radius = st.number_input('Radius', value=6) if include_radius else None

include_mass = st.checkbox('Include Mass', value=True)
mass = st.number_input('Mass', value=437) if include_mass else None

include_equilibrium_temp = st.checkbox('Include Equilibrium Temperature', value=True)
equilibrium_temp = st.number_input('Equilibrium Temperature', value=912) if include_equilibrium_temp else None

include_solar_radius = st.checkbox('Include Solar Radius', value=True)
solar_radius = st.number_input('Solar Radius', value=2) if include_solar_radius else None

include_solar_mass = st.checkbox('Include Solar Mass', value=True)
solar_mass = st.number_input('Solar Mass', value=1) if include_solar_mass else None

include_rotational_velocity = st.checkbox('Include Rotational Velocity', value=True)
rotational_velocity = st.number_input('Rotational Velocity', value=6) if include_rotational_velocity else None

include_distance = st.checkbox('Include Distance', value=True)
distance = st.number_input('Distance', value=696) if include_distance else None

include_gaia_magnitude = st.checkbox('Include Gaia Magnitude', value=True)
gaia_magnitude = st.number_input('Gaia Magnitude', value=12) if include_gaia_magnitude else None

# Search button
if st.button('Search'):
    results = search_planet(stars=stars, 
                            moons=moons, 
                            disc_year=disc_year, 
                            orbital_period=orbital_period, 
                            radius=radius, 
                            mass=mass, 
                            equilibrium_temp=equilibrium_temp, 
                            solar_radius=solar_radius, 
                            solar_mass=solar_mass, 
                            rotational_velocity=rotational_velocity, 
                            distance=distance, 
                            gaia_magnitude=gaia_magnitude)
    if isinstance(results, str):
        st.write(results)
    else:
        st.write('Matching planets:')
        st.write(results)
