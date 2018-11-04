# -*- coding: utf-8 -*-
"""
Function DOPE_to_dict:

- Manages DOPE_Score and DOPE_to_dict (respectively see DOPE_Score/compute_dope.py and DOPE_Score/dope_to_dictionary)
- Compute scores for a list of threadings/Proteins of class "Chain"

# Inputs:
- Threadings: list of objects of class 'Chain' or single object
- path_to_dope_par: path to file dope.par (e.g., 'Data/dope.par')
- dope_dict: output of DOPE_to_dict (see DOPE_Score/dope_to_dictionary.py)
- atom_selection: list of string(s) of single string to select atoms. If None or False, no selection is made. (default: "CA")
- mean_per_residue: boolean specifying if for each Residue 2.x, a mean of scores must be computed. Ignored if len(atom_selection) = 1. (default: True)

# Output: dictionary of the form {Prot_name_Chain_name : score}

/!\ WARNINGS /!\
When atome_selection = None or False, making a dictionary is very long
and memory consuming (I aborted the process, my computer couldn't handle it)
This is because it is necessary to iterate twice on atom_selection list (see DOPE_to_dict in DOPE_Score/dope_to_dictionary)

    ==> find a more inteligent way to build the dictionary
"""

from DOPE_Score.dope_to_dictionary import DOPE_to_dict  # pyre-ignore
from DOPE_Score.score_per_chain import DOPE_score  # pyre-ignore
import numpy as np  # pyre-ignore
import pandas as pd  # pyre-ignore


def compute_DOPE_score(threadings, path_to_dope_par, atom_selection="CA", mean_per_residue=True):

    dope_matrix = pd.read_table(
        path_to_dope_par, header=None, sep=" ")   # Read matrix dope.par
    # Column 1 contains atoms
    atoms = np.unique(dope_matrix.iloc[:, 1])
    # Reproduced behaviour when theadings is a list
    threadings = [threadings] if threadings.__class__ != list else threadings
    if atom_selection:
        atom_selection = [atom_selection] if atom_selection.__class__ != list else atom_selection
        if all(atm in atoms for atm in atom_selection):
            # Subsample dope_matrix to later on create a dictionary faster
            dope_matrix = dope_matrix[dope_matrix.iloc[:, 1].isin(atom_selection)]
            # Subsample dope_matrix to later on create a dictionary faster
            dope_matrix = dope_matrix[dope_matrix.iloc[:, 3].isin(atom_selection)]
        else:
            raise ValueError("compute_DOPE_score: parameter 'atom_selection' contains erroneous values.")
    else:
        # No atom selection when atome_selection = None or atome_selection = False
        atom_selection = atoms

    dope_dict = DOPE_to_dict(dope_matrix=dope_matrix,
                             atom_selection=atom_selection)

    scores = dict()
    for thread in threadings:
        for chain in thread:
            score_thread = DOPE_score(Chain=thread[chain],
                                      dope_dict=dope_dict,
                                      atom_selection=atom_selection,
                                      mean_per_residue=mean_per_residue)
            scores.update(score_thread)
    return scores
