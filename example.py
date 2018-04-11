import buckinghampy
from buckinghampy.parameters import *

parameters = []

# Use to find the Reynolds number.
parameters.append([velocity, density, length, viscosity])

# Use to find Planck's exponential
parameters.append([speed_of_light, boltzmann, planck, temperature, frequency])

# Use to find the Rayleigh number.
parameters.append(
    [
        density,
        gravity,
        thermal_expansivity,
        temperature,
        length,
        thermal_diffusivity,
        viscosity,
    ]
)

# Use to find the Rayleigh number and alpha dt
parameters.append(
    [
        density,
        gravity,
        thermal_expansivity,
        temperature,
        length,
        thermal_conductivity,
        heat_capacity,
        viscosity,
    ]
)

# Use to find the Darcy number
parameters.append([hydraulic_permeability, length])

# Use to find the rotational convection numbers
parameters.append(
    [
        length,
        magnetic_permeability,
        kinematic_viscosity,
        velocity,
        length,
        electrical_conductivity,
        rotation_rate,
    ]
)

for parameter_set in parameters:
    nondimensional_numbers = buckinghampy.find_nondimensional_numbers(parameter_set)
    print('Finding nondimensional numbers...')
    for n in nondimensional_numbers:
        print(n)
