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

ion_names = {
    'guan':'Guanidinium',
    'mamm':'Methylammonium',
    'imim':'Imidazolium',
    'acet':'Acetate',
    'esna':'Ethylsulfonate',
    'mso4':'Methylsulfate'
}
engine_ff = {
    'gromacs':'CHARMM36',
    'namd':'CHARMM36',
    'openmm':'AMOEBA'
}
engine_colors = {'namd':'blue', 'openmm':'red'}


for data in ['pmf', 'gr']:
    fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
    fig.set_size_inches(12, 11)

    for i in range(3):
        ax[2, i].set_xlabel(r'$r$ (\AA)')
        for j in range(3):
            ax[j, i].axhline(color='black', linewidth=0.5)
            ax[j, i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)

    for j, anion in enumerate(['acet', 'esna', 'mso4']):
        ax[j,0].set_ylabel(ion_names[anion])
        for i, cation in enumerate(['guan', 'imim', 'mamm']):
            if j == 0:
                ax[0, i].set_title(ion_names[cation])
            for k, engine in enumerate(['namd', 'openmm']):
                if engine == 'namd':
                    data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{anion}_{cation}'
                else:
                    data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'

                for ion in [cation]:
                    vals = np.loadtxt(f'{data_dir}/{data}_water_{ion}.txt')
                    ax[j, i].plot(vals[:,0], vals[:,1], label=f'{engine_ff[engine]}\n{ion_names[ion]}', color=engine_colors[engine])
                ax[j, i].legend(handlelength=0.6, frameon=False, fontsize=16)

    ax[0, 0].set_xlim(0, 16)
    if data == 'pmf':
        ax[0, 0].set_ylim(-0.65, 0.6)

    if data == 'pmf':
        st = fig.supylabel('PMF [kcal/mol]')
    elif data == 'gr':
        st = fig.supylabel(r'$g \; (r)$')

    plt.subplots_adjust(wspace=0.05, hspace=0.05)

    fig.savefig(f'./images/charmm_comparison_water_cation_{data}.png', dpi=300, bbox_extra_artists=[st], bbox_inches='tight')
    fig.savefig(f'./images/charmm_comparison_water_cation_{data}.pdf', bbox_extra_artists=[st], bbox_inches='tight')
