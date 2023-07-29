import numpy as np
import pandas as pd
import sys
sys.path.append('/home/chase/codes/python_functions')
import matplotlib.pyplot as plt
import plotting as my_plot

fig, ax = my_plot.instantiate_fig()
plt.close()

## More general
# cmin, cmax = c, c
# prod = Ka * (cmax + cmin)
# pbound = (1 + prod - np.sqrt((prod + 1)**2 - 4*Ka**2 * cmax * cmin))/(2*Ka*cmin)

## Stoichiometic solution
# prod = c * Ka

vals = np.linspace(0.001, 1, 1000)
p_bound = np.zeros(len(vals))
for i, prod in enumerate(vals):
    p_bound[i] = (1 + 2*prod - np.sqrt(4*prod + 1))/(2*prod)

fig, ax = my_plot.instantiate_fig(xlabel=r'$K_{A} c$', ylabel=r'$P_{\mathsf{bound}}$')
ax.plot(vals, p_bound)
ax.set_xlim(0, max(vals))
ax.set_ylim(0, max(p_bound))
my_plot.set_layout(fig, ax)

# plt.show()
fig.savefig(f'./images/pbound_equation_stoichiometric_solution.png', dpi=300)
