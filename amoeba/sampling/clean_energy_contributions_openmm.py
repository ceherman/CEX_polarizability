import numpy as np
import pandas as pd

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        data_dir = f'{anion}_{cation}'
        pmf = np.loadtxt(f'{data_dir}/pmf_central_atoms.txt')
        df_means = pd.read_csv(f'./{data_dir}/pair_data/pairwise_ener_means.csv')
        assert np.allclose(pmf[:,0], df_means['r'].values)

        df_clean = pd.DataFrame()
        df_clean['r'] = pmf[:,0]
        df_clean['pmf'] = pmf[:,1]
        df_clean['pmf_seom'] = pmf[:,2]
        df_clean['direct'] = df_means['inter_mean']
        df_clean['direct_seom'] = df_means['inter_seom']
        df_clean['w_solv'] = df_clean['pmf'] - df_clean['direct']
        df_clean['w_solv_seom'] = np.sqrt(df_clean['pmf_seom']**2 + df_clean['direct_seom']**2)

        df_clean['elect'] = df_means['multipole_inter_mean']
        df_clean['elect_seom'] = df_means['multipole_inter_seom']
        df_clean['vdw'] = df_means['vdw_inter_mean']
        df_clean['vdw_seom'] = df_means['vdw_inter_seom']
        df_clean['polar'] = df_means['inter_mean'] - df_means['multipole_inter_mean'] - df_means['vdw_inter_mean']
        df_clean['polar_seom'] = np.sqrt(df_means['inter_seom']**2 + df_means['multipole_inter_seom']**2 + df_means['vdw_inter_seom']**2)

        df_clean.to_csv(f'./{data_dir}/final_clean.csv', index=False)

