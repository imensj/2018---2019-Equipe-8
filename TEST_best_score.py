from pathlib import Path

from parsers.foldrec_parser import foldrec_parser
from prot_threading.prot_threading import prot_thread
from parsers.pdb_tools import pdb_writer
from DOPE_Score.compute_dope import compute_DOPE_score

# FOLDREC file
foldrec_path = "2018---2019-partage/Data/outputs_ORION/hemery.foldrec"

# Parse foldrec
prots = foldrec_parser(foldrec_path)

# Get scores
scores = list()
for prot in prots:
    # Threading
    query = dict()
    template = dict()
    for chain_name, chain in prot.items():
        query[chain_name], template[chain_name] = prot_thread(chain)
    prot_score = compute_DOPE_score(query, template)
    # Score min score of all chains
    min_ = min(list(prot_score.values()))
    for chain, s in prot_score.items():
        if s == min_:
            min_chain = min_
            break
    scores.append((min_, query))

# Sort it
f = (lambda x: x[0])
scores.sort(key=f, reverse=True)

# Get winner
winner = scores[0][1]
print('Best template is :', winner) # winner.prot_name
