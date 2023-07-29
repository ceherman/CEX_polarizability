import pandas as pd
import numpy as np

df_Ka = pd.read_csv('./results_Ka_gr_tip.csv')

text = 'central_atoms'
data = 'pmf'

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        data_dir = f'{anion}_{cation}'
        for k, engine in enumerate(['namd_tip', 'openmm', 'namd_tip_scaled']):
            if engine == 'namd_tip':
                df_data = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{data_dir}/final_clean_pme_off.csv')
            elif engine == 'namd_tip_scaled':
                df_data = pd.read_csv(f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{data_dir}/final_clean_pme_off_scaled_up.csv')
            elif engine == 'openmm':
                df_data = pd.read_csv(f'./{data_dir}/final_clean.csv')

            r_pmf_min = df_data.loc[df_data['pmf'] == df_data['pmf'].min(), 'r'].iloc[0]
            pmf_min = df_data['pmf'].min()
            pmf_min_seom = df_data.loc[df_data['pmf'] == df_data['pmf'].min(), 'pmf_seom'].iloc[0]

            index = df_Ka.loc[(df_Ka.anion == anion) & (df_Ka.cation == cation) & (df_Ka.engine == engine)].index
            assert len(index) == 1
            index = index[0]

            df_Ka.at[index, 'r_pmf_min'] = r_pmf_min
            df_Ka.at[index, 'pmf_min'] = pmf_min
            df_Ka.at[index, 'pmf_min_seom'] = pmf_min_seom

df_Ka.to_csv('./results_Ka_gr_tip_with_pmf_min.csv', index=False)


