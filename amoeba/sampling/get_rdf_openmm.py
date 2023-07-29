import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import rdf_mod_chase
import block_averaging_functions as block
import sys
sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot
fig, ax = my_plot.instantiate_fig(1, 1)
# Place rdf_mod_chase in the MDAnalysis/analysis directory - like:
# /home/chase/anaconda3/lib/python3.7/site-packages/MDAnalysis/analysis

def get_info(traj):
    nframes = len(traj.trajectory)
    vals = np.zeros((nframes,3))
    for i, ts in enumerate(traj.trajectory):
        vals[i,:] = ts.dimensions[:3]
    return nframes, np.mean(vals)

# text = 'charged_atoms'
# selections = {
#     'acet':'resname ACET and element O',
#     'esna':'resname ESNA and element O',
#     'mso4':'resname MSO4 and element O',
#     'guan':'resname GUAN and element N',
#     'imim':'resname IMIM and element N',
#     'mamm':'resname MAMM and element N'
# }
text = 'central_atoms'
selections = {
    'acet':'resname ACET and name C2',
    'esna':'resname ESNA and name S',
    'mso4':'resname MSO4 and name S',
    'guan':'resname GUAN and name C',
    'imim':'resname IMIM and name CE1',
    'mamm':'resname MAMM and name NZ'
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

for anion in ['mso4']: # ['acet', 'esna', 'mso4']:
    for cation in ['mamm']: # ['guan', 'imim', 'mamm']:
        data_dir = f'{anion}_{cation}'
        print(data_dir)

        if data_dir == 'esna_mamm':
            pdb_file = 'starting_packmol.pdb'
        else:
            pdb_file = 'starting.pdb'

        topfile = f'{data_dir}/{pdb_file}'
        traj = mda.Universe(topfile, *dcd_files[data_dir])

        nframes, boxl = get_info(traj)
        hboxl = boxl/2.0

        group_1 = traj.select_atoms(selections[anion])
        group_2 = traj.select_atoms(selections[cation])

        nbins = 300
        rdf = rdf_mod_chase.InterRDF(group_1, group_2, nbins=nbins, range=(0.0, hboxl))
        run = rdf.run()

        seom_vals, mvals = np.zeros(nbins), np.zeros(nbins)
        for i in range(nbins):
            print(f'Computing SEOM for bin {i}')
            stats = block.std_eom(rdf.results.frame_rdf[:,i])
            mValue, sigma_raw, stdev_raw, seom_raw, inefficiency, seom = stats
            seom_vals[i], mvals[i] = seom, mValue

        assert np.allclose(rdf.results.rdf, mvals)
        assert np.allclose(rdf.results.rdf, np.mean(rdf.results.frame_rdf, axis=0))

        # g(r)__________________________________________________________________________
        gr_array = np.zeros((nbins,3))
        gr_array[:,0] = rdf.results.bins
        gr_array[:,1] = rdf.results.rdf
        gr_array[:,2] = seom_vals
        np.savetxt(f'{data_dir}/gr_{text}.txt',gr_array,fmt='%8.5f')

        fig, ax = my_plot.instantiate_fig(xlabel=r'$r$ ($\AA$)', ylabel='$g \; (r)$')
        ax.plot(rdf.results.bins, rdf.results.rdf)
        ax.fill_between(rdf.results.bins, rdf.results.rdf-2*seom_vals,
                        rdf.results.rdf+2*seom_vals, alpha=0.3)
        my_plot.set_layout(fig, ax)
        fig.savefig(f'{data_dir}/gr_{text}.png', dpi=300, transparent=False, bbox_inches='tight')

        # PMF___________________________________________________________________________
        kcal_per_mol_per_kT = 0.592
        pmf = -1.0 * kcal_per_mol_per_kT * np.log(rdf.results.rdf) # kcal/mol
        pmf_seom = kcal_per_mol_per_kT * seom_vals / rdf.results.rdf

        pmf_array = np.zeros((nbins,3))
        pmf_array[:,0] = rdf.results.bins
        pmf_array[:,1] = pmf
        pmf_array[:,2] = pmf_seom
        np.savetxt(f'{data_dir}/pmf_{text}.txt',pmf_array,fmt='%8.5f')

        fig, ax = my_plot.instantiate_fig(xlabel=r'$r$ ($\AA$)', ylabel='PMF [kcal/mol]')
        ax.axhline(color='black', linewidth=0.5)
        ax.plot(rdf.results.bins, pmf)
        ax.fill_between(rdf.results.bins, pmf-2*pmf_seom, pmf+2*pmf_seom, alpha=0.3)
        ax.set_ylim(-2.2, 1.5)
        my_plot.set_layout(fig, ax)
        fig.savefig(f'{data_dir}/pmf_{text}.png', dpi=300, transparent=False, bbox_inches='tight')


