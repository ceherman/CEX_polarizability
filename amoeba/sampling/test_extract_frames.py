import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import distances
import os
import json
import sys
sys.path.append('/home/chase/namd/openmm/from_arjun/pdb2txyz')
import manipulate_txyz as manip_xyz

xyz_dir = '/home/chase/namd/openmm/from_arjun/pdb2txyz/get_pdb_mapping'
file = f'{xyz_dir}/pdb_to_xyz_index_map.json'
with open(file, 'r') as f:
    pdb_to_xyz = json.load(f)

def anint(x):
    tmp = int(x)
    diff = x - tmp
    if diff >= 0.5:
        return tmp + 1.0
    elif diff <= -0.5:
        return tmp - 1.0
    else:
        return tmp

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

for anion in ['acet']: # ['acet', 'esna', 'mso4']: #
    mol_anion = manip_xyz.readtxyz(f'{xyz_dir}/{anion}.txyz')
    for cation in ['guan']: # ['guan', 'imim', 'mamm']: #
        mol_cation = manip_xyz.readtxyz(f'{xyz_dir}/{cation}.txyz')
        mol_combined = manip_xyz.combinemols(mol_anion, mol_cation)
        data_dir = f'{anion}_{cation}'
        if data_dir == 'esna_mamm':
            pdb_file = 'starting_packmol.pdb'
        else:
            pdb_file = 'starting.pdb'
        topfile = f'{data_dir}/{pdb_file}'
        traj = mda.Universe(topfile, *dcd_files[data_dir])

        for i_anion in range(1): # range(22):
            resi_anion = 1 + i_anion
            anion_selection_all  = f'resid {resi_anion}'
            anion_selection_atom = f'resid {resi_anion} and name {atoms[anion]}'
            group_a_all  = traj.select_atoms(anion_selection_all)
            group_a_atom = traj.select_atoms(anion_selection_atom)

            for i_cation in range(1): # range(22):
                resi_cation = 23 + i_cation
                cation_selection_all  = f'resid {resi_cation}'
                cation_selection_atom = f'resid {resi_cation} and name {atoms[cation]}'
                group_c_all  = traj.select_atoms(cation_selection_all)
                group_c_atom = traj.select_atoms(cation_selection_atom)

                xyz_coord_a = np.zeros((len(traj.trajectory), len(group_a_all.atoms), 3))
                xyz_coord_c = np.zeros((len(traj.trajectory), len(group_c_all.atoms), 3))
                xyz_coord_combined = np.zeros((len(traj.trajectory), len(group_a_all.atoms) + len(group_c_all.atoms), 3))

                for i, ts in enumerate(traj.trajectory):
                    if i % 100 == 0:
                        progress = i/len(traj.trajectory) * 100
                        print(f'{progress:.1f}%')

                    # Check whether we need to translate an ion across the PBC
                    box = ts.dimensions
                    assert box[0] == box[1] == box[2]

                    coord_a_all  = group_a_all.positions
                    coord_c_all  = group_c_all.positions
                    coord_a_atom = group_a_atom.positions[0]
                    coord_c_atom = group_c_atom.positions[0]
                    coord_c_atom_before = coord_c_atom
                    d1 = distances.distance_array(coord_a_atom, coord_c_atom, box=box)[0][0]

                    coord_a_atom_norm = coord_a_atom / box[0]
                    coord_c_atom_norm = coord_c_atom / box[0]

                    coord_norm_diff = coord_c_atom_norm - coord_a_atom_norm
                    wrap = np.array([anint(val) for val in coord_norm_diff])
                    coord_norm_diff = coord_norm_diff - wrap

                    # I'm shifting the cation and keeping the anion fixed
                    coord_c_atom_norm = coord_a_atom_norm + coord_norm_diff
                    coord_c_atom = coord_c_atom_norm * box[0]
                    d2 = distances.distance_array(coord_a_atom, coord_c_atom)[0][0] # no PBC
                    # Check that the separation distance is the same
                    assert np.allclose(d1, d2)
                    assert d2 <= np.sqrt(3) * box[0] / 2.0

                    coord_diff = coord_c_atom - coord_c_atom_before
                    if max(abs(coord_diff)) > 1e-2:
                        coord_c_all += coord_diff
                    # Check that coord_c_atom is in coord_c_all
                    assert min(np.sum((coord_c_all - coord_c_atom)**2, axis=1)) < 1e-3

                    xyz_coord_a[i] = coord_a_all[pdb_to_xyz[anion],:]
                    xyz_coord_c[i] = coord_c_all[pdb_to_xyz[cation],:]
                    xyz_coord_combined[i] = np.concatenate((xyz_coord_a[i], xyz_coord_c[i]))

                manip_xyz.writetarcfile(f'./temp_xyz/{anion}.arc', mol_anion, xyz_coord_a)
                manip_xyz.writetarcfile(f'./temp_xyz/{cation}.arc', mol_cation, xyz_coord_c)
                manip_xyz.writetarcfile(f'./temp_xyz/{anion}_{cation}.arc', mol_combined, xyz_coord_combined)


