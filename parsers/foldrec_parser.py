"""
.foldrec files parser
"""

import re
import os
from pathlib import Path
from .pdb_tools import pdb_parser

def foldrec_parser(filename):
    """
    Parse a foldrec file.

    Parameters
    ----------
    filename: string
        Path to the foldrec file.

    Output
    ------
    List of aligned prots.
    """
    # Read file
    with open(filename, 'r') as f:
        raw = f.readlines()

    # Get only alignment details
    for i, row in enumerate(raw):
        if re.match('^.*ALIGNMENTS DETAILS', row):
            align_raw = raw[i:]
            break

    # Cut alignment details by templates
    align_cuts = []
    idx = None
    idx_old = None
    for i, row in enumerate(align_raw):
        mo = re.match('^No (\d+)\s$', row)
        if mo:
            idx_old = idx
            idx = i
            if idx_old is None:
                continue
            align_cuts.append(align_raw[idx_old:idx])
        if i+1 == len(align_raw):
            align_cuts.append(align_raw[idx:])

    # RegEx patterns
    align_re = r'^Alignment\s*:\s*([\w-]+).*vs\s*([\w-]+)\s*:\s*(.*)'
    score_re = r'^Score\s*:\s*([-\d\.]+)\s*.*Normalized score\s*:\s*([-\d\.]+)'
    id_re = r'.*Query coverage\s*:\s*([\d\.]+).*Identity\s*:\s*([\d\.na-]+)'
    query_re = r'^Query\s*(\d+)\s*([\w-]*)\s*(\d+)'
    template_re = r'^Template\s*(\d+)\s*([\w-]*)\s*(\d+)'

    print('--> Parsing foldrec file <--')
    # Parse cuts
    data = []
    for i,cut in enumerate(align_cuts):
        d = dict()
        # Get only first query and first template
        first_query = True
        first_template = True
        for row in cut:
            # Match Alignment line
            if re.match(align_re, row):
                mo = re.match(align_re, row)
                d['query'] = mo.group(1)
                d['template'] = mo.group(2)
                d['scop'] = mo.group(3)
            # Match Score line
            if re.match(score_re, row):
                mo = re.match(score_re, row)
                d['score'] = float(mo.group(1))
                d['normalized_score'] = float(mo.group(2))
                mo = re.match(id_re, row)
                d['query_coverage'] = float(mo.group(1))
                d['identity'] = float(mo.group(2))
            # Match Query line
            if re.match(query_re, row):
                if first_query:
                    mo = re.match(query_re, row)
                    d['query_seq'] = mo.group(2)
                    d['query_start'] = int(mo.group(1))
                    d['query_end'] = int(mo.group(3))
                    first_query = False
            # Match Template line
            if re.match(template_re, row):
                if first_template:
                    mo = re.match(template_re, row)
                    d['template_seq'] = mo.group(2)
                    d['template_start'] = int(mo.group(1))
                    d['template_end'] = int(mo.group(3))
                    first_template = False
        # Skip alignment with itself
        if d['identity'] == 100 and d['query_coverage'] == 100:
            continue
        # Skip not aligned templates
        if d['identity'] == float('nan') or d['query_coverage'] == 0:
            continue
        # Compute alignment structure
        query_seq_str = ""
        template_seq_str = ""
        query_start = d['query_start']
        query_th, last_query = 0, 0
        temp_start = d['template_start']
        temp_th, last_temp = 0, 0
        align_struct = []
        # Iterate over sequences
        for k, (query_aa, temp_aa) in enumerate(zip(d['query_seq'],
                                                    d['template_seq'])):
            temp_n = temp_start + k - temp_th
            query_n = query_start + k - query_th
            # Check if the AA is aligned
            if query_aa == '-':
                query_n = None
                # If the AA is not aligned increment the threshold
                query_th += 1
            else:
                query_seq_str += query_aa
            # Check if the AA is aligned
            if temp_aa == '-':
                temp_n = None
                # If the AA is not aligned increment the threshold
                temp_th += 1
            else:
                template_seq_str += temp_aa
            # These lines are used to check if there is an error
            # Can be delete if the script is robust enough
            if query_n is not None:
                last_query = query_n
            if temp_n is not None:
                last_temp = temp_n
            align_struct.append((query_aa, temp_n))

        if (last_query, last_temp) != (d['query_end'], d['template_end']):
            raise Exception('Alignment error')
        d['align_struct'] = align_struct
        d['query_seq_str'] = query_seq_str
        d['template_seq_str'] = template_seq_str

        # Get PDB file path
        dir_path = Path("HOMSTRAD") / d['template']
        try:
            files = os.listdir(dir_path)
            pdb = [f for f in files if '.pdb' in f]
            if len(pdb) != 1:
                raise Exception('{} pdb files found'.format(len(pdb)))
            else:
                pdb_path = dir_path / pdb[0]
        except FileNotFoundError:
            print('{} template not found'.format(d['template']))
            pdb_path = 'not_found'
        d['pdb_path'] = pdb_path

        # Check if all fields got parsed
        keys = {'query', 'template', 'scop',
                'score', 'normalized_score', 'query_coverage', 'identity',
                'query_seq', 'query_start', 'query_end',
                'template_seq', 'template_start', 'template_end',
                'query_seq_str', 'template_seq_str',
                'align_struct', 'pdb_path'
        }
        if set(d.keys()) != keys:
            raise Exception('Data not found in foldrec file')
        else:
            if d['pdb_path'] != 'not_found':
                data.append(d)

    # Create prot list
    prots = list()
    for d in data:
        print(' -> Parsing {} pdb file.'.format(d['template']))
        prot = pdb_parser(d['pdb_path'], prot_name=d['template'])
        for chain in prot.values():
            chain.align = d['align_struct']
        prots.append(prot)

    return prots
