import numpy as np
import pandas as pd
import os
import sys
import plotly.express as px

for engine in ['namd']: # ['openmm', 'gromacs']:
    for j, anion in enumerate(['acet', 'esna', 'mso4']):
        for i, cation in enumerate(['guan', 'mamm', 'imim']):
            for ion in [anion, cation]:
                if engine == 'namd':
                    data_dir = f'/home/chase/namd/ion_pairs/cgenff/brute_force/{anion}_{cation}'
                else:
                    data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'
                data = np.loadtxt(f'{data_dir}/pmf_water_{ion}.txt')
                df = pd.DataFrame(data, columns=['r', 'pmf'])
                fig = px.line(df, x="r", y="pmf", title=f'{engine}_{anion}_{cation}_{ion}')
                # fig.update_yaxes(range=[-0.6, 0.5])
                fig.update_xaxes(range=[0, 10])
                fig.show()



