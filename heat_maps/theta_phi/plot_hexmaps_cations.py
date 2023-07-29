import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import sys
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

fig, ax = my_plot.instantiate_fig_roman(fontsize=22)
plt.close()

fontsize=24

engines = ['namd', 'openmm', 'namd_scaled']
cations = ['guan', 'imim', 'mamm']
anions = ['acet', 'esna', 'mso4']
cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'acetate', 'esna':'ethylsulfonate', 'mso4':'methylsulfate'}
ff_names = {'namd':'CHARMM36', 'openmm':'AMOEBA', 'namd_scaled':'CHARMM36 + ECC'}
gridsizes = {'namd':50, 'openmm':100, 'namd_scaled':50}
phi_ticks = {'guan':[0, 45, 90], 'imim':[0, 45, 90], 'mamm':[0, 45, 90, 135, 180]}

# font = {'weight': 'normal', 'size': 15}
# plt.rc('font', **font)
# plt.rcParams.update({"savefig.facecolor":'white'})

for n, cation in enumerate(cations):
    print('\n', cation)
    fig, ax = plt.subplots(nrows=3, ncols=3, sharex=True, sharey=True, constrained_layout=True)
    fig.set_size_inches(11, 10)

    # Apply axis labels, format ticks, etc.
    for m, engine in enumerate(engines):
        ax[m, 0].set_ylabel(f'{ff_names[engine]}\n\n'+r'$\alpha$ [Degrees]', fontsize=fontsize, labelpad=15)
        if cation == 'mamm':
            ax[m, 0].set_ylim([0, 180])
        else:
            ax[m, 0].set_ylim([0, 90])

    for k in range(3):
        ax[2, k].set_xlabel(r'$\theta$ [Degrees]', fontsize=fontsize, labelpad=10)
        ax[2, k].set_xlim([0,180])
        for m in range(3):
            ax[m, k].tick_params(axis='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)
            ax[m, k].set_xticks([0, 90, 180])
            ax[m, k].set_yticks(phi_ticks[cation])

    for l, anion in enumerate(anions):
        ax[0, l].set_title(f'{cation_names[cation]}\n{anion_names[anion]}', fontsize=fontsize)

    # Load data and plot
    for i, engine in enumerate(engines):
        for l, anion in enumerate(anions):
            fname = f'{engine}_{anion}_{cation}'
            print(fname)
            thetas = np.loadtxt(fname + '_bound_theta_array.dat')
            phis = np.loadtxt(fname + '_bound_phi_array.dat')
            ax[i, l].hexbin(thetas, phis, cmap='cool', gridsize=gridsizes[engine])


    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.cool), ax=ax[:, 2], location='right', fraction=0.1)
    cbar.set_label('System-specific normalized frequency', labelpad=10, fontsize=fontsize)

    plt.savefig(f'./cation_hexmaps_{cation}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'./cation_hexmaps_{cation}.eps', bbox_inches='tight')
    plt.savefig(f'./cation_hexmaps_{cation}.pdf', bbox_inches='tight')
