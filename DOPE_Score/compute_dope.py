# -*- coding: utf-8 -*-
"""
Function DOPE_to_dict:

- Manages DOPE_Score and DOPE_to_dict (respectively see DOPE_Score/compute_dope.py and DOPE_Score/dope_to_dictionary)
- Compute scores for a list of threadings/Proteins of class "Chain"

# Inputs:
- Threadings: list of objects of class 'Chain' or single object
- path_to_dope_par: path to file dope.par (e.g., '2018---2019-partage/Codes/Params/dope.par')
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

from .score_per_chain import DOPE_score
import numpy as np  # pyre-ignore
import pandas as pd  # pyre-ignore


def compute_DOPE_score(query, template, atom_selection=("CA",), mean_per_residue=True):
    scores = dict()
    for chain_name in query:
        score_query = DOPE_score(
                chain=query[chain_name],
                atom_selection=atom_selection,
                mean_per_residue=mean_per_residue
        )
        score_temp = DOPE_score(
                chain=template[chain_name],
                atom_selection=atom_selection,
                mean_per_residue=mean_per_residue
        )
        scores[chain_name] = score_query / score_temp if score_temp != 0 else -1
    return scores
