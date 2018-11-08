import pandas as pd  # pyre-ignore

def DOPE_to_dict():
    path = '2018---2019-partage/Codes/Params/dope.par'
    dope_mat = pd.read_table(path, header=None, sep=' ')

    #print('-- DOPE DICT LOADING --')
    dope_dict = dict()
    for i, row in dope_mat.iterrows():
        res1 = row[0]
        atom1 = row[1]
        res2 = row[2]
        atom2 = row[3]
        pot = row[4:].values
        if res1 not in dope_dict:
            dope_dict[res1] = dict()
        if atom1 not in dope_dict[res1]:
            dope_dict[res1][atom1] = dict()
        if res2 not in dope_dict[res1][atom1]:
            dope_dict[res1][atom1][res2] = dict()
        dope_dict[res1][atom1][res2][atom2] = pot
    #print('-- DOPE DICT LOADED --')
    return dope_dict
