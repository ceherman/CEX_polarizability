import numpy as np
import pandas as pd
from scipy import integrate
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

fig, ax = my_plot.instantiate_fig_roman()
plt.close()

cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}
engine_names = {'namd_tip':'CHARMM36', 'namd_tip_scaled':'CHARMM36 + ECC', 'openmm':'AMOEBA'}
colors = {'acet':'red', 'esna':'blue', 'mso4':'limegreen'}

f = open('../rshell.json')
rshell_data = json.load(f)

fig, ax = plt.subplots(3, 3, sharex=True, sharey=True)
fig.set_size_inches(12, 11)
fig.supylabel(r'$K_{A}$ [M$^{-1}$]')

for i in range(3):
    ax[2, i].set_xlabel(r'$R_{Shell}$ [\AA]')
    for j in range(3):
        ax[j, i].axhline(color='black', linewidth=0.5)
        ax[j, i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)

for j, engine in enumerate(['namd_tip', 'openmm', 'namd_tip_scaled']):
    ax[j,0].set_ylabel(engine_names[engine], labelpad=20)
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        if j == 0:
            ax[0, i].set_title(cation_names[cation])

        for k, anion in enumerate(['acet', 'esna', 'mso4']):
            if engine == 'namd_tip':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{anion}_{cation}'
            elif engine == 'namd_tip_scaled':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{anion}_{cation}'
            else:
                data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'

            volumes = np.load(f'{data_dir}/volumes.npy')
            vals = np.loadtxt(f'{data_dir}/gr_central_atoms.txt')
            r_vals, rdf, err_rdf = vals[:,0], vals[:,1], vals[:,2]
            var_rdf = np.nan_to_num(err_rdf**2)

            integrand = r_vals**2 * rdf
            var_integrand = r_vals**4 * var_rdf

            integral, var_integral = np.zeros(len(r_vals)), np.zeros(len(r_vals))

            for n in range(len(r_vals)):
                integral[n] = integrate.trapz(x=r_vals[:n], y=integrand[:n])
                var_integral[n] = np.sum(var_integrand[:n])

            err_integral = np.sqrt(var_integral)
            Ka = 4*np.pi*6.022e-4*integral # 6.022e-4 to convert [A^3/number] to [M-1]
            Ka_err = 4*np.pi*6.022e-4*err_integral # [M-1]

            ax[j, i].plot(r_vals, Ka, label=anion_names[anion], color=colors[anion])
            ax[j, i].fill_between(r_vals, Ka-2*Ka_err, Ka+2*Ka_err, color=colors[anion], alpha=0.3)

            r_max_integral = rshell_data[engine][f'{anion}_{cation}']
            index_max = np.abs(r_vals - r_max_integral).argmin()
            ax[j, i].plot(r_max_integral, Ka[index_max], 'o', color='black', markersize=4)

            if engine == 'namd_tip_scaled' and cation == 'imim':
                r_max_integral = rshell_data['namd_tip_scaled_app'][f'{anion}_{cation}']
                index_max = np.abs(r_vals - r_max_integral).argmin()
                ax[j, i].plot(r_max_integral, Ka[index_max], 's', color='black', markersize=7, fillstyle='none')


leg = ax[0, 2].legend(handlelength=0.7, frameon=False, fontsize=20, loc='upper left')
for line in leg.get_lines():
    line.set_linewidth(2.0)

plt.tight_layout()
plt.subplots_adjust(wspace=0.05, hspace=0.05)
ax[0, 0].set_ylim(0, 2.7)
ax[0, 0].set_xlim(3, 8.0)

fig.savefig(f'./images/Ka_vs_Rshell_anion_comparison.eps', bbox_inches='tight')
fig.savefig(f'./images/Ka_vs_Rshell_anion_comparison.pdf', bbox_inches='tight')
fig.savefig(f'./images/Ka_vs_Rshell_anion_comparison.png', dpi=300, bbox_inches='tight')
