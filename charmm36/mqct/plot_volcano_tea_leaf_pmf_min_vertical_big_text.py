import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

fig, ax = my_plot.instantiate_fig(fontsize=32)
plt.close()

fig, ax = plt.subplots(2, 1, sharex=True, sharey=True)
fig.set_size_inches(8, 16)
font = {'weight': 'normal', 'size':32}
plt.rc('font', **font)
ax[0].set_title("CHARMM36", pad=-40, fontsize=32)
ax[1].set_title("AMOEBA", pad=-40, fontsize=32)
ax[1].set_xlabel(r'$\mu^{ex}_{Anion} - \mu^{ex}_{Cation}$ [kcal/mol]', labelpad=10)

for i in range(2):
    ax[i].set_ylabel(r'-1 $\times$ PMF min [kcal/mol]', labelpad=15)
    ax[i].tick_params(axis='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)
    ax[i].set_xlim(-55, 15)
    ax[i].set_ylim(0, 2.5)
    # ax[i].set_xticks([-50, -40, -30, -20, -10, 0, 10])
    ax[i].axvline(x=0, color='grey', linewidth=1)

df_Ka_charmm = pd.read_csv('./Ka_vs_hydration_diff_tip.csv')
df_Ka_amoeba = pd.read_csv('~/namd/openmm/mqct/Ka_vs_hydration_diff.csv')

cations = ['guan', 'imim', 'mamm']
anions = ['acet', 'esna', 'mso4']
ion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate', 'guan':'guanidinium', 'mamm':'methylammonium', 'imim':'imidazolium'}
colors = {'guan':'red', 'imim':'blue', 'mamm':'limegreen'}
markers = {'acet':'v', 'esna':'s', 'mso4':'D'}

for cation in cations:
    for anion in anions:
        label = ion_names[anion] + '\n' + ion_names[cation]
        color = colors[cation]
        marker = markers[anion]

        for i, df in enumerate([df_Ka_charmm, df_Ka_amoeba]):
            df_temp = df.loc[(df.anion == anion) & (df.cation == cation)].copy()
            df_temp.reset_index(drop=True, inplace=True)

            x = df_temp.at[0, 'anion_minus_cation_hydration']
            y = -1 * df_temp.at[0, 'pmf_min']
            xerr = df_temp.at[0, 'anion_minus_cation_hydration_err']
            yerr = df_temp.at[0, 'pmf_min_seom']

            ax[i].scatter(x, y, marker=marker, color=color, label=label, s=65)
            # ax[i].errorbar(x, y, xerr=2*xerr, yerr=2*yerr, fmt=' ', color=color, capsize=5, alpha=0.3)

plt.subplots_adjust(hspace=0.15)

plt.savefig('./images/volcano_tea_leaf_pmf_min_vertical_big_text.png', dpi=300, bbox_inches='tight')
