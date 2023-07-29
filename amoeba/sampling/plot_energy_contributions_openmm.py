import numpy as np
import pandas as pd
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot
fig, ax = my_plot.instantiate_fig()
plt.close()

def plot_with_seom(ax, r_vals, means, seom, label=None):
    ax.plot(r_vals, means, label=label)
    ax.fill_between(r_vals, means-2*seom, means+2*seom, alpha=0.3)
    return

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}

fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
fig.set_size_inches(12, 11)
fig.supylabel('Energy [kcal/mol]')
for i in range(3):
    ax[2, i].set_xlabel(r'$r$ ($\AA$)')
    for j in range(3):
        ax[j, i].axhline(color='black', linewidth=0.5)

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    ax[j,0].set_ylabel(anion_names[anion])
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        if j == 0:
            ax[0, i].set_title(cation_names[cation])
        data_dir = f'{anion}_{cation}'

        pmf = np.loadtxt(f'{data_dir}/pmf_central_atoms.txt')
        plot_with_seom(ax[j, i], pmf[:,0], pmf[:,1], pmf[:,2], label='PMF')

        df_means = pd.read_csv(f'./{data_dir}/pair_data/pairwise_ener_means.csv')
        plot_with_seom(ax[j, i], df_means['r'], df_means['inter_mean'], df_means['inter_seom'], label='Total')
        plot_with_seom(ax[j, i], df_means['r'], df_means['multipole_inter_mean'], df_means['multipole_inter_seom'], label=f'Multipole')
        plot_with_seom(ax[j, i], df_means['r'], df_means['vdw_inter_mean'], df_means['vdw_inter_seom'], label='VdW')
        plot_with_seom(ax[j, i], df_means['r'], df_means['polar_inter_mean'], df_means['polar_inter_mean'], label='Polar (wrong)')
        ax[j, i].plot(df_means['r'], df_means['inter_mean'] - df_means['multipole_inter_mean'] - df_means['vdw_inter_mean'], label='Polar (diff)')

ax[0, 0].legend(handlelength=0.7, frameon=False, fontsize=16)
ax[0, 0].set_xlim(0, 16)
my_plot.set_layout(fig, ax)
plt.subplots_adjust(wspace=0.05, hspace=0.05)
fig.savefig(f'./images_v2_namd/energy_contributions_openmm.png', dpi=300)
