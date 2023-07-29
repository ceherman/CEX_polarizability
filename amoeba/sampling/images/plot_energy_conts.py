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

def plot_with_seom(ax, r_vals, means, seom, label=None, color=None, ls=None):
    ax.plot(r_vals, means, label=label, color=color, ls=ls)
    ax.fill_between(r_vals, means-2*seom, means+2*seom, alpha=0.3, color=color)
    return

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}

for k, (entry, label) in enumerate([('elect', r'$U_{Elect}$'),
                                    ('vdw', r'$U_{VdW}$'),
                                    ('direct', r'$U_{Total}$'),
                                    ('w_solv', r'$W_{Solv}$')]):
    fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
    fig.set_size_inches(12, 11)
    fig.supylabel(f'{label} [kcal/mol]')

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

            data_dir = f'{anion}_{cation}'
            df_amoeba = pd.read_csv(f'../{data_dir}/final_clean.csv')
            df_charmm = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{data_dir}/final_clean_pme_off.csv')
            df_ecc = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{data_dir}/final_clean_pme_off_scaled_up.csv')

            plot_with_seom(ax[j, i], df_charmm['r'], df_charmm[f'{entry}'], df_charmm[f'{entry}_seom'], label=f'CHARMM36', color='blue')
            plot_with_seom(ax[j, i], df_amoeba['r'], df_amoeba[f'{entry}'], df_amoeba[f'{entry}_seom'], label=f'AMOEBA', color='red')
            plot_with_seom(ax[j, i], df_ecc['r'], df_ecc[f'{entry}'], df_ecc[f'{entry}_seom'], label=f'CHARMM36 + ECC', color='limegreen')

            if entry == 'vdw':
                ax[j, i].set_ylim(-2.5, 10)
            elif entry == 'elect' or entry == 'direct':
                ax[j, i].set_ylim(-125, 0)
            elif entry == 'w_solv':
                ax[j, i].set_ylim(0, 140)

    leg = ax[0, 0].legend(handlelength=0.7, frameon=False, fontsize=16, handletextpad=0.5)
    for line in leg.get_lines():
        line.set_linewidth(2.0)

    for line in leg.get_lines():
        line.set_linewidth(2.0)

    ax[0, 0].set_xlim(2.8, 17)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.05, hspace=0.05)

    fig.savefig(f'./images/energy_conts_{entry}.eps', bbox_inches='tight')
    fig.savefig(f'./images/energy_conts_{entry}.pdf', bbox_inches='tight')
    fig.savefig(f'./images/energy_conts_{entry}.png', dpi=300, bbox_inches='tight')

