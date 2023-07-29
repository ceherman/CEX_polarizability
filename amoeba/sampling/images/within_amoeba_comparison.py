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
    ax.plot(r_vals, means, label=label, ls=ls)
    ax.fill_between(r_vals, means-2*seom, means+2*seom, alpha=0.3)
    return

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}

for k, (entry, label) in enumerate([('pmf', 'PMF'),
                                    ('elect', r'$U_{Elect}$'),
                                    ('vdw', r'$U_{VdW}$'),
                                    ('direct', r'$U_{Total}$'),
                                    ('w_solv', r'$W_{Solv}$'),
                                    ('polar', r'$U_{Polar}$')]):
    fig, ax = plt.subplots(1, 3, sharex=True, sharey=True)
    fig.set_size_inches(12, 5.5)
    ax[0].set_ylabel(f'{label} [kcal/mol]')

    for i in range(3):
        ax[i].set_xlabel(r'$r$ (\AA)')
        ax[i].axhline(color='black', linewidth=0.5)
        ax[i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)


    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        ax[i].set_title(cation_names[cation])

        for j, anion in enumerate(['acet', 'esna', 'mso4']):
            data_dir = f'{anion}_{cation}'
            df_amoeba = pd.read_csv(f'../{data_dir}/final_clean.csv')

            plot_with_seom(ax[i], df_amoeba['r'], df_amoeba[f'{entry}'], df_amoeba[f'{entry}_seom'], label=anion_names[anion])
            if entry == 'vdw':
                ax[i].set_ylim(-2.5, 10)
            elif entry == 'elect' or entry == 'direct':
                ax[i].set_ylim(-140, 0)
            elif entry == 'w_solv':
                ax[i].set_ylim(0, 140)
            elif entry == 'pmf':
                ax[i].set_ylim(-2, 1)
            elif entry == 'polar':
                ax[i].set_ylim(-30, 0)

    ax[0].legend(handlelength=0.7, frameon=False, fontsize=20, handletextpad=0.5)
    ax[0].set_xlim(2.5, 12)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.05)

    fig.savefig(f'./images/within_amoeba_anion_comparison_{entry}.eps', bbox_inches='tight')
    fig.savefig(f'./images/within_amoeba_anion_comparison_{entry}.pdf', bbox_inches='tight')
    fig.savefig(f'./images/within_amoeba_anion_comparison_{entry}.png', dpi=300, bbox_inches='tight')

