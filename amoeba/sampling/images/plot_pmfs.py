import numpy as np
import pandas as pd
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

fig, ax = my_plot.instantiate_fig_roman()
plt.close()

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}
engine_ff = {'namd_tip':'CHARMM36', 'namd_tip_scaled':'CHARMM36 + ECC', 'openmm':'AMOEBA'}
text = 'central_atoms'
colors = {'openmm':'red', 'namd_tip':'blue', 'namd_tip_scaled':'limegreen'}

f = open('../rshell.json')
rshell_data = json.load(f)

fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
fig.set_size_inches(12, 11)

data = 'pmf'
fig.supylabel('PMF [kcal/mol]')

for i in range(3):
    ax[2, i].set_xlabel(r'$r$ [\AA]')
    for j in range(3):
        ax[j, i].axhline(color='black', linewidth=0.5)
        ax[j, i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    ax[j,0].set_ylabel(anion_names[anion])
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        if j == 0:
            ax[0, i].set_title(cation_names[cation])

        for k, engine in enumerate(['namd_tip', 'openmm', 'namd_tip_scaled']):
            if engine == 'namd_tip':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{anion}_{cation}'
            elif engine == 'namd_tip_scaled':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{anion}_{cation}'
            else:
                data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'

            vals = np.loadtxt(f'{data_dir}/{data}_{text}.txt')
            ax[j, i].plot(vals[:,0], vals[:,1], label=engine_ff[engine], color=colors[engine])
            ax[j, i].fill_between(vals[:,0], vals[:,1]-2*vals[:,2], vals[:,1]+2*vals[:,2], alpha=0.3, color=colors[engine])


            r = rshell_data[engine][f'{anion}_{cation}']
            row = (np.abs(vals[:,0] - r)).argmin()
            ax[j, i].plot(vals[row,0], vals[row,1], marker='o', color='black', markersize=4)

            if engine == 'namd_tip_scaled' and cation == 'imim':
                r = rshell_data['namd_tip_scaled_app'][f'{anion}_{cation}']
                row = (np.abs(vals[:,0] - r)).argmin()
                ax[j, i].plot(vals[row,0], vals[row,1], marker='s', color='black', markersize=7, fillstyle='none')

leg = ax[1, 1].legend(handlelength=0.7, frameon=False, fontsize=16, loc='lower right')
for line in leg.get_lines():
    line.set_linewidth(2.0)

ax[0, 0].set_xlim(2.5, 10.5)
ax[0, 0].set_ylim(-2.3, 1.5)

my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05, hspace=0.05)

fig.savefig(f'./images/pmfs.eps', bbox_inches='tight')
fig.savefig(f'./images/pmfs.pdf', bbox_inches='tight')
fig.savefig(f'./images/pmfs.png', dpi=300, bbox_inches='tight')

