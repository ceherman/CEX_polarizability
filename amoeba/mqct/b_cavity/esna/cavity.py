from openmm.app import *
from openmm import *
from openmm.unit import *
from dcdsubsetreporter import DCDSubsetReporter
from sys import stdout, argv
import numpy as np
import datetime

# As before (in brute-force ion-pair simulations)
def print_time(return_time=False):
	system_time = datetime.datetime.now()
	print("\nSystem Time is:", system_time)
	if return_time:
		return system_time
	else:
		return

temperature = 298*kelvin
pressure = 1*bar
timestep = 1.0*femtoseconds

system_time_1 = print_time(True)
print('Creating the simulation system...')

platform = Platform.getPlatformByName('CUDA')
properties = {'Precision':'mixed'}

pdb = PDBFile('../starting.pdb')
allatominfo = list(pdb.topology.atoms())

forcefield = ForceField('../../AMOEBA-BIO-2018_residues_zero_masses.xml')
system = forcefield.createSystem(pdb.topology, nonbondedMethod=PME,
								 nonbondedCutoff=1*nanometer,
                                 ewaldErrorTolerance=1e-5,
								 polarization='mutual',
                                 mutualInducedTargetEpsilon=1e-5)
integrator = LangevinMiddleIntegrator(temperature, 10/picoseconds, timestep)
# integrator = NoseHooverIntegrator(temperature, 10/picosecond, timestep)
barostat = MonteCarloBarostat(pressure,temperature)
system.addForce(barostat)

# Defining the groups of forces
for force in system.getForces():
    if isinstance(force, AmoebaMultipoleForce) or isinstance(force, AmoebaVdwForce) or isinstance(force, AmoebaGeneralizedKirkwoodForce):
        force.setForceGroup(1)

# Sphere forces (for each ion heavy atom)
half_length = 3.56 / 2.0 # nanometers
pdb_heavy = PDBFile('heavy.pdb')

for i, atom in enumerate(pdb_heavy.positions):
	x0 = (atom.x + half_length) * nanometer
	y0 = (atom.y + half_length) * nanometer
	z0 = (atom.z + half_length) * nanometer

	my_function = f'4.0*epsilon{i}*(frac^6)*((frac^6) - 1.0) + epsilon{i};\
	                frac = sigma{i}/(r- bubble{i} + sigma{i}*(2^(1/6)));\
	                r = min(bubble{i},abs(periodicdistance(x, y, z, x{i}, y{i}, z{i})));'
	print(my_function)
	sphereforce = CustomExternalForce(my_function)
	sphereforce.addGlobalParameter(f"x{i}", x0)
	sphereforce.addGlobalParameter(f"y{i}", y0)
	sphereforce.addGlobalParameter(f"z{i}", z0)

	sphereforce.addGlobalParameter(f"epsilon{i}", 0.155425*kilocalories_per_mole)
	sphereforce.addGlobalParameter(f"sigma{i}", 3.165492*angstrom)
	sphereforce.addGlobalParameter(f"bubble{i}", 0*angstrom)

	Oindexlist = []
	for i in range(system.getNumParticles()):
	    if allatominfo[i].name == 'O':
	        sphereforce.addParticle(i, [])
	        Oindexlist.append(i)
	system.addForce(sphereforce)

# # What I used to check
# for i, atom in enumerate(pdb_heavy.positions):
# 	print(atom.x + half_length, atom.y + half_length, atom.z + half_length)
# # Other part of the check
# for k, force in enumerate(system.getForces()[-4:]):
# 	print('\n', k)
# 	for i in range(force.getNumGlobalParameters()):
# 		print(force.getGlobalParameterName(i), force.getGlobalParameterDefaultValue(i))

bubbles = [ 0.0254, 0.1292, 0.2971, 0.5000, 0.7029, 0.8708, 0.9746,
			1.0254, 1.1292, 1.2971, 1.5000, 1.7029, 1.8708, 1.9746,
			2.0254, 2.1292, 2.2971, 2.5000, 2.7029, 2.8708, 2.9746,
			3.0254, 3.1292, 3.2971, 3.5000, 3.7029, 3.8708, 3.9746,
			4.0254, 4.1292, 4.2971, 4.5000, 4.7029, 4.8708, 4.9746]*angstrom


nstates = len(bubbles)
nsteps_per_eql = 100000
nsteps_per_prod = 300000
totaltimemax = (nsteps_per_eql+nsteps_per_prod)*nstates

simulation = Simulation(pdb.topology, system, integrator, platform, properties)
simulation.context.setPositions(pdb.positions)
print_time()
print('The simulation system has been created. Preparing for simulation...')

simulation.context.setVelocitiesToTemperature(temperature)
simulation.reporters.append(StateDataReporter('sim.log', 1000, step=True, time=True, totalEnergy=True, potentialEnergy=True, kineticEnergy=True,
											  temperature=True, volume=True, density=True, elapsedTime=True))
simulation.reporters.append(StateDataReporter(stdout, 1000, step=True, totalEnergy=True, remainingTime=True, totalSteps=totaltimemax))


for k in range(nstates):
	print('bubble radius:', bubbles[k])
	for i, atom in enumerate(pdb_heavy.positions):
		simulation.context.setParameter(f'bubble{i}', bubbles[k])
		# print(simulation.context.getParameter(f'bubble{i}'))

	print_time()
	print('Starting equilibration...\n')
	simulation.step(nsteps_per_eql)

	simulation.reporters.append(DCDSubsetReporter('prod' + str(k) + '.dcd', 25, Oindexlist))

	print_time()
	print('Starting production...\n')
	simulation.step(nsteps_per_prod)

	simulation.reporters.pop(-1)
	simulation.saveState('State' + str(k) + '.stt' )

system_time_2 = print_time(True)
print('Finished simulation.\n')
time_delta = system_time_2 - system_time_1
print(f'Total simulation time:  {time_delta}')
