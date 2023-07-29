import mdtraj as md
import numpy as np
import copy
import matplotlib.pyplot as plt

def dist_check(uvec):
	dist_check = np.sqrt((uvec*uvec).sum(axis=2))
	print(dist_check)

def unitvector(vec):
	nvecs = len(vec)
	natoms = len(vec[0,:,0])
	l2norm = np.sqrt((vec*vec).sum(axis=2))
	print(np.shape(vec))
	print(np.shape(l2norm))
	return vec/l2norm.reshape(nvecs,natoms,1)

def gettheta(unitvec1,unitvec2):
	nvecs = len(unitvec2)
	costheta = np.sum(unitvec2*unitvec1.reshape(nvecs,1,3),axis=-1)
	return np.arccos(costheta)*180/np.pi # costheta #

def getrandtheta(traj,source_A,source_B,angle_A):
	nsource_A = len(source_A)
	nsource_B = len(source_B)
	norm = nsource_A*nsource_B * np.sum(1.0 / traj.unitcell_volumes)
	theta_array = np.array([])
	dist_array = np.array([])
	pairs = np.stack((source_A, angle_A), axis=-1)
	disps = md.compute_displacements(traj, pairs, periodic=True, opt=True)
	uvec_A = unitvector(disps)
	#pairs = np.stack((source_B, target_B), axis=-1)
	#disps = md.compute_displacements(traj, pairs, periodic=True, opt=True)
	#uvec_B = unitvector(disps)

	for i in range(0,nsource_A):
		sourcearray = np.full(nsource_B, source_A[i], dtype=int)
		pairs = np.stack((sourcearray, source_B), axis=-1)
		dists = md.compute_distances(traj, pairs, periodic=True, opt=True)
		dist_array = np.append(dist_array,dists.flatten())

		disps = md.compute_displacements(traj, pairs, periodic=True, opt=True)
		uvec_B = unitvector(disps)
		thetas = gettheta(uvec_A[:,i,:],uvec_B)
		theta_array = np.append(theta_array,thetas.flatten())
	return dist_array, theta_array, norm


cation_atoms = {
    'guan':'resname GUAN and name C',
	'imim':'resname IMIM and name CE1',
	'mamm':'resname MAMM and name NZ'
}

anion_atoms = {
	'acet':'resname ACET and name C2',
	'esna':'resname ESNA and name S',
	'mso4':'resname MSO4 and name S',
}

anion_angle_atoms = {
	'acet':'resname ACET and name C1',
	'esna':'resname ESNA and name C1',
	'mso4':'resname MSO4 and name OS1',
}

for k, engine in enumerate(['namd', 'namd_scaled', 'openmm']):
	for i, cation in enumerate(['guan', 'imim', 'mamm']):
		for j, anion in enumerate(['acet', 'esna', 'mso4']):
			if engine == 'namd':
				data_dir = f'/lustre/lenhoff/users/2688/namd/brute_force_tip/{anion}_{cation}'
				dcd_files = ['sampling_1.dcd']
			elif engine == 'namd_scaled':
				data_dir = f'/lustre/lenhoff/users/2688/namd/brute_force_tip_scaled/{anion}_{cation}'
				if (anion == 'acet' and (cation == 'imim' or cation == 'mamm')) or (anion == 'esna' and (cation == 'guan' or cation == 'imim')):
					dcd_files = ['sampling_1.dcd', 'sampling_2.dcd']
				else:
					dcd_files = ['sampling_1.dcd']
			elif engine == 'openmm':
				data_dir = f'/lustre/lenhoff/users/2688/ion_pairs/{anion}_{cation}'
				if (cation == 'guan' and (anion == 'acet' or anion == 'esna')) or (cation == 'mamm' and anion == 'mso4'):
					dcd_files = ['trajectory_1.dcd', 'trajectory_2.dcd']
				else:
					dcd_files = ['trajectory_1.dcd']
			else:
				assert False

			pdbname = f'{data_dir}/starting.pdb'
			dcdname = [f'{data_dir}/{dcd}' for dcd in dcd_files]

			traj = md.load(dcdname, top=pdbname)
			top = traj.topology

			source_A = top.select(anion_atoms[anion])
			angle_A = top.select(anion_angle_atoms[anion])
			source_B = top.select(cation_atoms[cation])

			dist_array, theta_array, norm = getrandtheta(traj, source_A, source_B, angle_A)

			thetaedges  = np.linspace(0, 180, 50)
			distedges  = np.linspace(0, 2, 100)
			H, xedge, yedge = np.histogram2d(dist_array,theta_array,bins=(distedges, thetaedges))

			V = (4 / 3) * np.pi * (np.power(xedge[1:], 3) - np.power(xedge[:-1], 3))
			ntheta = len(yedge)-1
			V_per_bin = V #/ntheta*ntheta
			H = H.T/(norm*V_per_bin)

			np.savetxt(f'{engine}_{anion}_{cation}_xedge.dat',xedge,fmt='%.18e')
			np.savetxt(f'{engine}_{anion}_{cation}_yedge.dat',yedge,fmt='%.18e')
			np.savetxt(f'{engine}_{anion}_{cation}_hists.dat',H.T,fmt='%.18e')


