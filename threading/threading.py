from structureTools_MeetU import *
import sys

# renvoie les CA d'une liste d'atome
def search_ca(list_atom):

    for at in list_atom:
        if at.endswith('CA'):
            return at

# Renvoie la liste des paires pouvant servir à l'enfilage
# list(seq1,seq2,list(int,int,int,int)) -> list(tuple(str,str))
def conserved_pairs(ali):
    seq_1, seq_2, (q_start, q_end, t_start, t_end) = ali

    list_pairs = []
    GAP = '-'
    reslist = []
    # Initialisation
    q_i = q_start - 1
    t_i = t_start - 1

    for r1, r2 in zip(seq_1, seq_2):

        if r1 != GAP:
            q_i += 1
        if r2 != GAP:
            t_i += 1

        if r1 != GAP and r2 != GAP:

            list_pairs.append(('_'.join((str(q_i), r1)),
                                '_'.join((str(t_i), r2))))
            reslist.append(str(q_i))
    return list_pairs, reslist

def init_dpdb():
    dpdb = {'reslist':[],
            'chains': [' '],
            ' ':{'reslist':[]}
            }
    return dpdb

def convert_amino_acid(res_code):

    res_dict_3to1 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
                     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
                     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
                     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

    res_dict_1to3 = {'C': 'CYS', 'D': 'ASP', 'S': 'SER', 'Q': 'GLN', 'K': 'LYS',
                     'I': 'ILE', 'P': 'PRO', 'T': 'THR', 'F': 'PHE', 'N': 'ASN',
                     'G': 'GLY', 'H': 'HIS', 'L': 'LEU', 'R': 'ARG', 'W': 'TRP',
                     'A': 'ALA', 'V': 'VAL', 'E': 'GLU', 'Y': 'TYR', 'M': 'MET'}

    if len(res_code) == 3:
        return res_dict_3to1[res_code]
    elif len(res_code) == 1:
        return res_dict_1to3[res_code]

# recupère et met à jour les info de résidu (resname, resnum, atomlist)
def config_res_enfile(res_template, resname_query, resnum_query, CA=True):


    res_enfile = {'resname': resname_query,
                   'resnum': resnum_query}
    if CA:

        atom_ca = [at for at in res_template['atomlist'] if at.endswith('CA')]

        res_enfile['atomlist'] = atom_ca
        res_enfile[atom_ca[0]] = res_template[atom_ca[0]]
    else:
        print ("pas de prise en compte des atom non CA pour l'instant!")

    return res_enfile


def ajout_res_dpdb(list_pairs, template, enfilage):

    template_chain = template['chains'][0]
    for pair in list_pairs:

        (qi, q_res), (ti, t_res) = pair[0].split('_'), pair[1].split('_')

        enfilage[' ']['reslist'].append(str(qi))

        # recup resi template corresp
        res_template = template[template_chain][ti]

        #recupe resname du residu query: code 1 lettre -> 3 lettres
        resname_query = convert_amino_acid(q_res)

        # config du dictionnaire residu pour l'enfilage
        res_enfile = config_res_enfile(res_template, resname_query, qi)

        enfilage[' '][str(qi)] = res_enfile

    return enfilage




def main():

    # --------------------------------------------------------------------------
    if (len(sys.argv) < 3):
        print("USAGE: ", sys.argv[0], "<pdb file query> <pdb file template>")
        sys.exit(1)
    query_fn = sys.argv[1]
    template_fn = sys.argv[2]
    # --------------------------------------------------------------------------
    # Lecture fichier PDB

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

    template = parsePDBMultiChains(template_fn, CG=False)

    # --------------------------------------------------------------------------
    # print d'information
    print('-'*50)
    print('Chaînes dans le template: {chaines:>20}'.format(
        chaines = 'no chains'   if    ','.join(template['chains'])==' '
                                else  ','.join(template['chains'])
                                                        ))

    print('Nombre de résidus: {:>20d}'.format(len(template['reslist'])))
    # --------------------------------------------------------------------------

    ali = [
        '-----MLIKVKTLTGKEIEIDIEPTDTIDRIKERVEEKEGIPPVQQRLI-YAGKQL---ADDKTAKDYNIEGGSVLHLVLAL',
        'NAEPVSKLRIRTPSGEFLERRFLASNKLQIVFDFVASKGFPWDEYKLLSTFPRRDVTQLDPNKSLLEVKLFPQETLFLEAKE',
        [1,73,1,82]
           ]



    # On souhaite pour chaque résidus query enfilable lui attribuer les
    # coordonnées du CA (pour l'instant) du résidus template correspondant.

    list_pairs,reslist = conserved_pairs(ali)

    enfilage = init_dpdb()

    # ajout reslist
    enfilage['reslist'] = reslist
    enfilage[' ']['reslist'] = reslist

    enfilage = ajout_res_dpdb(list_pairs, template, enfilage)

    print (enfilage)
    #writePDB(enfilage)


    # python LecturePDB.py 1ubq.atm 1h8ca.atm


main()
