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

from .score_per_chain import DOPE_score
import numpy as np  # pyre-ignore
import pandas as pd  # pyre-ignore


def compute_DOPE_score(threadings, atom_selection=("CA"), mean_per_residue=True):

    # Reproduced behaviour when theadings is a list
    threadings = [threadings] if threadings.__class__ != list else threadings
    scores = dict()
    for thread in threadings:
        for chain in thread:
            score_thread = DOPE_score(chain=thread[chain],
                                      atom_selection=atom_selection,
                                      mean_per_residue=mean_per_residue)
            scores.update(score_thread)
    return scores
