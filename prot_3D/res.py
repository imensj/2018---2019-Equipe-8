"""
Data structure for residues.
"""

from .atom import Atom


class Res:
    """
    Data structure for residues.

    Parameters
    ----------
    res_num: scalar value
        Residue number as described in the PDB file.

    res_name: string
        Residue name. Use 3-letters code.

    atoms: dictionary of Atom instances
        Atoms of the residue. The dictionary must be built as :

            atoms = {atom_name: atom, ...}
                atom_name: string
                    Atom name as described in the PDB file (For example : 'CA'
                    for carbon alpha).
                atom: Atom instance
                    Atom data structure.
    """

    def __init__(
            self: 'Res',
            res_num: int,
            res_name: str,
            curres=None,
            atoms=None
            ) -> None:
        self.res_num = res_num
        self.res_name = res_name
        self.curres = curres
        if atoms is None:
            self.atoms = dict()
        else:
            self.atoms = atoms

    def iteratoms(self: 'Res'):
        """
        Iterate on atom names and atoms
        """
        return self.atoms.items()

    # String conversion
    def __str__(self: 'Res') -> str:
        """
        Define string conversion.
        Used by print to represent the object.
        """
        return "{} (n°{}) : {}".format(
            self.res_name, self.res_num, self.atoms)

    # Iterability implementation
    def __iter__(self: 'Res'):
        """
        Create an iterator.
        Iterate the atoms of the residue.
        """
        return iter(list(self.atoms.values()))

    # Operator overload
    def __getitem__(self: 'Res', key: int) -> Atom:
        """
        Overload the '[]' index operator.
        Access an atom by its atom_name.
        """
        return self.atoms[key]

    def __setitem__(self: 'Res', key: int, item: Atom) -> None:
        """
        Overload of item assignment.
        Set an atom.
        """
        self.atoms[key] = item

    def __contains__(self: 'Res', key: str) -> bool:
        """
        Overload of 'in' operator.
        Search if the key is contains in the atoms dictionary.
        """
        return key in self.atoms

