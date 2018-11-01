#!/usr/bin/env python

import math, string
from prot_3D.chain import Chain
from prot_3D.res import Res
from prot_3D.atom import Atom


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
            # print('after th', resnum)
            if not resnum in prot[chain]:
                # print('asign', resnum)
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
                # print('set', resnum)
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

# TODO: adapt write functions to data structures

# def writePDB(dPDB, filout = "out.pdb", bfactor = False) :
#     """purpose: according to the coordinates in dPDB, writes the corresponding PDB file.
#        If bfactor = True, writes also the information corresponding to the key bfactor
#        of each residue (one key per residue) in dPDB.
#        input: a dico with the dPDB format
#        output: PDB file.
#     """

#     fout = open(filout, "w")

#     for chain in dPDB["chains"]:
#         for res in dPDB[chain]["reslist"] :
#             for atom in dPDB[chain][res]["atomlist"] :
#                 if bfactor :
#                     fout.write("ATOM  %5s  %-4s%3s %s%4s    %8.3f%8.3f%8.3f  1.00%7.3f X X\n"%(dPDB[chain][res][atom]["id"], atom, dPDB[chain][res]["resname"],chain, res,dPDB[chain][res][atom]["x"], dPDB[chain][res][atom]["y"],dPDB[chain][res][atom]["z"],dPDB[chain][res]["bfactor"] ))
#                 else:
#                     fout.write("ATOM  %5s  %-4s%3s %s%4s    %8.3f%8.3f%8.3f  1.00  1.00 X X\n"%(dPDB[chain][res][atom]["id"], atom, dPDB[chain][res]["resname"],chain, res,dPDB[chain][res][atom]["x"], dPDB[chain][res][atom]["y"],dPDB[chain][res][atom]["z"] ))

#     fout.close()


# def initBfactor(dPDB):
#     """purpose: initiation of the bfactor key for each residue
#        input: a dico with the dPDB format
#     """

#     for chain in dPDB["chains"]:
#         for res in dPDB[chain]["reslist"]:
#             dPDB[chain][res]["bfactor"] = 0


# def generateFastPDB(x, y, z, res = "GEN", atomname = "X", atomid = 1, resid = 1, chain = " ", bfactor = ""):
#     """ //// DEBUG FUNCTION ////
#         purpose: creates a mini dico dPDB for one atom and its 3D coordinates.
#         The idea is to call after the writePDB(my_mini_dico) in order to visualize
#         with Pymol the coordinates of the corresponding atom.
#         input: x, y, z (3D coordinates of the atom we want to visualize)
#         output: a mini dPDB dico for one atom
#         usage: my_mini_dico = generateFastPDB(xi, yi, zi)

#     """

#     dPDB = {}
#     dPDB["chains"] = [chain]
#     dPDB[chain] = {}
#     dPDB[chain]["reslist"] = [resid]
#     dPDB[chain][resid] = {}
#     dPDB[chain][resid]["atomlist"] = [atomname]
#     dPDB[chain][resid][atomname] = {}
#     dPDB[chain][resid][atomname]["id"] = atomid
#     dPDB[chain][resid]["resname"] = res
#     dPDB[chain][resid][atomname]["x"] = x
#     dPDB[chain][resid][atomname]["y"] = y
#     dPDB[chain][resid][atomname]["z"] = z
#     if bfactor != "":
#         dPDB[chain][resid][atomname]["bfactor"] = bfactor

#     return dPDB
