import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import distances
import os
import json
import sys
import manipulate_txyz as manip_xyz

def anint(x):
    tmp = int(x)
    diff = x - tmp
    if diff >= 0.5:
        return tmp + 1.0
    elif diff <= -0.5:
        return tmp - 1.0
    else:
        return tmp

anion = sys.argv[1]
cation = sys.argv[2]
ion = sys.argv[3]
resi = sys.argv[4]

data_dir = f'{anion}_{cation}'
output_dir =f'{data_dir}/pair_data/'

xyz_dir = './xyz_pdb_mapping'
file = f'{xyz_dir}/pdb_to_xyz_index_map.json'
with open(file, 'r') as f:
    pdb_to_xyz = json.load(f)

atoms = {
    'acet':'C2',
    'esna':'S',
    'mso4':'S',
    'guan':'C',
    'imim':'CE1',
    'mamm':'NZ'
}
indeces = {
    'acet_guan':[1, 2],
    'acet_imim':[1],
    'acet_mamm':[1],
    'esna_guan':[1, 2],
    'esna_imim':[1],
    'esna_mamm':[1],
    'mso4_guan':[1],
    'mso4_imim':[1],
    'mso4_mamm':[1, 2]
}
dcd_files = {}
for key, index_list in indeces.items():
    dcd_files[key] = [f'{key}/trajectory_{i}.dcd' for i in index_list]

mol_ion = manip_xyz.readtxyz(f'{xyz_dir}/{ion}.txyz')

if data_dir == 'esna_mamm':
    pdb_file = 'starting_packmol.pdb'
else:
    pdb_file = 'starting.pdb'

topfile = f'{data_dir}/{pdb_file}'
traj = mda.Universe(topfile, *dcd_files[data_dir])

ion_selection_all  = f'resid {resi}'
group_all  = traj.select_atoms(ion_selection_all)

xyz_coord = np.zeros((len(traj.trajectory), len(group_all.atoms), 3))

for i, ts in enumerate(traj.trajectory):
    # Check whether we need to translate an ion across the PBC
    box = ts.dimensions
    assert box[0] == box[1] == box[2]
    coord_all  = group_all.positions
    xyz_coord[i] = coord_all[pdb_to_xyz[ion],:]

manip_xyz.writetarcfile(f'./{output_dir}/{ion}_{resi}.arc', mol_ion, xyz_coord)
