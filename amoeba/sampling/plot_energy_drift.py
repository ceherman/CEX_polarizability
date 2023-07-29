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
        if data_dir == 'acet_guan' or data_dir == 'esna_guan' or data_dir == 'mso4_mamm':
            data = pd.concat([pd.read_csv(f'./{data_dir}/sim_1.log'), pd.read_csv(f'./{data_dir}/sim_2.log')])
        else:
            data = pd.read_csv(f'./{data_dir}/sim_1.log')
        data.rename(columns={'#"Progress (%)"':'Progress (%)'}, inplace=True)

        xlabel = 'Time (ps)'
        ylabel = 'Total Energy (kJ/mole)'
        fig, ax = my_plot.instantiate_fig(xlabel=xlabel, ylabel=ylabel)
        ax.plot(data[xlabel], data[ylabel])

        my_plot.set_layout(fig, ax)
        fig.subplots_adjust(hspace=0)
        fig.savefig(f'./images/energy_drift_plots_{data_dir}.png', dpi=300)
