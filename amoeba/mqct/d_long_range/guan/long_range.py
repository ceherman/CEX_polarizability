from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout, argv
import numpy as np
import datetime

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

pdb = PDBFile('./starting.pdb')
allatominfo = list(pdb.topology.atoms())

forcefield = ForceField('../../AMOEBA-BIO-2018_residues_zero_masses.xml')
system = forcefield.createSystem(pdb.topology, nonbondedMethod=PME,
								 nonbondedCutoff=1*nanometer,
                                 ewaldErrorTolerance=1e-5,
								 polarization='mutual',
                                 mutualInducedTargetEpsilon=1e-5)
integrator = LangevinMiddleIntegrator(temperature, 10/picoseconds, timestep)
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
	# print(my_function)
	sphereforce = CustomExternalForce(my_function)
	sphereforce.addGlobalParameter(f"x{i}", x0)
	sphereforce.addGlobalParameter(f"y{i}", y0)
	sphereforce.addGlobalParameter(f"z{i}", z0)

	sphereforce.addGlobalParameter(f"epsilon{i}", 0.155425*kilocalories_per_mole)
	sphereforce.addGlobalParameter(f"sigma{i}", 3.165492*angstrom)
	sphereforce.addGlobalParameter(f"bubble{i}", 0.0*angstrom)

	Oindexlist = []
	for i in range(system.getNumParticles()):
	    if allatominfo[i].name == 'O':
	        sphereforce.addParticle(i, [])
	        Oindexlist.append(i)
	system.addForce(sphereforce)

simulation = Simulation(pdb.topology, system, integrator, platform, properties)
simulation.context.setPositions(pdb.positions)
print_time()
print('The simulation system has been created. Preparing for simulation...')

simulation.minimizeEnergy()
simulation.context.setVelocitiesToTemperature(temperature)

simulation.reporters.append(StateDataReporter('sim.log', 1000, step=True, time=True, totalEnergy=True, potentialEnergy=True, kineticEnergy=True,
											  temperature=True, volume=True, density=True, elapsedTime=True))
simulation.reporters.append(StateDataReporter(stdout, 1000, step=True, totalEnergy=True))


bubbles = [ 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0 ]*angstrom
nstates = len(bubbles)

for k in range(nstates):
	print('bubble radius:', bubbles[k])
	for i, atom in enumerate(pdb_heavy.positions):
		simulation.context.setParameter(f'bubble{i}', bubbles[k])
	simulation.step(1000)

simulation.saveState('after_expansion.xml' )
positions = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(simulation.topology, positions, open(f'after_expansion.pdb', 'w'))

print_time()
print('Starting equilibration...\n')
simulation.step(100000)

simulation.saveState('after_equilibration.xml' )
positions = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(simulation.topology, positions, open(f'after_equilibration.pdb', 'w'))


simulation.reporters.append(DCDReporter(f'prod.dcd', 100))
print_time()
print('Starting production...\n')
simulation.step(900000)

simulation.saveState('after_production.xml' )
positions = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(simulation.topology, positions, open(f'after_production.pdb', 'w'))


system_time_2 = print_time(True)
print('Finished simulation.\n')
time_delta = system_time_2 - system_time_1
print(f'Total simulation time:  {time_delta}')
