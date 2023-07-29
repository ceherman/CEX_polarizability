import numpy as np
import pandas as pd
import os
import sys
import json
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

ion = sys.argv[1]

fig, ax = my_plot.instantiate_fig()
plt.close()

df = pd.read_csv('./sim.log')
xlabel, ylabel = 'Time (ps)', "Box Volume (nm^3)"

fig, ax = my_plot.instantiate_fig(xlabel=xlabel, ylabel=ylabel)
ax.plot(df[xlabel], df[ylabel])
my_plot.set_layout(fig, ax)
plt.savefig(f'../images/box_volumes/{ion}.png', dpi=300, bbox_inches='tight')
