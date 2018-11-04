#! /usr/bin/env python3
import os
from parsers.pdb_tools import *
from parsers.foldrec_parser import *
from prot_3D.atom import *
from pathlib import Path

# filename = './HOMSTRAD/cdh/cdh-sup.pdb'
# x = pdb_parser(filename)
# print(x['C'][100]['N'])
# print(x['I'][500])

# path = Path('./HOMSTRAD')
# dirs = os.listdir(path)
# for d in dirs:
#     dir_path = path / d
#     if os.path.isdir(dir_path):
#         print(d)
#         files = os.listdir(dir_path)
#         pdb = [f for f in files if '.pdb' in f]
#         if len(pdb) != 1:
#             raise Exception('{} pdb files found'.format(len(pdb)))
#         else:
#             pdb_path = dir_path / pdb[0]
#             print(pdb_path)
#             x = pdb_parser(pdb_path)
#             print(x)

# path = Path('./HOMSTRAD')
# dirs = os.listdir(path)
# for d in {'SET', 'sh3'}:
#     dir_path = path / d
#     if os.path.isdir(dir_path):
#         print(d)
#         files = os.listdir(dir_path)
#         pdb = [f for f in files if '.pdb' in f]
#         if len(pdb) != 1:
#             raise Exception('{} pdb files found'.format(len(pdb)))
#         else:
#             pdb_path = dir_path / pdb[0]
#             print(pdb_path)
#             x = pdb_parser(pdb_path)
#             print(x)

# TEST FOLDREC PARSER

filename = './outputs_ORION/hemery.foldrec'
temp_seq, prots = foldrec_parser(filename)
for seq, prot in zip(temp_seq, prots):
    print('####', prot['A'].prot_name, '####')
    seq_A = prot['A'].get_seq()
    comp = str()
    for aa, aa_A in zip(seq, seq_A):
        if aa == aa_A:
            comp += '-'
        else:
            comp += aa
    print('A :', prot['A'].get_seq())
    print('B :', prot['B'].get_seq())
    print('x :', comp)
for key, chain in prots[-1].items():
    print(key)
    seq_A = chain.get_seq()
    comp = str()
    for aa, aa_A in zip(seq, seq_A):
        if aa == aa_A:
            comp += '-'
        else:
            comp += aa
    print('chain :', seq_A)
    print('comp :', comp)
