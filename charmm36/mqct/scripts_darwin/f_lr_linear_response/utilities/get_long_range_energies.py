import numpy as np
import pandas as pd
import os
import sys
import json
import block_averaging_functions as block

# Here lr_estimate refers to the linear response model estimate for long-range contributions

energies = np.loadtxt('./energies.txt')
elect, vdw = energies[:,1], energies[:,2]
total_ener = energies[:,1] + energies[:,2]
np.savetxt('./elect_plus_vdw.txt', total_ener)

for (label, data) in [('total', total_ener), ('elect', elect), ('vdw', vdw)]:

    mean = data.mean()
    variance = data.var(ddof=1)
    stdev = data.std(ddof=1)

    lr_estimate = mean + variance / (2 * 0.592) # 0.592 kcal/mol = 1 kT
    var_term = variance / (2 * 0.592)

    seov = stdev / np.sqrt(2 * (len(data) - 1))

    stats = block.std_eom(data)
    (stats_mean, stats_variance, stats_stdev, stats_seom_raw, stats_inefficiency, stats_seom) = stats

    lr_estimate_seom = np.sqrt(stats_seom**2 + seov**2 * 1/((2*0.592)**2))

    with open(f'results_{label}.dat', 'w') as f:
        f.write(f'{lr_estimate:.10f}\t{lr_estimate_seom:.10f}\n')

    with open(f'results_{label}_other_info.dat', 'w') as f:
        f.write(f'{mean:.10f}\t{var_term:.10f}\t{lr_estimate:.10f}\n')

stacked = np.stack([elect, vdw])
cov = np.cov(stacked)[0][1]
with open(f'results_covariance.dat', 'w') as f:
    f.write(f'{cov:.10f}')
