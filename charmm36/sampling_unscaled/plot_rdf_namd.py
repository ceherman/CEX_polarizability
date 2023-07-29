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

text = 'central_atoms'

for anion in ['acet', 'esna', 'mso4']:
    for cation in ['guan', 'imim', 'mamm']:
        data_dir = f'{anion}_{cation}'

        # g(r)__________________________________________________________________________
        # gr_array = np.zeros((nbins,3))
        # gr_array[:,0] = rdf.results.bins
        # gr_array[:,1] = rdf.results.rdf
        # gr_array[:,2] = seom_vals
        gr_array = np.loadtxt(f'{data_dir}/gr_{text}.txt')

        fig, ax = my_plot.instantiate_fig(xlabel=r'$r$ ($\rm{\AA}$)', ylabel='$g \; (r)$')
        ax.plot(gr_array[:,0], gr_array[:,1])
        ax.fill_between(gr_array[:,0], gr_array[:,1]-2*gr_array[:,2], gr_array[:,1]+2*gr_array[:,2], alpha=0.3)
        my_plot.set_layout(fig, ax)
        ax.set_xlim(2, 10.5)
        fig.savefig(f'{data_dir}/gr_{text}.png', dpi=300, transparent=False, bbox_inches='tight')

        # PMF___________________________________________________________________________
        kcal_per_mol_per_kT = 0.592
        # pmf = -1.0 * kcal_per_mol_per_kT * np.log(gr_array[:,1]) # kcal/mol
        # pmf_seom = kcal_per_mol_per_kT * gr_array[:,2] / gr_array[:,1]

        # pmf_array = np.zeros((nbins,3))
        # pmf_array[:,0] = rdf.results.bins
        # pmf_array[:,1] = pmf
        # pmf_array[:,2] = pmf_seom
        pmf_array = np.loadtxt(f'{data_dir}/pmf_{text}.txt')

        fig, ax = my_plot.instantiate_fig(xlabel=r'$r$ ($\rm{\AA}$)', ylabel='PMF [kcal/mol]')
        ax.axhline(color='black', linewidth=0.5)
        ax.plot(pmf_array[:,0], pmf_array[:,1])
        ax.fill_between(pmf_array[:,0], pmf_array[:,1]-2*pmf_array[:,2], pmf_array[:,1]+2*pmf_array[:,2], alpha=0.3)
        ax.set_ylim(-2.2, 1.5)
        my_plot.set_layout(fig, ax)
        ax.set_xlim(2, 10.5)
        ax.set_ylim(-2.3, 1.5)
        fig.savefig(f'{data_dir}/pmf_{text}.png', dpi=300, transparent=False, bbox_inches='tight')


