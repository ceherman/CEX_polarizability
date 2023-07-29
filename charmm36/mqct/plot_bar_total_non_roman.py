import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

def plot_bar_with_2x_err(ax, xs, ys, yerrs, width, label=None):
    ax.bar(xs, ys, width, label=label)
    ax.errorbar(xs, ys, yerr=2*yerrs, fmt=' ', color='black', capsize=5)
    return

fig, ax = my_plot.instantiate_fig(fontsize=28)
plt.close()

df_charmm = pd.read_csv('./results.csv')
df_amoeba = pd.read_csv('~/namd/openmm/mqct/results.csv')
df_exp = pd.read_csv('~/namd/openmm/mqct/lit_data_for_plot.csv')

assert df_exp.at[1, 'ion'] == 'guan'
guan_data = df_exp[df_exp['ion'] == 'guan'].copy()
df_exp.drop(index=[1], inplace=True)

fig, ax = plt.subplots(1, 4, sharex=True, sharey=True, gridspec_kw={'width_ratios': [1, 1, 1, 1.3]})
fig.set_size_inches(20, 9)

fig, ax = my_plot.instantiate_fig(ylabel=r'$\mu^{ex}$ [kcal/mol]', fontsize=28, x=9, y=9)
ax.set_xticks(df_charmm.index)
ax.set_xticklabels(df_charmm['nice_name'], rotation=35, ha='right', rotation_mode='anchor')
ax.tick_params(axis='both', direction='in', length=6, bottom=True, top=False, left=True, right=True)
# ax.axhline(color='black', lw=1)

width = 0.33
width_3 = 0.25

plot_bar_with_2x_err(ax, df_charmm.index-width_3, df_charmm['total'], df_charmm['total_err'], width_3, label='CHARMM36')
plot_bar_with_2x_err(ax, df_amoeba.index, df_amoeba['total'], df_amoeba['total_err'], width_3, label='AMOEBA')

exp_yerr = np.sqrt(2.5**2 + 5.82**2)
ax.bar(df_exp['ref_index']+width_3, df_exp['exp_est'], width_3, label='Experiment')
ax.errorbar(df_exp['ref_index']+width_3, df_exp['exp_est'], yerr=exp_yerr, fmt=' ', color='black', capsize=5)

ax.bar(guan_data['ref_index']+width_3, guan_data['exp_est'], width_3, color='tab:green', hatch='\\')
ax.errorbar(guan_data['ref_index']+width_3, guan_data['exp_est'], yerr=exp_yerr, fmt=' ', color='black', capsize=5)

ax.legend(handlelength=1.2, frameon=False, handletextpad=0.5, loc='lower center', fontsize=25)
ax.set_ylim(-120, 0)

my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05)

plt.savefig('./images/bar_plot_total_non_roman.png', dpi=300, bbox_inches='tight')
