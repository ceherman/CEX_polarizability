import mdtraj as md
import numpy as np

pdbfile = './heavy.pdb'
traj_heavy = md.load(pdbfile, top=pdbfile)
half_length = 3.56 / 2.0 # nanometers
traj_heavy.xyz[0] += half_length
traj_heavy.save('check_heavy_shifted.pdb')
