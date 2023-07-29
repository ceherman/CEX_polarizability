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

df = pd.read_csv(f'../results_Ka_gr_tip.csv')

# cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}

fig, ax = plt.subplots(1, 3, sharey=True, gridspec_kw={'width_ratios':[1, 1, 4/3]})
fig.set_size_inches(14, 7)
ax[0].set_title("CHARMM36")
ax[1].set_title("AMOEBA")
ax[2].set_title("CHARMM36 + ECC")
ax[0].set_ylabel(r'$K_{A}$ [M$^{-1}$]', labelpad=15)

x = np.arange(3)
x_ecc = np.arange(4)
rotation = 30

for i in range(2):
    ax[i].set_xticks(x)
    ax[i].set_xticklabels(['Guanidinium', 'Imidazolium', 'Methylammonium'], rotation=rotation, ha='right', rotation_mode='anchor')

ax[2].set_xticks(x_ecc)
ax[2].set_xticklabels(['Guanidinium', r'Imidazolium (comp. $R_{Shell}$)', r'Imidazolium (app. $R_{Shell}$)', 'Methylammonium'], rotation=rotation, ha='right',rotation_mode='anchor')

for i in range(3):
    ax[i].tick_params(axis='both',direction='in',length=6, bottom=True, top=False, left=True, right=True)

n_bars = 3
width = 1.0/(n_bars + 1)

for k, engine in enumerate(['namd_tip', 'openmm', 'namd_tip_scaled']):
    for j, anion in enumerate(['acet', 'esna', 'mso4']):
        df_temp = df[(df.engine == engine) & (df.anion == anion)]
        if engine == 'namd_tip_scaled':
            df_app = df[(df.engine == 'namd_tip_scaled_app') & (df.anion == anion) & (df.cation == 'imim')]
            df_temp.reset_index(drop=True, inplace=True)
            df_app.reset_index(drop=True, inplace=True)
            df_temp = pd.concat([df_temp.iloc[:2], df_app, df_temp.iloc[2:]]).reset_index(drop=True)
            vals, errs = df_temp['Ka_M-1'], df_temp['Ka_err_M-1']
            ax[k].bar(x_ecc + (j-1)*width, vals, width, label=anion_names[anion])
            ax[k].errorbar(x_ecc + (j-1)*width, vals, yerr=2*errs, fmt=' ', color='black', capsize=5)
        else:
            vals, errs = df_temp['Ka_M-1'], df_temp['Ka_err_M-1']
            ax[k].bar(x + (j-1)*width, vals, width, label=anion_names[anion])
            ax[k].errorbar(x + (j-1)*width, vals, yerr=2*errs, fmt=' ', color='black', capsize=5)

ax[0].legend(handlelength=0.7, frameon=False, handletextpad=0.5, fontsize=20)
ax[0].set_ylim(0, 2.5)
my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05)

# fig.savefig(f'./images/Ka_bar_plot_with_imim_app_non_roman.eps', bbox_inches='tight')
fig.savefig(f'./images/Ka_bar_plot_with_imim_app_non_roman.pdf', bbox_inches='tight')
fig.savefig(f'./images/Ka_bar_plot_with_imim_app_non_roman.png', dpi=300, bbox_inches='tight')
