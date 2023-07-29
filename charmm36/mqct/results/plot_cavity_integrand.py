import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

fig, ax = my_plot.instantiate_fig_roman(fontsize=20)
plt.close()

ion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate', 'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
ions = ['acet', 'esna', 'mso4', 'guan', 'imim', 'mamm']

amoeba_path = '/home/chase/namd/openmm/mqct/b_cavity'
charmm_path = '/home/chase/namd/ion_pairs/cgenff/mqct_for_darwin_tip/e_cavity'
columns = ['r', 'force', 'seom', 'ignore']

fig, ax = plt.subplots(3, 2, sharex=True, sharey=True)
fig.set_size_inches(9, 12, forward=True)

for i in range(2):
    ax[2, i].set_xlabel(r'$\lambda$ [\AA]')
for i in range(3):
    ax[i, 0].set_ylabel('Force [kcal/(mol \AA)]', labelpad=15)
    for j in range(2):
        ax[i, j].tick_params(axis='both', which='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)

for i, ion in enumerate(ions):
    if i < 3:
        j, k = i, 0
    else:
        j, k = i-3, 1
    ax[j, k].text(0.07, 0.88, ion_names[ion], horizontalalignment='left', transform=ax[j, k].transAxes)

    df_amoeba = pd.read_fwf(f'{amoeba_path}/{ion}/force.dat', header=None)
    df_charmm = pd.read_fwf(f'{charmm_path}/{ion}/force.dat', header=None)
    df_amoeba.columns = columns
    df_charmm.columns = columns

    ax[j, k].errorbar(df_charmm['r'], df_charmm['force'], yerr=2*df_charmm['seom'], fmt='-o', capsize=5, markersize=5, label='CHARMM36')
    ax[j, k].errorbar(df_amoeba['r'], df_amoeba['force'], yerr=2*df_amoeba['seom'], fmt='-o', capsize=5, markersize=5, label='AMOEBA')

ax[0, 0].legend(frameon=False, loc='center left', handletextpad=0.5, fontsize=16, handlelength=1)
plt.subplots_adjust(wspace=0.05, hspace=0.15)

ax[0, 0].set_ylim(0, None)
ax[0, 0].set_xlim(0, 5.1)

plt.savefig(f'./images/cavity_integrand.png', dpi=300, bbox_inches='tight')
plt.savefig(f'./images/cavity_integrand.pdf', bbox_inches='tight')

