""" A class representing a nondimensional number """

from fractions import Fraction

from typing import List, Dict


class Parameter(object):
    """
    A lightweight class representing a parameter.
    """

    def __init__(self, symbol: str, units: Dict[str, int]) -> None:
        self.units = units
        self.symbol = symbol


class NondimensionalNumber(object):
    """
    Class which represents a nondimensional number.
    You initialize it with the list of parameters used
    in a particular problem and the specific vector of 
    Fraction types that represents the power of each parameter
    in the nondimensional number.
    """

    def __init__(
        self, parameters: List[Parameter], nondimensional_vector: List[Fraction]
    ) -> None:
        self.parameters = parameters
        self.vector = nondimensional_vector
        self.string_representation = self._parse_nondimensional_number()

    def _parse_nondimensional_number(self) -> str:
        """
        Takes the list of parameters and the nondimensional number
        vector, and parses it into a string that may be typeset 
        with LaTeX
        """
        # Initialize two empty strings for the numerator and
        # denominator of the nondimensional number
        numerator_string = ""
        denominator_string = ""

        for p, n in zip(self.parameters, self.vector):
            # No need to typeset the parameters if they do not
            # appear in the nondimensional number
            if n == 0:
                continue

            # If the exponent on the parameter is one,
            # we do not need to write it.
            if n == 1 or n == -1:
                parsed_parameter = p.symbol
            # If the exponent is a whole number, we do
            # not need to represent it as a fraction.
            elif n.denominator == 1 or n.denominator == -1:
                parsed_parameter = p.symbol + "^{%i}" % (abs(n.numerator))
            # Otherwise, represent it as a fraction
            else:
                parsed_parameter = p.symbol + "^{%i/%i}" % (
                    abs(n.numerator), abs(n.denominator)
                )

            # Depending upon whether the exponent is positive or
            # negative, put it in the numerator or the denominator
            if n > 0:
                numerator_string = " ".join([numerator_string, parsed_parameter])
            elif n < 0:
                denominator_string = " ".join([denominator_string, parsed_parameter])

        # If the numerator is empty, make it a one
        if numerator_string == "":
            parsed_number = "\\frac{1}{" + denominator_string + "}"
        # If the denominator is empty, there is no need for a fraction
        elif denominator_string == "":
            parsed_number = numerator_string
        # Otherwise make it a fraction
        else:
            parsed_number = "\\frac{" + numerator_string + "}{" + denominator_string + "}"

        # And we are done! We return a LaTeX string
        return parsed_number

    # Let IPython know how this may be typeset with LaTeX

    def _repr_latex_(self) -> str:
        return "$$" + self.string_representation + "$$"

    # Return the string form of the nondimensional number

    def __str__(self) -> str:
        return self.string_representation


# This is a bit of a hack: Here I am subclassing
# the builtin Python list type and adding a
# function for print_latex(). This allows
# IPython to be able to render a list of
# nondimensional numbers as well as a single one.


class NondimensionalNumberList(list):
    # Make a comma delimited list of the
    # nondimensional numbers

    def __str__(self) -> str:
        string_representation = ""
        for n in range(len(self)):
            s = str(self.__getitem__(n))
            string_representation += s
            if n != len(self) - 1:
                string_representation += ", "
        return string_representation

    # Add symbols for typesetting with LaTeX

    def print_latex(self) -> str:
        return "$$" + self.__str__() + "$$"


# Register the print_latex function with IPython if we are using it
try:
    get_ipython().display_formatter.formatters["text/latex"].for_type(
        NondimensionalNumberList, NondimensionalNumberList.print_latex
    )
except:
    pass
