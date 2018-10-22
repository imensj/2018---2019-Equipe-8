"""
Data structure for atoms.
"""

import numpy as np # pyre-ignore
import copy

class Atom:
    """
    Data structure for atoms.

    Parameters
    ----------
    x, y, z: scalar values
        Cartesian coordinates of the atom.

    element: string
        Chemical element symbol.

    atom_num: integer
        Atom number in the PDB file.
    """

    def __init__(self: Atom, x: float, y: float, z: float, element: str, atom_num: int) -> None:
        self.coord = np.array([x, y, z])
        self.element = element
        self.atom_num = atom_num

    # String conversion
    def __str__(self: Atom) -> str:
        """
        Define string conversion.
        Used by print to represent the object
        """
        return "{} (n°{}) : {}".format(
                self.element, self.atom_num, self.coord)

    # Operator overload
    def __add__(self: Atom, other: Atom) -> Atom:
        """
        Overload of '+' operator.
        """
        if type(other) is Atom:
            return self.coord + other.coord
        elif type(other) is np.ndarray:
            new = copy.deepcopy(self)
            new.coord = new.coord + other
            return new
        elif type(other) is list:
            new = copy.deepcopy(self)
            new.coord = new.coord + np.array(other)
            return new
        else:
            raise Exception("Addition not implemented for this type")

    def __sub__(self: Atom, other) -> Atom:
        """
        Overload of '-' operator.
        """
        if type(other) is Atom:
            return self.coord - other.coord
        elif type(other) is np.ndarray:
            return self.__add__(-other)
        elif type(other) is list:
            return self.__add__(- np.array(other))
        else:
            raise Exception("Addition not implemented for this type")