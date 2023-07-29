import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis import rdf_mod_chase
import block_averaging_functions as block
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

fig, ax = my_plot.instantiate_fig(1, 1, fontsize=26)

text = 'central_atoms'

f = open('/home/chase/namd/openmm/ion_pairs/rshell.json')
rshell_data = json.load(f)


for anion in ['acet', 'esna', 'mso4']:
    for cation in ['guan', 'imim', 'mamm']:
        data_dir = f'{anion}_{cation}'
        rshell = rshell_data['namd_tip'][data_dir]

        # g(r)__________________________________________________________________________
        gr_array = np.loadtxt(f'{data_dir}/gr_{text}.txt')

        # fig, ax = my_plot.instantiate_fig(xlabel=r'$r$ ($\rm{\AA}$)', ylabel=r'$g \; (r)$')
        # ax.plot(gr_array[:,0], gr_array[:,1])
        # ax.fill_between(gr_array[:,0], gr_array[:,1]-2*gr_array[:,2], gr_array[:,1]+2*gr_array[:,2], alpha=0.3)
        # my_plot.set_layout(fig, ax)
        # ax.set_xlim(2, 10.5)
        # fig.savefig(f'{data_dir}/gr_{text}.png', dpi=300, transparent=False, bbox_inches='tight')

        # PMF___________________________________________________________________________
        pmf_array = np.loadtxt(f'{data_dir}/pmf_{text}.txt')

        # fig, ax = my_plot.instantiate_fig(xlabel=r'$r$ ($\rm{\AA}$)', ylabel='PMF [kcal/mol]')
        # ax.axhline(color='black', linewidth=0.5)
        # ax.plot(pmf_array[:,0], pmf_array[:,1])
        # ax.fill_between(pmf_array[:,0], pmf_array[:,1]-2*pmf_array[:,2], pmf_array[:,1]+2*pmf_array[:,2], alpha=0.3)
        # ax.set_ylim(-2.2, 1.5)
        # my_plot.set_layout(fig, ax)
        # ax.set_xlim(2, 10.5)
        # ax.set_ylim(-2.3, 1.5)
        # fig.savefig(f'{data_dir}/pmf_{text}.png', dpi=300, transparent=False, bbox_inches='tight')

        # Together 1_________________________________________________________________

        fig, ax = plt.subplots(2, 1, sharex=True)
        fig.set_size_inches(7, 12)

        ax[1].set_xlabel(r'$r$ ($\rm{\AA}$)')
        ax[0].set_ylabel(r'$g \; (r)$')
        ax[1].set_ylabel('PMF [kcal/mol]')

        ax[0].plot(gr_array[:,0], gr_array[:,1])
        ax[0].fill_between(gr_array[:,0], gr_array[:,1]-2*gr_array[:,2], gr_array[:,1]+2*gr_array[:,2], alpha=0.3)

        ax[1].plot(pmf_array[:,0], pmf_array[:,1])
        ax[1].fill_between(pmf_array[:,0], pmf_array[:,1]-2*pmf_array[:,2], pmf_array[:,1]+2*pmf_array[:,2], alpha=0.3)

        ax[0].set_xlim(2, 10)
        ax[0].set_ylim(0, 14)
        ax[1].set_ylim(-2.3, 1.5)
        ax[1].axhline(y=0, color='black', lw=1)
        plt.subplots_adjust(hspace=0.1)
        fig.savefig(f'{data_dir}/gr_and_pmf_{text}.png', dpi=300, transparent=False, bbox_inches='tight')

        # Together 2_________________________________________________________________

        fig, ax = plt.subplots(2, 1, sharex=True)
        fig.set_size_inches(7, 12)

        ax[1].set_xlabel(r'$r$ ($\rm{\AA}$)')
        ax[0].set_ylabel(r'$g \; (r)$')
        ax[1].set_ylabel('PMF [kcal/mol]')

        sub_index = gr_array[:,0] <= rshell

        ax[0].plot(gr_array[:,0], gr_array[:,1])
        ax[0].fill_between(gr_array[:,0][sub_index], gr_array[:,1][sub_index], alpha=0.3)

        ax[1].plot(pmf_array[:,0], pmf_array[:,1])
        ax[1].fill_between(pmf_array[:,0], pmf_array[:,1]-2*pmf_array[:,2], pmf_array[:,1]+2*pmf_array[:,2], alpha=0.3)

        ax[0].set_xlim(2, 10)
        ax[0].set_ylim(0, 14)
        ax[1].set_ylim(-2.3, 1.5)
        ax[1].axhline(y=0, color='black', lw=1)
        plt.subplots_adjust(hspace=0.1)
        fig.savefig(f'{data_dir}/gr_and_pmf_{text}_gr_integrand.png', dpi=300, transparent=False, bbox_inches='tight')

