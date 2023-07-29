from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout, argv
import numpy as np
import datetime

# Functions____________________________________________________________________

def print_time(return_time=False):
	system_time = datetime.datetime.now()
	print("\nSystem Time is:", system_time)
	if return_time:
		return system_time
	else:
		return

# Major intput params__________________________________________________________

iteration = 0
new_time_ns = 0.3*nanoseconds
prev_cumulative_time_ns = 0.0*nanoseconds

temperature = 298*kelvin
pressure = 1*bar
timestep = 1.0*femtoseconds

new_steps = round(new_time_ns/timestep)
prev_steps = round(prev_cumulative_time_ns/timestep)

# Ceate simulation system______________________________________________________

system_time_1 = print_time(True)
print('Creating the simulation system...')

platform = Platform.getPlatformByName('CUDA')
properties = {'Precision':'mixed'}

pdb = PDBFile('starting.pdb')
forcefield = ForceField('AMOEBA-BIO-2018_residues.xml')
system = forcefield.createSystem(pdb.topology, nonbondedMethod=PME, 
								 nonbondedCutoff=1*nanometer,
                                 ewaldErrorTolerance=1e-5, 
								 polarization='mutual',
                                 mutualInducedTargetEpsilon=1e-5)
integrator = LangevinMiddleIntegrator(temperature, 10/picoseconds, timestep)
# integrator = NoseHooverIntegrator(temperature, 10/picosecond, timestep)
barostat = MonteCarloBarostat(pressure,temperature)
system.addForce(barostat)
simulation = Simulation(pdb.topology, system, integrator, platform, properties)

print_time()
print('The simulation system has been created. Preparing for simulation...')

# Prepare the system for simulation____________________________________________

if iteration == 0:
	simulation.context.setPositions(pdb.positions)
	print_time()
	print('Starting minimization...')
	simulation.minimizeEnergy()
	print_time()
	print('Minimization complete.')
	simulation.context.setVelocitiesToTemperature(temperature)
elif iteration > 0:
	prev_iteration = iteration - 1
	simulation.loadCheckpoint(f'checkpoint_{prev_iteration}.chk')
	print_time()
	print(f'The checkpoint_{prev_iteration}.chk file has been loaded.')

# Run__________________________________________________________________________

simulation.reporters.append(StateDataReporter(f'sim_{iteration}.log', 100, 
							step=True, time=True, totalEnergy=True, 
							potentialEnergy=True, kineticEnergy=True, 
							temperature=True, volume=True, density=True, 
							elapsedTime=True, progress=True, 
							remainingTime=True,
							totalSteps=prev_steps+new_steps)) 
simulation.reporters.append(DCDReporter(f'trajectory_{iteration}.dcd', 100))
simulation.reporters.append(CheckpointReporter(f'checkpoint_{iteration}.chk', 100))

print_time()
print('Starting simulation...\n')
simulation.step(new_steps)

simulation.saveState(f'final_state_{iteration}.xml')
positions = simulation.context.getState(getPositions=True).getPositions()
PDBFile.writeFile(simulation.topology, positions, 
				  open(f'final_position_{iteration}.pdb', 'w'))

system_time_2 = print_time(True)
print('Finished simulation.\n')

time_delta = system_time_2 - system_time_1
print(f'Total simulation time:  {time_delta}')
