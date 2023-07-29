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

cations = ['guan', 'imim', 'mamm']
anions = ['acet', 'esna', 'mso4']
cation_names = {'guan':'Guanidinium', 'mamm':'Methylammonium', 'imim':'Imidazolium'}
anion_names = {'acet':'Acetate', 'esna':'Ethylsulfonate', 'mso4':'Methylsulfate'}

fig, ax = plt.subplots(nrows=3, ncols=3, sharex=True, sharey=True, constrained_layout=True)
fig.set_size_inches(10, 9)
supylabel = fig.supylabel(r'$\cos(\theta)$')
ax[0, 0].set_xlim([0,12])
ax[0, 0].set_ylim([-1,1])
fontsize=24

for m, anion in enumerate(anions):
    ax[m, 0].set_ylabel(f'{anion_names[anion]}', fontsize=fontsize)

for m, cation in enumerate(cations):
    ax[0, m].set_title(f'{cation_names[cation]}', fontsize=fontsize)

for k in range(3):
    ax[2, k].set_xlabel(r'$r~($\AA$)$', fontsize=fontsize)
    for m in range(3):
        ax[m, k].tick_params(axis='both', direction='in', length=6, bottom=True, top=True, left=True, right=True)

norm = mpl.colors.Normalize(vmin=0, vmax=1)
cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.cool), ax=ax[:, 2], location='right', fraction=0.12)
cbar.set_label('System-specific normalized frequency', labelpad=10, fontsize=fontsize)

engine = 'openmm'
for l, anion in enumerate(anions):
    for n, cation in enumerate(cations):
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
        norm_z[norm_z < 0.001] = np.nan
        ax[l, n].scatter(Xarr,Yarr,marker='s',c=norm_z, cmap='cool')

# plt.subplots_adjust(wspace=0.05, hspace=0.1)
plt.savefig('./amoeba_heatmaps.eps', transparent=False, bbox_inches='tight')
plt.savefig('./amoeba_heatmaps.png', dpi=300, bbox_inches='tight')
