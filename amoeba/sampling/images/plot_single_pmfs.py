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
engine_ff = {'namd_tip':'CHARMM36', 'namd_tip_scaled':'CHARMM36 + ECC', 'openmm':'AMOEBA'}
text = 'central_atoms'
colors = {'openmm':'red', 'namd_tip':'blue', 'namd_tip_scaled':'limegreen'}

f = open('../rshell.json')
rshell_data = json.load(f)

data = 'pmf'

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    for i, cation in enumerate(['guan', 'imim', 'mamm']):

        fig, ax = my_plot.instantiate_fig(xlabel=r'$r \; \; [\rm{\AA}]$', ylabel='PMF [kcal/mol]', fontsize=24)
        ax.axhline(color='black', linewidth=0.5)
        ax.tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)

        for k, engine in enumerate(['namd_tip', 'openmm', 'namd_tip_scaled']):
            if engine == 'namd_tip':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{anion}_{cation}'
            elif engine == 'namd_tip_scaled':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{anion}_{cation}'
            else:
                data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'

            vals = np.loadtxt(f'{data_dir}/{data}_{text}.txt')
            ax.plot(vals[:,0], vals[:,1], label=engine_ff[engine], color=colors[engine])
            ax.fill_between(vals[:,0], vals[:,1]-2*vals[:,2], vals[:,1]+2*vals[:,2], alpha=0.3, color=colors[engine])

            r = rshell_data[engine][f'{anion}_{cation}']
            row = (np.abs(vals[:,0] - r)).argmin()
            ax.plot(vals[row,0], vals[row,1], marker='o', color='black', markersize=4)

            if engine == 'namd_tip_scaled' and cation == 'imim':
                r = rshell_data['namd_tip_scaled_app'][f'{anion}_{cation}']
                row = (np.abs(vals[:,0] - r)).argmin()
                ax.plot(vals[row,0], vals[row,1], marker='s', color='black', markersize=7, fillstyle='none')

        leg = ax.legend(handlelength=0.7, frameon=False, fontsize=24, loc='upper right')
        for line in leg.get_lines():
            line.set_linewidth(2.0)

        ax.set_xlim(2.5, 10.5)
        # ax.set_ylim(-2.3, 1.5)
        ax.set_ylim(-1, 1)

        my_plot.set_layout(fig, ax)
        fig.savefig(f'./images/pmfs_single_{cation}_{anion}.png', dpi=300, bbox_inches='tight')

