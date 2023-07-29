import mdtraj as md
import numpy as np
import copy
import matplotlib.pyplot as plt
import json
import time
start_time = time.time()

# A:  anion
# B:  cation

def dist_check(uvec):
	dist_check = np.sqrt((uvec*uvec).sum(axis=2))
	print(dist_check)
	return

def unitvector(vec):
	nvecs = len(vec)
	natoms = len(vec[0,:,0])
	l2norm = np.sqrt((vec*vec).sum(axis=2))
	# print(np.shape(vec))
	# print(np.shape(l2norm))
	# a = vec/l2norm.reshape(nvecs,natoms,1)
	# print(np.shape(a))
	return vec/l2norm.reshape(nvecs,natoms,1)

def gettheta(unitvec1,unitvec2):
	nvecs = len(unitvec2) # n_frames, equivalent to np.shape(unitvec2)[0]
	costheta = np.sum(unitvec2*unitvec1.reshape(nvecs,1,3),axis=-1) # [n_frames, n_pairs]
	return np.arccos(costheta)*180/np.pi # costheta

def getrandtheta(traj,source_A,source_B,angle_A):
	# source_A = central anion atom (i.e. array of atom indeces)
	# angle_A = "tail" anion atom; theta = angle formed by source_B -- source_A -- angle_A
	# source_B = central cation atom

	nsource_A = len(source_A)
	nsource_B = len(source_B)
	theta_array = np.array([])
	dist_array = np.array([])
	norm = nsource_A*nsource_B * np.sum(1.0 / traj.unitcell_volumes) # average number concentration

	pairs = np.stack((source_A, angle_A), axis=-1) # source_A to angle_A
	disps = md.compute_displacements(traj, pairs, periodic=True, opt=True) # [n_frames, n_pairs, 3], within A
	uvec_A = unitvector(disps) # [n_frames, n_pairs, 3]

	for i in range(0, nsource_A): # N.B. iterate over A
		sourcearray = np.full(nsource_B, source_A[i], dtype=int)
		pairs = np.stack((sourcearray, source_B), axis=-1) # source_A to source_B

		dists = md.compute_distances(traj, pairs, periodic=True, opt=True) # [n_frames, n_pairs]
		dist_array = np.append(dist_array,dists.flatten())

		disps = md.compute_displacements(traj, pairs, periodic=True, opt=True) # [n_frames, n_pairs, 3], A to B
		uvec_B = unitvector(disps) # [n_frames, n_pairs, 3]
		thetas = gettheta(uvec_A[:,i,:],uvec_B) # [n_frames, n_pairs]
		theta_array = np.append(theta_array,thetas.flatten())

	return dist_array, theta_array, norm

def get_phi_dihedral(traj, angle_B, source_B, source_A, angle_A):
	phi_array = np.array([])
	for i, (val_source_A, val_angle_A) in enumerate(zip(source_A, angle_A)):
		source_A_array = np.full(len(source_B), val_source_A, dtype=int)
		angle_A_array  = np.full(len(source_B), val_angle_A, dtype=int)
		indices = np.stack((angle_B, source_B, source_A_array, angle_A_array), axis=-1)
		phis = np.abs(md.compute_dihedrals(traj, indices, periodic=True))
		phi_array = np.append(phi_array, phis.flatten())
	return phi_array * 180/np.pi

def get_phi_plane(traj, plane_1, plane_2, plane_3, source_B, source_A):
	# https://onlinemschool.com/math/library/analytic_geometry/plane_line/#:~:text=Proof%20of%20the%20formula%20of%20angle%20between%20line%20and%20plane,-From%20the%20equation&text=Since%20%CF%86%20%3D%2090%C2%B0%20%2D%20%CF%88,the%20line%20and%20the%20plane.
	# plane points are in the cation (B)

	pairs = np.stack((plane_1, plane_2), axis=-1)
	in_plane_1 = md.compute_displacements(traj, pairs, periodic=True, opt=True)
	uvec_in_plane_1 = unitvector(in_plane_1) # [n_frames, n_pairs, 3]

	pairs = np.stack((plane_1, plane_3), axis=-1)
	in_plane_2 = md.compute_displacements(traj, pairs, periodic=True, opt=True)
	uvec_in_plane_2 = unitvector(in_plane_2) # [n_frames, n_pairs, 3]

	plane_normal = np.cross(uvec_in_plane_1, uvec_in_plane_2)
	uvec_plane_normal = unitvector(plane_normal)

	phi_array = np.array([])
	for i, val_source_A in enumerate(source_A):
		source_A_array = np.full(len(source_B), val_source_A, dtype=int)
		pairs = np.stack((source_B, source_A_array), axis=-1)
		B_to_A = md.compute_displacements(traj, pairs, periodic=True, opt=True)
		uvec_B_to_A = unitvector(B_to_A) # [n_frames, n_pairs, 3]
		sin_phis = np.abs(np.sum(uvec_plane_normal*uvec_B_to_A, axis=-1))
		phis = np.arcsin(sin_phis)
		phi_array = np.append(phi_array, phis.flatten())
	return phi_array * 180/np.pi


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

f = open('./rshell.json')
rshell_data = json.load(f)

for k, engine in enumerate(['namd', 'namd_scaled', 'openmm']):
	for i, cation in enumerate(['guan', 'imim', 'mamm']):
		for j, anion in enumerate(['acet', 'esna', 'mso4']):
			rshell = rshell_data[engine][f'{anion}_{cation}'] / 10.0 # nm

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

			source_A = top.select(anion_atoms[anion]) # central anion atom (i.e. array of atom indeces)
			angle_A = top.select(anion_angle_atoms[anion]) # "tail" anion atom; theta = angle formed by source_B -- source_A -- angle_A
			source_B = top.select(cation_atoms[cation]) # central cation atom

			dist_array, theta_array, norm = getrandtheta(traj, source_A, source_B, angle_A)

			if cation == 'guan':
				plane_1 = top.select('resname GUAN and name N1')
				plane_2 = top.select('resname GUAN and name N2')
				plane_3 = top.select('resname GUAN and name N3')
				phi_array = get_phi_plane(traj, plane_1, plane_2, plane_3, source_B, source_A)
				# phi_edges = np.linspace(0, 90, 50)
			elif cation == 'imim':
				plane_1 = top.select('resname IMIM and name CG')
				plane_2 = top.select('resname IMIM and name CD2')
				plane_3 = top.select('resname IMIM and name CE1')
				phi_array = get_phi_plane(traj, plane_1, plane_2, plane_3, source_B, source_A)
				# phi_edges = np.linspace(0, 90, 50)
			elif cation == 'mamm':
				angle_B = top.select('resname MAMM and name CE')
				phi_array = get_phi_dihedral(traj, angle_B, source_B, source_A, angle_A)
				# phi_edges = np.linspace(0, 180, 50)
			else:
				assert False

			bound_theta_array = theta_array[dist_array <= rshell]
			bound_phi_array = phi_array[dist_array <= rshell]

			# np.savetxt(f'{engine}_{anion}_{cation}_dist_array.dat', dist_array, fmt='%.18e')
			# np.savetxt(f'{engine}_{anion}_{cation}_theta_array.dat', theta_array, fmt='%.18e')
			# np.savetxt(f'{engine}_{anion}_{cation}_phi_array.dat', phi_array, fmt='%.18e')
			np.savetxt(f'{engine}_{anion}_{cation}_bound_theta_array.dat', bound_theta_array, fmt='%.18e')
			np.savetxt(f'{engine}_{anion}_{cation}_bound_phi_array.dat', bound_phi_array, fmt='%.18e')

			seconds = time.time() - start_time
			print(f'{seconds:.2f} seconds')
