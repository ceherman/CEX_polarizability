import numpy as np
import pandas as pd
import os
import sys
import json
import math
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot
fig, ax = my_plot.instantiate_fig()
plt.close()

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'acetate', 'esna':'ethylsulfonate', 'mso4':'methylsulfate'}

data_names = [('pmf', 'PMF'), ('w_solv', r'$W_{Indirect}$'), ('direct', r'$U_{Direct}$'),
              ('elect', r'$U_{Elect}$'), ('vdw', r'$U_{VdW}$'), ('polar', r'$U_{Polar}$')]

fig, ax = plt.subplots(2, 3, sharex=True)
fig.set_size_inches(22, 12, forward=True)
fig.supylabel(r'Energy at $r = \langle r_{\mathsf{PMF \; min}} \rangle_{\mathsf{FF}}$ [kcal/mol]')

n_rows = 2
for d, (entry, label) in enumerate(data_names):
    ax[d%n_rows, math.floor(d/n_rows)].set_ylabel(label, fontsize=22)

    df_all = pd.DataFrame()
    for i, anion in enumerate(['acet', 'esna', 'mso4']):
        for j, cation in enumerate(['guan', 'imim', 'mamm']):
            index = i*3 + j
            df_all.at[index, 'anion'] = anion
            df_all.at[index, 'cation'] = cation
            df_all.at[index, 'pair_name'] = f'{cation_names[cation]} {anion_names[anion]}'

            data_dir = f'{anion}_{cation}'
            df_amoeba = pd.read_csv(f'./{data_dir}/final_clean.csv')
            df_charmm = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force/{data_dir}/final_clean_pme_off.csv')
            df_ecc = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force_scaled/{data_dir}/final_clean_pme_off.csv')
            for df in [df_charmm, df_ecc]:
                df['polar'] = 0.0
                df['polar_seom'] = 0.0

            r_pmf_min = 0.0
            for df in [df_amoeba, df_charmm, df_ecc]:
                r_pmf_min += df.loc[df['pmf'] == df['pmf'].min(), 'r'].iloc[0]
            r_pmf_min /= 3.0

            for df, name in [(df_amoeba, 'amoeba'), (df_charmm, 'charmm'), (df_ecc, 'ecc')]:
                r_pmf_min_index = df.iloc[(df['r'] - r_pmf_min).abs().argsort()].index[0]
                df_all.at[index, name] = df.at[r_pmf_min_index, entry]
                df_all.at[index, f'{name}_seom'] = df.at[r_pmf_min_index, f'{entry}_seom']

    width = 0.25
    ax[d%n_rows, math.floor(d/n_rows)].set_xticks(df_all.index)
    for k, (name, label) in enumerate([('charmm', 'CHARMM36'), ('amoeba', 'AMOEBA'), ('ecc', 'CHARMM36+ECC')]):
        ax[d%n_rows, math.floor(d/n_rows)].bar(df_all.index-width+k*width, df_all[f'{name}'], width, label=label)
        # ax[d%n_rows, math.floor(d/n_rows)].errorbar(df_all.index-width+k*width, df_all[f'{name}'], yerr=2*df_all[f'{name}_seom'], fmt=' ', color='black', capsize=5)
    ax[d%n_rows, math.floor(d/n_rows)].axhline(color='black', linewidth=0.5)


for i in range(3):
    ax[1, i].set_xticklabels(df_all.pair_name, rotation=40, ha='right', rotation_mode='anchor', fontsize=16)

ax[0, 2].legend(loc='best', fontsize=18, frameon=False, handletextpad=0.8, handlelength=1)
plt.tight_layout()
plt.subplots_adjust(hspace=0.00, wspace=0.3)
# plt.show()
fig.savefig(f'./images_v2_namd/bar_pmf_contributions_subplots.png', dpi=300)
