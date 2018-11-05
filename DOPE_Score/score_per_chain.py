# -*- coding: utf-8 -*-
"""
Function DOPE_Score:

To be called by compute_DOPE_score function (see DOPE_Score/compute_dope.py).

Returns a DOPE score for 1 Chain of 1 protein

# Inputs:
- Chain: object of class 'Chain' extracted this way : Chain = object_chain["chain_name"]
- dope_dict: output of DOPE_to_dict (see DOPE_Score/dope_to_dictionary.py)
- atom_selection: list of string(s) to select atoms (Must be equal to the one used for DOPE_to_dict function). Cannot be empty
- mean_per_residue: boolean specifying if for each Residue 2.x, a mean of scores must be computed. Ignored if len(atom_selection) = 1. (default: True)

# Output: dictionary of the form {Prot_name_Chain_name : score}
"""
import numpy as np  # pyre-ignore
import itertools
from math import sqrt
from .dope_dict import dope_dict


def DOPE_score(chain, atom_selection=None, mean_per_residue=True):

    chain_name = chain.chain_name
    prot_name = chain.prot_name
    res = chain.residues
    print("#~#~#~# Computing DOPE score for %s (Chain '%s') #~#~#~#\n" %
          (prot_name, chain_name))
    SCORE = 0
    # Tupple of all doubletons (Residue x, Residue y) for all x,y in res_number such that x != y
    res_combi = itertools.combinations(res.keys(), 2)
    for res1, res2 in res_combi:
        res_name1 = res[res1].res_name
        res_name2 = res[res2].res_name

        if not atom_selection:
            set_atm1 = set(res[res1].atoms.keys())
            set_atm2 = set(res[res2].atoms.keys())
        else:
            set_atm1 = set(res[res1].atoms.keys()) & set(atom_selection)
            set_atm2 = set(res[res2].atoms.keys()) & set(atom_selection)
            # Tupple of all doubletons (Atom x, Atom y) for all (x,y) in (res1.atoms, res2.atom2) such that Atom x and y are in atom_selection
        atm_combi = itertools.product(set_atm1, set_atm2)
        mean = []
        for atm1, atm2 in atm_combi:

            coord1 = res[res1].atoms[atm1].coord
            coord2 = res[res2].atoms[atm2].coord
            distance = coord1 - coord2
            distance = [d**2 for d in distance]
            distance = sqrt(sum(distance))
            # Operations on distances : compute vector's norm

            if distance <= 15.0 and distance >= 0.25:
                pot_idx = round((distance - 0.25)//0.5)
                mean.append(dope_dict[res_name1][atm1][res_name2][atm2][pot_idx])

        # i.e. at least 1 distance in [0.25,0.15] because
        if len(mean) > 0:
            # if mean empty, creates error when mean_per_residue = True
            SCORE += np.mean(mean) if mean_per_residue else sum(mean)
    result = {"_".join([Prot_name, Chain_name]): SCORE}
    return result
