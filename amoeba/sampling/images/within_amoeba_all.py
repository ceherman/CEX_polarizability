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
    ax.plot(r_vals, means, label=label, ls=ls, color=color)
    ax.fill_between(r_vals, means-2*seom, means+2*seom, alpha=0.3, color=color)
    return

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}
anion_colors = {'acet':'red', 'esna':'blue', 'mso4':'limegreen'}

fig, ax = plt.subplots(6, 3, sharex=True, sharey='row')
fig.set_size_inches(16, 24)

for i in range(3):
    ax[5, i].set_xlabel(r'$r$ [\AA]')
    for j in range(5):
        ax[j, i].axhline(color='black', linewidth=0.5)
        ax[j, i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)

for i, cation in enumerate(['guan', 'imim', 'mamm']):
    ax[0, i].set_title(cation_names[cation])

for k, (entry, label) in enumerate([('pmf', 'PMF'),
                                    ('w_solv', r'$W_{Solv}$'),
                                    ('direct', r'$U_{Total}$'),
                                    ('elect', r'$U_{Elect}$'),
                                    ('vdw', r'$U_{VdW}$'),
                                    ('polar', r'$U_{Polar}$')]):
    ax[k, 0].set_ylabel(f'{label} [kcal/mol]')

    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        for j, anion in enumerate(['acet', 'esna', 'mso4']):
            data_dir = f'{anion}_{cation}'
            df_amoeba = pd.read_csv(f'../{data_dir}/final_clean.csv')

            plot_with_seom(ax[k, i], df_amoeba['r'], df_amoeba[f'{entry}'], df_amoeba[f'{entry}_seom'], label=anion_names[anion], color=anion_colors[anion])
            if entry == 'vdw':
                ax[k, i].set_ylim(-2.5, 10)
            elif entry == 'elect' or entry == 'direct':
                ax[k, i].set_ylim(-140, 0)
            elif entry == 'w_solv':
                ax[k, i].set_ylim(0, 140)
            elif entry == 'pmf':
                ax[k, i].set_ylim(-2, 1)
            elif entry == 'polar':
                ax[k, i].set_ylim(-30, 0)

leg = ax[0, 0].legend(handlelength=0.7, frameon=False, fontsize=24, handletextpad=0.5)
for line in leg.get_lines():
    line.set_linewidth(2.0)

ax[0, 0].set_xlim(2.5, 12)
plt.tight_layout()
plt.subplots_adjust(wspace=0.05, hspace=0.07)

# fig.savefig(f'./images/within_amoeba_anion_comparison_{entry}.eps', bbox_inches='tight')
fig.savefig(f'./images/within_amoeba_anion_comparison_all.pdf', bbox_inches='tight')
fig.savefig(f'./images/within_amoeba_anion_comparison_all.png', dpi=300, bbox_inches='tight')

