import numpy as np
import pandas as pd
import os
import sys
import plotly.express as px

for engine in ['namd_tip_scaled']: # ['openmm', 'gromacs']:
    for j, anion in enumerate(['acet', 'esna', 'mso4']):
        for i, cation in enumerate(['guan', 'mamm', 'imim']):
            if engine == 'namd_tip':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip/{anion}_{cation}'
            elif engine == 'namd_tip_scaled':
                data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force_tip_scaled/{anion}_{cation}'
            else:
                data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'
            data = np.loadtxt(f'{data_dir}/pmf_central_atoms.txt')
            df = pd.DataFrame(data, columns=['r', 'pmf', 'seom'])
            fig = px.line(df, x="r", y="pmf", title=f'{engine}_{anion}_{cation}')
            fig.show()



