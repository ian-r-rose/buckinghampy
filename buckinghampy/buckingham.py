from __future__ import division
from __future__ import print_function

# Symbolic math probably works better for this 
# problem, and the matrix operations are never 
# going to be so large that it makes a difference
use_symbolic_math = True
try:
    import sympy
# Otherwise, try the numerical implementation
except ImportError:
    import numpy as np
    from scipy.linalg import svd
    from numpy.linalg import norm
    import scipy.optimize as opt
    use_symbolic_math = False

from fractions import Fraction

def _construct_dimension_matrix( parameters ):
    """
    Given a list of parameters, construct a dimensional matrix.
    The matrix is n_units by n_parameters, and the entries correspond
    to the exponent of a particular unit in a particular parameter
    """

    # create a set containing all the fundamental units
    # of the problems
    units = set()
    for p in parameters:
        for key in p.units:
            units.add(key)

    # sets are unordered, but we would like to 
    # alphebatize this so we know how to go between
    # the unit and the column of the dimension matrix
    # so we convert the set to a list and sort that
    units =list(units)
    units.sort()

    # Allocate the space for the dimension matrix
    if use_symbolic_math:
        dimension_matrix = sympy.zeros( len(units), len(parameters) )
    else:
        dimension_matrix = np.asmatrix( np.empty(shape=(len(units), len(parameters))))
    
    # now fill the dimension matrix
    for i,u in enumerate(units):
        for j,p in enumerate(parameters):
            entry = p.units[u] if u in p.units else 0. 
            dimension_matrix[i,j] = entry

    return units, dimension_matrix


def _calculate_dimensional_nullspace(dimensional_matrix):
    """
    Given a dimensional matrix, calculate the nullspace
    and return that. This is for use without symbolic math
    """
    eps = 1.e-4
 
    U, S, Vh = svd( dimensional_matrix )

    # The columns of V that correspond to small singular values
    # (or do not exist) are the left nullspace for the matrix.
    # select them, appropriately transpose them, and return them
    null_mask = ( np.append(S, np.zeros(len(Vh)-len(S))) <= eps)
    null_space = np.compress(null_mask, Vh, axis=0)

    null_space = np.transpose(null_space)
    return null_space

def _sparsify_basis ( basis ):
    """
    Parameters
    ----------
    basis: numpy array
        A 2D array correspnding to the basis, 
        with the columns corresponding to basis vectors.
   
    Returns
    -------
    new_basis: numpy array
        A 2D array correspnding to the attempt at a sparser basis, 
        with the columns corresponding to basis vectors.
    """
   
    eps = 1.e-4
    new_basis = basis.copy()
    n_cols = new_basis.shape[1]
    n_rows = new_basis.shape[0]

    # Okay, this is kind of ugly.  The idea is that we want to make a new basis by
    # making linear combinations of the old basis vectors, while attempting to 
    # minimize the L1 norm of the new basis vectors.  So we loop over each basis
    # vector and try to make a new one of all the vectors AFTER it in the list.
    # After this minimization is complete, we project that (now sparse) vector
    # out of the rest of them in a standard Gram-Schmidt way, and move on to the
    # next vector.  After all are done, we return the new basis.  

    #lambda function for computing L1 norm of a vector
    l1 = lambda x : np.sum( np.abs (x) )
 
    # Add a linear combination of all but the first column of B into
    # the first column of B, according to x
    combine = lambda B, x: np.dot( B, np.append( np.array([1.0,]), x) )
    
    #Loop over all the columns
    for i in range( n_cols ):

        #Find a linear combination of all the columns after the ith one that minimizes
        # the L1 norm of the ith column
        sp = opt.fmin( lambda x : l1(combine( new_basis[:, i:n_cols], x )), np.ones(n_cols-i-1), disp=0, xtol = eps)
        new_basis[:,i] = np.reshape(combine( new_basis[:, i:n_cols], sp), (n_rows,))
        new_basis[:,i] = new_basis[:,i]/norm(new_basis[:,i])

        #Now project that column out of all the others.
        for j in range (i+1, n_cols):
            new_basis[:,j] = new_basis[:,j] - np.dot(new_basis[:,i], new_basis[:,j])*new_basis[:,i]
            new_basis[:,j] = new_basis[:,j]/norm(new_basis[:,j])


    #Finally, there should now be a lot of near-zero entries in the new basis.
    #Explicitly zero them out.
    new_basis[ np.abs(new_basis) < eps ] = 0.
    return new_basis

def _rationalize_basis( basis ):
    """
    Given a basis with floating point numbers, attempt to convert them
    to rational numbers with low-value denominators.  Not particularly
    reliable, so doing this with symbolic math is preferable.
    """
    n_cols = basis.shape[1]

    rational_basis = []

    for i in range(n_cols):
        basis_vector = basis[:,i]
        min_val = np.amin(np.abs(basis_vector[np.nonzero(basis_vector)]))
        rational_basis_vector = [] 
        for entry in basis_vector:
            rational_basis_vector.append( Fraction( entry / min_val ).limit_denominator(16) )

        rational_basis.append(rational_basis_vector)

    return rational_basis

def _integrify_basis( basis ):
    """
    Take a vector basis with sympy.Rational in the entries,
    and scale them so they are all integers by finding the least
    common multiple of the denominators and multiplying by that.
    """

    def _gcd(a, b):
	"""Return greatest common divisor using Euclid's Algorithm."""
	while b:
	    a, b = b, a % b
	return a

    def _lcm(a, b):
	"""Return lowest common multiple."""
	return a * b // _gcd(a, b)

    def _lcmm(*args):
	"""Return lcm of args."""   
	return reduce(_lcm, args)

    #This is intended for lists of type sympy.Rational
    assert( use_symbolic_math )

    new_basis = []
    for vec in basis:
        #Make a list of the denominators
        denominators = [sympy.fraction(e)[1] for e in vec]
        #Find the least common multiple
        least_common_multiple = _lcmm( *denominators )
        #Multiply all the entries by that, make it a python Fraction object
        new_vec = [ Fraction( int(e*least_common_multiple), 1 ) for e in vec]
        new_basis.append(new_vec)

    return new_basis


def _parse_nondimensional_number( parameters, nondim ):
    """
    Turn a nondimensional number vector (which was the output of
    some nullspace calculation) and parse it into a LaTeX string.
    """

    numerator_values = ''
    denominator_values = ''

    for p,n in zip(parameters,nondim):
        if n == 0:
            continue #Do nothing if the parameter is not present in this number

        #If the exponent is one, we do not need to write it
        if n == 1 or n == -1:
            parsed_parameter = p.symbol
        #If the exponent is a whole number, we do not need to represent it as a fraction
        elif n.denominator == 1 or n.denominator == -1:
            parsed_parameter = p.symbol + '^{%i}'%(abs(n.numerator))
        #Otherwise, represent it as a fraction
        else:
            parsed_parameter = p.symbol + '^{%i/%i}'%(abs(n.numerator), abs(n.denominator))
        
        if n > 0: # The exponent is positive, put it in the numerator
            numerator_values = ' '.join( [numerator_values, parsed_parameter] )
        elif n < 0: #The exponent is negative, put it in the denominator
            denominator_values = ' '.join( [denominator_values,parsed_parameter])

    #If nothing is in the numerator, make it a one
    if numerator_values == '':
        parsed_number = '\\frac{1}{'+denominator_values+'}'
    #If nothing is in the denominator, no need to make it a fraction
    elif denominator_values == '':
        parsed_number = numerator_values
    #Otherwise, make a fraction of the numerator and denominator
    else:
        parsed_number = '\\frac{' + numerator_values + '}{'+denominator_values+'}'

    return parsed_number

def find_nondimensional_numbers( parameters ):
    """
    Given a list with entries of type buckinghampy.Parameter,
    find the set of nondimensional numbers which characterize that
    set.

    Parameters
    ----------
    parameters : list of buckinghampy.Parameter objects

    Returns
    -------
    nondimensional_numbers : a list of LaTeX ready strings
        which are a valid (but not necessarily unique)
        nondimensionalization of the problem
    """

    # Construct the matrix of dimensions
    units, dimension_matrix = _construct_dimension_matrix( parameters )

    # Sympy works better for this problem than doing it numerically,
    # so we prefer this (use_symbolic_math is true if we successfully
    # imported sympy)
    if use_symbolic_math:
        # Get the nullspace
        nullspace = dimension_matrix.nullspace()
        #Make all of the entries of the nullspace integers
        integrified_nullspace = _integrify_basis( nullspace )
        nondimensional_basis = integrified_nullspace #Rename
    else:
        # Get the nullspace
        nullspace = _calculate_dimensional_nullspace( dimension_matrix )
        # Make an attempt at making the nullspace sparser
        sparse_nullspace = _sparsify_basis(nullspace)
        #Make an attempt at turning the result into rational numbers
        rational_nullspace = _rationalize_basis(sparse_nullspace)
        nondimensional_basis = rational_nullspace # Rename

    # Parse the basis vectors of the nullspace into LaTeX strings
    nondimensional_numbers = []
    for nondim in nondimensional_basis:
        nondimensional_numbers.append( _parse_nondimensional_number( parameters, nondim ) )

    return nondimensional_numbers
