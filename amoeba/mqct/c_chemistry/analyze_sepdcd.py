import matplotlib.pyplot as plt
import itertools
import mdtraj as md
import numpy as np
from numpy.core.fromnumeric import mean
from mywallfunction import forcelj126wall
forcelj126wall_v = np.vectorize(forcelj126wall)

bubbles = np.array([ 2.0254, 2.1292, 2.2971, 2.5000, 2.7029, 2.8708, 2.9746,
                     3.0254, 3.1292, 3.2971, 3.5000, 3.7029, 3.8708, 3.9746,
                     4.0254, 4.1292, 4.2971, 4.5000, 4.7029, 4.8708, 4.9746])/10

nstates = len(bubbles)
topfile = '../starting_O.pdb'
dcdindicator = 'prod'
epsilon = 0.155425 # check units with Arjun
sigma = 0.3165492 # nm

testfile = dcdindicator + '0.dcd'
trajog = md.load(testfile, top=topfile) # original trajectory
nframes = trajog.n_frames
natoms = trajog.n_atoms

# Add dummy heavy atoms
half_length = 3.56 / 2.0 # nanometers
traj_heavy = md.load('heavy.pdb', top='heavy.pdb')
xyz_heavy_shifted = traj_heavy.xyz[0] + half_length
top_heavy = traj_heavy.topology
res_name_heavy = top_heavy.residue(0).name

xyz2 = np.zeros([nframes,traj_heavy.n_atoms,3])
for i in range(nframes):
    xyz2[i,:,:] = xyz_heavy_shifted
traj2 = md.Trajectory(xyz=xyz2, topology=top_heavy)

traj = trajog.stack(traj2)
topology = traj.topology
heavy_idx = topology.select(f"resname {res_name_heavy}")
oxygenids = topology.select("water and name O")
noxygens = len(oxygenids)

# print([topology.atom(i) for i in heavy_idx])
# print(noxygens)

pairs_list = []
for i in heavy_idx:
    atom_id = np.full(len(oxygenids), i)
    pairs_list.append(np.stack((atom_id, oxygenids), axis=-1))

for i, bubble_val in enumerate(bubbles):
    total_force = np.zeros((nframes,1))
    for pairs in pairs_list:
        all_out = []
        mylambda = bubble_val - sigma*(2**(1/6))
        dcdfile = dcdindicator + str(i) + '.dcd'
        trajog = md.load(dcdfile, top=topfile)
        traj = trajog.stack(traj2)
        dists = md.compute_distances(traj, pairs, periodic=True, opt=True)
        forces = np.zeros((nframes,1))
        for frame in range(0,nframes):
            dists_compare = dists[frame]
            neededargs = np.nonzero(dists_compare<bubble_val)[0]
            if neededargs.size != 0:
                forces[frame]=np.sum(forcelj126wall_v(dists_compare[neededargs],bubble_val,epsilon,sigma,mylambda))
        total_force += forces
    np.savetxt('force' + str(i) + '.dat', total_force, fmt='%15.10f')
    print("%8.4f %8.4f" % (bubble_val*10,np.mean(total_force)))
