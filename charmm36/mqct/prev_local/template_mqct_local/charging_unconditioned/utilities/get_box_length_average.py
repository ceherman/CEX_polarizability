import sys
import numpy as np

lambda_vals = [0.1127, 0.5000, 0.8873]
lengths = []
for lam in lambda_vals:
    temp = np.loadtxt(f'./q_{lam:.4f}/box_length.dat')
    lengths.append(temp[0])
average = np.mean(np.array(lengths))

with open('average_length.dat', 'w') as f:
    f.write(f'{average:.10f}\n')
