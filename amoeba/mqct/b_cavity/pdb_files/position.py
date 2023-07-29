import mdtraj as md

for ion in ['acet', 'esna', 'mso4', 'guan', 'imim', 'mamm']:
    pdbfile = f'{ion}.pdb'
    traj = md.load(pdbfile, top=pdbfile)
    center = md.compute_center_of_mass(traj)[0]
    traj.xyz[0] -= center
    # traj.save(f'{ion}_centered.pdb')

