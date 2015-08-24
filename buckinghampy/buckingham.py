from fractions import Fraction
import numpy as np
from scipy.linalg import svd
from numpy.linalg import norm
import scipy.optimize as opt



def construct_dimension_matrix( parameters ):

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
    dimension_matrix = np.asmatrix( np.empty(shape=(len(units), len(parameters))))
    
    # now fill the dimension matrix
    for i,u in enumerate(units):
        for j,p in enumerate(parameters):
            entry = p.units[u] if u in p.units else 0. 
            dimension_matrix[i,j] = entry

    return units, dimension_matrix


def calculate_dimensional_nullspace(dimensional_matrix):
    eps = 1.e-4
 
    U, S, Vh = svd( dimensional_matrix )

    # The columns of V that correspond to small singular values
    # (or do not exist) are the left nullspace for the matrix.
    # select them, appropriately transpose them, and return them
    null_mask = ( np.append(S, np.zeros(len(Vh)-len(S))) <= eps)
    null_space = np.compress(null_mask, Vh, axis=0)

    null_space = np.transpose(null_space)
    return null_space

def sparsify_basis ( basis ):
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

def rationalize_basis( basis ):
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

def parse_nondimensional_number( parameters, nondim ):
    numerator_values = ''
    denominator_values = ''
    

    for p,n in zip(parameters,nondim):
        if n == 0:
            continue

        if n == 1 or n == -1:
            parsed_parameter = p.symbol
        elif n.denominator == 1 or n.denominator == -1:
            parsed_parameter = p.symbol + '^{%i}'%(abs(n.numerator))
        else:
            parsed_parameter = p.symbol + '^{%i/%i}'%(abs(n.numerator), abs(n.denominator))
        
        if n > 0:
            numerator_values = ' '.join( [numerator_values, parsed_parameter] )
        elif n < 0:
            denominator_values = ' '.join( [denominator_values,parsed_parameter])


    if numerator_values == '':
        parsed_number = '\\frac{1}{'+denominator_values+'}'
    elif denominator_values == '':
        parsed_number = numerator_values
    else:
        parsed_number = '\\frac{' + numerator_values + '}{'+denominator_values+'}'

    return parsed_number

def find_nondimensional_numbers( parameters ):
    units, dimension_matrix = construct_dimension_matrix( parameters ) 
    nullspace = calculate_dimensional_nullspace( dimension_matrix )
    sparser_nullspace = sparsify_basis(nullspace)
    rational_nullspace = rationalize_basis( sparser_nullspace)

    nondimensional_numbers = []
    for nondim in rational_nullspace:
        nondimensional_numbers.append( parse_nondimensional_number( parameters, nondim ) )
    return nondimensional_numbers

