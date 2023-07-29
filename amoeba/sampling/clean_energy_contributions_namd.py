import numpy as np
import pandas as pd

for data_dir in ['acet_guan', 'acet_imim', 'acet_mamm', 'esna_guan', 'esna_imim', 'esna_mamm', 'mso4_guan', 'mso4_imim', 'mso4_mamm']:
    pmf = np.loadtxt(f'{data_dir}/pmf_central_atoms.txt')
    df_means = pd.read_csv(f'./{data_dir}/pair_data_charmm/pairwise_ener_means_pme_off.csv')
    assert np.allclose(pmf[:,0], df_means['r'].values)

    df_clean = pd.DataFrame()
    df_clean['r'] = pmf[:,0]
    df_clean['pmf'] = pmf[:,1]
    df_clean['pmf_seom'] = pmf[:,2]
    df_clean['direct'] = df_means['elect_mean'] + df_means['vdw_mean']
    df_clean['direct_seom'] = np.sqrt(df_means['elect_seom']**2 + df_means['vdw_seom']**2)
    df_clean['w_solv'] = df_clean['pmf'] - df_clean['direct']
    df_clean['w_solv_seom'] = np.sqrt(df_clean['pmf_seom']**2 + df_clean['direct_seom']**2)

    df_clean['elect'] = df_means['elect_mean']
    df_clean['elect_seom'] = df_means['elect_seom']
    df_clean['vdw'] = df_means['vdw_mean']
    df_clean['vdw_seom'] = df_means['vdw_seom']

    df_clean.to_csv(f'./{data_dir}/final_clean_charmm_pme_off_ener_conts.csv', index=False)
