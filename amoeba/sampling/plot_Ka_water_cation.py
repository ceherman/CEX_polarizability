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

df = pd.read_csv(f'./results_Ka_gr_water.csv')

anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}
cations = ['Guanidinium', 'Imidazolium', 'Methylammonium']
# cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
# anions = ['Acetate', 'Ethylsulfonate', 'Methylsulfate']

fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
fig.set_size_inches(10, 7)
ax[0].set_ylabel(r'$K_{\mathsf{Water - Cation}}$ [M$^{-1}$]')
x = np.arange(3)
for i in range(2):
    ax[i].set_xticks(x)
    ax[i].set_xticklabels(cations, rotation=30, ha='right', rotation_mode='anchor')
ax[0].set_title("CHARMM36")
ax[1].set_title("AMOEBA")

n_bars = 3
width = 1.0/(n_bars + 1)

for k, engine in enumerate(['namd', 'openmm']):
    for j, anion in enumerate(['acet', 'esna', 'mso4']):
        df_temp = df[(df.engine == engine) & (df.anion == anion) & (df.ion == 'cation')]
        ax[k].bar(x + (j-1)*width, df_temp['Ka_M-1'], width, label=anion_names[anion])

ax[0].set_ylim(0, 0.35)
ax[0].legend(handlelength=0.7, frameon=False, fontsize=16)
my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05)
# plt.show()

fig.savefig(f'./images_v2_namd/charmm_comparison_Ka_gr_water_cation.png', dpi=300)
