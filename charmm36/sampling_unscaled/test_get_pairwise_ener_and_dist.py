import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import sys
sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot
fig, ax = my_plot.instantiate_fig(1, 1)

def get_log_data(log_file):
    with open(log_file, mode='r') as f:
        data_list = []
        for line in f:
            if "ETITLE:" in line:
                title = line.split()
                title = title[1:]
            elif "ENERGY:" in line:
                data_vals = line.split()
                data_vals = [float(f) for f in data_vals[1:]]
                data_list.append(data_vals)
            else:
                pass
        df = pd.DataFrame(data_list, columns=title)
    return df

for anion in ['acet']: # ['acet', 'esna', 'mso4']:
    for cation in ['guan']: # ['guan', 'imim', 'mamm']:
        data_dir = f'{anion}_{cation}'
        frame_distances = np.load(f'{data_dir}/frame_distances.npy')
        for i_anion in range(1): # range(22):
            resi_anion = 1 + i_anion
            for i_cation in range(1): # range(22):
                resi_cation = 23 + i_cation
                file = f'./{data_dir}/pair_{resi_anion}_{resi_cation}/pair.log'
                df = get_log_data(file)

                df['dist'] = frame_distances[:,i_anion,i_cation]
                fig, ax = my_plot.instantiate_fig(xlabel=r'$r$ ($\AA$)', ylabel='Energy [kcal/mol]')
                ax.scatter(df['dist'], df['ELECT'], label='Elect.')
                ax.scatter(df['dist'], df['VDW'], label='VdW')
                my_plot.set_layout(fig, ax, legend=True)
                plt.show()


# df[['ELECT', 'VDW']]

# frame_distances[:,i_anion,i_cation]
