import numpy as np
import pandas as pd
import json
import block_averaging_functions as block

f = open('rshell.json')
rshell_data = json.load(f)

df_Ka = pd.DataFrame()

n = 0
for k, engine in enumerate(['gromacs', 'openmm']):
    for i, cation in enumerate(['guan', 'imim', 'mamm']):
        for j, anion in enumerate(['acet', 'esna', 'mso4']):
            data_dir = f'/home/chase/namd/{engine}/ion_pairs/{anion}_{cation}'
            rshell = rshell_data[engine][f'{anion}_{cation}']

            volumes = np.load(f'{data_dir}/volumes.npy')
            frame_distances = np.load(f'{data_dir}/frame_distances.npy')
            n_frames, n_anions, n_cations = np.shape(frame_distances)

            c_c = np.zeros((n_frames))
            n_0 = np.zeros((n_frames))
            n_1 = np.zeros((n_frames))
            n_2 = np.zeros((n_frames))
            n_3 = np.zeros((n_frames))
            n_4 = np.zeros((n_frames))
            n_5 = np.zeros((n_frames))
            # n_6 = np.zeros((n_frames))

            for i in range(n_frames):
                associated = frame_distances[i,:,:] < rshell
                anion_association = np.sum(associated, axis=1)
                cation_association = np.sum(associated, axis=0)

                n_0[i] = np.max([(anion_association == 0).sum(), (cation_association == 0).sum()])
                n_1[i] = np.max([(anion_association == 1).sum(), (cation_association == 1).sum()])
                n_2[i] = np.max([(anion_association == 2).sum(), (cation_association == 2).sum()])
                n_3[i] = np.max([(anion_association == 3).sum(), (cation_association == 3).sum()])
                n_4[i] = np.max([(anion_association == 4).sum(), (cation_association == 4).sum()])
                n_5[i] = np.max([(anion_association == 5).sum(), (cation_association == 5).sum()])
                # n_6[i] = (anion_association == 6).sum()

                # Converted from [number/A^3] to [M]
                c_c[i] = n_cations/volumes[i] * 1e4/6.022 # (cation_association == 0).sum() / volumes[i] * 1e4/6.022 #

            n_0_sum = np.sum(n_0)
            n_1_sum = np.sum(n_1)
            n_2_sum = np.sum(n_2)
            n_3_sum = np.sum(n_3)
            n_4_sum = np.sum(n_4)
            n_5_sum = np.sum(n_5)

            Ka = n_1_sum / ( (n_0_sum + n_2_sum + n_3_sum + n_4_sum + n_5_sum) * np.mean(c_c))

            df_Ka.at[n, 'engine'] = engine
            df_Ka.at[n, 'anion'] = anion
            df_Ka.at[n, 'cation'] = cation
            df_Ka.at[n, 'Ka_M-1'] = Ka

            n += 1
            print(engine, f'{anion}_{cation}', Ka)

            break
        break
    break

# df_Ka.to_csv('./results_Ka_counting_pratt.csv', index=False)
