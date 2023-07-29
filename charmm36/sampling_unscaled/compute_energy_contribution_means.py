import numpy as np
import pandas as pd
from datetime import datetime

print(datetime.now())

for anion in ['acet', 'esna', 'mso4']:
    for cation in ['guan', 'imim', 'mamm']:
        data_dir = f'{anion}_{cation}'
        print(data_dir)
        df = pd.read_csv(f'./{data_dir}/pairwise_ener_and_dist.csv')
        rdf = np.loadtxt(f'./{data_dir}/gr_central_atoms.txt')
        r_vals = rdf[:,0]
        delta_r = r_vals[1] - r_vals[0]
        half_delta_r = r_vals[0]
        assert abs(half_delta_r*2 - delta_r) < 1e-5

        elect_mean = np.zeros(len(r_vals))
        elect_var = np.zeros(len(r_vals))
        elect_seom = np.zeros(len(r_vals))
        vdw_mean = np.zeros(len(r_vals))
        vdw_var = np.zeros(len(r_vals))
        vdw_seom = np.zeros(len(r_vals))

        for i, r in enumerate(r_vals):
            df_temp = df[(r - half_delta_r <= df['DIST']) & (df['DIST'] < r + half_delta_r)]
            if len(df_temp) == 0:
                elect_mean[i] = np.nan
                elect_var[i] = np.nan
                elect_seom[i] = np.nan
                vdw_mean[i] = np.nan
                vdw_var[i] = np.nan
                vdw_seom[i] = np.nan
            else:
                mean = df_temp.mean(axis=0)
                var = df_temp.var(axis=0)
                assert r - half_delta_r <= mean['DIST'] < r + half_delta_r
                n_pts = len(df_temp)
                elect_mean[i] = mean['ELECT']
                elect_var[i] = var['ELECT']
                elect_seom[i] = np.sqrt(var['ELECT'] / n_pts)
                vdw_mean[i] = mean['VDW']
                vdw_var[i] = var['VDW']
                vdw_seom[i] = np.sqrt(var['VDW'] / n_pts)
            print(r)

        df_means = pd.DataFrame({'r':r_vals, 'elect_mean':elect_mean,
                                'elect_var':elect_var, 'elect_seom':elect_seom,
                                'vdw_mean':vdw_mean, 'vdw_var':vdw_var,
                                'vdw_seom':vdw_seom})
        df_means.to_csv(f'./{data_dir}/pairwise_ener_means.csv', index=False)

print(datetime.now())
