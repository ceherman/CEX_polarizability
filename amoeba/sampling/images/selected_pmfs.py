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

fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
fig.set_size_inches(8, 5)

data = 'pmf'
ax[0].set_ylabel('PMF [kcal/mol]')
ax[0].set_title('Guanidinium\nacetate')
ax[1].set_title('Imidazolium\nmethylsulfate')

for i in range(2):
    ax[i].set_xlabel(r'$r$  [$\rm{\AA}$]')
    ax[i].axhline(color='black', linewidth=0.5)
    ax[i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)

for i, pair in enumerate([('guan', 'acet'), ('imim', 'mso4')]):
    cation, anion = pair

    for k, engine in enumerate(['namd_tip', 'openmm', 'namd_tip_scaled']):
        if engine == 'namd_tip':
            data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{anion}_{cation}'
        elif engine == 'namd_tip_scaled':
            data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{anion}_{cation}'
        else:
            data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'

        vals = np.loadtxt(f'{data_dir}/{data}_{text}.txt')
        ax[i].plot(vals[:,0], vals[:,1], label=engine_ff[engine], color=colors[engine])
        ax[i].fill_between(vals[:,0], vals[:,1]-2*vals[:,2], vals[:,1]+2*vals[:,2], alpha=0.3, color=colors[engine])

        r = rshell_data[engine][f'{anion}_{cation}']
        row = (np.abs(vals[:,0] - r)).argmin()
        ax[i].plot(vals[row,0], vals[row,1], marker='o', color='black', markersize=4)

        if engine == 'namd_tip_scaled' and cation == 'imim':
            r = rshell_data['namd_tip_scaled_app'][f'{anion}_{cation}']
            row = (np.abs(vals[:,0] - r)).argmin()
            ax[i].plot(vals[row,0], vals[row,1], marker='s', color='black', markersize=7, fillstyle='none')

leg = ax[1].legend(handlelength=0.7, frameon=False, fontsize=15, loc='lower right')
for line in leg.get_lines():
    line.set_linewidth(2.0)

ax[0].set_xlim(2.5, 10.5)
ax[0].set_ylim(-2.3, 1.5)

my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05)

fig.savefig(f'./tsrc_selected_images/selected_pmfs.png', dpi=300, bbox_inches='tight')

