import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import distances

indeces = {
    'acet_guan':[1],
    'acet_imim':[1],
    'acet_mamm':[1],
    'esna_guan':[1],
    'esna_imim':[1],
    'esna_mamm':[1],
    'mso4_guan':[1],
    'mso4_imim':[1],
    'mso4_mamm':[1]
}
dcd_files = {}
for key, index_list in indeces.items():
    dcd_files[key] = [f'{key}/sampling_{i}.dcd' for i in index_list]

anion = 'acet'
cation = 'guan'
data_dir = f'{anion}_{cation}'
topfile = f'{data_dir}/starting.pdb'
traj = mda.Universe(topfile, *dcd_files[data_dir])

i_anion = 0
i_cation = 1
group_1 = traj.select_atoms('resid 1 and name C2')
group_2 = traj.select_atoms('resid 24 and name C')

pair_distances = np.zeros((len(traj.trajectory), len(group_1), len(group_2)))
for i, ts in enumerate(traj.trajectory):
    box = ts.dimensions
    distances.distance_array(group_1.positions, group_2.positions,
                             box=box, result=pair_distances[i,:,:])

frame_distances = np.load(f'{data_dir}/frame_distances.npy')

print(np.allclose(pair_distances[:,0,0], frame_distances[:,i_anion,i_cation]))

