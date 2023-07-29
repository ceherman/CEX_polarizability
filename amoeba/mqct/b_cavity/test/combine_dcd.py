import mdtraj as md

pdbfile = f'../starting_O.pdb'
dcd_files = [f'prod{i}.dcd' for i in range(35)]
traj = md.load(dcd_files, top=pdbfile)
traj.save('combined.dcd')


# # From Arjun - mdtraj
# import mdtraj as md
# import numpy as np

# fileid = np.array([1, 3, 18, 50])
# nstates = len(bubbles)

# trajarr = []
# for i in range(nstates):
#     traj = md.load('traj_' + '{:2.0f}'.format(fileid[i]) + '.dcd', top='psffile.psf')
#     trajarr.append(traj)
#     print(traj.n_frames)

# fulltraj = md.join(trajarr)
# fulltraj.save_dcd('allframes.dcd')



# # From Arjun - MDAnalysis
# import MDAnalysis as mda
# import numpy as np
# import glob, sys

# preq = sys.argv[1] #'../charmm/FabFab_Mab1_charmm_00_'
# filenames = glob.glob(preq + '_*.dcd')
# filenames.sort()

# u = mda.Universe('../combine-psfgen/FabFab_Mab1.psf',[filenames])
# lu = len(u.atoms)

# with mda.Writer(preq + '.dcd', n_atoms=lu) as w:
#     for ts in u.trajectory:
#         w.write(u.atoms)


# # Also be aware of catdcd
