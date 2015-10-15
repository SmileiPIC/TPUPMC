# ---------------------------------------------
# SIMULATION PARAMETERS FOR THE PIC-CODE SMILEI
# ---------------------------------------------


# dim: Geometry of the simulation
dim = '1d3v'


# order of interpolation
#
interpolation_order = 2

# SIMULATION TIME 
# either use the resolution (res_time) or time-step (timestep)
#
# res_time  : temporal resolution 
# time step : time step
# sim_time  : duration of the simulation 
#
timestep = 0.9e-2
sim_time = 100.0

# SIMULATION BOX : for all space directions (in 2D & 3D use vector of doubles)
# either use the resolution (res_space) or cell-length (cell_length)
#
# res_space   : spatial resolution 
# sim_length  : length of the simulation 
# cell_length : cell-length 
#
cell_length = 1.0e-2
sim_length  = 1.03


# ELECTROMAGNETIC BOUNDARY CONDITIONS
# bc_em_type_long/trans : boundary conditions used for EM fields 
#                         in the longitudinal or transverse directions
#                         periodic      = periodic BC (using MPI topology)
#                         silver-muller = injecting/absorbing
#
bc_em_type_x = ['periodic']


# RANDOM seed 
# this is used to randomize the random number generator
#
random_seed = 0


# DEFINE ALL SPECIES
# species_type: ion, electron, positron, test ...
# initialization_type: regular, cold or (isotrop) Maxwell?~H~RJuettner distribution
# n_part_per_cell: number of particle?~H~Rper?~H~Rcell
# c_part_max: factor on the memory reserved for the total number of particles
# mass: particle mass in units of the electron mass
# charge: particle charge in units of e (?~H~Re is the electron charge)
# density: species density in units of the normalization density
# mean_velocity: mean velocity of the species (3D vector) in units of the light velocity
# temperature: temperature of the species in units of m_e c^2
# dynamics_type: species type of dynamics = norm or rrLL
# time_frozen: time during which the particles are frozen in units of the normalization time
# radiating: boolean, if true incoherent radiation are calculated using the Larmor formula 
#

npart=10

Species(
	species_type = 'ion',
	initPosition_type = 'regular',
	initMomentum_type = 'cold',
	n_part_per_cell = npart,
	mass = 1836.0,
	charge = 1.0,
	nb_density = 1.0,
	time_frozen = 10000.0,
	bc_part_type_west = 'none',
	bc_part_type_east = 'none'
)


Species(
	species_type = "eon1",
	initPosition_type = "regular",
	initMomentum_type = "cold",
	n_part_per_cell = npart/2,
	mass = 1.0,
	charge = -1.0,
	nb_density = 0.5,
	bc_part_type_west = "none",
	bc_part_type_east = "none",
	mean_velocity = [0.1, 0, 0] 
)

Species(
	species_type = "eon2",
	initPosition_type = "regular",
	initMomentum_type = "cold",
	n_part_per_cell = npart/2,
	mass = 1.0,
	charge = -1.0,
	nb_density = 0.5,
	bc_part_type_west = "none",
	bc_part_type_east = "none",
	mean_velocity = [-0.1, 0, 0] 
)





# ---------------------
# DIAGNOSTIC PARAMETERS
# ---------------------

# DUMP DIAGS
#
every = 20

DiagScalar (
 	precision = 3,
	vars = ['Etot', 'Eparticles', 'EFields', 'E_eon1', 'N_eon1', 'E_eon2', 'N_eon2', 'Ex_U']
)
 

# PHASE-SPACE DIAGNOSTICS
DiagPhase (
 	kind    = ['xpx'],
 	species = ['eon1', 'eon2'],
 
 	first = [0,1.0, 100],
 	second = [-0.4,0.4, 100],
 	
 	deflate=5
)

fieldsToDump = ['Jx', 'Rho_eon1']

