import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import sys
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

fig, ax = my_plot.instantiate_fig()
plt.close()

engines = ['namd', 'openmm', 'namd_scaled']
cations = ['guan', 'imim', 'mamm']
anions = ['acet', 'esna', 'mso4']
cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'acetate', 'esna':'ethylsulfonate', 'mso4':'methylsulfate'}
ff_names = {'namd':'CHARMM36', 'openmm':'AMOEBA', 'namd_scaled':'CHARMM36 + ECC'}
gridsizes = {'namd':50, 'openmm':100, 'namd_scaled':50}

fig, ax = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True, constrained_layout=True)
fig.set_size_inches(9, 11)

fontsize=28
for m, engine in enumerate(engines):
    ax[m, 0].set_ylim([0, 90])
    ax[m, 0].set_ylabel(f'{ff_names[engine]}\n\n'+r'$\alpha$  [Degrees]', fontsize=fontsize-2, labelpad=15)

for k in range(2):
    ax[2, k].set_xlabel(r'$\theta$ [Degrees]', fontsize=fontsize, labelpad=10)
    ax[2, k].set_xlim([0, 180])

    for m in range(3):
        ax[m, k].tick_params(axis='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)
        ax[m, k].set_xticks([0, 90, 180])
        ax[m, k].set_yticks([0, 45, 90])

for col_index, pair in enumerate([('guan', 'acet'), ('imim', 'acet')]):
    cation, anion = pair

    ax[0, col_index].set_title(f'{cation_names[cation]}\n{anion_names[anion]}', fontsize=fontsize, loc='center', ha='center', va='bottom')

    # Load data and plot
    for i, engine in enumerate(engines):
        fname = f'{engine}_{anion}_{cation}'
        print(fname)
        thetas = np.loadtxt(fname + '_bound_theta_array.dat')
        phis = np.loadtxt(fname + '_bound_phi_array.dat')
        ax[i, col_index].hexbin(thetas, phis, cmap='cool', gridsize=gridsizes[engine])


norm = mpl.colors.Normalize(vmin=0, vmax=1)
cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.cool), ax=ax[:, 1], location='right', fraction=0.15)
cbar.set_label('System-specific normalized frequency', labelpad=10, fontsize=fontsize)

plt.savefig(f'./cation_hexmaps_selected_acet.png', dpi=300, bbox_inches='tight')
