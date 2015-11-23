# ---------------------------------------------
# SIMULATION TP_proj1.py
# ---------------------------------------------

# dim: Geometry of the simulation
#      1d3v = cartesian grid with 1d in space + 3d in velocity
dim = '1d3v'

# order of interpolation
interpolation_order = 2

# sim_time : duration of the simulation 
sim_time = 30.0

# timestep : time step
timestep = 0.01

# cell_length : cell-length 
cell_length = [0.01]

# sim_length  : length of the simulation 
sim_length  = 1.0

# ELECTROMAGNETIC BOUNDARY CONDITIONS
bc_em_type_x = ['periodic']

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

DiagScalar (
 	precision = 3,
	vars = ['Utot', 'Ukin', 'Uelm', 'Ukin_eon', 'Ntot_eon', 'Uelm_Ex']
)
 
DiagPhase (
 	kind    = ['xpx'],
 	species = ['eon'],
 	first = [0,1.0, 50],
 	second = [-0.002, 0.002, 100],
 	deflate=5
)

fieldsToDump = ['Jx', 'Rho_eon']
