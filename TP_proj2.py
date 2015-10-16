# ---------------------------------------------
# SIMULATION TP_proj2.py
# ---------------------------------------------

# dim: Geometry of the simulation
dim = '1d3v'

# SIMULATION TIME 
# sim_time  : duration of the simulation 

sim_time = 100.0

# SIMULATION BOX 

cell_length = [1.0e-2]
sim_length  = [1.03]

# time step : time step
timestep = 0.9*cell_length[0]

# order of interpolation
interpolation_order = 2

# ELECTROMAGNETIC BOUNDARY CONDITIONS
bc_em_type_x = ['periodic']

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
	nb_density = cosine(0.5,amplitude=0.01,xnumber=1),
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
	nb_density = cosine(0.5,amplitude=0.01,xnumber=1),
	bc_part_type_west = "none",
	bc_part_type_east = "none",
	mean_velocity = [-0.1, 0, 0] 
)

# ---------------------
# DIAGNOSTIC PARAMETERS
# ---------------------

# run diagnostics every steps
every = 20

DiagScalar (
 	precision = 3,
	vars = ['Utot', 'Ukin', 'Uelm', 'Ukin_eon1', 'Ukin_eon2', 'Ntot_eon1', 'Ntot_eon2', 'Uelm_Ex']
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

