import sys
import MDAnalysis as mda
import numpy as np

import block_averaging_functions as block_average

dcd_file = sys.argv[1]
psf_file = sys.argv[2]

u = mda.Universe(psf_file, dcd_file)

box_length = []
for ts in u.trajectory:
    assert ts.dimensions[0] == ts.dimensions[1] == ts.dimensions[2]
    box_length.append(ts.dimensions[0])
box_length = np.array(box_length)
# np.savetxt('box_length.dat', box_length, fmt='%.10f')

stats = block_average.std_eom(box_length)
out = np.array([[stats[0], stats[-1]]])
np.savetxt('box_length.dat', out, fmt='%.10f', delimiter='\t')




