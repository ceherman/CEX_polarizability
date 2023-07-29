import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot
my_plot.instantiate_fig(1, 1)


df_Ka_charmm = pd.read_csv('./Ka_vs_hydration_diff_tip.csv')
df_Ka_amoeba = pd.read_csv('~/namd/openmm/mqct/Ka_vs_hydration_diff.csv')

fig, ax = my_plot.instantiate_fig(8, 7, xlabel=r'$\mu^{ex}_{Anion} - \mu^{ex}_{Cation}$ [kcal/mol]', ylabel=r'$K_{A}$ [M$^{-1}$]')

for i, (df, label) in enumerate([(df_Ka_charmm, 'CHARMM36'), (df_Ka_amoeba, 'AMOEBA')]):
    ax.scatter(df['anion_minus_cation_hydration'], df['Ka_M-1'], label=label)
    ax.errorbar(df['anion_minus_cation_hydration'], df['Ka_M-1'], xerr=2*df['anion_minus_cation_hydration_err'], yerr=2*df['Ka_err_M-1'], fmt=' ', color=f'C{i}', capsize=5)

my_plot.set_layout(fig, ax, legend=True)
plt.savefig('./images/volcano.png', dpi=300, bbox_inches='tight')
