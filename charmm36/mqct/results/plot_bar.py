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

fig, ax = my_plot.instantiate_fig_roman(fontsize=24)
plt.close()

df_charmm = pd.read_csv('./results.csv')
df_amoeba = pd.read_csv('~/namd/openmm/mqct/results.csv')
df_exp = pd.read_csv('~/namd/openmm/mqct/lit_data_for_plot.csv')

assert df_exp.at[1, 'ion'] == 'guan'
guan_data = df_exp[df_exp['ion'] == 'guan'].copy()
df_exp.drop(index=[1], inplace=True)

fig, ax = plt.subplots(1, 4, sharex=True, sharey=True, gridspec_kw={'width_ratios': [1, 1, 1, 1.3]})
fig.set_size_inches(20, 9)
ax[0].set_ylabel(r'$\mu^{ex}$ [kcal/mol]')
ax[0].set_title(r"Packing $(\lambda_G = 5$ \AA$)$")
ax[1].set_title(r"Long-range $(\lambda_G = 5$ \AA$)$")
ax[2].set_title(r"Chemistry $(\lambda_G = 5$ \AA$)$")
ax[3].set_title("Total")

for i in range(4):
    ax[i].set_xticks(df_charmm.index)
    ax[i].set_xticklabels(df_charmm['nice_name'], rotation=45, ha='right', rotation_mode='anchor')
    ax[i].tick_params(axis='both', direction='in', length=6, bottom=True, top=False, left=True, right=True)
    ax[i].axhline(color='black', lw=1)

width = 0.33
width_3 = 0.25

plot_bar_with_2x_err(ax[0], df_charmm.index-width/2, df_charmm['cavity'], df_charmm['cavity_err'], width, label='CHARMM36')
plot_bar_with_2x_err(ax[1], df_charmm.index-width/2, df_charmm['long_range'], df_charmm['long_range_err'], width, label='CHARMM36')
plot_bar_with_2x_err(ax[2], df_charmm.index-width/2, df_charmm['chemistry'], df_charmm['chemistry_err'], width, label='CHARMM36')
plot_bar_with_2x_err(ax[3], df_charmm.index-width_3, df_charmm['total'], df_charmm['total_err'], width_3, label='CHARMM36')

plot_bar_with_2x_err(ax[0], df_amoeba.index+width/2, df_amoeba['cavity'], df_amoeba['cavity_err'], width, label='AMOEBA')
plot_bar_with_2x_err(ax[1], df_amoeba.index+width/2, df_amoeba['long_range'], df_amoeba['long_range_err'], width, label='AMOEBA')
plot_bar_with_2x_err(ax[2], df_amoeba.index+width/2, df_amoeba['chemistry'], df_amoeba['chemistry_err'], width, label='AMOEBA')
plot_bar_with_2x_err(ax[3], df_amoeba.index, df_amoeba['total'], df_amoeba['total_err'], width_3, label='AMOEBA')

exp_yerr = np.sqrt(2.5**2 + 5.82**2)
ax[3].bar(df_exp['ref_index']+width_3, df_exp['exp_est'], width_3, label='Experiment')
ax[3].errorbar(df_exp['ref_index']+width_3, df_exp['exp_est'], yerr=exp_yerr, fmt=' ', color='black', capsize=5)

ax[3].bar(guan_data['ref_index']+width_3, guan_data['exp_est'], width_3, color='tab:green', hatch='\\')
ax[3].errorbar(guan_data['ref_index']+width_3, guan_data['exp_est'], yerr=exp_yerr, fmt=' ', color='black', capsize=5)

ax[0].legend(handlelength=1.2, frameon=False, handletextpad=0.5)
ax[3].legend(handlelength=1.2, frameon=False, handletextpad=0.5, loc='upper left')
ax[0].set_ylim(-100, 40)

my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05)

plt.savefig('./images/bar_plot.png', dpi=300, bbox_inches='tight')
plt.savefig('./images/bar_plot.eps', bbox_inches='tight')
plt.savefig('./images/bar_plot.pdf', bbox_inches='tight')
