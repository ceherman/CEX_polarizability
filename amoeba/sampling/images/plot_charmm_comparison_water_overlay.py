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

ions = ['acet', 'esna', 'mso4', 'guan', 'imim', 'mamm']
anions = ['acet', 'esna', 'mso4']
cations = ['guan', 'imim', 'mamm']

ion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate', 'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
engine_ff = {'namd':'CHARMM36', 'openmm':'AMOEBA', 'namd_scaled':'CHARMM36 + ECC'}
engine_colors = {'namd':'blue', 'openmm':'red', 'namd_scaled':'limegreen'}


for data in ['pmf', 'gr']:
    fig, ax = plt.subplots(3, 2, sharex=True, sharey=True)
    fig.set_size_inches(9, 12, forward=True)

    for i in range(2):
        ax[2, i].set_xlabel(r'$r$ [\AA]')
        for j in range(3):
            ax[j, i].axhline(color='black', linewidth=0.5)
            ax[j, i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)
            if data == 'pmf':
                ax[j, 0].set_ylabel('PMF [kcal/mol]')
            elif data == 'gr':
                ax[j, 0].set_ylabel(r'$g \; (r)$')

    for i, anion in enumerate(anions):
        ax[i, 0].text(0.6, 0.88, ion_names[anion], horizontalalignment='center', transform=ax[i, 0].transAxes)
        for m, cation in enumerate(cations):
            for k, engine in enumerate(['namd', 'openmm', 'namd_scaled']):
                if engine == 'namd':
                    data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{anion}_{cation}'
                elif engine == 'namd_scaled':
                    data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{anion}_{cation}'
                else:
                    data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'

                vals = np.loadtxt(f'{data_dir}/{data}_water_{anion}.txt')
                if m == 0:
                    ax[i, 0].plot(vals[:,0], vals[:,1], label=f'{engine_ff[engine]}', color=engine_colors[engine])
                else:
                    ax[i, 0].plot(vals[:,0], vals[:,1], color=engine_colors[engine])

    for i, cation in enumerate(cations):
        ax[i, 1].text(0.6, 0.88, ion_names[cation], horizontalalignment='center', transform=ax[i, 1].transAxes)
        for m, anion in enumerate(anions):
            for k, engine in enumerate(['namd', 'openmm', 'namd_scaled']):
                if engine == 'namd':
                    data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{anion}_{cation}'
                elif engine == 'namd_scaled':
                    data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{anion}_{cation}'
                else:
                    data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'

                vals = np.loadtxt(f'{data_dir}/{data}_water_{cation}.txt')
                if m == 0:
                    ax[i, 1].plot(vals[:,0], vals[:,1], label=f'{engine_ff[engine]}', color=engine_colors[engine])
                else:
                    ax[i, 1].plot(vals[:,0], vals[:,1], color=engine_colors[engine])

    ax[0, 0].set_xlim(2, 12)
    if data == 'pmf':
        ax[0, 0].set_ylim(-0.7, 0.6)

    leg = ax[0, 0].legend(handlelength=0.6, frameon=False, fontsize=16, loc='lower right')
    for line in leg.get_lines():
        line.set_linewidth(2.0)

    plt.subplots_adjust(wspace=0.05, hspace=0.05)

    fig.savefig(f'./images/charmm_comparison_water_overlay_{data}.png', dpi=300, bbox_inches='tight')
    fig.savefig(f'./images/charmm_comparison_water_overlay_{data}.pdf', bbox_inches='tight')
