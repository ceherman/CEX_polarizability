import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot
fig, ax = my_plot.instantiate_fig()
plt.close()

def plot_diff_from_amoeba(ax, df, column, label=None, color=None, ls=None):
    diff = df[f'{column}_r_amoeba'].values - df_amoeba[column].values
    seom = np.sqrt((df[f'{column}_seom_r_amoeba'].values)**2 + (df_amoeba[f'{column}_seom'].values)**2)
    ax.plot(r_amoeba, diff, label=label, color=color, ls=ls)
    ax.fill_between(r_amoeba, diff-2*seom, diff+2*seom, alpha=0.3, color=color)
    return

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}
prop_names = {'pmf':'PMF', 'direct':'Direct', 'w_solv':'Indirect', 'elect':'Elect.', 'vdw':'VdW', 'polar':'Polar'}

fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
fig.set_size_inches(12, 11)
fig.supylabel(r'$\xi_{CHARMM36} - \xi_{AMOEBA}$ [kcal/mol]')

for i in range(3):
    ax[2, i].set_xlabel(r'$r$ ($\AA$)')
    for j in range(3):
        ax[j, i].axhline(color='black', linewidth=0.5)

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    ax[j,0].set_ylabel(anion_names[anion])
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        if j == 0:
            ax[0, i].set_title(cation_names[cation])

        data_dir = f'{anion}_{cation}'
        df_amoeba = pd.read_csv(f'./{data_dir}/final_clean.csv')
        df_charmm = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force/{data_dir}/final_clean_pme_off.csv')
        df_charmm['polar'] = 0.0
        df_charmm['polar_seom'] = 0.0

        r_amoeba = df_amoeba['r'].values
        df_charmm['r_amoeba'] = r_amoeba

        interp_columns = ['pmf', 'direct', 'w_solv', 'elect', 'vdw', 'polar']
        interp_columns_seom = [f'{column}_seom' for column in interp_columns]
        kind = 'linear'
        for column in interp_columns + interp_columns_seom:
            spline_charmm = interp1d(df_charmm['r'].values, df_charmm[column].values, kind=kind, bounds_error=False)
            df_charmm[f'{column}_r_amoeba'] = spline_charmm(r_amoeba)

        for k, column in enumerate(interp_columns):
            plot_diff_from_amoeba(ax[j, i], df_charmm, column, color=f'C{k}', ls='-', label=r'$\xi = $' + f'{prop_names[column]}')

ax[0, 0].set_xlim(2.8, 8)
ax[0, 2].legend(handlelength=1, frameon=False, fontsize=12, loc='lower right', bbox_to_anchor=(1.04, -0.03), ncol=2)
plt.tight_layout()
plt.subplots_adjust(wspace=0.05, hspace=0.05)
fig.savefig(f'./images_v2_namd/energy_contributions_comparison_diff_all.png', dpi=300)
