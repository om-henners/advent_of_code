#!/usr/bin/env python
"""
Solution 2

Just run the maachine for a while?
"""
from functools import partial
import math
from typing import TextIO, Union, Dict, List, Tuple

import parse
from scipy.optimize import minimize_scalar


class FuelConverter:
    """A fuel converter.

    Parsess all the recipes, then provides access methods for every data type
    """

    def __init__(self, file: Union[TextIO, str]):
        """Create the fuel converter.

        Requires a file-like object (or path) that contains the recipes
        """
        # store the current resource stocks
        self.current_stock: Dict[str, int] = {}
        # store all the required precursors and quantities
        self.formulas: Dict[str, Dict[str, Union[int, Tuple[str, int]]]] = {}
        self.used_ore = 0
        self._parse_recipes(file)

    def _parse_recipes(self, file: Union[TextIO, str]):
        """Do the work of parsing the input file

        Recipes in the file are expected to be in the form:

        10 ORE => 10 A
        1 ORE => 1 B
        7 A, 1 B => 1 C
        7 A, 1 C => 1 D
        7 A, 1 D => 1 E
        7 A, 1 E => 1 FUEL

        Where the output of the process on the right uses the
        quantities of precursors on the left.
        """
        if isinstance(file, str):
            file = open(file)

        pattern = parse.compile('{quantity:d} {chemical:3.4l}')

        for line in file:
            precursors, product = line.split('=>')

            parse_result = pattern.search(product)

            # now initialse all the bits:
            self.current_stock[parse_result['chemical']] = 0
            self.formulas[parse_result['chemical']] = {
                'produced': parse_result['quantity'],
                'precursors': []
            }

            for pr in pattern.findall(precursors):
                self.formulas[parse_result['chemical']]['precursors'].append(
                    (pr['chemical'], pr['quantity'])
                )

    def ORE(self, n):
        """
        Get some amount of ore from the rings of Saturn.
        """
        self.used_ore += n

    def get_resource(self, resource, n):
        """
        Gets some number of a particular resource
        """
        if self.current_stock[resource] < n:

            units_to_produce = math.ceil((n - self.current_stock[resource]) / self.formulas[resource]['produced'])

            for precursor, quantity in self.formulas[resource]['precursors']:
                p = getattr(self, precursor)
                p(quantity * units_to_produce)
            self.current_stock[resource] += self.formulas[resource]['produced'] * units_to_produce

        self.current_stock[resource] -= n

    def __getattr__(self, attr):
        """
        Called when the object type isn't explicitly defined
        """
        return partial(self.get_resource, attr)

    def stores_at_zero(self):
        """Check if there are exactly 0 left in the stores"""
        return sum(self.current_stock.values()) == 0


def ore_for_fuel(fuel: int):
    """Given some amount of fuel get the absolute difference between 1 trillian and used fuel"""
    fuel_converter = FuelConverter('input')
    fuel_converter.FUEL(fuel)
    return abs(1_000_000_000_000 - fuel_converter.used_ore)


def main():

    res = minimize_scalar(ore_for_fuel, bounds=(1_000_000, 10_000_000), method='bounded')
    candidate_fuel = round(res.x)

    fuel_converter = FuelConverter('input')
    fuel_converter.FUEL(candidate_fuel)

    if fuel_converter.used_ore > 1_000_000_000_000:
        candidate_fuel -= 1

    print('fuel used', int(candidate_fuel))


if __name__ == '__main__':
    main()
