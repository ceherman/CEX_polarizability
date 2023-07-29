import numpy as np
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt

sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

fig, ax = my_plot.instantiate_fig_roman(fontsize=24)
plt.close()

df = pd.read_csv('./results.csv')

fig, ax = my_plot.instantiate_fig_roman(7, 7, ylabel=r'$\mu^{ex}_{\mathsf{Long-range; \; Linear \; Response}}$ [kcal/mol]',
                                        xlabel=r'$\mu^{ex}_{\mathsf{Long-range; \; Gaussian \; Quadrature}}$ [kcal/mol]',
                                        ypad=15, xpad=15)

min_val = -60 # min(df['long_range'].min(), df['long_range_gauss'].min())
max_val = -30 # max(df['long_range'].max(), df['long_range_gauss'].max())
ax.set_xlim(min_val, max_val)
ax.set_ylim(min_val, max_val)
ticks = np.arange(-60, -29, 5)
ax.set_xticks(ticks)

ax.scatter(df['long_range_gauss'], df['long_range'])
ax.errorbar(df['long_range_gauss'], df['long_range'], yerr=2*df['long_range_err'], xerr=2*df['long_range_gauss_err'], fmt=' ', capsize=5)
ax.plot([min_val, max_val], [min_val, max_val], color='black')

plt.savefig('./images/long_range_method_parity.png', dpi=300, bbox_inches='tight')
plt.savefig('./images/long_range_method_parity.pdf', bbox_inches='tight')
