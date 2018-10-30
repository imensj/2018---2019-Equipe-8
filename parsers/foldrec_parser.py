"""
.foldrec files parser
"""

import re
import os
from pathlib import Path

def foldrec_parser(filename):
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
        query_start = d['query_start']
        query_th, last_query = 0, 0
        temp_start = d['template_start']
        temp_th, last_temp = 0, 0
        align_struct = []
        for k, (query_aa, temp_aa) in enumerate(zip(d['query_seq'],
                                                    d['template_seq'])):
            temp_n = temp_start + k - temp_th
            query_n = query_start + k - query_th
            if query_aa == '-':
                query_n = None
                query_th += 1
            if query_n is not None:
                last_query = query_n
            if temp_aa == '-':
                temp_n = None
                temp_th += 1
            if temp_n is not None:
                last_temp = temp_n
            # print('{}, temp_th {}, query_th {}, {}'.format(
            #     (query_n, temp_n), temp_th, query_th, (query_aa, temp_aa)))
            align_struct.append((query_n, temp_n))
        # print('{}, nb {}'.format(d['template'], i+1))
        # print(len(d['template_seq']))
        # print('Computed', (last_query, last_temp))
        # print('Data', (d['query_end'], d['template_end']))
        if (last_query, last_temp) != (d['query_end'], d['template_end']):
            raise Exception('Alignment error')
        d['align_struct'] = align_struct
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
                'align_struct', 'pdb_path'
        }
        if set(d.keys()) != keys:
            raise Exception('Data not found in foldrec file')
        else:
            data.append(d)

        # Print data
        # for key, item in d.items():
        #     print('{} : {}'.format(key, item))
    print('len data = {}'.format(len(data)))
    print('len raw data = {}'.format(len(align_cuts)))
    temp_nb = 3
    print(data[temp_nb]['template'])
    print(data[temp_nb]['pdb_path'])
    # print(data[temp_nb]['query_start'])
    # print(data[temp_nb]['align_struct'])

def main():
    filename = 'outputs_ORION/Agglutinin.foldrec'
    foldrec_parser(filename)

if __name__ == '__main__':
    main()
