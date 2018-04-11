""" Workhorse functions for buckinghampy """

from typing import List, Tuple, Any
from fractions import Fraction
from functools import reduce

import sympy

# Local imports
from .nondimensional import NondimensionalNumber, NondimensionalNumberList
from .parameters import Parameter


def _construct_dimension_matrix(parameters: List[Parameter]) -> Tuple[List[str], Any]:
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
    unit_list = list(units)
    unit_list.sort()

    # Allocate the space for the dimension matrix
    dimension_matrix = sympy.zeros(len(unit_list), len(parameters))

    # now fill the dimension matrix
    for i, u in enumerate(unit_list):
        for j, p in enumerate(parameters):
            entry = p.units[u] if u in p.units else 0
            dimension_matrix[i, j] = entry

    return unit_list, dimension_matrix


def _integrify_basis(basis: Any) -> Any:
    """
    Take a vector basis with sympy.Rational in the entries,
    and scale them so they are all integers by finding the least
    common multiple of the denominators and multiplying by that.
    """

    def _gcd(a: int, b: int):
        """Return greatest common divisor using Euclid's Algorithm."""
        while b:
            a, b = b, a % b
        return a

    def _lcm(a: int, b: int) -> int:
        """Return lowest common multiple."""
        return a * b // _gcd(a, b)

    def _lcmm(*args: int) -> int:
        """Return lcm of args."""
        return reduce(_lcm, args)

    new_basis = []
    for vec in basis:
        # Make a list of the denominators
        denominators: List[int] = [sympy.fraction(e)[1] for e in vec]
        # Find the least common multiple
        least_common_multiple = _lcmm(*denominators)
        # Multiply all the entries by that, make it a python Fraction object
        new_vec = [Fraction(int(e * least_common_multiple), 1) for e in vec]
        new_basis.append(new_vec)

    return new_basis


def find_nondimensional_numbers(
    parameters: List[Parameter]
) -> NondimensionalNumberList:
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
    units, dimension_matrix = _construct_dimension_matrix(parameters)

    # Get the nullspace
    nullspace = dimension_matrix.nullspace()
    # Make all of the entries of the nullspace integers
    nondimensional_basis = _integrify_basis(nullspace)

    # Parse the basis vectors of the nullspace into LaTeX strings
    nondimensional_numbers = NondimensionalNumberList(
        [NondimensionalNumber(parameters, n) for n in nondimensional_basis]
    )

    return nondimensional_numbers
