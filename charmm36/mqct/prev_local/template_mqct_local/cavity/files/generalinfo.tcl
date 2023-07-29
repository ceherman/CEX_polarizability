#The following is list of variables used in this script
#------
#------
#com: it is a list. The list element has the information 
#pertaining to the residues of the protein. 
#the format of this information is: { ... residuenumber[i] xcoord[i] ycoord[i] zcoord[i] distance[i] ...} 
#here xcoord, yccord, and zcoord are the coordinates of the geometric center of mass
#(geometric center/centroid) of the heavy atoms (bones) of the residue number k. 
# distance is the maximum distance between geometric center of heavy atoms of residue k 
# and any atom of residue k. residuenumber is residue number. 
#-----
#bones: it is a list. The list elements have the
#information pertaining to the heavy atoms in the bones file. 
#the format of this information is: {... heavyatomnumber[i] residuenumber[i] xcoord[i] ycoord[i] zcoord[i] ...}
#here xcoord, ycoord, and zcoord are the x.y, and z co-oridantes of the heavy atom, 
#and residue number is the residue number of the heavy atom. heavyatomnumber is unique identification index
# of the heavy atom. 
# 
#------
#numcom: number of residues, also the number of centers of mass.
#-----
#numbones: number of heavy atoms in the entire protein
#
