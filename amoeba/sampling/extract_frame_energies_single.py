import pandas as pd
import sys

def get_data(line, my_list, n=-2):
    data = line.split()
    my_list.append(float(data[n]))
    return

log_file = sys.argv[1]

vdw, multipole, polar = [], [], []
with open(log_file, mode='r') as f:
    for line in f:
        if 'Intermolecular Energy' in line:
            get_data(line, inter)
        elif 'Van der Waals' in line:
            get_data(line, vdw)
        elif 'Atomic Multipoles' in line:
            get_data(line, multipole)
        elif 'Polarization' in line:
            get_data(line, polar)
        else:
            pass

df = pd.DataFrame({'vdw':vdw, 'multipole':multipole, 'polar':polar})
df.to_csv(f'./{log_file[:-4]}.csv', index=False)
