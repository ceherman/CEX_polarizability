import numpy as np
import pandas as pd
import os
import sys
import json

df = pd.read_csv('./sim.log')
vol = df["Box Volume (nm^3)"].mean()
length = vol ** (1.0/3.0)
length *= 10 # Angstroms

with open('average_length.dat', 'w') as f:
    f.write(f'{length:.10f}\n')
