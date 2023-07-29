import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

fig, ax = my_plot.instantiate_fig(fontsize=22)
plt.close()

fig, ax = plt.subplots(1, 3)
fig.set_size_inches(24, 6, forward=True)
for i in range(3):
    ax[i].tick_params(axis='both', which='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)

ion = 'imim'

ax[0].set_title('Packing')
ax[0].set_xlabel(r'$\lambda$ [$\rm{\AA}$]', labelpad=10)
ax[0].set_ylabel(r'Force [kcal/(mol $\rm{\AA}$)]', labelpad=15)
amoeba_path_cav = '/home/chase/namd/openmm/mqct/b_cavity'
charmm_path_cav = '/home/chase/namd/ion_pairs/cgenff/mqct_for_darwin_tip/e_cavity'
columns_cav = ['r', 'force', 'seom', 'ignore']
df_amoeba_cav = pd.read_fwf(f'{amoeba_path_cav}/{ion}/force.dat', header=None)
df_charmm_cav = pd.read_fwf(f'{charmm_path_cav}/{ion}/force.dat', header=None)
df_amoeba_cav.columns = columns_cav
df_charmm_cav.columns = columns_cav
ax[0].errorbar(df_charmm_cav['r'], df_charmm_cav['force'], yerr=2*df_charmm_cav['seom'], fmt='-o', capsize=5, markersize=5, label='CHARMM36')
ax[0].errorbar(df_amoeba_cav['r'], df_amoeba_cav['force'], yerr=2*df_amoeba_cav['seom'], fmt='-o', capsize=5, markersize=5, label='AMOEBA')
ax[0].set_ylim(0, 31)
ax[0].set_xlim(0, 5.1)


def get_plot_vals(file, skiprows=0):
    binding_energies = np.loadtxt(file, skiprows=skiprows)
    mean, stdev = binding_energies.mean(), binding_energies.std(ddof=1)
    hist, bin_edges = np.histogram(binding_energies, bins=20, density=True)
    bin_width = bin_edges[1] - bin_edges[0]
    bin_mid_points = bin_edges[:-1] + bin_width / 2.0
    x_axis = np.arange(bin_edges[0], bin_edges[-1], 0.05)
    return bin_mid_points, hist, x_axis, mean, stdev

ax[1].set_title('Long-range')
ax[1].set_xlabel(r'Interaction energy ($\epsilon$) [kcal/mol]', labelpad=10)
# ax[1].set_xlabel(r'Interaction energy ($\epsilon$)' + '\n' + '[kcal/mol]')
ax[1].set_ylabel(r'$P(\epsilon \; \vert \; \lambda = 5 \; \rm{\AA})$', labelpad=15)
ax[1].set_yscale('log')
bin_mid_points_amoeba, hist_amoeba, x_axis_amoeba, mean_amoeba, stdev_amoeba = get_plot_vals(f'/home/chase/namd/openmm/mqct/d_long_range/{ion}/long_range_intermolecular.csv', skiprows=1)
bin_mid_points_charmm, hist_charmm, x_axis_charmm, mean_charmm, stdev_charmm = get_plot_vals(f'./f_lr_linear_response/{ion}/elect_plus_vdw.txt', skiprows=0)
ax[1].scatter(bin_mid_points_charmm, hist_charmm, label='CHARMM36')
ax[1].plot(x_axis_charmm, norm.pdf(x_axis_charmm, mean_charmm, stdev_charmm))
ax[1].scatter(bin_mid_points_amoeba, hist_amoeba, label='AMOEBA')
ax[1].plot(x_axis_amoeba, norm.pdf(x_axis_amoeba, mean_amoeba, stdev_amoeba))
ax[1].set_ylim(1e-5, 1)
ax[1].set_xlim(-80, -20)

ax[2].set_title('Chemistry')
ax[2].set_ylabel(r'Force [kcal/(mol $\rm{\AA}$)]', labelpad=15)
ax[2].set_xlabel(r'$\lambda$ [$\rm{\AA}$]', labelpad=10)
amoeba_path_chem = '/home/chase/namd/openmm/mqct/c_chemistry'
charmm_path_chem = '/home/chase/namd/ion_pairs/cgenff/mqct_for_summit_tip/b_chemistry_with_charges'
df_amoeba_chem = pd.read_fwf(f'{amoeba_path_chem}/{ion}/force.dat', header=None)
df_charmm_chem = pd.read_fwf(f'{charmm_path_chem}/{ion}/force.dat', header=None)
df_amoeba_chem.columns = columns_cav
df_charmm_chem.columns = columns_cav
df_amoeba_chem = df_amoeba_chem[df_amoeba_chem['r'] > 2.0]
df_charmm_chem = df_charmm_chem[df_charmm_chem['r'] > 2.0]
ax[2].errorbar(df_charmm_chem['r'], df_charmm_chem['force'], yerr=2*df_charmm_chem['seom'], fmt='-o', capsize=5, markersize=5, label='CHARMM36')
ax[2].errorbar(df_amoeba_chem['r'], df_amoeba_chem['force'], yerr=2*df_amoeba_chem['seom'], fmt='-o', capsize=5, markersize=5, label='AMOEBA')
ax[2].set_ylim(0, 31)
ax[2].set_xlim(0, 5.1)


plt.subplots_adjust(wspace=0.4)
ax[0].legend(frameon=False, loc='center left', handletextpad=0.5, handlelength=1)
plt.savefig(f'./images/single_ion_mqct_{ion}.png', dpi=300, bbox_inches='tight')
