import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

fig, ax = my_plot.instantiate_fig()
plt.close()

def plot_diff_from_amoeba(ax, df, column, label=None, color=None, ls=None, absolute=True):
    diff = df[f'{column}_r_amoeba'].values - df_amoeba[column].values
    seom = np.sqrt((df[f'{column}_seom_r_amoeba'].values)**2 + (df_amoeba[f'{column}_seom'].values)**2)
    if absolute:
        ax.plot(r_amoeba, abs(diff), label=label, color=color, ls=ls)
        ax.fill_between(r_amoeba, abs(diff)-2*seom, abs(diff)+2*seom, alpha=0.3, color=color)
    else:
        ax.plot(r_amoeba, diff, label=label, color=color, ls=ls)
        ax.fill_between(r_amoeba, diff-2*seom, diff+2*seom, alpha=0.3, color=color)
    return

fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
fig.set_size_inches(8, 5)
ax[0].set_ylabel(r'$\vert \; U_{CHARMM36} - U_{AMOEBA} \; \vert$' + '\n[kcal/mol]', labelpad=15)

ax[0].set_title('Guanidinium\nacetate')
ax[1].set_title('Imidazolium\nmethylsulfate')

prop_names = {'elect':r'$U_{Elect}$', 'vdw':r'$U_{VdW}$', 'polar':r'$U_{Polar}$'}
colors = ['blue', 'red', 'limegreen']


for i in range(2):
    ax[i].set_xlabel(r'$r$  [$\rm{\AA}$]')
    ax[i].axhline(color='black', linewidth=0.5)
    ax[i].tick_params(axis='both',direction='in',length=6, bottom=True, top=True, left=True, right=True)

for i, pair in enumerate([('guan', 'acet'), ('imim', 'mso4')]):
    cation, anion = pair

    data_dir = f'{anion}_{cation}'
    df_amoeba = pd.read_csv(f'../{data_dir}/final_clean.csv')
    df_charmm = pd.read_csv(f'../{data_dir}/final_clean_charmm_pme_off_ener_conts.csv')
    df_charmm['polar'] = 0.0
    df_charmm['polar_seom'] = 0.0

    r_amoeba = df_amoeba['r'].values
    df_charmm['r_amoeba'] = r_amoeba

    interp_columns = ['elect', 'vdw', 'polar']
    interp_columns_seom = [f'{column}_seom' for column in interp_columns]
    kind = 'linear'
    for column in interp_columns + interp_columns_seom:
        spline_charmm = interp1d(df_charmm['r'].values, df_charmm[column].values, kind=kind, bounds_error=False)
        df_charmm[f'{column}_r_amoeba'] = spline_charmm(r_amoeba)

    for k, column in enumerate(interp_columns):
        plot_diff_from_amoeba(ax[i], df_charmm, column, color=colors[k], ls='-', label=r'$U = $' + f' {prop_names[column]}')

ax[0].set_xlim(2.8, 8)
ax[0].set_ylim(0, 20)
leg = ax[1].legend(handlelength=1, frameon=False, fontsize=22)
for line in leg.get_lines():
    line.set_linewidth(2.0)

plt.tight_layout()
plt.subplots_adjust(wspace=0.05, hspace=0.05)

fig.savefig(f'./tsrc_selected_images/cross_ff_analysis_energy_cont_diff.png', dpi=300, bbox_inches='tight')
