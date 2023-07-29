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

assert (df_Ka_charmm['anion'] == df_Ka_amoeba['anion']).all()
assert (df_Ka_charmm['cation'] == df_Ka_amoeba['cation']).all()

fig, ax = my_plot.instantiate_fig(8, 7, xlabel=r'$\Delta \mu^{ex}_{AMOEBA}$ [kcal/mol]', ylabel=r'$\Delta \mu^{ex}_{CHARMM36}$ [kcal/mol]')

ax.scatter(df_Ka_amoeba['anion_minus_cation_hydration'],
           df_Ka_charmm['anion_minus_cation_hydration'], color='blue')
ax.errorbar(df_Ka_amoeba['anion_minus_cation_hydration'],
            df_Ka_charmm['anion_minus_cation_hydration'],
            xerr=2*df_Ka_amoeba['anion_minus_cation_hydration_err'],
            yerr=2*df_Ka_charmm['anion_minus_cation_hydration_err'],
            fmt=' ', color='blue', capsize=5, alpha=0.3)

min_val = min(df_Ka_amoeba['anion_minus_cation_hydration'].min(), df_Ka_charmm['anion_minus_cation_hydration'].min())*1.05
max_val = max(df_Ka_amoeba['anion_minus_cation_hydration'].max(), df_Ka_charmm['anion_minus_cation_hydration'].max())*2

ax.set_xlim([min_val, max_val])
ax.set_ylim([min_val, max_val])
ax.plot([min_val, max_val], [min_val, max_val], color='black', lw=1)

my_plot.set_layout(fig, ax)
plt.savefig('./images/mu_diff_parity.png', dpi=300, bbox_inches='tight')
