"""
Dictionary to convert AA codes.
"""

three2one = {'ALA': 'A',
             'ARG': 'R',
             'ASP': 'D',
             'ASN': 'N',
             'CYS': 'C',
             'GLU': 'E',
             'GLN': 'Q',
             'GLY': 'G',
             'HIS': 'H',
             'ILE': 'I',
             'LEU': 'L',
             'LYS': 'K',
             'MET': 'M',
             'PHE': 'F',
             'PRO': 'P',
             'SER': 'S',
             'THR': 'T',
             'TRP': 'W',
             'TYR': 'Y',
             'VAL': 'V'}

one2three = {v: k for k, v in three2one.items()}
