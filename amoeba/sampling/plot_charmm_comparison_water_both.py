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

for data in ['pmf', 'gr']:
    fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
    fig.set_size_inches(12, 11)

    if data == 'pmf':
        fig.supylabel('PMF [kcal/mol]')
    elif data == 'gr':
        fig.supylabel(r'$g \; (r)$')

    for i in range(3):
        ax[2, i].set_xlabel(r'$r$ ($\AA$)')
        for j in range(3):
            ax[j, i].axhline(color='black', linewidth=0.5)

    for j, anion in enumerate(['acet', 'esna', 'mso4']):
        ax[j,0].set_ylabel(ion_names[anion])
        for i, cation in enumerate(['guan', 'imim', 'mamm']):
            if j == 0:
                ax[0, i].set_title(ion_names[cation])
            for ion in [anion, cation]:
                for k, engine in enumerate(['namd', 'openmm']):
                    if engine == 'namd':
                        data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force/{anion}_{cation}'
                    else:
                        data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'
                    vals = np.loadtxt(f'{data_dir}/{data}_water_{ion}.txt')
                    ax[j, i].plot(vals[:,0], vals[:,1], label=f'{engine_ff[engine]} {ion_names[ion]}')
                ax[j, i].legend(handlelength=0.6, frameon=False, fontsize=11)

    ax[0, 0].set_xlim(0, 16)
    if data == 'pmf':
        ax[0, 0].set_ylim(-1.1, 1.1)
    elif data == 'gr':
        pass
    my_plot.set_layout(fig, ax)
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    fig.savefig(f'./images_v2_namd/charmm_comparison_water_both_{data}.png', dpi=300)
