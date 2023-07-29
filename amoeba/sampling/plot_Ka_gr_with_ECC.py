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

method = 'gr'
df = pd.read_csv(f'./results_Ka_{method}.csv')

# cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}
cations = ['Guanidinium', 'Imidazolium', 'Methylammonium']

fig, ax = plt.subplots(1, 3, sharex=True, sharey=True)
fig.set_size_inches(14, 7)
ax[0].set_ylabel(r'$K_{A}$ [M$^{-1}$]')
x = np.arange(3)
for i in range(3):
    ax[i].set_xticks(x)
    ax[i].set_xticklabels(cations, rotation=30, ha='right', rotation_mode='anchor')
ax[0].set_title("CHARMM36")
ax[1].set_title("CHARMM36 + ECC")
ax[2].set_title("AMOEBA")

n_bars = 3
width = 1.0/(n_bars + 1)

for k, engine in enumerate(['namd', 'namd_scaled', 'openmm']):
    for j, anion in enumerate(['acet', 'esna', 'mso4']):
        df_temp = df[(df.engine == engine) & (df.anion == anion)]
        # print(df_temp)
        # print('\n')
        vals, errs = df_temp['Ka_M-1'], df_temp['Ka_err_M-1']
        ax[k].bar(x + (j-1)*width, vals, width, label=anion_names[anion])
        ax[k].errorbar(x + (j-1)*width, vals, yerr=2*errs, fmt=' ', color='black', capsize=5)

ax[0].legend(handlelength=0.7, frameon=False, fontsize=16)
ax[0].set_ylim(0, 2.5)
my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05)
# plt.show()

fig.savefig(f'./images_v2_namd/charmm_comparison_Ka_{method}_with_ECC.png', dpi=300)
