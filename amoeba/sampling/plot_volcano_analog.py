import numpy as np
import pandas as pd
import sys
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

fig, ax = my_plot.instantiate_fig()
plt.close()

ref = 'exp_or_qm' # 'sim_kcal_mol'

df_Ka = pd.read_csv('./results_Ka_gr.csv')
df_mu = pd.read_csv('./mqct_hydration_results_namd_spce.csv')

fig, ax = my_plot.instantiate_fig(xlabel=r'$\mu^{ex}_{-} - \mu^{ex}_{+}$ [kcal/mol]', ylabel=r'$K_{A}$ [M$^{-1}$]')

mu_diff = []
Ka_vals = []

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        try:
            mu_anion = df_mu.loc[df_mu.ion == anion, ref].iloc[0]
            mu_cation = df_mu.loc[df_mu.ion == cation, ref].iloc[0]
            Ka = df_Ka.loc[(df_Ka.engine == 'namd') & (df_Ka.anion == anion) & (df_Ka.cation == cation), 'Ka_M-1'].iloc[0]
            Ka_vals.append(Ka) # -1.0*np.log(Ka)
            mu_diff.append(mu_anion - mu_cation)
            print(mu_anion - mu_cation, Ka, anion, cation)
        except:
            pass

ax.scatter(mu_diff, Ka_vals)

my_plot.set_layout(fig, ax)
# plt.show()
if ref == 'sim_kcal_mol':
    ref = 'sim'
fig.savefig(f'./images_v2_namd/volcano_analog_{ref}.png', dpi=300)
