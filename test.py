from parsers.pdb_tools import pdb_parser
from parsers.foldrec_parser import foldrec_parser
from prot_threading.prot_threading import prot_thread
from DOPE_Score.compute_dope import compute_DOPE_score

path = './2018---2019-partage/Data/outputs_ORION/hemery.foldrec'
prots = foldrec_parser(path)
target = 'Peptidase_A6'
for prot in prots:
    for chain in prot.values():
        prot_name = chain.prot_name
    if prot_name == target:
        c = prot
prot = c['A']
print(prot['117']['CA'])
print(prot['85']['CA'])
a = prot.align
a = [x for i,x in a if x is not None]
print(prot.get_seq())
print(''.join(a))
quer, temp = prot_thread(prot)
# print(len(quer.residues))
# print(quer)
# print(temp['117']['CA'])
# print(temp['85']['CA'])
score =  compute_DOPE_score({'A': quer}, {'A': temp})

# pdb = pdb_parser('./2018---2019-partage/Data/HOMSTRAD/SPEC/2spca.atm')
# print(pdb['A'])
# print(pdb['A']['0'].res_name)
# print(pdb['A']['0'])
