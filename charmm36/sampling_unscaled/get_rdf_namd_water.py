import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import rdf
import block_averaging_functions as block
import sys
sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot
fig, ax = my_plot.instantiate_fig(1, 1)

def get_info(traj):
    nframes = len(traj.trajectory)
    vals = np.zeros((nframes,3))
    for i, ts in enumerate(traj.trajectory):
        vals[i,:] = ts.dimensions[:3]
    return nframes, np.mean(vals)

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

for anion in ['acet', 'esna', 'mso4']:
    for cation in ['guan', 'imim', 'mamm']:
        data_dir = f'{anion}_{cation}'
        pdb_file = 'starting.pdb'
        topfile = f'{data_dir}/{pdb_file}'
        traj = mda.Universe(topfile, *dcd_files[data_dir])
        print(data_dir)

        nframes, boxl = get_info(traj)
        hboxl = boxl/2.0

        for ion in [anion, cation]:
            print(f'\t{ion}')
            group_1 = traj.select_atoms(selections[ion])
            group_2 = traj.select_atoms('resname TIP3 and name OH2')

            nbins = 300
            computed_rdf = rdf.InterRDF(group_1, group_2, nbins=nbins, range=(0.0, hboxl))
            run = computed_rdf.run()

            # g(r)______________________________________________________________
            gr_array = np.zeros((nbins,2))
            gr_array[:,0] = computed_rdf.results.bins
            gr_array[:,1] = computed_rdf.results.rdf
            np.savetxt(f'{data_dir}/gr_water_{ion}.txt',gr_array,fmt='%8.5f')

            # PMF_______________________________________________________________
            kcal_per_mol_per_kT = 0.592
            pmf = -1.0 * kcal_per_mol_per_kT * np.log(computed_rdf.results.rdf) # kcal/mol

            pmf_array = np.zeros((nbins,2))
            pmf_array[:,0] = computed_rdf.results.bins
            pmf_array[:,1] = pmf
            np.savetxt(f'{data_dir}/pmf_water_{ion}.txt',pmf_array,fmt='%8.5f')




