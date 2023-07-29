import numpy as np
import pandas as pd
import os
import sys
import json

df_Ka = pd.read_csv('/home/chase/namd/openmm/ion_pairs/results_Ka_gr_tip_with_pmf_min.csv')
df_Ka_amoeba = df_Ka[df_Ka['engine'] == 'openmm'].copy()

df = pd.read_csv('./results.csv') # hydration free energies

for i, cont in df_Ka_amoeba.iterrows():
    anion = df.loc[df['ion'] == cont['anion'], 'total'].iloc[0]
    anion_err = df.loc[df['ion'] == cont['anion'], 'total_err'].iloc[0]
    cation = df.loc[df['ion'] == cont['cation'], 'total'].iloc[0]
    cation_err = df.loc[df['ion'] == cont['cation'], 'total_err'].iloc[0]
    
    df_Ka_amoeba.at[i, 'anion_minus_cation_hydration'] = anion - cation
    df_Ka_amoeba.at[i, 'anion_minus_cation_hydration_err'] = np.sqrt(anion_err**2 + cation_err**2)
    
df_Ka_amoeba.to_csv('./Ka_vs_hydration_diff.csv', index=False)
