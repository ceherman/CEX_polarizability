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

engine_ff = {'gromacs':'CHARMM36', 'namd_tip':'CHARMM36', 'namd_tip_scaled':'CHARMM36 + ECC', 'openmm':'AMOEBA'}
colors = {'openmm':'red', 'namd_tip':'blue', 'namd_tip_scaled':'limegreen'}

for data in ['gr']: # ['pmf', 'gr']:
    fig, ax = my_plot.instantiate_fig_roman()
    ax.set_xlabel(r'$r_{\mathsf{H-N}}$ [\AA]')

    if data == 'pmf':
        ax.set_ylabel('PMF [kcal/mol]')
    elif data == 'gr':
        ax.set_ylabel(r'$g\; (r_{\mathsf{H-N}})$', labelpad=15)

    for k, engine in enumerate(['namd_tip', 'openmm', 'namd_tip_scaled']):
        if engine == 'namd_tip':
            data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/acet_guan'
        elif engine == 'namd_tip_scaled':
            data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/acet_guan'
        else:
            data_dir = f'/home/chase/namd/{engine}/ion_pairs/acet_guan'
        vals = np.loadtxt(f'{data_dir}/{data}_acet_H_guan_N.txt')
        ax.plot(vals[:,0], vals[:,1], label=engine_ff[engine], color=colors[engine])

    leg = ax.legend(handlelength=0.7, frameon=False, fontsize=18)
    for line in leg.get_lines():
        line.set_linewidth(2.0)

    if data == 'pmf':
        ax.set_xlim(2, 10)
        ax.set_ylim(-2, 1)
        ax.axhline(color='black', linewidth=0.5)
    elif data == 'gr':
        ax.set_xlim(2, 10)
        ax.set_ylim(0, 8)

    # my_plot.set_layout(fig, ax)
    fig.savefig(f'./images/acet_H_guan_N_{data}.eps', bbox_inches='tight')
    fig.savefig(f'./images/acet_H_guan_N_{data}.pdf', bbox_inches='tight')
    fig.savefig(f'./images/acet_H_guan_N_{data}.png', dpi=300, bbox_inches='tight')
