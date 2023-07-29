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
engine_ff = {'namd_tip':'CHARMM36', 'namd_tip_scaled':'CHARMM36 + ECC', 'openmm':'AMOEBA'}
text = 'central_atoms'
colors = {'openmm':'red', 'namd_tip':'blue', 'namd_tip_scaled':'limegreen'}

f = open('../rshell.json')
rshell_data = json.load(f)

data = 'pmf'

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    for i, cation in enumerate(['guan', 'imim', 'mamm']):

        fig, ax = plt.subplots(2, 1, sharex=True, sharey=False)
        fig.set_size_inches(8, 12)
        for i in range(2):
            ax[i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)

        font = {'weight': 'normal', 'size': 32}
        plt.rc('font', **font)

        ax[1].set_xlabel(r'$r \; \; [\rm{\AA}]$')
        ax[0].set_ylabel(r'$W_{Solv}$')
        ax[1].set_ylabel(r'$U_{In \; vacuo}$')

        for i, entry in enumerate(['w_solv', 'direct']):

            data_dir = f'{anion}_{cation}'
            df_amoeba = pd.read_csv(f'../{data_dir}/final_clean.csv')
            df_charmm = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{data_dir}/final_clean_pme_off.csv')
            df_ecc = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{data_dir}/final_clean_pme_off_scaled_up.csv')

            plot_with_seom(ax[i], df_charmm['r'], df_charmm[f'{entry}'], df_charmm[f'{entry}_seom'], label=f'CHARMM36', color='blue')
            plot_with_seom(ax[i], df_amoeba['r'], df_amoeba[f'{entry}'], df_amoeba[f'{entry}_seom'], label=f'AMOEBA', color='red')
            plot_with_seom(ax[i], df_ecc['r'], df_ecc[f'{entry}'], df_ecc[f'{entry}_seom'], label=f'CHARMM36 + ECC', color='limegreen')

        leg = ax[0].legend(handlelength=0.7, handletextpad=0.5, frameon=False, fontsize=27, loc='lower left')
        for line in leg.get_lines():
            line.set_linewidth(2.0)

        ax[0].set_xlim(2.5, 10.5)
        ax[0].set_ylim(0, 110)
        ax[1].set_ylim(-110, 0)

        my_plot.set_layout(fig, ax)
        fig.savefig(f'./images/pmfs_single_wsolv_vs_utotal_{cation}_{anion}.png', dpi=300, bbox_inches='tight')

