import numpy as np
import pandas as pd
import os
import sys

for anion in ['acet', 'esna', 'mso4']:
    for cation in ['guan', 'imim', 'mamm']:
        print(f'{anion}_{cation}')
        df = pd.read_csv(f'../{anion}_{cation}/pair_data/pairwise_ener_and_dist_head.csv')

        df['diff'] = df['inter'] - df['vdw_inter'] - df['multipole_inter'] - df['polar_inter']
        print(df.head())
        print(df.tail())
        print()
