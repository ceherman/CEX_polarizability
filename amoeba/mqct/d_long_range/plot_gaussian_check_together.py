import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt
from scipy.stats import norm

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

fig, ax = my_plot.instantiate_fig_roman()
plt.close()

ion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate', 'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
ions = ['acet', 'esna', 'mso4', 'guan', 'imim', 'mamm']

fig, ax = plt.subplots(3, 2, sharex=True, sharey=True)
fig.set_size_inches(8, 12, forward=True)

for i in range(2):
    ax[2, i].set_xlabel(r'Interaction energy ($\epsilon$)' + '\n' + '[kcal/mol]')
for i in range(3):
    ax[i, 0].set_ylabel(r'$P(\epsilon)$')

# ax[0, 0].set_title('Anions')
# ax[0, 1].set_title('Cations')

for i, ion in enumerate(ions):
    binding_energies = np.loadtxt(f'./{ion}/long_range_intermolecular.csv', skiprows=1)
    mean, stdev = binding_energies.mean(), binding_energies.std(ddof=1)

    hist, bin_edges = np.histogram(binding_energies, bins=20, density=True)
    bin_width = bin_edges[1] - bin_edges[0]
    bin_mid_points = bin_edges[:-1] + bin_width / 2.0
    x_axis = np.arange(bin_edges[0], bin_edges[-1], 0.05)

    if i < 3:
        j, k = i, 0
    else:
        j, k = i-3, 1

    ax[j, k].scatter(bin_mid_points, hist)
    ax[j, k].plot(x_axis, norm.pdf(x_axis, mean, stdev))
    ax[j, k].text(0.51, 0.88, ion_names[ion], horizontalalignment='center', transform=ax[j, k].transAxes)

ax[0, 0].set_yscale('log')
ax[0, 0].set_ylim(1e-5, 1)

plt.subplots_adjust(wspace=0.05, hspace=0.05)
# my_plot.set_layout(fig, ax)
plt.savefig(f'./images/gaussian_check/together.png', dpi=300, bbox_inches='tight')
