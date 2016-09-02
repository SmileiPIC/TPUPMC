# ---------------------------------------------
# SIMULATION TP_proj2.py
# ---------------------------------------------
my_every=20
npart=10
velocity=0.02
amplitude=0.02
Main(
    geometry = "1d3v",
    interpolation_order = 2,
    sim_time = 50.0,
    cell_length = [0.02],
    timestep = 0.02,
    sim_length  = [1.0],
    number_of_patches = [ 2 ],
    print_every = my_every,
    bc_em_type_x = ['periodic'],
    poisson_iter_max=0
)

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
	nb_density = cosine(0.5,xamplitude=amplitude,xnumber=1),
	bc_part_type_west = "none",
	bc_part_type_east = "none",
	mean_velocity = [velocity, 0, 0] 
)

Species(
	species_type = "eon2",
	initPosition_type = "regular",
	initMomentum_type = "cold",
	n_part_per_cell = npart/2,
	mass = 1.0,
	charge = -1.0,
	nb_density = cosine(0.5,xamplitude=amplitude,xnumber=1),
	bc_part_type_west = "none",
	bc_part_type_east = "none",
	mean_velocity = [-velocity, 0, 0] 
)

DiagScalar (
 	precision = 3,
 	every=my_every,
	vars = ['Utot', 'Ukin', 'Uelm', 'Ukin_eon1', 'Ukin_eon2', 'Ntot_eon1', 'Ntot_eon2', 'Uelm_Ex']
)
 
DiagParticles(
	output = "density",
	every = my_every,
 	species = ['eon1', 'eon2'],
	axes = [
		["x", 0., 1., 100],
		["px", -4*velocity, 4*velocity, 100]
	]
)

DiagFields(
    every = my_every,
    fields = ['Jx', 'Rho_eon1', 'Rho_eon2']
)

