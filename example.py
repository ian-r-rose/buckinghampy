from __future__ import print_function

import buckinghampy
from buckinghampy.parameters import *

#parameters = [ velocity, density, length, viscosity] 
#parameters = [ speed_of_light, boltzmann, planck, temperature, frequency] 
#parameters = [ density, gravity, thermal_expansivity, temperature, length, thermal_diffusivity, viscosity]
#parameters = [ density, gravity, thermal_expansivity, temperature, length, thermal_conductivity, heat_capacity, viscosity]
#parameters = [hydraulic_permeability, length]
parameters = [ length, magnetic_permeability, kinematic_viscosity, velocity, length, electrical_conductivity, rotation_rate]

nondimensional_numbers = buckinghampy.find_nondimensional_numbers( parameters ) 
for n in nondimensional_numbers:
    print(n)
