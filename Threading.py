# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 20:03:43 2018

@author: Florian
"""

#import os

from parsers.foldrec_parser import foldrec_parser
from parsers.pdb_tools import pdb_parser
from prot_3D import *
from pathlib import Path
from DOPE_Score.dope_to_dictionary import DOPE_to_dict
from DOPE_Score.score_per_chain import DOPE_score
from DOPE_Score.compute_dope import compute_DOPE_score



filename = '2018---2019-partage/Data/outputs_ORION/hemery.foldrec'
#prots, seq_borders, ali = foldrec_parser(filename)
folds = foldrec_parser(filename)
Threadings = list()
Query_seq_borders = list()
Query_cov = list()
Templates = list()
for n, d in enumerate(folds):
    if not "-" in d["query_seq"]:
        Threading = chain.Chain(chain_name = "Q", prot_name = d["query"]+str(n+1))

        template_pdb = pdb_parser(infile = d['pdb_path'],
                                  prot_name = d['template'],
                                  CG = False)


        res_list_query = [convert_aa.one2three[atm] for atm in d['query_seq']]
        res_list_template = [convert_aa.one2three[atm] for atm in d['template_seq'] if atm != "-" ]
        template = chain.Chain(chain_name = chain_template, prot_name= d["template"])

        chain_template = list(template_pdb.keys())
        diffs = [abs(len(template_pdb[ch].residues) - len(res_list_template)) for ch in chain_template]
        chain_template = chain_template[diffs.index(min(diffs))]
        if d["template_start"] == list(template_pdb[chain_template].residues.keys())[0]:

            for num_query, res in enumerate(res_list_query):
                corresp_numres = d["align_struct"][num_query][1]
                if corresp_numres:
                    corresp_numres = corresp_numres - 1 + list(template_pdb[chain_template].residues.keys())[0]
                    corresp_coord = template_pdb[chain_template][corresp_numres]["CA"].coord

                #else:
                    #corresp_coord = [999,999,999]

                    new_atm = atom.Atom(x = corresp_coord[0],
                                        y = corresp_coord[1],
                                        z = corresp_coord[2],
                                        element = "CA",
                                        atom_num = i)
                    Threading[d['query_start']+i] = Res(res_num = d['query_start']+i,
                                                        res_name = res,
                                                        atoms = {"CA" : new_atm})
                    template[corresp_numres] = Res(res_num = corresp_numres,
                                                   res_name = res_list_template[i],
                                                   atoms = {"CA" : template_pdb[chain_template][corresp_numres]["CA"]})
    Threadings.append({"Q":Threading})
    Query_seq_borders.append([d['query_start'],d['query_end']])
    Query_cov.append(d['query_coverage'])
    Templates.append({chain_template : template})


DOPE_template = compute_DOPE_score(Templates,
                                   path_to_dope_par = "2018---2019-partage-master/Codes/Params/dope.par",
                                   atom_selection ="CA")

DOPE_query = compute_DOPE_score(Threadings,
                                path_to_dope_par = "2018---2019-partage-master/Codes/Params/dope.par",
                                atom_selection ="CA")

SCORE_final = list()
for template, query in zip(DOPE_template.values(), DOPE_query.values()):
    SCORE_final.append(template - query)

