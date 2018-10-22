"""
Data structure for protein.
"""

from .res import Res


class Prot:
    """
    Data structure for proteins.

    Parameters
    ----------
    name: string
        Protein name.

    residues: dictionary of Res instances
        Residues of the protein. The dictionary must be built as:

            residues = {res_num: residue, ...}
                res_num : integer
                    Residue number as described in the PDB file.
                residue : Res instance
                    Residue data structure.

    align: list or tuple of tuples
        Alignment of template sequence and query sequence. Must be built as:

            align = [(query_res_nb_1, template_res_nb_2), ...]
                If a residue does not match, pair it with None.
    """

    def __init__(self: Prot, name: str, residues=dict(), align=None) -> None:
        self.name = name
        self.residues = residues
        self.align = align

    # String conversion
    def __str__(self: Prot) -> str:
        """
        Define string conversion.
        Used by print to represent the object.
        """
        return "{} : {}".format(self.name, self.residues)

    # Iterability implementation
    def __iter__(self: Prot):
        """
        Create an iterator.
        Iterate the residues of the protein.
        """
        list_res = list(self.residues.items())
        f_sort = (lambda x: x[0])
        list_res.sort(key=f_sort)
        return iter([x for i, x in list_res])

    # Operator overload
    def __getitem__(self: Prot, key: int) -> Res:
        """
        Overload the '[]' index operator.
        Access to the residue from its res_num.
        Return a residue or a list of residues.
        Warning ! the index start at 1 (like in the PDB file).
        """
        if isinstance(key, slice):
            max_res_num = max(self.residues.keys())
            idx = list(range(max_res_num + 1))
            return [self.residues[i] for i in idx[key]]
        else:
            if key < 0:
                key = len(self.residues) + key + 1
            return self.residues[key]

    def __setitem__(self: Prot, key: int, items) -> None:
        """
        Overload of item assignment.
        Set a residues or a list of residues.
        """
        if isinstance(key, slice):
            idx = list(range(key.stop))
            if len(idx[key]) != len(items):
                raise Exception(
                    'Not the same number of elements on both sides')
            for i, item in zip(idx[key], items):
                print(i)
                self.residues[i] = item
        else:
            if key < 0:
                key = len(self.residues) + key + 1
            self.residues[key] = items
