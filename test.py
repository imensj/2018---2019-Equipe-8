from parsers.foldrec_parser import foldrec_parser
from prot_threading.prot_threading import prot_thread
from parsers.pdb_tools import pdb_writer
from pathlib import Path

prots = foldrec_parser('./2018---2019-partage/Data/outputs_ORION/hemery.foldrec')
for prot in prots:
    query = dict()
    temp = dict()
    for chain_name, chain in prot.items():
        query[chain_name], temp[chain_name] = prot_thread(chain)
        prot_name = chain.prot_name
    path = Path('test_pdb')
    query_path = path / "{}-query.pdb".format(prot_name)
    temp_path = path / "{}-temp.pdb".format(prot_name)
    pdb_writer(query, query_path)
    pdb_writer(temp, temp_path)
