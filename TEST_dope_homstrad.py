from DOPE_Score.compute_dope import *
from prot_3D.atom import Atom
from prot_3D.res import Res
from prot_3D.chain import Chain
from parsers.pdb_tools import *
""" Randomly sample proteins """

import glob
import re
import numpy as np
from random import sample

path_HOMSTRAD = "./2018---2019-partage/Data/HOMSTRAD"
length = len(path_HOMSTRAD)
last = path_HOMSTRAD[length - 1: length]
length_split = len(re.split("(?:\\\\|/)", path_HOMSTRAD))
length_split = length_split - 1 if last == "/" or last == "\\" else length_split

path_pattern = path_HOMSTRAD
path_pattern += "**/*-sup.pdb" if last == "/" or last == "\\" else "/**/*-sup.pdb"
list_files = glob.glob(path_pattern, recursive=True)
list_files = [re.sub("\\\\", "/", f) for f in list_files]

print("Found %d pdb candidates\n" % len(list_files))

nProts = 5
prot_samp = sample(list_files, nProts)
prot_names = [re.split("/", p)[length_split] for p in prot_samp]
print("Sample:\n - ", "\n - ".join(prot_names))

""" Calculate DOPE Score on the proteins """

Prots = []
for path, name in zip(prot_samp, prot_names):
    Prots.append(pdb_parser(path, prot_name=name))


final = compute_DOPE_score(threadings=Prots,
                           #path_to_dope_par="2018---2019-partage/Codes/Params/dope.par",
                           atom_selection=["CA", "O"],
                           mean_per_residue=True)

print(final)
