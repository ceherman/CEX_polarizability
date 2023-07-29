import numpy as np
import pandas as pd
import sys

def get_log_data(log_file):
    with open(log_file, mode='r') as f:
        data_list = []
        for line in f:
            if "ETITLE:" in line:
                title = line.split()
                title = title[1:]
            elif "ENERGY:" in line:
                data_vals = line.split()
                if "ENERGY:" == data_vals[0]:
                    data_vals = [float(f) for f in data_vals[1:]]
                    data_list.append(data_vals)
            else:
                pass
        df = pd.DataFrame(data_list, columns=title)
    return df

anion = sys.argv[1]
cation = sys.argv[2]

data_dir = f'{anion}_{cation}'
print(data_dir)
frame_distances = np.load(f'./{data_dir}/frame_distances.npy')

for i_anion in range(22):
    resi_anion = 1 + i_anion
    for i_cation in range(22):
        resi_cation = 23 + i_cation
        print(resi_anion, resi_cation)
        
        if (anion == 'acet' and (cation == 'imim' or cation == 'mamm')) or (anion == 'esna' and (cation == 'guan' or cation == 'imim')):
            file_1 = f'./{data_dir}/pair_{resi_anion}_{resi_cation}/pair_pme_off.log'
            df_1 = get_log_data(file_1)
            file_2 = f'./{data_dir}/pair_{resi_anion}_{resi_cation}/pair_pme_off_2.log'
            df_2 = get_log_data(file_2)
            df = pd.concat([df_1, df_2])
        else:
            file_1 = f'./{data_dir}/pair_{resi_anion}_{resi_cation}/pair_pme_off.log'
            df = get_log_data(file_1)
        
        df['DIST'] = frame_distances[:,i_anion,i_cation]
        df['resi_anion'] = resi_anion
        df['resi_cation'] = resi_cation
        df_relevant = df[['DIST', 'ELECT', 'VDW', 'resi_anion', 'resi_cation']]
        if i_anion == 0 and i_cation == 0:
            df_combined = df_relevant.copy()
        else:
            df_combined = pd.concat([df_combined, df_relevant])

df_combined.to_csv(f'./{data_dir}/pairwise_ener_and_dist_pme_off.csv', index=False)

