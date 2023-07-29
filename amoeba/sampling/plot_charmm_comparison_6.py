import numpy as np
import pandas as pd
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

fig, ax = my_plot.instantiate_fig()
plt.close()

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}
text = 'central_atoms'

for show_rshell in [True, False]:
    if show_rshell:
        f = open('rshell.json')
        rshell_data = json.load(f)

    for data in ['pmf', 'gr']:
        fig, ax = plt.subplots(2, 3, sharex=True, sharey=True)
        fig.set_size_inches(12, 8)

        if data == 'pmf':
            fig.supylabel('PMF [kcal/mol]')
        elif data == 'gr':
            fig.supylabel(r'$g \; (r)$')

        ax[0, 0].set_ylabel('CHARMM36')
        ax[1, 0].set_ylabel('AMOEBA')
        for i in range(3):
            ax[1, i].set_xlabel(r'$r$ ($\AA$)')
            for j in range(2):
                ax[j, i].axhline(color='black', linewidth=0.5)

        for i, cation in enumerate(['guan', 'imim', 'mamm']):
            ax[0, i].set_title(cation_names[cation])
            for j, anion in enumerate(['acet', 'esna', 'mso4']):
                for k, engine in enumerate(['namd', 'openmm']): # enumerate(['gromacs', 'openmm']):
                    if engine == 'namd':
                        data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force/{anion}_{cation}'
                    else:
                        data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'
                    vals = np.loadtxt(f'{data_dir}/{data}_{text}.txt')
                    ax[k, i].plot(vals[:,0], vals[:,1], label=anion_names[anion])
                    ax[k, i].fill_between(vals[:,0], vals[:,1]-2*vals[:,2],
                                          vals[:,1]+2*vals[:,2], alpha=0.3)
                    if show_rshell:
                        r = rshell_data[engine][f'{anion}_{cation}']
                        row = (np.abs(vals[:,0] - r)).argmin()
                        ax[k, i].plot(vals[row,0], vals[row,1], marker='o',
                                      markersize=10, color=f'C{j}', fillstyle='none')
                        ax[k, i].plot(vals[row,0], vals[row,1], marker='x',
                                      markersize=7, color='black')

        ax[0, 0].legend(handlelength=0.7, frameon=False, fontsize=16)
        ax[0, 0].set_xlim(0, 15)
        if data == 'pmf':
            ax[0, 0].set_ylim(-2.2, 1.5)
        elif data == 'gr':
            pass

        my_plot.set_layout(fig, ax)
        plt.subplots_adjust(wspace=0.1, hspace=0.05)

        if show_rshell:
            fig.savefig(f'./images_v2_namd/charmm_comparison_6_{data}_with_rshell.png', dpi=300)
        else:
            fig.savefig(f'./images_v2_namd/charmm_comparison_6_{data}.png', dpi=300)
