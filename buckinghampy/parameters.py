class Parameter( object ):
    def __init__(self, symbol, units):
        self.units = units
        self.symbol = symbol

velocity = Parameter('u', {'m' :  1,\
                           's' : -1})

density = Parameter(u'\\rho', {'kg' :  1,\
                               'm'  : -3} )

length = Parameter('L', {'m' : 1} )

viscosity = Parameter( '\\eta', {'kg' :  1,\
                                 'm'  : -1,\
                                 's'  : -1} )

temperature = Parameter( 'T', {'K' : 1} )

thermal_expansivity = Parameter( '\\alpha', {'K' : -1 } )

thermal_conductivity = Parameter( 'k', {'kg' :  1,\
                                        'm'  :  1,\
                                        's'  : -3,\
                                        'K'  : -1} )

thermal_diffusivity = Parameter  ( '\\kappa', {'m' :  2 ,\
                                               's' : -1})

gravity = Parameter( 'g', {'m' :  1,\
                           's' : -2})

rotation_rate = Parameter( '\\Omega', {'s' :  -1} )

specific_heat = Parameter( 'c', {'m' :  2,\
                                 's' : -2,\
                                 'K' : -1} )

heat_capacity = specific_heat


pressure = Parameter( 'P', {'kg' :  1,\
                            'm'  : -1,\
                            's'  : -2} )

bulk_modulus = Parameter( 'K', {'kg' :  1,\
                                'm'  : -1,\
                                's'  : -2} )

compressibility = Parameter( '\\xi', {'kg' : -1,\
                                      'm'  :  1,\
                                      's'  :  2} )


debye_temperature = Parameter( '\\Theta_{D}', {'K' : 1} )

einstein_temperature = Parameter( '\\Theta_{E}', {'K' : 1} )


mass = Parameter( 'M', {'kg' : 1 } )

decay_time = Parameter( '\\tau', {'s' : 1 } )

speed_of_light = Parameter( 'c', {'m' :  1,\
                                  's' : -1} )

wavelength = Parameter('\\lambda' , {'m' :  -1})

frequency = Parameter('\\nu' , {'s' :  -1})

planck = Parameter('h',  {'m'  :  2,\
                          'kg' :  1,\
                          's'  : -1} )
boltzmann = Parameter('k_{B}',  {'m'  :  2,\
                                 'kg' :  1,\
                                 'K'  : -1,\
                                 's'  : -2} )

