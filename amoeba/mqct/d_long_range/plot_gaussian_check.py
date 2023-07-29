import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt
from scipy.stats import norm

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot
fig, ax = my_plot.instantiate_fig()
plt.close()

ion = sys.argv[1]

binding_energies = np.loadtxt('long_range_intermolecular.csv', skiprows=1)
mean, stdev = binding_energies.mean(), binding_energies.std(ddof=1)

hist, bin_edges = np.histogram(binding_energies, bins=20, density=True)
bin_width = bin_edges[1] - bin_edges[0]
bin_mid_points = bin_edges[:-1] + bin_width / 2.0
x_axis = np.arange(bin_edges[0], bin_edges[-1], 0.01)

fig, ax = my_plot.instantiate_fig(xlabel='Long-range interaction energy [kcal/mol]', ylabel='Normalized frequency')
ax.set_yscale('log')

ax.scatter(bin_mid_points, hist)
ax.plot(x_axis, norm.pdf(x_axis, mean, stdev))

ax.set_ylim(1e-5, 1)
my_plot.set_layout(fig, ax)
plt.savefig(f'../images/gaussian_check/{ion}.png', dpi=300, bbox_inches='tight')
