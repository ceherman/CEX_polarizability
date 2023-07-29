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

## p_bound from the two methods should be the same
# df = pd.read_csv(f'./results_Ka_counting_direct.csv')
df = pd.read_csv(f'./results_Ka_counting_difference_for_unassociated.csv')

# cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}
cations = ['Guanidinium', 'Imidazolium', 'Methylammonium']

fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
fig.set_size_inches(10, 7)
ax[0].set_ylabel(r'$P_{\mathsf{bound}}$')
x = np.arange(3)
for i in range(2):
    ax[i].set_xticks(x)
    ax[i].set_xticklabels(cations, rotation=30, ha='right', rotation_mode='anchor')
ax[0].set_title("CHARMM36")
ax[1].set_title("AMOEBA")

n_bars = 3
width = 1.0/(n_bars + 1)

for k, engine in enumerate(['gromacs', 'openmm']):
    for j, anion in enumerate(['acet', 'esna', 'mso4']):
        df_temp = df[(df.engine == engine) & (df.anion == anion)]
        # print(df_temp)
        # print('\n')
        vals, errs = df_temp['p_bound'], df_temp['p_err']
        ax[k].bar(x + (j-1)*width, vals, width, label=anion_names[anion])
        ax[k].errorbar(x + (j-1)*width, vals, yerr=2*errs, fmt=' ', color='black', capsize=5)

ax[0].legend(handlelength=0.7, frameon=False, fontsize=16)
ax[0].set_ylim(0, 1)
my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05)
# plt.show()

fig.savefig(f'./images/charmm_comparison_pbound_counting.png', dpi=300)
