import numpy as np
import pandas as pd
from scipy import integrate
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

df_Ka, df_Kd = pd.DataFrame(), pd.DataFrame()
text = 'central_atoms'
f = open('rshell_water.json')
rshell_data = json.load(f)
n = 0

ion_order = {0:'anion', 1:'cation'}

for k, engine in enumerate(['gromacs', 'namd', 'openmm']):
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        for j, anion in enumerate(['acet', 'esna', 'mso4']):
            if engine == 'namd':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force/{anion}_{cation}'
            else:
                data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'

            for m, ion in enumerate([anion, cation]):
                vals = np.loadtxt(f'{data_dir}/gr_water_{ion}.txt')

                r_vals, rdf = vals[:,0], vals[:,1]

                r_max_integral = rshell_data[engine][f'{anion}_{cation}'][ion]
                index_max = np.abs(r_vals - r_max_integral).argmin()
                assert abs(r_max_integral - r_vals[index_max]) < 0.01
                # index_max = np.where(r_vals == r_max_integral)[0][0]

                integrand = r_vals**2 * rdf
                integral = integrate.trapz(x=r_vals[:index_max], y=integrand[:index_max])

                Ka = 4*np.pi*6.022e-4*integral # 6.022e-4 to convert [A^3/number] to [M-1]
                Kd = 1/Ka # [M]

                df_Ka.at[n, 'engine'] = engine
                df_Ka.at[n, 'anion'] = anion
                df_Ka.at[n, 'cation'] = cation
                df_Ka.at[n, 'ion'] = ion_order[m]
                df_Ka.at[n, 'Ka_M-1'] = Ka

                df_Kd.at[n, 'engine'] = engine
                df_Kd.at[n, 'anion'] = anion
                df_Kd.at[n, 'cation'] = cation
                df_Kd.at[n, 'ion'] = ion_order[m]
                df_Kd.at[n, 'Kd_M'] = Kd

                print(n, engine, anion, cation, ion, Ka)
                n += 1

df_Ka.to_csv('./results_Ka_gr_water.csv', index=False)
df_Kd.to_csv('./results_Kd_gr_water.csv', index=False)
