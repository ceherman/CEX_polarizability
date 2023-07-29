import numpy as np
import pandas as pd
import os
import sys
import json

sys.path.append('./utilities/')
import block_averaging_functions as block

# Here lr_estimate refers to the linear response model estimate for long-range contributions

df = pd.DataFrame()

for i, ion in enumerate(['acet', 'esna', 'mso4', 'guan', 'imim', 'mamm']):
    df.at[i, 'ion'] = ion

    energies = np.loadtxt(f'./{ion}/energies.txt')
    elect = energies[:,1]
    vdw = energies[:,2]
    total_ener = energies[:,1] + energies[:,2]

    for (label, data) in [('total', total_ener), ('elect', elect), ('vdw', vdw)]:
        mean = data.mean()
        variance = data.var(ddof=1)
        stdev = data.std(ddof=1)

        lr_estimate = mean + variance / (2 * 0.592) # 0.592 kcal/mol = 1 kT
        seov = stdev / np.sqrt(2 * (len(data) - 1))

        stats = block.std_eom(data)
        (stats_mean, stats_variance, stats_stdev, stats_seom_raw, stats_inefficiency, stats_seom) = stats
        lr_estimate_seom = np.sqrt(stats_seom**2 + seov**2 * 1/((2*0.592)**2))

        df.at[i, label] = lr_estimate
        df.at[i, f'{label}_seom'] = lr_estimate_seom

    stacked = np.stack([elect, vdw])
    cov = np.cov(stacked)[0][1]
    df.at[i, 'cov_term'] = cov / 0.592

    assert abs(df.at[i, 'elect'] + df.at[i, 'vdw'] + df.at[i, 'cov_term'] - df.at[i, 'total']) < 0.01

df.to_csv('./long_range_partitioning.csv', index=False)
