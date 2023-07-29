import numpy as np
import pandas as pd
import json
import block_averaging_functions as block

# This script is implemented to only count 1:1 pairs as a complex.
# The direct counting and counting unassociated by difference methods differ
# in how the unassociated ions are counted, since I'm ignoring 2:1 complexes,
# etc.; the methods do not differ in counting the 1:1 complexes, so p_bound is
# the same.
# The counting unassociated by difference method forces the assumption of
# stoichiometric binding to be satisfied, so p_bound + p_unbound = 1 and
# p_bound computed by counting agrees with p_bound computed from Ka. This is not
# the case for the direct counting method.

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
            n_max = max(n_anions, n_cations)
            n_min = min(n_anions, n_cations)
            assert len(volumes) == n_frames

            c_ac = np.zeros((n_frames))
            c_a = np.zeros((n_frames))
            c_c = np.zeros((n_frames))
            f_bound = np.zeros((n_frames))
            n_ac_sum = 0
            n_a_sum = 0
            n_c_sum = 0

            for i in range(n_frames):
                # progress = i/n_frames*100
                # print(f'{progress:.1f}%')

                associated = frame_distances[i,:,:] < rshell
                anion_association = np.sum(associated, axis=1)
                cation_association = np.sum(associated, axis=0)

                n_bound_anion = (anion_association == 1).sum()
                n_bound_cation = (cation_association == 1).sum()
                n_bound = min(n_bound_anion, n_bound_cation)
                n_ac_sum += n_bound
                f_bound[i] = n_bound/n_min

                # Direct counting
                n_free_anion = (anion_association == 0).sum()
                n_free_cation = (cation_association == 0).sum()

                # # Counting unassociated by difference
                # n_free_anion = n_anions - n_bound
                # n_free_cation = n_cations - n_bound

                n_a_sum += n_free_anion
                n_c_sum += n_free_cation

                # Converted from [number/A^3] to [M]
                c_ac[i] = n_bound/volumes[i] * 1e4/6.022
                c_a[i] = n_free_anion/volumes[i] * 1e4/6.022
                c_c[i] = n_free_cation/volumes[i] * 1e4/6.022

            c_ac_stats = list(block.std_eom(c_ac))
            c_a_stats = list(block.std_eom(c_a))
            c_c_stats = list(block.std_eom(c_c))
            f_bound_stats = list(block.std_eom(f_bound))
            # mValue, sigma_raw, stdev_raw, seom_raw, inefficiency, seom = stats

            num = c_ac_stats[0]
            den = c_a_stats[0]*c_c_stats[0]
            Ka = num/den

            num_var = c_ac_stats[-1]**2
            den_var = (den**2) * ((c_a_stats[-1]/c_a_stats[0])**2 + (c_c_stats[-1]/c_c_stats[0])**2)
            Ka_var = (Ka**2) * (num_var/(num**2) + den_var/(den**2))
            Ka_err = np.sqrt(Ka_var)

            df_Ka.at[n, 'engine'] = engine
            df_Ka.at[n, 'anion'] = anion
            df_Ka.at[n, 'cation'] = cation
            df_Ka.at[n, 'Ka_M-1'] = Ka
            df_Ka.at[n, 'Ka_err_M-1'] = Ka_err

            p_bound = n_ac_sum/(n_min * n_frames)
            assert abs(f_bound_stats[0] - p_bound) < 1e-5
            p_unbound_a = n_a_sum/(n_anions * n_frames)
            p_unbound_c = n_c_sum/(n_cations * n_frames)

            df_Ka.at[n, 'p_bound'] = p_bound
            df_Ka.at[n, 'p_err'] = f_bound_stats[-1]
            df_Ka.at[n, 'p_unbound_anion'] = p_unbound_a
            df_Ka.at[n, 'p_unbound_cation'] = p_unbound_c
            # df_Ka.at[n, 'pb_bua_sum'] = p_bound + p_unbound_a
            # df_Ka.at[n, 'pb_buc_sum'] = p_bound + p_unbound_c

            cmax = n_max/np.mean(volumes) * 1e4/6.022
            cmin = n_min/np.mean(volumes) * 1e4/6.022
            prod = Ka * (cmax + cmin)
            p_bound_from_Ka = (1 + prod - np.sqrt((prod + 1)**2 - 4*Ka**2 * cmax * cmin))/(2*Ka*cmin)

            df_Ka.at[n, 'p_bound_from_Ka'] = p_bound_from_Ka
            df_Ka.at[n, 'c_M'] = cmax

            n += 1
            print(engine, f'{anion}_{cation}', rshell, Ka, Ka_err)

    #         break
    #     break
    # break

df_Ka.to_csv('./results_Ka_counting_direct.csv', index=False)
# df_Ka.to_csv('./results_Ka_counting_difference_for_unassociated.csv', index=False)
