import numpy as np
import pandas as pd
import os
import sys
import json
import seaborn as sns
import matplotlib.pyplot as plt
import math
from scipy.stats import sem, pearsonr, linregress

# I can control the plotting with xdata, ydata like this ########################
def corrfunc(x, y, ax=None, **kwargs):
    """Plot the correlation coefficient in the top left hand corner of a plot."""
    not_nan_indeces = ~np.isnan(x)&~np.isnan(y)
    x = x[not_nan_indeces]
    y = y[not_nan_indeces]
    r, pvalue = pearsonr(x, y)
#     print(pvalue)
    ax = ax or plt.gca()
    ax.annotate(f'ρ = {r:.2f}', xy=(.02, 0.98), xycoords=ax.transAxes)

def plot_unity(xdata, ydata, **kwargs):
    points = np.linspace(min_val, max_val, 100)
    plt.gca().plot(points, points, color='k', marker=None, linestyle='--', linewidth=1.0)

def plot_linear(x, y, **kwargs):
    not_nan_indeces = ~np.isnan(x)&~np.isnan(y)
    x = x[not_nan_indeces]
    y = y[not_nan_indeces]
    regression = linregress(x, y)
    x_vals = np.linspace(min_val, max_val, 100)
    y_vals = regression.slope * x_vals + regression.intercept
    plt.gca().plot(x_vals, y_vals, color='k', marker=None, linestyle='--', linewidth=1.0)

def set_axes_off_diag(xdata, ydata, **kwargs):
    plt.gca().set_xlim(min_val, max_val)
    plt.gca().set_ylim(min_val, max_val)

def set_axes_diag(xdata, **kwargs):
    plt.gca().set_xlim(min_val, max_val)

# def hide_current_axis(*args, **kwds):
#     plt.gca().set_visible(False)

#################################################################################

sns.set_context("notebook", font_scale=1.1)

for anion in ['acet', 'esna', 'mso4']:
    for cation in ['guan', 'imim', 'mamm']:
        print(f'{anion}_{cation}')

        df = pd.read_csv(f'../{anion}_{cation}/pair_data/pairwise_ener_and_dist_head.csv')
        df_temp = df[['multipole_inter', 'vdw_inter', 'polar_inter']].copy()
        df_temp.columns = ['Elect.', 'VdW', 'Polar.']
        df_plot = df_temp # .sample(10000)

        # Ad hoc
        min_val = math.floor(min(df_plot.min()))
        max_val = math.ceil(max(df_plot.max()))

        grid = sns.pairplot(df_plot, corner=True, diag_kind='kde')

        # grid.map_offdiag(plot_linear)
        # grid.map_offdiag(set_axes_off_diag)
        grid.map_offdiag(corrfunc)

        fig = grid.fig
        fig.patch.set_alpha(1)
        fig.savefig(f'./images_pair_corr/{anion}_{cation}.png', dpi=300)

# bbox_inches='tight'
