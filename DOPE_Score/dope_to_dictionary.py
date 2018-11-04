# -*- coding: utf-8 -*-
"""
Function DOPE_to_dict:

To be called by compute_DOPE_score function (see DOPE_Score/compute_dope.py).

Creates a dictonary of statistical potentials of the form:

    {Residue 1.1 : {Atom 1.1 : {Residue 2.1 : {Atom 2.1 : arrayofscores[0.25 - 0.75, 0.75 - 1.25, ..., 14.75 - 15.0}     | Dictionary #1       |                                   |
                                               ...                                                                       | of array of scores  |                                   |
                                               ...                                                                       | based on distances  | Dictionary #1                     |
                                              {Atom 2.n2 : arrayofscores[0.25 - 0.75, 0.75 - 1.25, ..., 14.75 - 15.0}    | (in Ångström)       | of possible residues for given    |
                                ...                                                                                                            | Residue 1.1 and Atom 1.1          | Dictionary #1
                                ...                                                                                                            |                                   | of possible atoms
                               {Residue 2.r2 : {Dictionary #r2 of array of scores based on distances (in Ångström)}                            |                                   | for given Residue 1.1
                    ...                                                                                                                                                            |
                    ...                                                                                                                                                            |
                   {Atom 1.n1 : {Dictionary #n2 of possible residues for given Residue 1.1 and Atom 1. n2}                                                                         |
    ...
    ...
   {Residue 1.r1 : {Dictionary #r1 of possible atoms for given Residue 1.r2}

r2: Number of possible residues
r1: Number of comparable residues with the Residue 1.x (r1 = r2)
n1: Number of possible atoms given Residue 1.x (value of n1 depends on the residue itself, but usually = len(atom_selection))
n2: Number of possible atoms given Residue 2.x (value of n2 depends on the residue itself, but usually = len(atom_selection))

# Inputs:
- dope_matrix: matrix given by 'dope.par' (in Data/) read with pandas.
    column 0: Residues 1.1 to 1.r1
    column 1: Atoms 1.1 to 1.n1
    column 2: Residues 2.1 to 2.r2
    column 3: Atoms 2.1 to 2.n2
    columns 4 to last: array of scores based on distances
- atom_selection: list of string(s) corresponding to atoms found in 'dope.par'. Cannot be empty

# Output: dictionary (see above)
"""
import numpy as np  # pyre-ignore
import pandas as pd  # pyre-ignore


def DOPE_to_dict(dope_matrix, atom_selection):
    residues = np.unique(dope_matrix.iloc[:, 0])
    full_dict = dict()
    for ref_res in residues:
        dict_atm1 = dict()
        # Subsample dope_matrix for each residue 1.x to iterate quicker creating 'distaances' object
        sub_dope_matrix = dope_matrix[dope_matrix.iloc[:, 0] == ref_res]
        for atm1 in atom_selection:
            dict_res2 = dict()
            for res2 in residues:
                dict_atm2 = dict()
                for atm2 in atom_selection:
                    distances = sub_dope_matrix[(sub_dope_matrix.iloc[:, 0] == ref_res) & (sub_dope_matrix.iloc[:, 1] == atm1) & # With ravel: distances.shape = (30,)
                    (sub_dope_matrix.iloc[:, 2] == res2) & (sub_dope_matrix.iloc[:, 3] == atm2)].iloc[:, 4:].values.ravel() # Without: distances.shape = (1, 30)
                    """
                    Check each time that built dictionary is not empty.
                    For example, if CH2 in atom_selection:
                    a lot of residues do not present is and
                    a lot of empty dictionary can be made
                    """
                    if len(distances) != 0:
                        dict_atm2[atm2] = distances
                if len(dict_atm2) != 0:
                    dict_res2[res2] = dict_atm2
            if len(dict_res2) != 0:
                dict_atm1[atm1] = dict_res2
        if len(dict_atm1) != 0:
            full_dict[ref_res] = dict_atm1

    return full_dict
