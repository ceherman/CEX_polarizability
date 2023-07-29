import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

fig, ax = my_plot.instantiate_fig()
plt.close()

n = 1
fs_per_step = 2

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
        df['time_ns'] = df['TS'] * fs_per_step * 1e-6
    return df

for j, anion in enumerate(['acet', 'esna', 'mso4']): # enumerate(['acet']):
    for i, cation in enumerate(['guan', 'mamm', 'imim']): # enumerate(['guan']):
        data_dir = f'{anion}_{cation}'
        df = get_log_data(f'./{data_dir}/sampling_{n}.log')

        entries = ['TEMP', 'PRESSURE', 'VOLUME', 'TOTAL']
        fig, ax = plt.subplots(len(entries), 1, sharex=True)
        fig.set_size_inches(6, len(entries)*3.5, forward=True)
        ax[len(entries)-1].set_xlabel('Time [ns]')

        for i, ylabel in enumerate(entries):
            ax[i].set_ylabel(ylabel)
            ax[i].plot(df['time_ns'], df[ylabel])

        my_plot.set_layout(fig, ax)
        fig.subplots_adjust(hspace=0)
        fig.savefig(f'./images/equilibration_plots_{n}_{data_dir}.png', dpi=300)

        print(data_dir)
