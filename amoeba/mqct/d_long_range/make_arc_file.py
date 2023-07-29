import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import distances
import os
import json
import sys
import manipulate_txyz_ceh as manip_xyz

which_group = sys.argv[1]
if which_group == 'all':
    starting_res_id = 1
    selection_text = 'all'
elif which_group == 'water':
    starting_res_id = 2
    selection_text = 'not resid 1'

xyz_dir = '../xyz_pdb_mapping'
pdb_file = 'starting.pdb'
dcd_file = 'prod.dcd'

mol_combined, atom_id_list = manip_xyz.pdb_file_to_tobj(pdb_file, xyz_dir, starting_res_id)
traj = mda.Universe(pdb_file, dcd_file)
xyz_coord = np.zeros((len(traj.trajectory), mol_combined.natoms, 3))

selection = traj.select_atoms(selection_text)

for i, ts in enumerate(traj.trajectory):
    coord = selection.positions
    xyz_coord[i] = coord[atom_id_list,:]

manip_xyz.writetarcfile(f'./{which_group}.arc', mol_combined, xyz_coord)
