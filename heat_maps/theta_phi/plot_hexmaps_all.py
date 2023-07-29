import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import sys
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot
fig, ax = my_plot.instantiate_fig_roman()
plt.close()

engines = ['namd', 'openmm', 'namd_scaled']
cations = ['guan', 'imim', 'mamm']
anions = ['acet', 'esna', 'mso4']
cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'acetate', 'esna':'ethylsulfonate', 'mso4':'methylsulfate'}
ff_names = {'namd':'CHARMM36', 'openmm':'AMOEBA', 'namd_scaled':'CHARMM36+ECC'}

# font = {'weight': 'normal', 'size': 15}
# plt.rc('font', **font)
# plt.rcParams.update({"savefig.facecolor":'white'})

fig, ax = plt.subplots(nrows=3, ncols=9, sharex=True, sharey=False, constrained_layout=True)
fig.set_size_inches(27, 11)
# supylabel = fig.supylabel(r'$\cos(\theta)$')

fontsize=28
for m, engine in enumerate(engines):
    # ax[m, 0].set_ylim([0, 180])
    ax[m, 0].set_ylabel(f'{ff_names[engine]}\n\n'+r'$\alpha$  [Degrees]', fontsize=fontsize)
for k in range(9):
    ax[2, k].set_xlabel(r'$\theta$  [Degrees]', fontsize=fontsize)
    ax[2, k].set_xlim([0,180])
    for m in range(3):
        ax[m, k].tick_params(axis='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)
for l, anion in enumerate(anions):
    for n, cation in enumerate(cations):
        col_index = l*3 + n
        ax[0, col_index].set_title(f'{cation_names[cation]}\n{anion_names[anion]}', fontsize=fontsize, rotation=30, loc='left', ha='left', va='bottom')


for i, engine in enumerate(engines):
    for l, anion in enumerate(anions):
        for n, cation in enumerate(cations):
            col_index = l*3 + n
            fname = f'{engine}_{anion}_{cation}'
            print(fname)
            thetas = np.loadtxt(fname + '_bound_theta_array.dat')
            phis = np.loadtxt(fname + '_bound_phi_array.dat')
            ax[i, col_index].hexbin(thetas, phis, cmap='cool')


norm = mpl.colors.Normalize(vmin=0, vmax=1)
cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.cool), ax=ax[:, 8], location='right', fraction=0.12)
cbar.set_label('System-specific normalized frequency', labelpad=10, fontsize=fontsize)

# plt.subplots_adjust(wspace=0.05, hspace=0.1)
# plt.savefig('./all_heatmaps.eps', transparent=False, bbox_inches='tight')
plt.savefig('./all_hexmaps.png', dpi=300, bbox_inches='tight')
