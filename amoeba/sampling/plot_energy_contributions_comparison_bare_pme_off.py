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

def plot_with_seom(ax, r_vals, means, seom, label=None, color=None, ls=None):
    ax.plot(r_vals, means, label=label, color=color, ls=ls)
    ax.fill_between(r_vals, means-2*seom, means+2*seom, alpha=0.3, color=color)
    return

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}

fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
fig.set_size_inches(15, 11)
fig.supylabel('Energy [kcal/mol]')
for i in range(3):
    ax[2, i].set_xlabel(r'$r$ ($\AA$)')
    for j in range(3):
        ax[j, i].axhline(color='black', linewidth=0.5)

data_names = [('pmf', 'PMF'), ('direct', r'$U_{Direct}$'), ('w_solv', r'$W_{Indirect}$')]

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    ax[j,0].set_ylabel(anion_names[anion])
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        if j == 0:
            ax[0, i].set_title(cation_names[cation])

        data_dir = f'{anion}_{cation}'
        df_amoeba = pd.read_csv(f'./{data_dir}/final_clean.csv')
        df_charmm = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force/{data_dir}/final_clean_pme_off.csv')
        df_ecc = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force_scaled/{data_dir}/final_clean_pme_off.csv')

        for k, (entry, label) in enumerate(data_names):
            plot_with_seom(ax[j, i], df_charmm['r'], df_charmm[f'{entry}'], df_charmm[f'{entry}_seom'], color=f'C{k}', ls='-', label=f'{label} CHARMM36')
            plot_with_seom(ax[j, i], df_ecc['r'], df_ecc[f'{entry}'], df_ecc[f'{entry}_seom'], color=f'C{k}', ls=':',  label=f'{label} ECC')
            plot_with_seom(ax[j, i], df_amoeba['r'], df_amoeba[f'{entry}'], df_amoeba[f'{entry}_seom'], color=f'C{k}', ls='--', label=f'{label} AMOEBA')

ax[0, 0].set_xlim(2.8, 17)
ax[0, 2].legend(handlelength=1, frameon=False, fontsize=16, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.subplots_adjust(wspace=0.05, hspace=0.05)
fig.savefig(f'./images_v2_namd/energy_contributions_comparison_bare_pme_off.png', dpi=300)
