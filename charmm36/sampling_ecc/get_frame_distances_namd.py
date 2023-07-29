import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import distances

selections = {
    'acet':'resname ACET and name C2',
    'esna':'resname ESNA and name S',
    'mso4':'resname MSO4 and name S',
    'guan':'resname GUAN and name C',
    'imim':'resname IMIM and name CE1',
    'mamm':'resname MAMM and name NZ'
}

indeces = {
    'acet_guan':[1],
    'acet_imim':[1, 2],
    'acet_mamm':[1, 2],
    'esna_guan':[1, 2],
    'esna_imim':[1, 2],
    'esna_mamm':[1],
    'mso4_guan':[1],
    'mso4_imim':[1],
    'mso4_mamm':[1]
}

dcd_files = {}
for key, index_list in indeces.items():
    dcd_files[key] = [f'{key}/sampling_{i}.dcd' for i in index_list]

for anion in ['acet', 'esna']: # , 'mso4'
    for cation in ['guan', 'imim', 'mamm']:
        data_dir = f'{anion}_{cation}'
        topfile = f'{data_dir}/starting.pdb'
        traj = mda.Universe(topfile, *dcd_files[data_dir])
        print(data_dir)

        group_1 = traj.select_atoms(selections[anion])
        group_2 = traj.select_atoms(selections[cation])

        frame_distances = np.zeros((len(traj.trajectory), len(group_1), len(group_2)))
        volumes = np.zeros((len(traj.trajectory)))

        for i, ts in enumerate(traj.trajectory):
            box = ts.dimensions
            # print(ts.volume, ts.dimensions)
            volumes[i] = box[0] * box[1] * box[2]
            distances.distance_array(group_1.positions, group_2.positions,
                                    box=box, result=frame_distances[i,:,:])
            # print(frame_distances[i,:4,:4])

        np.save(f'{data_dir}/volumes.npy', volumes, allow_pickle=False)
        np.save(f'{data_dir}/frame_distances.npy', frame_distances, allow_pickle=False)

