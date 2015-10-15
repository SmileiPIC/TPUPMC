# ---------------------------------------------
# SIMULATION PARAMETERS FOR THE PIC-CODE SMILEI
# ---------------------------------------------

# dim: Geometry of the simulation
#      1d3v = cartesian grid with 1d in space + 3d in velocity
#      2d3v = cartesian grid with 2d in space + 3d in velocity
#      3d3v = cartesian grid with 3d in space + 3d in velocity
#      2drz = cylindrical (r,z) grid with 3d3v particles
#
dim = '1d3v'


# order of interpolation
#
interpolation_order = 2

# SIMULATION TIME 
# either use the resolution (res_time) or time-step (timestep)
#
# res_time : temporal resolution 
# timestep : time step
# sim_time : duration of the simulation 
#
timestep = 0.01
sim_time = 30.0

# SIMULATION BOX : for all space directions (in 2D & 3D use vector of doubles)
# either use the resolution (res_space) or cell-length (cell_length)
#
# res_space   : spatial resolution 
# sim_length  : length of the simulation 
# cell_length : cell-length 
#
cell_length = [0.01]
sim_length  = [1.0]


# ELECTROMAGNETIC BOUNDARY CONDITIONS
# bc_em_type_long/trans : boundary conditions used for EM fields 
#                         in the longitudinal or transverse directions
#                         periodic      = periodic BC (using MPI topology)
#                         silver-muller = injecting/absorbing
#
bc_em_type_x = ['periodic']


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
   	species_geometry = 'constant',
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
	species_type = "eon",
	initPosition_type = "regular",
	initMomentum_type = "cold",
	n_part_per_cell = npart,
	mass = 1.0,
	charge = -1.0,
	nb_density = cosine(1,amplitude=0.01,xnumber=1),
	bc_part_type_west = "none",
	bc_part_type_east = "none"
)


# ---------------------
# DIAGNOSTIC PARAMETERS
# ---------------------


# global every for diagnostics
every = int(0.1/timestep)
print_every=10*every

# DIAG ON SCALARS 
#
DiagScalar (
 	precision = 3,
	vars = ['Etot', 'Eparticles', 'EFields', 'E_eon', 'N_eon', 'Ex_U']
)
 

# PHASE-SPACE DIAGNOSTICS
DiagPhase (
 	kind    = ['xpx'],
 	species = ['eon'],
 
 	first = [0,1.0, 50],
 	second = [-0.002,0.002, 100],
 	
 	deflate=5
)

fieldsToDump = ['Jx', 'Rho_eon']



