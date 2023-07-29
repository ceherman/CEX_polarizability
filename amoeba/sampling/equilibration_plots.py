import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
sys.path.append('/home/chase/codes/python_functions')
import plotting as my_plot

fig, ax = my_plot.instantiate_fig()
plt.close()

for j, anion in enumerate(['acet', 'esna', 'mso4']):
    for i, cation in enumerate(['guan', 'mamm', 'imim']):
        data_dir = f'{anion}_{cation}'
        data = pd.read_csv(f'./{data_dir}/sim_0.log')
        data.rename(columns={'#"Progress (%)"':'Progress (%)'}, inplace=True)

        xlabel = 'Time (ps)'
        ylabels = ['Temperature (K)', 'Total Energy (kJ/mole)', 'Box Volume (nm^3)']

        fig, ax = plt.subplots(3, 1, sharex=True)
        fig.set_size_inches(6, 11, forward=True)
        ax[2].set_xlabel(xlabel)
        for i, ylabel in enumerate(ylabels):
            ax[i].set_ylabel(ylabel)
            ax[i].plot(data[xlabel], data[ylabel])

        my_plot.set_layout(fig, ax)
        fig.subplots_adjust(hspace=0)
        fig.savefig(f'./images/equilibration_plots_{data_dir}.png', dpi=300)
