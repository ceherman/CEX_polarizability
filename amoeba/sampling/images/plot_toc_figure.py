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

df = pd.read_csv(f'../results_Ka_gr_tip.csv')

cation = 'guan'
anions = ['acet', 'esna', 'mso4']
ffs = ['CHARMM36', 'AMOEBA'] # consistent with order ['namd', 'openmm'] in df
x = np.array([0, 1.2])

fig, ax = my_plot.instantiate_fig_roman(x=7, y=4)
ax.set_ylabel(r'$K_{A}$', labelpad=10, fontsize=36) # [M$^{-1}$]
ax.set_xticks(x)
ax.set_xticklabels(ffs, rotation=0, ha='center', fontsize=36)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(top=False, right=False, left=False, bottom=False, pad=10)
ax.get_yaxis().set_ticks([])

n_bars = 3
width = 1.0/(n_bars + 1)

for j, anion in enumerate(anions):
    df_temp = df[((df.engine == 'namd_tip') | (df.engine == 'openmm')) & (df.anion == anion) & (df.cation == cation)]
    print(df_temp)
    print('\n')
    vals, errs = df_temp['Ka_M-1'], df_temp['Ka_err_M-1']
    ax.bar(x + (j-1)*width, vals, width, label=anion)
    ax.errorbar(x + (j-1)*width, vals, yerr=2*errs, fmt=' ', color='black', capsize=5)

# ax.legend(handlelength=0.7, frameon=False, fontsize=16)

fig.savefig(f'./images/toc_figure.png', dpi=300, bbox_inches='tight', transparent=True)
