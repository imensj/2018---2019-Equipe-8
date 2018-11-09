from prot_3D.atom import Atom
from prot_3D.res import Res
from prot_3D.chain import Chain

# 'reslist' |
# 'chains'   |
#  'A'      ¬
#            'reslist' |
#            '1'       ¬
#                       'resname'   |
#                       'resnum'    |
#                       'atomlist'  |
#                       '3_N'       ¬
#                                   'x'
#                                   'y'
#                                   'z'
#                                   'id'
#            '2'        |
#            .etc.      |
#
#
# 'B'       |

def dPDB_to_chains(dPDB, prot_name):
    chains = {}
    for chain in dPDB['chains']:
        residues = {}
        for res in dPDB[chain]['reslist']:
            atoms = {}
            for atom in res['atomlist']:
                atoms[atom] = Atom(x = res[atom]['x'],
                                   y = res[atom]['y'],
                                   z = res[atom]['z'],
                                   element = atom,
                                   atom_num = int(res[atom]['id']))
            residues[res['resnum']] = Res(res_num = int(res['resnum']),
                                        res_name = res['resname'],
                                        curres = None,
                                        atoms = atoms)
        chains[chain] = Chain(chain_name = chain,
                              prot_name = prot_name,
                              residues = residues,
                              align = None)
    return chains
