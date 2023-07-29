import numpy as np

# acet_guan
Ka = 0.37 # [M^-1]
c = 0.474608 # [M]

# acet_mamm
Ka = 0.31 # [M^-1]
c = 0.477750 # [M]

cmin, cmax = c, c

prod = Ka * (cmax + cmin)
pbound = (1 + prod - np.sqrt((prod + 1)**2 - 4*Ka**2 * cmax * cmin))/(2*Ka*cmin)

print(pbound)

# acet_guan 0.13223374405351188
# acet_mamm 0.11579046062614501
