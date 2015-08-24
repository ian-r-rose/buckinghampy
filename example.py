import buckinghampy
from buckinghampy.parameters import *

#parameters = [ velocity, density, length, viscosity] 
#parameters = [ speed_of_light, boltzmann, planck, temperature, frequency] 
parameters = [ density, gravity, thermal_expansivity, temperature, length, thermal_diffusivity, viscosity]
nondimensional_numbers = buckinghampy.find_nondimensional_numbers( parameters ) 
for n in nondimensional_numbers:
    print n
