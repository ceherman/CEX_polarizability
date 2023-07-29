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

fig, ax = my_plot.instantiate_fig_roman(fontsize=20)
plt.close()

def get_plot_vals(file, skiprows=0):
    binding_energies = np.loadtxt(file, skiprows=skiprows)
    mean, stdev = binding_energies.mean(), binding_energies.std(ddof=1)
    hist, bin_edges = np.histogram(binding_energies, bins=20, density=True)
    bin_width = bin_edges[1] - bin_edges[0]
    bin_mid_points = bin_edges[:-1] + bin_width / 2.0
    x_axis = np.arange(bin_edges[0], bin_edges[-1], 0.05)
    return bin_mid_points, hist, x_axis, mean, stdev

ion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate', 'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
ions = ['acet', 'esna', 'mso4', 'guan', 'imim', 'mamm']

fig, ax = plt.subplots(3, 2, sharex=True, sharey=True)
fig.set_size_inches(9, 12, forward=True)

for i in range(2):
    ax[2, i].set_xlabel(r'Interaction energy ($\epsilon$)' + '\n' + '[kcal/mol]')
for i in range(3):
    ax[i, 0].set_ylabel(r'$P(\epsilon \; \vert \; \lambda = 5$ \AA$)$', labelpad=15)
    for j in range(2):
        ax[i, j].set_yscale('log')
        ax[i, j].set_ylim(1e-5, 1)
        ax[i, j].set_xlim(-110, -15)
        ax[i, j].tick_params(axis='both', which='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)
        ax[i, j].set_yticks([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1])

for i, ion in enumerate(ions):
    bin_mid_points_amoeba, hist_amoeba, x_axis_amoeba, mean_amoeba, stdev_amoeba = get_plot_vals(f'/home/chase/namd/openmm/mqct/d_long_range/{ion}/long_range_intermolecular.csv', skiprows=1)
    bin_mid_points_charmm, hist_charmm, x_axis_charmm, mean_charmm, stdev_charmm = get_plot_vals(f'./f_lr_linear_response/{ion}/elect_plus_vdw.txt', skiprows=0)
    if i < 3:
        j, k = i, 0
    else:
        j, k = i-3, 1
    ax[j, k].scatter(bin_mid_points_charmm, hist_charmm, label='CHARMM36')
    ax[j, k].plot(x_axis_charmm, norm.pdf(x_axis_charmm, mean_charmm, stdev_charmm))
    ax[j, k].scatter(bin_mid_points_amoeba, hist_amoeba, label='AMOEBA')
    ax[j, k].plot(x_axis_amoeba, norm.pdf(x_axis_amoeba, mean_amoeba, stdev_amoeba))
    ax[j, k].text(0.51, 0.88, ion_names[ion], horizontalalignment='center', transform=ax[j, k].transAxes)

ax[0, 1].legend(frameon=False, loc='center left', bbox_to_anchor=(-0.05, 0.67), handletextpad=0.1, fontsize=16)
plt.subplots_adjust(wspace=0.05, hspace=0.15)

plt.savefig(f'./images/gaussian_check.png', dpi=300, bbox_inches='tight')
plt.savefig(f'./images/gaussian_check.pdf', bbox_inches='tight')
