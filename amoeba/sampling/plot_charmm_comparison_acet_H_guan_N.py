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

engine_ff = {'gromacs':'CHARMM36', 'namd':'CHARMM36', 'namd_scaled':'CHARMM36 + ECC', 'openmm':'AMOEBA'}

for data in ['pmf', 'gr']:
    fig, ax = my_plot.instantiate_fig()
    ax.set_xlabel(r'$r$ ($\AA$)')
    ax.axhline(color='black', linewidth=0.5)

    if data == 'pmf':
        ax.set_ylabel('PMF [kcal/mol]')
    elif data == 'gr':
        ax.set_ylabel(r'$g_{\mathsf{Acet \; H - Guan \; N}} \; (r)$')

    for k, engine in enumerate(['namd', 'namd_scaled', 'openmm']):
        if engine == 'namd':
            data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force/acet_guan'
        elif engine == 'namd_scaled':
            data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_scaled/acet_guan'
        else:
            data_dir = f'/home/chase/namd/{engine}/ion_pairs/acet_guan'
        vals = np.loadtxt(f'{data_dir}/{data}_acet_H_guan_N.txt')
        ax.plot(vals[:,0], vals[:,1], label=engine_ff[engine])

    ax.legend(handlelength=0.7, frameon=False, fontsize=16)
    ax.set_xlim(0, 10)
    if data == 'pmf':
        ax.set_ylim(-2.2, 1.5)
    elif data == 'gr':
        pass

    my_plot.set_layout(fig, ax)
    fig.savefig(f'./images_v2_namd/charmm_comparison_acet_H_guan_N_{data}.png', dpi=300)
