#!/usr/bin/env python

import math, string
from prot_3D.chain import Chain # pyre-ignore
from prot_3D.res import Res # pyre-ignore
from prot_3D.atom import Atom # pyre-ignore


########################################
#         PARSING TOOLS
########################################

def pdb_parser(infile, prot_name='unknown', CG=False) :
    """
    PDB file parser.

    Parameters
    ----------
    infile: string
        PDB file path

    prot_name: string
        Protein or family name

    CG: boolean
        Use CG Model !Warning!: Not curently implemented

    Output
    ------
    Dictionary of Chain structures built as:
        prot = {<chain_id>: Chain ...}
    """

    # Read PDB file
    f = open(infile, "r")
    lines = f.readlines()
    f.close()

    # var init
    prot = dict()

    # Browse PDB
    for line in lines :
        is_atom = line[0:4] == 'ATOM'
        is_hetatm = line[0:6] == 'HETATM'
        if (is_atom or (is_hetatm and (line[17:20].strip() == "MET"
                                        or line[17:20].strip() == "MSE"))):
            chain = line[21]
            if not chain in prot:
                prot[chain] = Chain(chain_name=chain, prot_name=prot_name)
            curres = line[22:27].strip()
            resnum = int(line[22:26])
            if not resnum in prot[chain]:
                # first time we encounter it
                prot[chain][resnum] = Res(res_num=resnum,
                                          res_name=line[17:20].strip(),
                                          curres=curres)
                alternateoccupancy = None
                occupancy = "%s"%(line[16:17])
                if occupancy != " " :
                    alternateoccupancy = occupancy
            else:
                # this is not a new residue
                occupancy = "%s"%(line[16:17])
                if occupancy != " " and alternateoccupancy == None:
                    # means we are in the first alternate location of that residue
                    alternateoccupancy = occupancy

            # if CG:
            #     # means we are parsing a CG model so we have to treat the CSE atomtypes
            #     # which can be redondant in terms of name the same res
            #     atomtype = "%s_%s"%(line[6:11].strip(), line[12:16].strip())
            # else:
            #     atomtype = line[12:16].strip()
            atomtype = line[12:16].strip()
            element = atomtype[:1]

            if occupancy == alternateoccupancy or occupancy == " ":
                # means this atom corresponds to the first rotamer found in the PDB for
                # this residue
                prot[chain][resnum][atomtype] = Atom(x=float(line[30:38]),
                                                     y=float(line[38:46]),
                                                     z=float(line[46:54]),
                                                     element=element,
                                                     atom_num=int(line[6:11])
                                                )

    return prot


#################################################
#           WRITING TOOLS
#################################################

def pdb_writer(prot, filout="out.pdb") :
    """
    Write a PDB file from Chain objects.

    Parameters
    ----------
    prot: dict
        Dictionary of chain built as:
            {"chain_name": Chain, ...}

    filout: string
        File path of the future PDB file.
    """

    fout = open(filout, "w")

    for chain_name, chain in prot.items():
        for res in chain:
            for atom_name, atom in res.iteratoms():
                fout.write(
                    ("ATOM  %5s  %-4s%3s %s%4s    "
                     "%8.3f%8.3f%8.3f  1.00  1.00 X X\n"
                     % (atom.atom_num, atom_name, res.res_name,
                         chain_name, res.res_num,
                         atom.coord[0], atom.coord[1], atom.coord[2])
                    )
                )

    fout.close()
