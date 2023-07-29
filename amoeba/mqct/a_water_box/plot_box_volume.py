import numpy as np
import pandas as pd
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot
fig, ax = my_plot.instantiate_fig()
plt.close()

df = pd.read_csv('./sim_0.log')
xlabel, ylabel = 'Time (ps)', "Box Volume (nm^3)"

fig, ax = my_plot.instantiate_fig(xlabel=xlabel, ylabel=ylabel)
ax.plot(df[xlabel], df[ylabel])
my_plot.set_layout(fig, ax)
plt.savefig('./box_volume_evolution.png', dpi=300, bbox_inches='tight')
