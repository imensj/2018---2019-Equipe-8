"""
Tool to thread query sequence on template 3D structure.
"""

from prot_3D.chain import Chain
from prot_3D.res import Res
from prot_3D.convert_aa import one2three
from copy import deepcopy

def prot_thread(chain, atoms=('CA',)):
    """
    Thread query sequence on the template 3D structures.

    Parameters
    ----------
    chain: Chain object
        Template chain object.

    atoms: list or tuple
        List of atoms to thread, default: carbon alpha only.

    Output
    ------
    Threaded chain object, truncated template chain object
    """
    # Get alignment
    align = chain.align
    # Remove sequence parts where query is not matching
    align_only_temp = [(q,t) for q,t in align if t is not None]
    # Define name
    new_name = 'from_{}'.format(chain.prot_name)
    trunc_name = 'trunc_{}'.format(chain.prot_name)
    # Define new chain structure
    threaded = Chain(chain_name=chain.chain_name, prot_name=new_name)
    trunc_temp = Chain(chain_name=chain.chain_name, prot_name=trunc_name)
    # Iterate on sequence
    for res, (query_letter, temp_num) in zip(chain, align_only_temp):
        # Only if template is matching with query
        if query_letter is not None:
            # Create new residues
            new_res = Res(temp_num, one2three[query_letter])
            for atom in atoms:
                new_res[atom] = deepcopy(res[atom])
            threaded[temp_num] = new_res
            # Create new template residues
            trunc_temp[temp_num] = deepcopy(res)

    return threaded, trunc_temp
