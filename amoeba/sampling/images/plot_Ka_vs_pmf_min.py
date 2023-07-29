import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot
fig, ax = my_plot.instantiate_fig_roman()
plt.close()

engine_ff = {'namd_tip':'CHARMM36', 'namd_tip_scaled':'CHARMM36 + ECC', 'openmm':'AMOEBA'}
colors = {'openmm':'red', 'namd_tip':'blue', 'namd_tip_scaled':'limegreen'}

df = pd.read_csv('../results_Ka_gr_tip_with_pmf_min.csv')

fig, ax = my_plot.instantiate_fig_roman()
ax.set_xlabel('PMF min [kcal/mol]', labelpad=10)
ax.set_ylabel(r'$K_{A}$ [M$^{-1}$]', labelpad=15)

for engine in ['namd_tip', 'openmm', 'namd_tip_scaled']:
    df_temp = df[df.engine == engine]
    x = df_temp['pmf_min']
    xerr = df_temp['pmf_min_seom']
    y = df_temp['Ka_M-1']
    yerr = df_temp['Ka_err_M-1']
    color = colors[engine]
    label = engine_ff[engine]

    ax.scatter(x, y, color=color, label=label)
    ax.errorbar(x, y, xerr=2*xerr, yerr=2*yerr, fmt=' ', color=color, capsize=5, alpha=0.3)

my_plot.set_layout(fig, ax, legend=True, handlelength=0.4, frameon=True)
plt.savefig('./images/Ka_vs_pmf_min.png', dpi=300, bbox_inches='tight')

