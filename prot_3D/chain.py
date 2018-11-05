"""
Data structure for protein.
"""

from .res import Res
from .convert_aa import three2one

class Chain:
    """
    Data structure for proteins.

    Parameters
    ----------
    chain_name: string
        Chain name.

    prot_name: string
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

            align = [(query_res_1letter_code, template_res_nb_2), ...]
                If a residue does not match, pair it with None.
    """

    def __init__(
            self: 'Chain',
            chain_name: str,
            prot_name: str,
            residues=None,
            align=None
            ) -> None:
        if residues is None:
            residues = dict()
        self.chain_name = chain_name
        self.prot_name = prot_name
        self.residues = residues
        self.align = align

    def reindex(self: 'Chain'):
        """
        Reindex res numbers to make it start from 1.
        """
        res_nums = list(self.residues)
        min_ = min(res_nums)
        new_res_nums = [n - min_ + 1 for n in res_nums]
        new_d = dict()
        for new_k, k in zip(new_res_nums, res_nums):
            new_d[new_k] = self.residues[k]
        self.residues = new_d

    def get_seq(self: 'Chain'):
        """
        Return chain sequence as a string of 1 letter coded AA.
        """
        seq = str()
        for res in self.residues.values():
            try:
                seq += three2one[res.res_name]
            except KeyError:
                seq += 'X'
        return seq

    # String conversion
    def __str__(self: 'Chain') -> str:
        """
        Define string conversion.
        Used by print to represent the object.
        """
        return "{} : {}".format(self.chain_name, self.residues)

    # Iterability implementation
    def __iter__(self: 'Chain'):
        """
        Create an iterator.
        Iterate the residues of the protein.
        """
        list_res = list(self.residues.items())
        f_sort = (lambda x: x[0])
        list_res.sort(key=f_sort)
        return iter([x for i, x in list_res])

    # Operator overload
    def __getitem__(self: 'Chain', key: int) -> Res:
        """
        Overload the '[]' index operator.
        Access to the residue from its res_num.
        Return a residue or a list of residues.
        Warning ! the index start at 1 (like in the PDB file).
        """
        # Broken slice since index can start from negative values
        # if isinstance(key, slice):
        #     max_res_num = max(self.residues.keys())
        #     idx = list(range(max_res_num + 1))
        #     return [self.residues[i] for i in idx[key]]
        # else:
        #     if key < 0:
        #         key = len(self.residues) + key + 1
        #     return self.residues[key]
        return self.residues[key]

    def __setitem__(self: 'Chain', key: int, items) -> None:
        """
        Overload of item assignment.
        Set a residues or a list of residues.
        """
        # Broken slice since index can start from negative values
        # if type(key) is not int:
        #     raise Exception('Keys must be integers')
        # if isinstance(key, slice):
        #     idx = list(range(key.stop))
        #     if len(idx[key]) != len(items):
        #         raise Exception(
        #             'Not the same number of elements on both sides')
        #     for i, item in zip(idx[key], items):
        #         print(i)
        #         self.residues[i] = item
        # else:
        #     if key < 0:
        #         key = len(self.residues) + key + 1
        #     self.residues[key] = items
        self.residues[key] = items

    def __contains__(self: 'Chain', key: int) -> bool:
        """
        Overload of 'in' operator.
        Search if the key is contains in the residues dictionary.
        """
        return key in self.residues
