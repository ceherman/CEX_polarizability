import numpy as np
import pandas as pd
import os
import sys
import json
import block_averaging_functions as block

# Here lr_estimate refers to the linear response model estimate for long-range contributions

df_all = pd.read_csv('./all.csv')
df_wat = pd.read_csv('./water.csv')
long_range = df_all['inter'] - df_wat['inter']
long_range.to_csv('./long_range_intermolecular.csv', index=False)

mean, variance, stdev = long_range.mean(), long_range.var(), long_range.std()
lr_estimate = mean + variance / (2 * 0.592) # 0.592 kcal/mol = 1 kT
var_term = variance / (2 * 0.592)

seov = stdev / np.sqrt(2 * (len(long_range) - 1))

stats = block.std_eom(long_range)
(stats_mean, stats_variance, stats_stdev, stats_seom_raw, stats_inefficiency, stats_seom) = stats

lr_estimate_seom = np.sqrt(stats_seom**2 + seov**2 * 1/((2*0.592)**2))

# print(mean, var_term, lr_estimate, seom, seov, lr_estimate_seom)

with open('results.dat', 'w') as f:
    f.write(f'{lr_estimate:.10f}\t{lr_estimate_seom:.10f}\n')

with open('results_other_info.dat', 'w') as f:
    f.write(f'{mean:.10f}\t{var_term:.10f}\t{lr_estimate:.10f}\n')
