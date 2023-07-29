import numpy as np
import pandas as pd
from scipy import integrate
import os
import sys
import json
import block_averaging_functions as block
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

df_Ka, df_Kd = pd.DataFrame(), pd.DataFrame()
text = 'central_atoms'
n = 0

for k, engine in enumerate(['gromacs', 'namd', 'namd_scaled', 'openmm']):
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        for j, anion in enumerate(['acet', 'esna', 'mso4']):
            if engine == 'namd':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force/{anion}_{cation}'
            elif engine == 'namd_scaled':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_scaled/{anion}_{cation}'
            else:
                data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'
            vals = np.loadtxt(f'{data_dir}/gr_{text}.txt')
            volumes = np.load(f'{data_dir}/volumes.npy')

            r_vals, rdf, err_rdf = vals[:,0], vals[:,1], vals[:,2]
            var_rdf = np.nan_to_num(err_rdf**2)

            r_max_integral = rshell_data[engine][f'{anion}_{cation}']
            index_max = np.abs(r_vals - r_max_integral).argmin()
            assert abs(r_max_integral - r_vals[index_max]) < 0.01
            # index_max = np.where(r_vals == r_max_integral)[0][0]

            integrand = r_vals**2 * rdf
            var_integrand = r_vals**4 * var_rdf

            integral = integrate.trapz(x=r_vals[:index_max], y=integrand[:index_max])
            var_integral = np.sum(var_integrand[:index_max])
            err_integral = np.sqrt(var_integral)

            Ka = 4*np.pi*6.022e-4*integral # 6.022e-4 to convert [A^3/number] to [M-1]
            Ka_err = 4*np.pi*6.022e-4*err_integral # [M-1]
            Ka_var = Ka_err**2

            Kd = 1/Ka # [M]
            Kd_var = Kd**2 * Ka_var / (Ka**2)
            Kd_err = np.sqrt(Kd_var)

            df_Ka.at[n, 'engine'] = engine
            df_Ka.at[n, 'anion'] = anion
            df_Ka.at[n, 'cation'] = cation
            df_Ka.at[n, 'Ka_M-1'] = Ka
            df_Ka.at[n, 'Ka_err_M-1'] = Ka_err

            df_Kd.at[n, 'engine'] = engine
            df_Kd.at[n, 'anion'] = anion
            df_Kd.at[n, 'cation'] = cation
            df_Kd.at[n, 'Kd_M'] = Kd
            df_Kd.at[n, 'Kd_err_M'] = Kd_err

            n_mol = 22
            cvals = n_mol/volumes * 1e4/6.022 # [M]
            c_stats = list(block.std_eom(cvals))
            c, c_err = c_stats[0], c_stats[-1]
            if engine == 'gromacs':
                c_err = 0

            prod = c * Ka
            p_bound_from_Ka = (1 + 2*prod - np.sqrt(4*prod + 1))/(2*prod)

            # prod_var = (prod**2) * ((c_err/c)**2 + (Ka_err/Ka)**2)
            # f1 = 4*prod
            # f1_var = 16*prod_var
            # f5 = f1 + 1
            # f5_var = f1_var
            # f2 = np.sqrt(f5)
            # f2_var = (0.5 * f5**(-0.5) * np.sqrt(f5_var))**2
            # f3 = 2*prod
            # f3_var = 4*prod_var
            # num = 1 + f3 - f2
            # num_var = f3_var + f2_var
            # den = f3
            # den_var = f3_var
            # assert num/den == p_bound_from_Ka
            # p_var = (p_bound_from_Ka**2) * (num_var/(num**2) + den_var/(den**2))
            # p_err = np.sqrt(p_var)

            df_Ka.at[n, 'p_bound'] = p_bound_from_Ka
            # df_Ka.at[n, 'p_err'] = p_err

            print(engine, cation, anion)
            n += 1

df_Ka.to_csv('./results_Ka_gr.csv', index=False)
df_Kd.to_csv('./results_Kd_gr.csv', index=False)
