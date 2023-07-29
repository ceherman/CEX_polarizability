import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import distances

anion = 'acet'
cation = 'guan'
data_dir = f'{anion}_{cation}'
topfile = f'{data_dir}/starting.pdb'
dcd_files = f'{data_dir}/sampling_1.dcd'
traj = mda.Universe(topfile, dcd_files)
group = traj.select_atoms('resnum 1 or resnum 23')
print(group.n_atoms)

with mda.Writer(f'{data_dir}/pair_1_23_single/single_pair.dcd', group.n_atoms) as W:
    for ts in traj.trajectory:
        W.write(group)

