from pathlib import Path

from parsers.foldrec_parser import foldrec_parser
from prot_threading.prot_threading import prot_thread
from prot_threading.prot_threading import AlignmentError
from parsers.pdb_tools import pdb_writer
from DOPE_Score.compute_dope import compute_DOPE_score

# FOLDREC file 
foldrec_path = Path('./2018---2019-partage/Data/outputs_ORION/FAD-oxidase_NC.foldrec')

# Parse foldrec
prots = foldrec_parser(foldrec_path)

# Get scores
scores = list()
for prot in prots:
    # Threading
    query = dict()
    template = dict()
    for chain_name, chain in prot.items():
        prot_name = chain.prot_name
        try:
            query_chain, template_chain = prot_thread(chain)
        except AlignmentError:
            continue
        if query_chain is not None and template_chain is not None:
            query[chain_name] = query_chain
            template[chain_name] = template_chain
    if len(query) == 0:
        continue
    prot_score = compute_DOPE_score(query, template)
    # Score min score of all chains
    min_ = min(list(prot_score.values()))
    for chain, s in prot_score.items():
        if s == min_:
            min_chain = chain
            break
    scores.append((min_, query[min_chain]))

# Sort it
f = (lambda x: x[0])
scores.sort(key=f, reverse=False)

# Get winner
N = 200
for i in range(N):
    print("{}# : {} ({:.2})".format(i+1, scores[i][1].prot_name[5:], scores[i][0]))

