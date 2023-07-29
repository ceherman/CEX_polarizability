import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json

import sys
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot
fig, ax = my_plot.instantiate_fig()
plt.close()

# Done with TIP3P
engines = ['namd', 'openmm', 'namd_scaled']
cations = ['guan', 'imim', 'mamm']
anions = ['acet', 'esna', 'mso4']
cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'acetate', 'esna':'ethylsulfonate', 'mso4':'methylsulfate'}
ff_names = {'namd':'CHARMM36', 'openmm':'AMOEBA', 'namd_scaled':'CHARMM36 + ECC'}
engine_map_to_rshell_names = {'namd':'namd_tip', 'namd_scaled':'namd_tip_scaled', 'openmm':'openmm'}

f = open('/home/chase/namd/openmm/ion_pairs/rshell.json')
rshell_data = json.load(f)

fig, axes = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True, constrained_layout=True)
fig.set_size_inches(9, 11)
# supylabel = fig.supylabel(r'$\cos(\theta)$')

fontsize=28
for m, engine in enumerate(engines):
    axes[m, 0].set_ylim([0, 180])
    axes[m, 0].set_ylabel(f'{ff_names[engine]}\n\n'+r'$\theta$  [Degrees]', fontsize=fontsize-2, labelpad=15)
    # axes[m, 0].set_ylabel(f'{ff_names[engine]}', fontsize=22)

for k in range(2):
    axes[2, k].set_xlabel(r'$r$  [$\rm{\AA}$]', fontsize=fontsize)
    axes[2, k].set_xlim([2, 8.5])
    for m in range(3):
        axes[m, k].tick_params(axis='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)
        axes[m, k].set_xticks([2, 5, 8])
        axes[m, k].set_yticks([0, 45, 90, 135, 180])

norm = mpl.colors.Normalize(vmin=0, vmax=1)
cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.cool), ax=axes[:, 1], location='right', fraction=0.15)
cbar.set_label('System-specific normalized frequency', labelpad=10, fontsize=fontsize)

for col_index, pair in enumerate([('guan', 'acet'), ('imim', 'mso4')]):
    cation, anion = pair

    axes[0, col_index].set_title(f'{cation_names[cation]}\n{anion_names[anion]}', fontsize=fontsize, loc='center', ha='center', va='bottom')

    for i, engine in enumerate(engines):
        fname = f'{engine}_{anion}_{cation}'
        xedge = np.loadtxt(fname + '_xedge.dat')
        yedge = np.loadtxt(fname + '_yedge.dat')
        Z = np.loadtxt(fname + '_hists.dat')

        X = (xedge[0:-1] + xedge[1:])/2
        Y = (yedge[0:-1] + yedge[1:])/2

        Xarr = np.array([])
        Yarr = np.array([])
        Zarr = np.array([])
        count=0
        for x_i in range(0,len(X)):
            for y_i in range(0,len(Y)):
                Xarr = np.append(Xarr,X[x_i]*10)
                Yarr = np.append(Yarr,Y[y_i])
                Zarr = np.append(Zarr,Z[x_i,y_i])
                count+=1

        norm_z = Zarr/np.max(Zarr)
        norm_z[norm_z < 0.0001] = np.nan
        axes[i, col_index].scatter(Xarr,Yarr,marker='s',c=norm_z, cmap='cool')

        rshell_engine = engine_map_to_rshell_names[engine]
        r = rshell_data[rshell_engine][f'{anion}_{cation}']
        axes[i, col_index].axvline(x=r, color='black', linestyle='--', linewidth=1)

plt.savefig('./heatmaps_selected.png', dpi=300, bbox_inches='tight')
